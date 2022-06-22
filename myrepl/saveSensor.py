try:
  import uasyncio as asyncio
except:
  import asyncio
try:
  import utime as time
except:
  import time

#import sh1107, mpu9250
#import dps310_simple as dps310
listSensorModify = {}

class BlinxSensor():
  def __init__(self, diffTicks, arraySensor, arrayName):
    self.arraySensor = arraySensor
    self.arrayName = arrayName
    self.ticks_boucle = 0
    self.time_ns = time.time_ns() - time.ticks_ms()
    self.ticks_max = 2**30

    def diffTicks(self, before, after, diffMax = 2000):
        if after >= before:
            return after-before
        else :
            if before + diffMax > ticks_max:
                self.resetTicks()
                return ticks_max - before + after
        return -1

  def save(self):
    for sensor in self.arraySensor:
      sensor.save()


"""
  def recordDataPart1(self):
      waiting = []

      # send the demand for donnee to the sensor
      for i in self.donnee['i2c']['function']:
        i.send()
        waiting.append(i.waiting())

      maxWait = max(waiting)
      timeWait = time.ticks_ms() + maxWait
      l_donneeAnalog = len(donnee['analog']['function'])
      l_donneeDigital = len(donnee['digital']['function'])
      finishWait, finishDonnee, indexAnalog = waitBetweenI2CSensor(timeWait, l_donneeAnalog, l_donneeDigital)

      return timeWait, finishWait, finishDonnee, l_donneeAnalog, indexAnalog

  def recordDataPart2(self, finishDonnee, l_donneeAnalog, indexAnalog):
      # capture the reply for donnee of the sensor
      for i in donnee['i2c']['function']:
        i.save(time.ticks_ms())

      # if we finish the time wait for the i2c sensor,
      # but we don't finish all analog sensor,
      # we finish it
      if not finishDonnee:
        while indexAnalog < l_donneeAnalog:
          donnee['analog']['function'][indexAnalog].save(time.ticks_ms())
          indexAnalog += 1


  def waitBetweenI2CSensor(self, timeWait, l_donneeAnalog, l_donneeDigital):
    # while we are waiting for the reply of the i2c sensor,
    # we will record the analog sensor

    indexDigital = 0
    while indexDigital < l_donneeDigital:
      donnee['digital']['function'][indexDigital].save(time.ticks_ms())
      indexDigital += 1

    indexAnalog = 0

    present = time.ticks_ms()
    finishWait =  timeWait > present
    finishDonnee = 0 < l_donneeAnalog
    finish = finishWait and finishDonnee
    if finishWait:
      while finish:
        present = time.ticks_ms()
        donnee['analog']['function'][indexAnalog].save(present)
        indexAnalog += 1

        finishWait =  timeWait > present
        finishDonnee = indexAnalog < l_donneeAnalog
        finish = finishWait and finishDonnee

    return finishWait, finishDonnee, indexAnalog
"""
