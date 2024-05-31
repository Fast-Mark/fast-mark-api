

class TXTLogger():
    def __init__(self, name: str) -> None:
        # self.name = name
        self.name = name
        with open(f"{name}.txt", 'w') as F:
            pass

    def print(self, msg):
        with open(f"{self.name}.txt", "w") as F:
            print(msg, file=F)
        