from button import textBox


from button import Button

def initializeTextBoxes(app):
    # textBox(left, top, width, height, textSize)
    boxLeft = 10
    boxTop = 100
    boxWidth = 100
    boxHeight = 50
    yd = 150
    xd = 120   # horizontal spacing for 2-column layout

    rodLeng = textBox(boxLeft, boxTop, boxWidth, boxHeight, 16, 'Enter Length (m)')
    supportLoc = textBox(boxLeft, boxTop + yd, boxWidth, boxHeight, 16, 'Enter Position (m)')

    pointLoadLoc = textBox(boxLeft, boxTop + yd*2, boxWidth, boxHeight, 16, 'Enter Position (m)')
    pointLoadMagn = textBox(boxLeft, boxTop + yd*3, boxWidth, boxHeight, 16, 'Enter Force (N)')

    distTop = boxTop + yd*4

    distStartLoc = textBox(boxLeft, distTop, boxWidth, boxHeight, 14, 'Start Postion (m)')
    distStartLoad = textBox(boxLeft + xd, distTop, boxWidth, boxHeight, 14, 'Start Load (N)')
    distEndLoc = textBox(boxLeft, distTop + boxHeight + 10, boxWidth, boxHeight, 14, 'End Postion (m)')
    distEndLoad = textBox(boxLeft + xd, distTop + boxHeight + 10, boxWidth, boxHeight, 14, 'End Load (F)')

    app.textBoxes = [
        rodLeng,
        supportLoc,
        pointLoadLoc,
        pointLoadMagn,
        distStartLoc,
        distStartLoad,
        distEndLoc,
        distEndLoad
    ]


    