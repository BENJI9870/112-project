from button import Button, textBox
from init_textboxes import initializeTextBoxes
from init_buttons import initializeRodButtons, initializeSupportButtons, initializePointLoadButtons, initializeOtherButtons, initializeAuto, initializeDistLoadButtons
from shear_moment import plotShearMoment, calcShearMoment
from cmu_graphics import *

def onAppStart(app):
    app.counter = 0
    app.background = 'white'
    app.rodLeng = None
    app.selectedSupport = None
    app.selectedPointLoadDir = None
    app.selectedDistLoadDir = None
    app.supports = []
    app.pointLoads = []
    app.distLoads = []
    app.setMaxShapeCount(10000)



    # layout settings
    app.sidePanelWidth = app.width / 4
    app.sideMargin = 75
    app.gap = 25

    initializeTextBoxes(app)
    initializeRodButtons(app)
    initializeSupportButtons(app)
    initializePointLoadButtons(app)
    initializeOtherButtons(app)
    initializeAuto(app)
    initializeDistLoadButtons(app)


def onMousePress(app, mouseX, mouseY):
    for button in app.buttons:
        button.handleClick(mouseX, mouseY)
    for textBox in app.textBoxes:
        textBox.handleClick(mouseX, mouseY)

def onStep(app):
    for button in app.buttons:
        button.update()

def onKeyPress(app, key):
    for textBox in app.textBoxes:
        textBox.handleKey(key)

def drawBeam(app):
    cx, cy = app.width*5/8, app.height*6/7
    if app.rodLeng != None:
        drawRect(cx, cy, app.width/2, 40, fill = 'gray', align = 'center')



def changePointLoadColors_and_Support(app, button):
    if button.text == 'Add':
        button.color = 'lightBlue'
    elif button.text.lower() == app.selectedSupport:
        button.color = 'orange'
    elif button.text.lower() == app.selectedPointLoadDir:
        button.color = 'orange'
    else:
        button.color = 'white'

def changeDistLoadColors(app, button):
    if button.text == 'Add':
        button.color = 'lightBlue'
    elif button.text.lower() == app.selectedDistLoadDir:
        button.color = 'orange'
    else:
        button.color = 'white'

def drawSupports(app):
    for support in app.supports[:2]:
        r = 25
        cx, cy = support['location'], app.height*6/7 + r + 20
        if support['type'] == 'pinned':
            drawRegularPolygon(cx, cy, r, 3, fill='pink')
        elif support['type'] == 'roller':
            drawCircle(cx, cy-5, r * 0.75, fill='pink')



def drawPointLoads(app):
    for load in app.pointLoads:
        d = -1 if load['direction'] == 'up' else 1
        cx = load['location']
        cy = app.height*6/7 - d*40
        # main line
        drawLine(cx, cy - 20*d, cx, cy + 20*d, lineWidth=2, fill='red')
        # arrow head
        tipY = cy + 20*d
        drawLine(cx, tipY, cx - 10, tipY - 10*d, lineWidth=2, fill='red')
        drawLine(cx, tipY, cx + 10, tipY - 10*d, lineWidth=2, fill='red')

        # label
        drawLabel(str(load['magnitude']), cx, tipY - 60*d, size=15)
#ChatGPT helped with this one
def drawDistLoads(app):
    for load in app.distLoads:
        d = -1 if load['direction'] == 'up' else 1

        cx1 = load['start location']
        cx2 = load['end location']

        startLoad = load['start load']
        endLoad = load['end load']

        beamY = app.height * 6/7 -d*20

        maxLoad = max(abs(startLoad), abs(endLoad))
        if maxLoad == 0:
            return

        scale = 40 / maxLoad

        y1 = beamY - d * startLoad * scale
        y2 = beamY - d * endLoad * scale

        # diagonal/top line
        drawLine(cx1, y1, cx2, y2, lineWidth=2, fill='purple')

        # start arrow
        drawLine(cx1, y1, cx1, beamY, lineWidth=2, fill='purple')
        drawLine(cx1, beamY, cx1 - 8, beamY - 8*d, lineWidth=2, fill='purple')
        drawLine(cx1, beamY, cx1 + 8, beamY - 8*d, lineWidth=2, fill='purple')

        # end arrow
        drawLine(cx2, y2, cx2, beamY, lineWidth=2, fill='purple')
        drawLine(cx2, beamY, cx2 - 8, beamY - 8*d, lineWidth=2, fill='purple')
        drawLine(cx2, beamY, cx2 + 8, beamY - 8*d, lineWidth=2, fill='purple')

        # labels
        drawLabel(str(startLoad), cx1, y1 - 15*d, size=15)
        drawLabel(str(endLoad), cx2, y2 - 15*d, size=15)
def plotGraphs(app):
    shearPoints, momentPoints = calcShearMoment(app)
    plotShearMoment(app, shearPoints, app.height/4-80, app.height/4, 'Shear Force on Beam', 'red')
    plotShearMoment(app, momentPoints, app.height/2-10, app.height/4, 'Bending Moment', 'blue')
    if shearPoints != []:
        x = app.sidePanelWidth + 30
        y = -50 + app.height*3/8

        drawLabel('Shear', x, y - 10, size=10, align='center')
        drawLabel('Force', x, y, size=10, align='center')
        drawLabel('(N)', x, y + 10, size=10, align='center')

        y = app.height*5/8
        drawLabel('Bending', x, y - 10, size=10, align='center')
        drawLabel('Moment', x, y, size=10, align='center')
        drawLabel('(Nm)', x, y + 10, size=10, align='center')
def redrawAll(app):
    # side panel
    drawRect(0, 0, app.sidePanelWidth, app.height,
             fill='darkBlue', opacity=25)

    # label
    drawLabel('Rod Length',
              app.sidePanelWidth/2, 75,
              size=20, bold=True, align="center")
    drawLabel('Support',
              app.sidePanelWidth/2, 225,
              size=20, bold=True, align="center")
    drawLabel('Point Loads', app.sidePanelWidth/2, 375,
              size=20, bold=True, align='center')
    drawLabel('Distributed Loads', app.sidePanelWidth/2, 675,
              size = 20, bold = True, align = 'center')

    # divider line
    drawLine(0, 175, app.sidePanelWidth, 175, lineWidth=2)
    drawLine(0, 325, app.sidePanelWidth, 325, lineWidth = 2)
    drawLine(0, 625, app.sidePanelWidth, 625, lineWidth=2)

    # draw UI
    for button in app.buttons:
        button.draw()

    #change colors of boxes
    for button in app.supportButtons:
        changePointLoadColors_and_Support(app,button)
        button.draw()
    for button in app.pointLoadButtons:
        changePointLoadColors_and_Support(app, button)
        button.draw()
    for button in app.distLoadButtons:
        changeDistLoadColors(app,button)
        button.draw()
    for textBox in app.textBoxes:
        textBox.draw()

    #draw beam and attatchments
    drawBeam(app)
    drawSupports(app)
    drawPointLoads(app)
    plotGraphs(app)
    drawDistLoads(app)
    
    # title
    drawLabel('Shear And Moment Graphing Calculator',
              app.width/2, 50,
              size=30, bold=True)

runApp(width=1500, height=1000)
#cmu_graphis.run()