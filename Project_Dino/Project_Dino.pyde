add_library('minim')

def setup():
    global totalScore, gamePause, gameSpeed
    size(1200, 600)

    totalScore = 0
    gamePause = 0
    
    #Game difficulty
    gameSpeed = 1
    
    #Testing use
    global collisionOn
    collisionOn = True
    
    global minim, bgmusic, jumpmusic, gameovermusic
    minim= Minim(this)
    bgmusic = minim.loadFile("BackgroundMusic.mp3")
    bgmusic.loop()
    
    jumpmusic = minim.loadFile("JumpingSoundEffect.mp3")
    gameovermusic = minim.loadFile("GameOverSound Effect.mp3")
    
    #Dino
    global DinoTotal, day_Dino
    global night_DinoTotal, night_Dino
    global dinoSize
    global DinoLeftConX, DinoLeftConY
    global DinoRightConX, DinoRightConY
    dinoSize = 120
    # 1 2 = run / 3 = jump / 4 5 = duck / 6 = die
    DinoTotal = 6
    day_Dino = []
    night_Dino = []
    DinoLeftConX = 19
    DinoLeftConY = 34
    DinoRightConX = 36
    DinoRightConY = 57
    night_DinoTotal = 6
    
    for i in range(DinoTotal):
        day_Dino.append(loadImage("day_Dino" + str(i+1) + ".png"))
        night_Dino.append(loadImage("night_Dino" + str(i+1) + ".png"))
        
    #obstacles
    global obstacle, obstacleTotal, obstacleX, obstacleY, obstacleSizeX, obstacleSizeY
    global obstacleNo
    obstacleTotal = 4
    obstacle = []
    obstacleX = []
    obstacleY = []
    obstacleSizeX = [110, 160, 90, 240]
    obstacleSizeY = [110, 110, 150, 150]
    obstacleNo = int(random(0, 4))
    
    for i in range(obstacleTotal):
        obstacle.append(loadImage("obstacle" + str(i+1) + ".png"))
        obstacleX.append(width*1.5)
        obstacleY.append(400)

    #background image
    global Cloud, CloudX, CloudY, CloudSize, CloudDX
    Cloud = loadImage("Cloud.png")
    CloudX = []
    CloudY = []
    CloudDX = []
    CloudSize = 205
    
    for i in range(3):
        CloudX.append(random(width*1.5, width*3))
        CloudY.append(random(0, height/10*4))
        CloudDX.append(random(5, 10))
        
    global night_moon, night_moonX, night_moonY, night_moonSize
    night_moon = loadImage("night_moon.png")
    night_moonX = width*1.2
    night_moonY = random(0, height/10*2)
    night_moonSize = 120
    
    #Text
    global StartText
    StartText = loadImage("StartText.png")
    
    global GameOverText
    GameOverText = loadImage("GameOverText.png")
    
    global restartbutton, restartbuttonX, restartbuttonY, restartbuttonSize
    restartbutton = loadImage("restartbutton.png")
    restartbuttonX = 550
    restartbuttonY = 350
    restartbuttonSize = 50
    
    #daygamerun
    global lineX, linedX
    lineX = 0
    linedX = 20
    
    global dinoX, dinoY, dinoJump, gravity, grounded
    dinoX = 50
    dinoY = 0
    
    #deletion of jumping
    dinoJump = 0
    gravity = 8
    grounded = False
    
    #deletion of running
    global totalRun
    totalRun = 0
    
    #Game Stage
    global Gamestage
    Gamestage = 0
    
    #The gap time of the scenario between day and night 
    global totalCircle, daynightGap
    totalCircle = 20 #50
    daynightGap = 10 #25
    
    #graduation of Background Colour
    global GradualColour
    GradualColour = 255
    
    #determine the game is in the first loop or not
    global daynightLoop
    daynightLoop = 0
    
def draw():
    global Gamestage
    if Gamestage == 0: 
        gamestart()
    elif Gamestage == 1: 
        gamerun()
    elif Gamestage == 2:
        daygameover()

def keyPressed():
    global dinoJump, Gamestage, gamePause, StartScore
    global totalScore
    if Gamestage == 0 and key == " ":
        Gamestage = 1
        dinoJump = -30
        StartScore = millis()/100
        if Gamestage == 0 or Gamestage == 1:
            jumpmusic.play()
            jumpmusic.rewind()
        
    if grounded == True and key == " ":
        dinoJump = -30 
        if Gamestage == 0 or Gamestage == 1:
            jumpmusic.play()
            jumpmusic.rewind()

    if Gamestage == 1:
        if key == "R" or key == "r":
            Gamestage = 2
        elif key == "P" or key == "p":
            if gamePause == False:
                totalScore = CurrentScore
                bgmusic.pause()
                gamePause = True
            elif gamePause == True:
                StartScore = millis()/100
                bgmusic.play()
                gamePause = False
        
def mousePressed():
    if mouseX >= restartbuttonX and \
    mouseY >= restartbuttonY and \
    mouseX <= restartbuttonX + restartbuttonSize and \
    mouseY <= restartbuttonY + restartbuttonSize:
        setup()
    
def gamestart():
    background(255)
    image(StartText, 200, 60)
    line(0, 505, 200, 505)
    image(day_Dino[2], 50, 400)
    fill(0)
    textSize(28)
    text("When Game is Running", 440, 200)
    text("Press Spacebar to Jump", 440, 260)
    text("Press P to Pause", 480, 320)
    text("Press R to End the Game", 430, 380)
    text("Score Would be continually Counted by Time", 300, 440) 
    text("Once Hit On an Obstacle", 430, 500)
    text("GAME OVER", 510, 560)
        
def gamerun():
    global gamePause
    if gamePause == False:
        global CurrentScore, Gamestage, StartScore, totalScore
        CurrentScore = millis()/100 - StartScore + totalScore
    
        global daynightLoop
        global GradualColour
    
        if CurrentScore/10%totalCircle < daynightGap and daynightLoop > 0:
            background(GradualColour)
            GradualColour += 5
            if GradualColour >= 255:
                GradualColour = 255
                
        elif CurrentScore/10%totalCircle < daynightGap and daynightLoop == 0:
            background(255)
        else:
            background(GradualColour)
            GradualColour -= 5
            if GradualColour <= 0:
                GradualColour = 0
            daynightLoop = 1
            
            if CurrentScore/10%totalCircle >= daynightGap and daynightLoop > 0:
                dayGradualColour = 0
            else:
                nightGradualColour = 255
    
        if CurrentScore/10%totalCircle < daynightGap:
            fill(0)
            textSize(20)
            text(str(CurrentScore), 1100, 50)
        else:
            fill(255)
            textSize(20)
            text(str(CurrentScore), 1100, 50)

        #horizon
        global lineX, linedX
        if CurrentScore/10%totalCircle < daynightGap:
            stroke(0)
            line(0, 505, lineX + 200, 505)
            lineX = lineX + linedX
            if lineX + 200 > width:
                linedX = 0
        else:
            stroke(255)
            line(0, 505, lineX + 200, 505)
            
        #background
        global Cloud, CloudX, CloudY, CloudDX
        for i in range (3):
            image(Cloud, CloudX[i], CloudY[i])
            CloudX[i] = CloudX[i] - CloudDX[i] 
            
            if CloudX[i] <= 0 - CloudSize:
                CloudX[i] = random(width*1.2, width*2)
                CloudY[i] = random(0, height/10*4)
                CloudDX[i] = random(5, 10)
                
        if CurrentScore/10%totalCircle >= daynightGap:
            global night_moon, night_moonX, night_moonY, night_moonSize
            image(night_moon, night_moonX, night_moonY)
            night_moonX -= 5
            
            if night_moonX <= 0 - night_moonSize:
                night_moonX = width*1.2
                night_moonY = random(0, height/10*2)

        #running
        global totalRun, dinoX, dinoY, grounded
        global dayDinoNo, nightDinoNo
        totalRun = totalRun + 1
        if totalRun/10 < 2 and grounded == True:
            if CurrentScore/10%totalCircle < daynightGap:
                image(day_Dino[0], dinoX, dinoY + 400)
            else:
                image(night_Dino[0], dinoX, dinoY + 400)
        
        if totalRun/10 >= 2 and grounded == True:
            if CurrentScore/10%totalCircle < daynightGap:
                image(day_Dino[1], dinoX, dinoY + 400)
            else:
                image(night_Dino[1], dinoX, dinoY + 400)
            
            if totalRun >= 40:
                totalRun = 0   
                
        if grounded == False:
            if CurrentScore/10%totalCircle < daynightGap:
                image(day_Dino[2], dinoX, dinoY + 400)
            else:
                image(night_Dino[2], dinoX, dinoY + 400)
            
        #jump
        global dinoJump, gravity
        if dinoY < 0:
            dinoY += gravity
            grounded = False
        else:
            grounded = True
            
        if dinoJump < 0:
            dinoJump += 1
            
        dinoY += dinoJump
        
        global obstacleNo, gameSpeed
        image(obstacle[obstacleNo], obstacleX[obstacleNo], obstacleY[obstacleNo], obstacleSizeX[obstacleNo], obstacleSizeY[obstacleNo])
        obstacleX[obstacleNo] = obstacleX[obstacleNo] - 10*gameSpeed
        
        if obstacleX[obstacleNo] <= 0 - width*1/3:
            obstacleX[obstacleNo] = width*1.5
            obstacleNo = int(random(0, 4))
            gameSpeed += 0.05
            if gameSpeed >= 3.5:
                gameSpeed = 3.5
        
        
        global dinoSize
        global DinoLeftConX, DinoLeftConY
        global DinoRightConX, DinoRightConY
        
        #collisionOn is for Testing use
        if collisionOn == True:
            if dinoY + 400 + dinoSize - DinoRightConY >= obstacleY[obstacleNo] and \
            dinoX + dinoSize - DinoRightConX >= obstacleX[obstacleNo] and \
            dinoX + DinoLeftConX <= obstacleX[obstacleNo] + obstacleSizeX[obstacleNo]:
                Gamestage = 2
    else:
        background(GradualColour)
        line(0, 505, lineX + 200, 505)
        
        if CurrentScore/10%totalCircle < daynightGap:
            fill(0)
            textSize(20)
            text(str(CurrentScore), 1100, 50)
        else:
            fill(255)
            textSize(20)
            text(str(CurrentScore), 1100, 50)
        
        if totalRun/10 < 2 and grounded == True:
            if CurrentScore/10%totalCircle < daynightGap:
                image(day_Dino[0], dinoX, dinoY + 400)
            else:
                image(night_Dino[0], dinoX, dinoY + 400)
    
        if totalRun/10 >= 2 and grounded == True:
            if CurrentScore/10%totalCircle < daynightGap:
                image(day_Dino[1], dinoX, dinoY + 400)
            else:
                image(night_Dino[1], dinoX, dinoY + 400)
        
        if grounded == False:
            if CurrentScore/10%totalCircle < daynightGap:
                image(day_Dino[2], dinoX, dinoY + 400)
            else:
                image(night_Dino[2], dinoX, dinoY + 400)
            
        global Cloud, CloudX, CloudY
        for i in range (3):
            image(Cloud, CloudX[i], CloudY[i])
        
        if CurrentScore/10%totalCircle >= daynightGap:
            global night_moon, night_moonX, night_moonY, night_moonSize
            image(night_moon, night_moonX, night_moonY)
    
        global obstacleNo
        image(obstacle[obstacleNo], obstacleX[obstacleNo], obstacleY[obstacleNo], obstacleSizeX[obstacleNo], obstacleSizeY[obstacleNo])
    
def daygameover():
    bgmusic.close()
    gameovermusic.play()
    if CurrentScore/10%totalCircle < daynightGap:
        background(255)
        fill(0)
        line(0, 505, lineX + 200, 505)
        image(day_Dino[5], dinoX, dinoY + 400)
    else:
        background(0)
        fill(255)
        line(0, 505, lineX + 200, 505)
        image(night_Dino[5], dinoX, dinoY + 400)

    for i in range (3):
        image(Cloud, CloudX[i], CloudY[i])
        
    for i in range(obstacleTotal):
        image(obstacle[i], obstacleX[i], obstacleY[i], obstacleSizeX[i], obstacleSizeY[i])
        
    image(GameOverText, 300, 200, 600, 100)
    image(restartbutton, restartbuttonX, restartbuttonY, restartbuttonSize, restartbuttonSize)

    fill(0)
    textSize(20)
    text(str(CurrentScore), 1100, 50)
    
