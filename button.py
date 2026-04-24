from cmu_graphics import *

class Button:
    def __init__(self, left, top, width, height, color, text, textSize, onClickFn):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = color
        self.defaultColor = color
        self.text = text
        self.onClickFn = onClickFn
        self.textSize = textSize
        self.clickTimer = 0
        
    def handleClick(self, mouseX, mouseY):
        left, right = self.left, self.left + self.width
        top, bottom = self.top, self.top + self.height
        if (left <= mouseX <= right) and (top <= mouseY <= bottom):
            self.onClickFn()
            self.clickTimer = 2
            self.color = 'white'

    def update(self):
        if self.clickTimer >0:
            self.clickTimer -= 1
            if self.clickTimer == 0:
                self.color = self.defaultColor

    def draw(self):
        drawRect(self.left, self.top, self.width, self.height, fill=self.color, border = 'black')
        cx, cy = self.left + self.width/2, self.top + self.height/2
        drawLabel(self.text, cx, cy, size=self.textSize)
        
class textBox:
    def __init__(self, left, top, width, height, textSize, text):
        self.left = left
        self.top = top
        self.height = height
        self.width = width
        self.color = 'lightGrey'
        self.selected = False
        self.textSize = textSize
        self.isDefaultText = True
        self.text = text
        self.defaultText = text
    
    def handleClick(self, mouseX, mouseY):
        left, right = self.left, self.left + self.width
        top, bottom = self.top, self.top + self.height
        if (left <= mouseX <= right) and (top <= mouseY <= bottom):
            self.color = 'white'
            self.selected = True

            if self.isDefaultText:
                self.text = ''
                self.isDefaultText = False
        else:
            self.color = 'lightGrey'
            self.selected = False
            if self.text == '':
                self.text = self.defaultText
                self.isDefaultText = True

    def handleKey(self, key):
        if not self.selected:
            return None
        if key.isdigit():
            self.text += key
        if key == 'backspace':
            self.text = self.text[:-1]
        self.isDefaultText = False

    def getValue(self):
        if self.text == '' or self.text == self.defaultText:
            return None
        return int(self.text)
    
    def draw(self):
        drawRect(self.left, self.top, self.width, self.height, fill = self.color, border='Black')
        cy = self.top + self.height/2
        if self.isDefaultText:
            opacityLevel = 60
            textSize = 11
        else:
            opacityLevel = 100
            textSize = self.textSize
        display = self.text + ('|' if self.selected else '')
        drawLabel(display, self.left+5, cy, size = textSize, align = 'left', opacity = opacityLevel)




# cmu_graphics.run()