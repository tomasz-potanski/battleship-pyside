class Timer:
    """
    Timer class to calculate the duration of the game
    """

    def __init__(self):
        self._elapsed = 0.0
        self._starttime = time()
        self._started = False

    def start(self):
        self._starttime = time()
        self._started = True

    def stop(self):
        self._elapsed += (time() - self._starttime)
        self._started = False

    def reset(self):
        self._elapsed = 0.0

    def get_elapsed(self):
        if self._started:
            return self._elapsed + time() - self._starttime
        else:
            return self._elapsed

    def get_result(self):
        # tuple: (hours, minutes, seconds, microseconds)
        if self._started:
            timee = self._elapsed + time() - self._starttime
        else:
            timee = self._elapsed

        seconds = timee
        minutes = seconds // 60
        seconds = round((seconds % 60), 3)
        hours = minutes // 60
        minutes %= 60
        mseconds = round((timee * 100), 3)
        return hours, minutes, seconds, mseconds