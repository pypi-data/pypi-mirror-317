import time


class TimerControl:
    """计时器控制器, 实现暂停与继续，可多次触发"""
    def __init__(self):
        self._start_time = None
        self._elapsed_time = 0

    def start(self):
        if self._start_time is None:
            self._start_time = time.time()

    def stop(self):
        if self._start_time is not None:
            self._elapsed_time += time.time() - self._start_time
            self._start_time = None

    def reset(self):
        self._start_time = None
        self._elapsed_time = 0

    def get_elapsed_time(self):
        return self._elapsed_time + (time.time() - self._start_time if self._start_time else 0)

    def trigger(self):
        print(f"计时器触发，累计运行时间: {self.get_elapsed_time():.2f} 秒")
