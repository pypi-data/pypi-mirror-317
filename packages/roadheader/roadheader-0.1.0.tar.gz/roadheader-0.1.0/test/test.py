from roadheader.playwright_Rh import PlaywrightRh
from roadheader.roadheader import Ore
from roadheader.roadheader import Target

class HTarget(Target):
    def __init__(self):
        self.url = "https://baidu.com"

class HtmlOre(Ore):
    def __init__(self, content):
        self.content = content

class HtmlRh(PlaywrightRh):
    def drill(self, target):
        self.page.goto(target.url)
        return [HtmlOre(self.page.content())]

    def convey(self, ores):
        for ore in ores:
            print(ore.content)

rh = HtmlRh()
rh.process(HTarget())
