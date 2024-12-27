import time

class Time:
  @classmethod
  def cycle_sleep(cls, elapsedTime, maxSleepTime = 1.0):
    time.sleep(maxSleepTime - min(elapsedTime, maxSleepTime))

class Stopwatch:
  def __init__(self):
    self.start()

  def start(self):
    self.__StartTime = time.perf_counter()
    self.__ElapsedTime = 0.0
    return self

  def stop(self):
    self.__ElapsedTime = time.perf_counter() - self.__StartTime
    return self

  def to_string(self, format = "{ElapsedTime:.3f}"):
    return format.format(ElapsedTime = self.__ElapsedTime)

  def __str__(self):
    return self.to_string()

  @property
  def ElapsedTime(self):
    return self.__ElapsedTime
