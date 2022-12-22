import uasyncio as asyncio
uart = None
def a():
	baud_rate = 76800
	uart = UART(0, baudrate=baud_rate, tx=10, rx=9)  # UART(0, baud_rate)
	uart.init(baudrate = baud_rate)#, rxbuf = 200)
	return uart

async def receiver():#uart):
  sreader = asyncio.StreamReader(uart) # sys.stdin)
  while True:
    data = await sreader.read()#0)
    print(data)

def b(uart, i=0):
  #os.dupterm(uart, i)
  #os.dupterm(None, i)
  loop = asyncio.get_event_loop()
  loop.create_task(receiver())#uart))
  loop.run_forever()

def c():
	global uart
	uart = a()
	b(uart)


