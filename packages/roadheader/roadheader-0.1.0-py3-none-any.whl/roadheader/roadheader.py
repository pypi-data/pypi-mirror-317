import traceback
from dataclasses import dataclass


@dataclass
class Target:
    ...


@dataclass
class Ore:
    ...


class Roadheader:
    def __init__(self):
        self.name = self.__class__.__name__

    def start_up(self):
        pass

    def shut_down(self):
        pass

    def drill(self, target: Target) -> list[Ore]:
        raise NotImplementedError

    def convey(self, ores: list[Ore]):
        raise NotImplementedError

    def process(self, target: Target):
        try:
            self.start_up()
        except Exception:
            print(f"{self.name} start_up error: {traceback.format_exc()=}")

        try:
            print(f"{self.name} start drill {target}")
            ores = self.drill(target)

            print(f"{self.name} start convey {len(ores)=}")
            self.convey(ores)

        except Exception:
            print(f"{self.name} drill/convey: {target=} {traceback.format_exc()=}")

        else:
            print(f"{self.name} finish process {target}")

        try:
            self.shut_down()
        except Exception:
            print(f"{self.name} shut_down error: {traceback.format_exc()=}")
