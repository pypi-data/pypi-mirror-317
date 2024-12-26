import time

class Toggle:
    def __init__(self) -> None:
        self.value: bool = False
        self.last_toggle_timestamp: float = time.time()

    def toggle(self) -> None:
        """Changes the state of the toggle."""
        self.value = not self.value
        self.last_toggle_timestamp = time.time()
