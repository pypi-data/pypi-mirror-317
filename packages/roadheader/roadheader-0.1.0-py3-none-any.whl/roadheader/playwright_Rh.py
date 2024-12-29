from .roadheader import Roadheader
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync


class PlaywrightRh(Roadheader):
    undetected = True

    def __init__(self):
        super().__init__()
        self.playwright_context_manager = None
        self.playwright_instance = None
        self.browser = None
        self.page = None

    def start_up(self):
        self.playwright_context_manager = sync_playwright()
        self.playwright_instance = self.playwright_context_manager.__enter__()
        self.browser = self.playwright_instance.chromium.launch()
        self.page = self.browser.new_page()

        if self.undetected:
            stealth_sync(self.page)

    def shut_down(self):
        if self.page:
            self.page.close()
            self.page = None

        if self.browser:
            self.browser.close()
            self.browser = None

        if self.playwright_context_manager:
            self.playwright_context_manager.__exit__()
            self.playwright_context_manager = None
            self.playwright_instance = None
