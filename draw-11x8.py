
import tkinter.simpledialog
from tkinter import * 

rows = 11
columns = 8
cellSize = 50

drawing = bytearray([0x00, 0x18, 0x18, 0x00, 0x38, 0x18, 0x18, 0x18, 0x18, 0x3c, 0x00])

class CustomDialog(tkinter.simpledialog.Dialog):

    def __init__(self, parent, title=None, text=None):
        self.data = text
        tkinter.simpledialog.Dialog.__init__(self, parent, title=title)

    def body(self, parent):
        self.text = Text(self, width=80, height=4)
        self.text.pack(fill="both", expand=True)
        self.text.insert("1.0", self.data)
        return self.text

window = Tk()

def show_dialog(text):
  window.clipboard_clear()
  window.clipboard_append(text)
  window.update()
  CustomDialog(window, title="already in clipboard", text=text)

def is_paint(x, y) :
  return (drawing[y] >> (7-x)) & 1
def set_paint(x,y) :
  drawing[y] = (drawing[y] ) | (1 << (7-x))
def unset_paint(x,y) :
  drawing[y] = (drawing[y] ) & ~(1 << (7-x))


canvas = Canvas(window, width=cellSize*columns, height=cellSize*rows, background='white')

def click_event(event):
    x = event.x//cellSize
    y = event.y//cellSize
    closest = canvas.find_closest(event.x, event.y, start=rows+columns)
    if is_paint(x, y) :
      if closest[0] >= (rows+columns-1):
        canvas.delete(closest)
        unset_paint(x,y)
    else :
      canvas.create_rectangle(x*cellSize, y*cellSize, (x+1)*cellSize, (y+1)*cellSize, fill="green")
      set_paint(x,y)
    

canvas.bind("<Button-1>", click_event)

for y in range(1,columns):
  ligne1 = canvas.create_line(y*cellSize, 0, y*cellSize, rows*cellSize)
for x in range(1,rows):
  ligne2 = canvas.create_line(0, x*cellSize, columns*cellSize, x*cellSize)
for x in range(0,columns):
  for y in range(0,rows):
    if (is_paint(x,y)):
      canvas.create_rectangle(x*cellSize, y*cellSize, (x+1)*cellSize, (y+1)*cellSize, fill="green")

canvas.pack(side=LEFT, padx=5, pady=5)


frame1 = PanedWindow(window, borderwidth=2, orient=VERTICAL)
frame1.pack(side=RIGHT, padx=30, pady=30)

def msgCallBack():
  formated_bytes = ', '.join('0x{:02x}'.format(x) for x in drawing)
  show_dialog(formated_bytes)

Button(frame1, text ='Get Bytes', command=msgCallBack).pack(padx=5, pady=5)



window.mainloop()