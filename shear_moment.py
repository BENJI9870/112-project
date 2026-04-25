from cmu_graphics import *
#chat gpt helped make the equations and make sure i called the correct keys for
#both functions
def calcShearMoment(app):
    if app.rodLeng == None or len(app.supports) < 2:
         return [], []
    if app.pointLoads == [] and app.distLoads==[]:
         return [], []
    L = app.rodLeng

    supports = sorted(app.supports, key=lambda s: s['Beam Location'])
    A = supports[0]
    B = supports[1]

    xA = A['Beam Location']
    xB = B['Beam Location'] 

    loadSum = 0
    loadSumDist = 0

    for load in app.pointLoads:
         d = -1 if load['direction'] == 'down' else 1
         P = load['magnitude'] * d
         x = load['Beam Location']

         loadSum += P
         loadSumDist += P * (x - xA)
    for load in app.distLoads:
         d = -1 if load['direction'] == 'down' else 1

         x1 = load['Start Beam']
         x2 = load['End Beam']
         w1 = load['start load'] * d
         w2 = load['end load'] * d

         totalForce = (w1 + w2) / 2 * (x2 - x1)

         if w1 + w2 == 0:
              centroid = (x1 + x2) / 2
         else:
              centroid = x1 + (x2 - x1) * (w1 + 2*w2) / (3*(w1 + w2))
         loadSum += totalForce
         loadSumDist += totalForce * (centroid - xA)

    reactB = -loadSumDist / (xB - xA)
    reactA = -loadSum - reactB

    shearPoints = []
    momentPoints = []
    steps = 100

    for i in range(steps+1):
         x = L * i / steps

         V = 0
         M = 0

         if x >= xA:
              V += reactA
              M += reactA * (x - xA)

         if x >= xB:
              V += reactB
              M += reactB * (x - xB)

         for load in app.pointLoads:
              d = -1 if load['direction'] == 'down' else 1
              P = load['magnitude'] * d
              xP = load['Beam Location']

              if x >= xP:
                   V += P
                   M += P * (x - xP)
         for load in app.distLoads:
               d = -1 if load['direction'] == 'down' else 1

               x1 = load['Start Beam']
               x2 = load['End Beam']
               w1 = load['start load'] * d
               w2 = load['end load'] * d

               if x > x1:
                    usedEnd = min(x, x2)
                    usedLength = usedEnd - x1

                    if usedLength > 0:
                         # load intensity at current usedEnd
                         wEnd = w1 + (w2 - w1) * (usedLength / (x2 - x1))

                         totalForce = (w1 + wEnd) / 2 * usedLength

                         if w1 + wEnd == 0:
                              centroid = x1 + usedLength / 2
                         else:
                              centroid = x1 + usedLength * (w1 + 2*wEnd) / (3*(w1 + wEnd))

                         V += totalForce
                         M += totalForce * (x - centroid)
         shearPoints.append((x, V))
         momentPoints.append((x, M))
   
    return shearPoints, momentPoints
 

def plotShearMoment(app, points, top, height, title, color):
     if points == []:
          return
     left = app.sidePanelWidth + 75
     width = app.width - app.sidePanelWidth - 150

     drawLabel(title, left + width/2, top - 20, size=18, bold=True)

     # axis
     zeroY = top + height/2
     drawLine(left, zeroY, left + width, zeroY, lineWidth= 4, fill='black')

     maxY = max(abs(y) for x, y in points)
     if maxY == 0:
          maxY = 1

     prevX, prevY = None, None

     for x, y in points:
          screenX = left + (x / app.rodLeng) * width
          screenY = zeroY - (y / maxY) * (height/2 - 10)

          if prevX != None:
               drawLine(prevX, prevY, screenX, screenY, fill=color, lineWidth=2)

          prevX, prevY = screenX, screenY

     for i in range(11):
          gridX = left + i * width / 10
          drawLine(gridX, top, gridX, top+height,
               opacity=30, lineWidth=1)
          x = app.rodLeng * i/10
          drawLabel(str(x),gridX, top+height+5, size = 10)
     drawLabel('Distance on Beam (m)', left + width/2, top+height+20, size = 10)
     for i in range(5):
          gridY = top + i * height / 4
          drawLine(left, gridY, left+width, gridY,
               opacity=30, lineWidth=1)
          y = maxY - maxY*2 *i/4
          drawLabel(str(int(y)),left-10, gridY, size = 10)

     





    

