def format_timedelta(td) -> str:
    total_seconds = td.total_seconds()

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}"

class Bar:

    def __init__(self, max: int, prefix: str = "", size: int = 40):
        self.max = max
        self.prefix = prefix
        self.size = size
        self.progress = 0

    def reset(self) -> None:
        self.progress = 0
        print(self, end="\r", flush=True)

    def update(self) -> None:
        self.progress += 1
        print(self, end="\r", flush=True)

    def finish(self) -> None:
        self.progress = self.max
        print(self, end="\n", flush=True)

    def __str__(self):
        x = int(self.size * self.progress / self.max)
        bar = "|" + x*"█" + (self.size-x)*" " + "| " + f"{self.progress/self.max*100:.0f}%"
        if len(self.prefix) > 0:
            return self.prefix + " " + bar
        else:
            return self.prefix + bar