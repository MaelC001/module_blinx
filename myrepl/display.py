import ssd1306

@register('display_create', "")
def displayCreate(self, typeDisplay, x, y):
  """
  connect to a display
  arg :
    - typeDisplay : str # sh1107 (grand, 128, 64) or ssd1306 (petit, 128, 32)
    - x : int
    - y : int
  """
  global display, displayType
  verification(typeDisplay, str, ['sh1107', 'ssd1306'])
  verification(x, int)
  verification(y, int)
  if display:
    clear()
  if typeDisplay != displayType or not display:
    displayType = typeDisplay
    if typeDisplay == 'sh1107':
      display = sh1107.SH1107_I2C(x, y, i2c)
    elif typeDisplay == 'sh1107':
      display = ssd1306.SSD1306_I2C(x,y,i2c)
  return ''

@register('display_text', "displayCreate")
def displayText(typeDisplay, x, y, show):
  """
  show text in the display
  arg :
    - typeDisplay : str #  sh1107 (grand, 128, 64) or ssd1306 (petit, 128, 32)
    - x : int
    - y : int
    - show :
        - text : str
        - x : int
        - y : int
        - taille : int
  """
  verification(typeDisplay, str, ['sh1107', 'ssd1306'])
  verification(show, dict)
  if typeDisplay != displayType or not display:
    displayCreate(typeDisplay, x, y)
  for i in show :
    text = i['text']
    x = i['x']
    y = i['y']
    t = i['taille']
    verification(text, str)
    verification(x, int)
    verification(y, int)
    verification(t, int)
    display.text(text, x, y, t)
  display.show()
  return ''

@register('display_clear', "displayCreate")
def displayClear(typeDisplay, y, x):
  """
  clear display
  arg :
    - typeDisplay : str # sh1107 (grand, 128, 64) or ssd1306 (petit, 128, 32)
    - x : int
    - y : int
  """
  verification(typeDisplay, str, ['sh1107', 'ssd1306'])
  if typeDisplay != displayType or not display:
    displayCreate(typeDisplay, y, x)
  clear()
  return ''

def clear():
  """
  clear display
  """
  display.fill(0)
  display.show()


class DisplayBlinx():
    pass