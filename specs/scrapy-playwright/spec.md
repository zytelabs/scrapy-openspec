# scrapy-playwright Specification

## Purpose
Defines how to render pages with a real browser using `scrapy-playwright` when a
project does NOT use Zyte API. This is an alternative to the `WebPage`/`BrowserPage`
strategy in the `project-settings` spec: a project uses **either** Zyte API
(`BrowserPage` + `browserHtml`) **or** `scrapy-playwright` for rendering, never
both. Reach for `scrapy-playwright` when Zyte API is unavailable or the target
rejects the native downloader, and stealth is needed via a patched browser
(patchright / camoufox).

## Requirements

### Requirement: scrapy-playwright is enabled with the stock handler, not a subclass
When browser rendering is provided by `scrapy-playwright`, the project SHALL set
the asyncio reactor and register the **stock** download handler for both schemes.
The download handler SHALL NOT be subclassed to force rendering.

```python
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
```

#### Scenario: Reactor and handlers are configured
- **WHEN** `settings.py` is loaded
- **THEN** `TWISTED_REACTOR` is the asyncio reactor and both `http` and `https`
  handlers are `scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler`

#### Scenario: The download handler is not subclassed
- **WHEN** reviewing the project
- **THEN** no custom class subclasses `ScrapyPlaywrightDownloadHandler`; rendering
  is enabled per request (see next requirement), not inside a handler override

### Requirement: Playwright is enabled per request via a downloader middleware
To render every request — including the request that `scrapy savefixture`
generates itself (it builds its own `Request` and ignores the spider's `start`) —
the project SHALL set `meta['playwright']` in a downloader middleware, following
the "Processing all requests with Playwright" pattern in the scrapy-playwright
FAQ. A downloader middleware (not a spider middleware) is REQUIRED because it is
the only variant that also covers start requests and the savefixture request.
`setdefault` SHALL be used so an individual request can opt out.

```python
# <project>/middlewares.py
class PlaywrightRequestMiddleware:
    def process_request(self, request):        # no `spider` arg: forward-compatible
        request.meta.setdefault("playwright", True)
        return None
```

```python
# settings.py
DOWNLOADER_MIDDLEWARES = {
    "<project>.middlewares.PlaywrightRequestMiddleware": 543,
}
```

#### Scenario: Every request is rendered
- **WHEN** the spider crawls and when `scrapy savefixture` runs
- **THEN** each request carries `meta['playwright'] = True` and is browser-rendered

#### Scenario: process_request omits the spider argument
- **WHEN** the middleware method is defined
- **THEN** it is `process_request(self, request)` — omitting `spider` avoids the
  Scrapy deprecation warning about the spider argument

### Requirement: The browser backend is selected via a provider class
The browser backend SHALL be chosen with the `PLAYWRIGHT_BROWSER_PROVIDER` hook,
pointing at a provider class in `<project>/providers.py`. The provider class body
SHALL match the scrapy-playwright pluggable-browser-providers docs, importing the
third-party library lazily inside the methods that use it. `PLAYWRIGHT_BROWSER_TYPE`
MUST match the backend: `"chromium"` for patchright, `"firefox"` for camoufox.

#### Patchright (patched Chromium)
**Install**: add the `patchright` dependency, then `patchright install chromium`
(reuses the shared `ms-playwright` Chromium cache; no separate binary).

```python
# settings.py
PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_BROWSER_PROVIDER = "<project>.providers.PatchrightBrowserProvider"
```

```python
# <project>/providers.py
from contextlib import AsyncExitStack
from scrapy_playwright.handler import Config


class PatchrightBrowserProvider:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.stack = AsyncExitStack()

    async def start(self) -> None:
        from patchright.async_api import async_playwright

        _patchright = await self.stack.enter_async_context(async_playwright())
        self.browser_type = _patchright.chromium

    async def launch_browser(self):
        return await self.browser_type.launch(**self.config.launch_options)

    async def launch_persistent_context(self, context_kwargs: dict):
        return await self.browser_type.launch_persistent_context(**context_kwargs)

    async def close(self) -> None:
        await self.stack.aclose()
```

#### Camoufox (patched Firefox)
**Install**: add the `camoufox` dependency, then `camoufox fetch` (downloads its
Firefox build).

```python
# settings.py
PLAYWRIGHT_BROWSER_TYPE = "firefox"
PLAYWRIGHT_BROWSER_PROVIDER = "<project>.providers.CamoufoxBrowserProvider"
```

```python
# <project>/providers.py
from contextlib import AsyncExitStack
from scrapy_playwright.handler import Config, PERSISTENT_CONTEXT_PATH_KEY


class CamoufoxBrowserProvider:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.stack = AsyncExitStack()

    async def start(self) -> None:
        pass

    async def launch_browser(self):
        from camoufox.async_api import AsyncCamoufox

        return await self.stack.enter_async_context(
            AsyncCamoufox(**self.config.launch_options)
        )

    async def launch_persistent_context(self, context_kwargs: dict):
        from camoufox.async_api import AsyncCamoufox

        return await self.stack.enter_async_context(
            AsyncCamoufox(
                persistent_context=True,
                user_data_dir=context_kwargs[PERSISTENT_CONTEXT_PATH_KEY],
                **self.config.launch_options,
            )
        )

    async def close(self) -> None:
        await self.stack.aclose()
```

#### Scenario: Provider and browser type agree
- **WHEN** `PLAYWRIGHT_BROWSER_PROVIDER` is the patchright provider
- **THEN** `PLAYWRIGHT_BROWSER_TYPE` is `"chromium"`; for the camoufox provider it
  is `"firefox"`

#### Scenario: Third-party imports are lazy
- **WHEN** a provider module is imported
- **THEN** `patchright`/`camoufox` are imported inside the provider methods, so an
  uninstalled backend only errors if that provider is actually selected

### Requirement: Camoufox needs no_viewport, set per request — never via PLAYWRIGHT_CONTEXTS
Camoufox manages its own viewport, so scrapy-playwright's default context creation
fails with `Browser.new_context: Protocol error (Browser.setDefaultViewport)`. The
fix is `no_viewport`, which SHALL be supplied per request through
`playwright_context_kwargs`, NOT through `PLAYWRIGHT_CONTEXTS`. Declaring a
`PLAYWRIGHT_CONTEXTS` "startup context" makes scrapy-playwright open an idle,
empty browser at engine start; the per-request form creates the context lazily on
the first real request instead. This is harmless for the patchright backend, so
the middleware MAY set it unconditionally.

```python
# in PlaywrightRequestMiddleware.process_request
request.meta.setdefault("playwright_context_kwargs", {"no_viewport": True})
```

#### Scenario: no_viewport avoids the setDefaultViewport error
- **WHEN** camoufox renders a page
- **THEN** the context is created with `no_viewport=True` and no
  `Browser.setDefaultViewport` protocol error occurs

#### Scenario: No idle startup browser
- **WHEN** the crawl starts
- **THEN** `PLAYWRIGHT_CONTEXTS` is empty and the browser launches on the first
  request, not at engine start — no empty browser window appears beforehand

### Requirement: Navigate with domcontentloaded under camoufox
scrapy-playwright waits for the `load` event by default. On sites that keep
executing scripts after `load`, one uncaught error can crash camoufox's Firefox
driver (a Playwright pageerror-handling bug: `Cannot read properties of undefined
(reading 'url')` → `Connection closed`/`EPIPE`), which takes down the whole
browser and stalls the crawl. Requests SHALL navigate with
`wait_until="domcontentloaded"` via `playwright_page_goto_kwargs`, which returns
at DOM-ready and still exposes server-rendered markup.

```python
# in PlaywrightRequestMiddleware.process_request
request.meta.setdefault(
    "playwright_page_goto_kwargs", {"wait_until": "domcontentloaded"}
)
```

#### Scenario: Post-load scripts do not crash the driver
- **WHEN** a page under camoufox runs scripts that throw after `load`
- **THEN** navigation has already returned at `domcontentloaded`, so the driver
  does not crash and the crawl continues

### Requirement: Concurrency accounts for one browser page per request
Under `scrapy-playwright` each concurrent request is an open browser page, which is
far heavier than an HTTP fetch and also caps `PLAYWRIGHT_MAX_PAGES_PER_CONTEXT`
(its default equals `CONCURRENT_REQUESTS`). Concurrency SHALL be kept modest
(single digits) rather than the high values used for plain HTTP or Zyte API.
`PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT` MAY be raised if pages time out under load.

#### Scenario: Concurrency is modest for browser rendering
- **WHEN** rendering with scrapy-playwright
- **THEN** `CONCURRENT_REQUESTS` is a small number (e.g. ≤ 8), not the 32×domains
  value used for HTTP/Zyte-API crawls
