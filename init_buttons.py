from button import Button
from shear_moment import plotShearMoment
import random
buttonWidth = 50
buttonHeight = 50

def distConvert(app, og1):
    beamLeft = app.width*5/8 - app.width/4
    beamWidth = app.width/2
    x1 = beamLeft + (og1 / app.rodLeng) * beamWidth
    return x1
def clearAll(app):
    app.rodLeng = None
    app.selectedSupport = None
    app.selectedPointLoadDir = None
    app.selectedDistLoadDir = None
    app.supports = []
    app.pointLoads = []
    app.distLoads = []
    for box in app.textBoxes:
        box.text = box.defaultText
        box.isDefaultText = True

def initializeRodButtons(app):
    buttonLeft = app.sidePanelWidth - app.sideMargin - buttonWidth

    def rodLengAdd():
        rodLeng = app.textBoxes[0].getValue()
        if rodLeng <2:
            return
        app.rodLeng = rodLeng

    box = app.textBoxes[0]
    rodLeng = Button(buttonLeft, box.top, buttonWidth, buttonHeight, 'lightBlue', 'Save', 12, rodLengAdd)

    app.rodButtons = [rodLeng]
    app.buttons = app.rodButtons

#---------
    #support
#--------
def initializeSupportButtons(app):
    buttonLeft = app.sidePanelWidth - app.sideMargin - buttonWidth

    def pinAdd():
        app.selectedSupport = 'pinned'

    def rollerAdd():
        app.selectedSupport = 'roller'

    def addSupport():
        supportLoc = app.textBoxes[1].getValue()
        if app.selectedSupport == None or app.rodLeng == None or supportLoc == None or len(app.supports) >= 2:
            return
        if supportLoc > app.rodLeng:
            return
        
        beamLeft = app.width*5/8 - app.width/4
        beamWidth = app.width/2
        x = beamLeft + (supportLoc / app.rodLeng) * beamWidth

        app.supports.append({
            'type': app.selectedSupport,
            'location': x,
            'Beam Location': supportLoc
        })
    
    #buttons for support
    box = app.textBoxes[1]
    pinSupport = Button(buttonLeft - buttonWidth*2.5, box.top, buttonWidth, buttonHeight, 'white', 'Pinned', 12, pinAdd)
    rollerSupport = Button(buttonLeft - buttonWidth*1.5, box.top, buttonWidth, buttonHeight, 'white', 'Roller', 12, rollerAdd)
    Support = Button(buttonLeft, box.top, buttonWidth, buttonHeight, 'lightBlue', 'Add', 12, addSupport)

    app.supportButtons = [pinSupport, rollerSupport, Support]
    app.buttons += app.supportButtons

#-----
# Point Load
#-----
def initializePointLoadButtons(app):
    buttonLeft = app.sidePanelWidth - app.sideMargin - buttonWidth
    def pointUpAdd():
        app.selectedPointLoadDir = 'up'
    def pointDownAdd():
        app.selectedPointLoadDir = 'down'
    def addLoad():
        loadLoc = app.textBoxes[2].getValue()
        loadMagn = app.textBoxes[3].getValue()

        if app.rodLeng == None or app.selectedPointLoadDir == None:
            return
        if loadLoc == None or loadMagn == None or loadMagn == '' or loadLoc == '':
            return
        if loadLoc > app.rodLeng:
            return

        beamLeft = app.width*5/8 - app.width/4
        beamWidth = app.width/2
        x = beamLeft + (loadLoc / app.rodLeng) * beamWidth

        app.pointLoads.append(({
            'location': x,
            'Beam Location': loadLoc,
            'magnitude': loadMagn,
            'direction': app.selectedPointLoadDir
        }))
        
    boxLoad = app.textBoxes[2]
    pointLoadUp = Button(buttonLeft - buttonWidth*2.5, boxLoad.top + 75, buttonWidth, buttonHeight, 'white', 'Up', 12, pointUpAdd)
    pointLoadDown = Button(buttonLeft - buttonWidth * 1.5, boxLoad.top + 75, buttonWidth, buttonHeight, 'white', 'Down', 12, pointDownAdd)
    pointLoad = Button(buttonLeft,boxLoad.top + 75, buttonWidth, buttonHeight, 'lightBlue', 'Add', 12, addLoad)
    app.pointLoadButtons = [pointLoadUp, pointLoadDown, pointLoad]
    app.buttons += app.pointLoadButtons


#-----
# Distributed Load
#-----
def initializeDistLoadButtons(app):
    buttonLeft = app.sidePanelWidth - app.sideMargin - buttonWidth

    def distUpAdd():
        app.selectedDistLoadDir = 'up'

    def distDownAdd():
        app.selectedDistLoadDir = 'down'

    def addDistLoad():
        startLoc  = app.textBoxes[4].getValue()
        startLoad = app.textBoxes[5].getValue()
        endLoc    = app.textBoxes[6].getValue()
        endLoad   = app.textBoxes[7].getValue()

        if app.rodLeng == None or app.selectedDistLoadDir == None:
            return
        if startLoc == None or endLoc == None or startLoad == None or endLoad == None:
            return
        if startLoc < 0 or endLoc < 0 or startLoc > app.rodLeng or endLoc > app.rodLeng:
            return
        if startLoc >= endLoc:
            return
        startX= distConvert(app, startLoc)
        endX = distConvert(app, endLoc)

        app.distLoads.append({
            'start location': startX,
            'end location': endX,
            'Start Beam': startLoc,
            'End Beam': endLoc,
            'start load': startLoad,
            'end load': endLoad,
            'direction': app.selectedDistLoadDir
        })

    boxLoad = app.textBoxes[6]

    distLoadUp = Button(buttonLeft - buttonWidth*2.5, boxLoad.top + 75,
                        buttonWidth, buttonHeight, 'white', 'Up', 12, distUpAdd)

    distLoadDown = Button(buttonLeft - buttonWidth*1.5, boxLoad.top + 75,
                          buttonWidth, buttonHeight, 'white', 'Down', 12, distDownAdd)

    distLoadAdd = Button(buttonLeft, boxLoad.top + 75,
                         buttonWidth, buttonHeight, 'lightBlue', 'Add', 12, addDistLoad)

    app.distLoadButtons = [distLoadUp, distLoadDown, distLoadAdd]
    app.buttons += app.distLoadButtons

def initializeAuto(app):
    def autoAdd():
        clearAll(app)

        supportOptions = ['pinned', 'roller']
        loadDirOptions = ['up', 'down']

        app.rodLeng = random.randint(2,100)
        #changing values of text box for length
        app.textBoxes[0].text = str(app.rodLeng)
        app.textBoxes[0].isDefaultText = False

        supportType1 = supportOptions[random.randint(0,1)]
        supportType2 = supportOptions[random.randint(0,1)]
        supportLoc1, supportLoc2 = random.sample(range(0,app.rodLeng), 2)
        app.selectedSupport = supportType2
        app.selectedPointLoadDir = loadDirOptions[random.randint(0,1)]
        app.selectedDistLoadDir = loadDirOptions[random.randint(0,1)]

        x1, x2 = distConvert(app, supportLoc1), distConvert(app, supportLoc2)
        app.supports = [{'location': x1, 'Beam Location': supportLoc1, 'type': supportType1}, 
                        {'location': x2, 'Beam Location': supportLoc2, 'type': supportType2}]
        
        numPointLoads = random.randint(1,20)
        for i in range(numPointLoads):
            pointLoc = random.randint(0,app.rodLeng)
            x = distConvert(app, pointLoc)
            magnitude = random.randint(1,1000)
            direction = loadDirOptions[random.randint(0,1)]
            app.pointLoads.append({'location': x, 
                                   'magnitude': magnitude, 
                                   'Beam Location': pointLoc, 
                                   'direction': direction})
            

        numDistLoads = random.randint(1,5)
        for i in range(numDistLoads):
            startLoc, endLoc = random.sample(range(0,app.rodLeng), 2)
            startX = distConvert(app, startLoc)
            endX = distConvert(app, endLoc)
            startLoad, endLoad = sorted(random.sample(range(0,1000),2))
            direction = loadDirOptions[random.randint(0,1)]
            app.distLoads.append({
                'start location': startX,
                'end location': endX,
                'Start Beam': startLoc,
                'End Beam': endLoc,
                'start load': startLoad,
                'end load': endLoad,
                'direction': direction
            })

    auto = Button(app.width - 100, 100, 50, 50, 'blue', 'Auto', 12, autoAdd)
    app.buttons += [auto]


def initializeOtherButtons(app):
    def makeClear():
        clearAll(app)
    clear = Button(app.width-100, 50, 50, 50, 'red','Clear', 15, makeClear)
    app.buttons+=[clear]




