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

ticks_boucle = 0
time_ns = time.time_ns() - time.ticks_ms()
ticks_max = 2**30

donnee = {
  "i2c" : {
    "function" : {},
    "name" : [],
  },
  "analog" : {
    "function" : {},
  },
  "digital" : {
    "function" : {},
  },
}

donneeSensor = []
donneeSensorName = []
donneeAnalog = []
donneeAnalogName = []
donneeDigital= []
donneeDigitalName = []
listSensorModify = {}


async def saveAllSensor():
  while True:


    # we will wait a minimum of 1 secondes before we recommence
    timeBefore = time.ticks_ms()

    timeWait, finishWait, finishDonnee, l_donneeAnalog, indexAnalog = recordDataPart1()

    # if we do all analog sensor,
    # but we did not finish the time wait for the i2c sensor,
    # we will sleep
    if not finishWait:
      diffTime = diffTicks(timeWait, time.ticks_ms())
      if diffTime > 0:
        await asyncio.sleep_ms(diffTime)

    recordDataPart2(finishDonnee, l_donneeAnalog, indexAnalog)

    present= time.ticks_ms()
    diffTime = 1000 - diffTicks(timeBefore, present)
    if diffTime > 0:
      await asyncio.sleep_ms(diffTime)

def diffTicks(before, after, diffMax = 2000):
  if after >= before:
    return after-before
  else :
    if before + diffMax > ticks_max:
      resetTicks()
      return ticks_max - before + after
    return -1

def resetTicks():
  global time_ns, ticks_boucle
  ticks_boucle += 1
  time_ns = time.time_ns() - time.ticks_ms()

def recordDataPart1():
    waiting = []

    # send the demand for donnee to the sensor
    for i in donnee['i2c']['function']:
      i.send()
      waiting.append(i.waiting())

    maxWait = max(waiting)
    timeWait = time.ticks_ms() + maxWait
    l_donneeAnalog = len(donnee['analog']['function'])
    l_donneeDigital = len(donnee['digital']['function'])
    finishWait, finishDonnee, indexAnalog = waitBetweenI2CSensor(timeWait, l_donneeAnalog, l_donneeDigital)

    return timeWait, finishWait, finishDonnee, l_donneeAnalog, indexAnalog

def recordDataPart2(finishDonnee, l_donneeAnalog, indexAnalog):
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


def waitBetweenI2CSensor(timeWait, l_donneeAnalog, l_donneeDigital):
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