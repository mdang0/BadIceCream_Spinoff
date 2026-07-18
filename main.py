'''Features: Create Ice, Break Ice, Enemy Tracking, Player + Enemy Random Spawn'''

from cmu_graphics import *
import math 
import copy
import random
def onAppStart(app):
    

    LEVEL_1 = [
    ['W', 'W', 'W','W','W','W','W','W','W','W'],
    ['W', '', 'W','','','W','W','','W','W'],
    ['W', '', '','','','','','','','W'],
    ['W', '', '','','F','','W','F','W','W'],
    ['W', 'W', '','','','I','','','','W'],
    ['W', '', '','','F','','','','','W'],
    ['W', '', '','I','','','','','','W'],
    ['W', '', '','','','','','','','W'],
    ['W', '', '','','','','I','','','W'],
    ['W', 'W', 'W','W','W','W','W','W','W','W']
    
    ]
    
    LEVEL_2 = [
    ['W', 'W', 'W','W','W','W','W','W','W','W'],
    ['W', 'F', 'W','','W','W','W','','W','W'],
    ['W', '', '','','W','','','','','W'],
    ['W', '', '','','F','','W','F','W','W'],
    ['W', 'W', '','','W','I','','','','W'],
    ['W', '', '','','F','','','W','W','W'],
    ['W', 'FI', '','I','W','','','','','W'],
    ['W', 'FI', '','','','','','','FI','W'],
    ['W', '', 'F','','','','I','','','W'],
    ['W', 'W', 'W','W','W','W','W','W','W','W']
    
    ]
    
    LEVEL_3 = [
    ['W', 'W', 'W','W','W','W','W','W','W','W'],
    ['W', 'F', '','','','W','W','','W','W'],
    ['W', '', 'W','','','','','','','W'],
    ['W', '', 'I','W','F','FI','W','F','W','W'],
    ['W', 'W', '','','','I','','F','','W'],
    ['W', '', '','W','F','','','F','W','W'],
    ['W', '', '','I','','W','','','','W'],
    ['W', '', 'FI','W','','','','FI','','W'],
    ['W', 'F', '','W','','','I','','','W'],
    ['W', 'W', 'W','W','W','W','W','W','W','W']
    ]
        
    app.levels = {
        1: LEVEL_1,
        2: LEVEL_2,
        3: LEVEL_3
    }
    app.enemyCount = {
        1: 1,
        2: 1,
        3: 2
    }
    resetApp(app)
    
def resetApp(app):
    #start constants
    app.rectX1, app.rectTop1, app.rectW1, app.rectH1 = 100, 120, 200, 60
    app.rectX2, app.rectTop2, app.rectW2, app.rectH2 = 100, 200, 200, 60
    app.rectX3, app.rectTop3, app.rectW3, app.rectH3 = 100, 280, 200, 60
    
    #board constants
    app.fill = 'skyBlue'
    app.margin = 40
    app.boardLeft = app.margin
    app.boardTop = app.margin
    app.boardWidth = app.width - 2*app.margin
    app.boardHeight = app.height - 2*app.margin
    app.cellBorderWidth = 2

    
    #game constants
    app.timer = 30
    app.timesOver = False
    app.timeCounter = 0
    app.isPaused = False
    app.stepsPerSecond = 30
    
    app.blockCooldown= False
    app.cooldownCounter = 0
    app.cooldownTimer = 0
    app.gameOver = False
    app.win = False
    app.fruits = []
    app.enemies = []
  
    
# help screen
def help_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='lightCyan')
    drawLabel('HOW TO PLAY', app.width/2, 50, size=40, bold=True, fill='navy')
    
    instructions = [
        '- Move player (black) with W A S D',
        "- Shoot Ice with SPACE in direction of player",
        '- Break Ice with F',
        "- Avoid the pursuing enemies (red)",
        '- Collect all fruits (orange) before time is out',
        '- BREAK the ice to collect fruit (green)',
        "", 
        'Press ENTER to begin :)',
        'Note: freeze your enemies and not yourself!'
        ""
        
        ]
    y = 100
    for line in instructions:
        drawLabel(line, app.width/2, y, size = 20, fill='black')
        y += 35
    
    
def help_onKeyPress(app, key):
        
    if key == 'enter':
        setActiveScreen('game')
    if key == 'tab':
        setActiveScreen('start')
#set start Screen 
#---------------------------
def start_redrawAll(app):
    drawRect(0, 0 , app.width, 100, fill='skyBlue')
    drawLabel('Bad Ice Cream', app.width/2, 60, size = 40, bold = True, font = 'arial')
    drawRect(0, 100, app.width, app.height, fill = 'pink')
    drawRect(app.rectX1, app.rectTop1, app.rectW1, app.rectH1, fill = 'white', border = 'black')
    drawLabel('Level 1', 200, 150, size = 20)
    drawRect(100, 200, 200, 60, fill = 'white', border = 'black')
    drawLabel('Level 2', 200, 230, size = 20)
    drawRect(100, 280, 200, 60, fill = 'white', border = 'black')
    drawLabel('Level 3', 200, 310, size = 20)


def start_onMousePress(app, mouseX, mouseY):
    if app.rectX1 <= mouseX <= app.rectX1 + app.rectW1 and app.rectTop1 <= mouseY <= app.rectTop1 + app.rectH1:
       
        startLevel(app, 1)
        setActiveScreen('help')
        return
        setActiveScreen('game')
        
    
    if app.rectX2 <= mouseX <= app.rectX2 + app.rectW2 and app.rectTop2 <= mouseY <= app.rectTop2 + app.rectH2:
        startLevel(app, 2)
        setActiveScreen('game')
        
    if app.rectX3 <= mouseX <= app.rectX3+app.rectW3 and app.rectTop3  <= mouseY <= app.rectTop3 + app.rectH3:
        startLevel(app, 3)
        setActiveScreen('game')
    else:
        return 
    

# set gameScreen----

def startLevel(app, selectedLevel):
    
    app.selectedLevel = selectedLevel
  
    app.board = copy.deepcopy(app.levels[app.selectedLevel])
    app.rows = len(app.board)
    app.cols = len(app.board[0])
    
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] in ['F', 'FI']:
                app.fruits.append((row, col))
                
    app.points = 0
    #character constants
    
    app.playerSpeed = 3
    pr,pc = findEmptyCell(app)
    px, py = celltoXY(app,pr, pc)
    app.player = Player(px, py, 10)
    
    
    for _ in range(app.enemyCount[selectedLevel]):
        getPlayerEnemySpawn(app, pr, pc)
    
#---- game mechanics ------    
class Player:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.direction = 'right' #default facing direction
       
    
    def move(self,app,dx,dy):
        
        cell = getCell(app, app.player.x, app.player.y) #find if touches a fruit first
        if cell != None:
            row, col = cell
            if collidesWithFruit(app,row, col):
                app.points += 1
                app.fruits.remove((row, col))
                app.board[row][col] = '' #remove fruit from board
                
                if app.fruits == []:
                    app.win = True
        
       
        if dx != 0 and dy != 0:
             scale = 1/ math.sqrt(2) #reduce speed increase for diagonal movement
        else:
            scale = 1
        
        dx *= scale
        dy *= scale
           
        newX = app.player.x + dx
        newY = app.player.y + dy
        if isValidMove(app, newX, newY, app.player.radius):
            app.player.x = newX
            app.player.y = newY

class Enemy:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
    

    def moveTowardPlayer (self, app): #used AI to help me develop this algorithm
        px, py = app.player.x, app.player.y
        
        dx = dy = 0
        
        
        if px > self.x:
            dx = self.speed #go right
            
        elif px < self.x:
            dx = -self.speed #go left
        
        if py > self.y:
            dy = self.speed #go down
        elif py < self.y:
            dy = -self.speed #go up
        
        self.tryMove(app, dx, 0) #move horizontal first
        self.tryMove(app, 0, dy) #move vertical next
    
    def tryMove(self, app, dx, dy):
        
        if dx == dy == 0:
            
            return
        newX = self.x + dx
        newY = self.y + dy
        
        if isValidMove(app, newX, newY, self.radius):
            self.x = newX
            self.y = newY

class Level:
    def __init__(self, app, wall, ice, fruits):
        
        self.wall = wall
        self.ice = ice
        self.fruits = fruits
        
        
    def findOptimalBoard(self, app):
        board = [([None] * app.cols) for row in range(app.rows)]
        cells = [(r,c) for r in range(app.rows) for c in range(app.cols)]
        random.shuffle(cells) #looked up on python library for random methods
        
        def place(target, char):
            for _ in range(target):
               
                r,c = cells.pop()
                board[r][c] = char
            
        place(self.wall, 'W')
        
        place(self.fruits, 'F')
        
        place(self.ice, 'I')
    
        for r in range(app.rows):
            for c in range(app.cols):
                if board[r][c] == None:
                    board[r][c] = ''
        return board
        

        
def findEmptyCell(app):
    emptyCellList = []
    myCells = []
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == '':
                emptyCellList.append((row, col))
    random.shuffle(emptyCellList) #make sure player or enemy is not in same place
    return (emptyCellList.pop())
    

def celltoXY(app, row, col):
    cellW, cellH = getCellSize(app)
    x = app.boardLeft + cellW * col + cellW/2
    y = app.boardTop + cellH * row + cellH/2
    return x, y


def getPlayerEnemySpawn(app, pr, pc):
    minSpawnDistance = 5
    
    while True:
        
        er,ec = findEmptyCell(app)
        
        dist = abs(pr-er) + abs(pc-ec) #searched mahattan distance
        
        if dist >= minSpawnDistance:
            #valid spawn
            
            ex, ey = celltoXY(app,er, ec)
            
            app.enemies.append(Enemy(ex, ey, 10 ,1.5))
            return
            
def loadFruit(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == 'F':
                app.fruits.append((row, col))
    return None


def enemyTouchesPlayer(app, enemy):
    ex, ey = enemy.x, enemy.y
    px, py = app.player.x, app.player.y
    
    distance = ((ex-px)**2 + (ey-py)**2)**0.5
    return distance < (enemy.radius + app.player.radius)
                  
def isValidMove(app, newX, newY, radius): #check every edge of circle
    edgePoints = [
        (newX - radius, newY),
        (newX + radius, newY),
        (newX, newY-radius),
        (newX, newY+radius)
        ]
    for (px, py) in edgePoints:
        cell = getCell(app, px, py)
        if cell == None:
            return False
        
        row, col = cell
        if app.board[row][col] in ['W', 'I', 'FI']:
            return False
  
        if not (0 <= row< app.rows and 0 <= col < app.cols):
            return False
           
            
    return True
       

#check for pickup fruit for points    
def collidesWithFruit(app, row, col):
    return (row, col) in app.fruits and app.board[row][col] == 'F'

def createIce(app):
    direction = app.player.direction
    
    cell = getCell(app, app.player.x, app.player.y)
    enemyCells = {getCell(app, e.x, e.y) for e in app.enemies}
    
    if cell == None:
        return
    row, col = cell
        
    def placeIce(row, col):
        if app.board[row][col] == 'F':
            app.board[row][col] = 'FI'
        elif app.board[row][col] == '':
            app.board[row][col] = 'I'
            
    if not app.blockCooldown:
        if direction == 'right':
            for c in range(col+1, app.cols):
                if (row, c) in enemyCells:
                    break
                
                if app.board[row][c] == 'W': break
                if app.board[row][c] == 'I': break
                placeIce(row, c)
                        
        elif direction == 'left':
            for c in range(col-1, -1, -1):
                if (row, c) in enemyCells: break
                if app.board[row][c] == 'W': break
                if app.board[row][c] == 'I':break
                placeIce(row, c)
            
        elif direction == 'up':
            
            for r in range(row-1, -1, -1):
                if (r, col) in enemyCells: break
                    

                if app.board[r][col] == 'W': break
                if app.board[r][col] == 'I': break
                placeIce(r, col)
                    
        elif direction == 'down':
            for r in range(row+1, app.rows):
                if (r, col) in enemyCells: break
                    
                
                if app.board[r][col] == 'W': break
                if app.board[r][col] == 'I': break
                placeIce(r, col)
        
        app.blockCooldown = True #boolean to signal cooldown for shooting ice

def breakIce(app):
   
        direction = app.player.direction
        
        cell = getCell(app, app.player.x, app.player.y)
        if cell == None:
            return
        
        row, col = cell
             
              
        def breakIce(row, col):
            if app.board[row][col] == 'I':
                app.board[row][col] = ''
            elif app.board[row][col] == 'FI':
                app.board[row][col] = 'F'
            
        if direction == 'right':
            for c in range(col, app.cols):
                if app.board[row][c] == 'W': break
                breakIce(row, c)

               
        if direction == 'left':
            for c in range(col,-1, -1): #start from player to wall
                if app.board[row][c] == 'W': break
                breakIce(row, c)

            
        if direction == 'up':
            for r in range(row, -1, -1):
                if app.board[r][col] == 'W': break
                breakIce(r, col)
               
               
                    
        if direction == 'down':
            for r in range(row, app.rows):
                if app.board[r][col] == 'W': break
                breakIce(r, col)
               
    

# draw 2d board cmu_notes

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill='skyBlue', border='black',
           borderWidth=2*app.cellBorderWidth)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)
            
def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    cell = app.board[row][col]
    
    if cell == 'W':
        color = 'brown'
    elif cell == 'F':
        color = 'orange'
    elif cell == 'I':
        color = 'cyan'
    elif cell=='FI':
        color = 'green'
    else:
        color = 'white'
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color)

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
    

#---- GAME SCREEN ------
def game_takeStep(app):
    #set time limit
    
    #make sure player can't spam blocks 
    if app.blockCooldown:
        app.cooldownTimer += 1
        if app.cooldownTimer > app.stepsPerSecond:
            app.cooldownTimer = 0 #reset 
            app.cooldownCounter += 1 #each second pass
            if app.cooldownCounter == 1: #1 seconds
                app.cooldownCounter = 0
                app.blockCooldown = False
                
    app.timeCounter += 1            
    if app.timer == 0:
        app.timesOver = True
    else:
        if app.timeCounter > app.stepsPerSecond:
            app.timeCounter = 0
            app.timer -= 1
            
def game_onStep(app):
    if app.isPaused or app.gameOver or app.win or app.timesOver:
        return
    
    game_takeStep(app)
    
    for enemy in (app.enemies):
        enemy.moveTowardPlayer(app)
        if enemyTouchesPlayer(app, enemy):
            app.gameOver = True
        
def game_redrawAll(app):
    
    if app.gameOver:
        clearBoard(app)
        drawLabel('YOU DIED', app.width/2, app.height/2, size = 20)
        drawLabel('Press r to restart', app.width/2, app.height/2 + 50, size =16)
        drawLabel('Press tab for levels', app.width/2, app.height/2 + 90, size =16)
        return
    if app.win:
        clearBoard(app)
        drawLabel('LEVEL CLEARED', app.width/2, app.height/2, size = 20)
        drawLabel('Press tab to return', app.width/2, app.height/2 + 50, size =16)
        return
    
    if app.timesOver:
        clearBoard(app)
        drawLabel('TIME IS UP', app.width/2, app.height/2, size = 20)
        drawLabel('Press r to restart', app.width/2, app.height/2 + 50, size =16)
        drawLabel('Press tab for levels', app.width/2, app.height/2 + 90, size =16)
        return
    
    
    drawBoard(app)
    drawTimer(app)
    drawFruitLeft(app)
    drawDirection(app)
   


    #draw player
    p = app.player
    drawCircle(p.x, p.y, p.radius) 
    
   
    for e in (app.enemies):
        drawCircle(e.x, e.y, e.radius, fill='red')
        
def game_onKeyHold(app, keys):
    app.keys = keys
    #movement
    dx = dy = 0
    if 'a' in app.keys and not app.isPaused:
        app.player.direction = 'left'
       
        dx -= app.playerSpeed
    if 'd' in app.keys and not app.isPaused:
        app.player.direction = 'right'
        dx += app.playerSpeed
    if 'w' in app.keys and not app.isPaused:
        app.player.direction = 'up'
        dy -= app.playerSpeed
    if 's' in app.keys and not app.isPaused:
        app.player.direction = 'down'
        dy+= app.playerSpeed
   
        
    app.player.move(app, dx, dy)


def game_onKeyPress(app, key):
    
    if key == 'space':
        createIce(app)
    if key == 'f' or key == 'F':
        breakIce(app)
    if key == 'tab':
        setActiveScreen('start')
        resetApp(app)
    if key == 't' or key == 'T':
        app.isPaused = not app.isPaused
    
    if key == 'r' or key =='R':
        resetApp(app)
        startLevel(app, app.selectedLevel)

    if key == 'h' or key == 'H':
        setActiveScreen('help')
        
#--- ADDITIONAL HELPERS
def drawTimer(app):
    size = 50
    drawLabel(f' Time Left: {app.timer}', app.width/2-100, size/2, size = 20, fill = 'black')

def drawFruitLeft(app):
    size = 50
    drawLabel(f' Fruits Left: {len(app.fruits)}', app.width/2+size*2, size/2, fill = 'black', size = 20)


def drawDirection(app):
    size= 50
    direction = app.player.direction
    direction = direction.upper()
    drawLabel(f'Player Direction: {direction}',  app.width/2, app.height-20, size =20, fill = 'brown')
    
    
def clearBoard(app):
    drawBoardBorder(app)
    



def main():

   
    runAppWithScreens(initialScreen = 'start') #screens from cmu_utils
main()