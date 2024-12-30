from playwright.sync_api import Page as SyncPage, BrowserContext as SyncBrowserContext
from playwright.async_api import Page as AsyncPage, BrowserContext as AsyncBrowserContext
from playwright_stealth import stealth_async as stealth_async_, stealth_sync as stealth_sync_


# # sites:
# https://github.com/Kaliiiiiiiiii-Vinyzu/patchright-python?tab=readme-ov-file#stealth
# https://bot.sannysoft.com
# https://www.browserscan.net/bot-detection
# https://abrahamjuliot.github.io/creepjs
# https://kaliiiiiiiiii.github.io/brotector
# https://arh.antoinevastel.com/bots/areyouheadless

# # pypi packages:
# undetected_playwright
# puppeteer-extra-plugin-stealth


async def stealth_async(pc: AsyncPage | AsyncBrowserContext, **kwargs):
    await stealth_async_(pc, **kwargs)


def stealth_sync(pc: SyncPage | SyncBrowserContext, **kwargs):
    stealth_sync_(pc, **kwargs)
