from psychopy import core, event, visual, gui
import random
import numpy as np
import time

#########
## DLG ##
#########
    
q = gui.Dlg(title = "Setup")
q.addField("Subject:")
q.addField("# of blocks:",2)
q.addField("# of trials:",20)
q.addField("Tutorial", choices=["yes", "no"])
q.addField("Training block", choices=["yes", "no"])
Q = q.show()
if not q.OK:
    print("Cancelled by the user.")
    core.quit()

##############
## Settings ##
##############

subjectID = Q[0]
nBlocks = int(Q[1])
nTrials = int(Q[2])

if Q[3] == "yes": tutorial = True
else: tutorial = False

if Q[4] == "yes": blockList = range(0,nBlocks + 1) ## Block 0 is the training block.
else: blockList = range(1,nBlocks + 1)

startingScore = 0
skipPenalty = -200
highProb = 80
lowProb = 20
instrLimit = 3
trialLimit = 3
winWidth = 1280
winHeight = 720

timenow = time.localtime(time.time())
year,month,day,hour,minute,second = timenow[0:6]

def end():
    log.close()
    win.close()
    core.quit()

##############
## Log file ##
##############

log = open("logs/" + str(subjectID) +
           "_" + str(year) + str(month) + str(day) + "_" +
           str(hour) + str(minute) + str(second) +
           ".csv","w")

log.write("BLOCK_ID,TRIAL_ID,REWARD,PENALTY,POSITION,PROBABILITY,PRISM,REACTION,RT,OUTCOME,SCORE,ERROR-SCALE_RESP,ERROR-SCALE_RT,SURPRISE-SCALE_RESP,SURPRISE-SCALE_RT,SCALE_ORDER\n")

########################
## Stimuli definition ##
########################

win = visual.Window([winWidth,winHeight], gammaErrorPolicy = "ignore")

canonBody = visual.Circle(win, size = 70, units = "pix", fillColor = "black", lineColor = "black", pos = [0, -200], autoDraw = False)
canonBarrel = visual.Rect(win, size = [40,70], units = "pix", fillColor = "black", lineColor = "black", pos = [0, -150], autoDraw = False)

prismVert = visual.Rect(win, size = [40,100], units = "pix", fillColor = "black", lineColor = None, pos = [0,0])
prismHoriz = visual.Rect(win, size = [80,40], units = "pix", fillColor = "black", lineColor = None, pos = [12,0])

targetOuter = visual.Circle(win, size = 60, units = "pix", fillColor = "blue", lineColor = None, pos = [0,150], autoDraw = False)
targetMiddle = visual.Circle(win, size = 40, units = "pix", fillColor = "white", lineColor = None, pos = [0,150], autoDraw = False)
targetInner = visual.Circle(win, size = 20, units = "pix", fillColor = "blue", lineColor = None, pos = [0,150], autoDraw = False)

laserVert = visual.Line(win, start = [0,-150], end = [0,150], lineWidth = 2, units = "pix", fillColor = "cyan", lineColor = "cyan")
laserHoriz = visual.Line(win, start = [0,0], end = [200,0], lineWidth = 2, units = "pix", fillColor = "cyan", lineColor = "cyan")

message = visual.TextStim(win, text = "", pos = [0,0], units = "pix", alignHoriz = "center")
instr = visual.TextStim(win, text = "Prism %:\nHit:\nMiss:", pos = [-340,0], units = "pix", alignHoriz = "left")
values = visual.TextStim(win, text = "##\n##\n##", pos = [-250,0], units = "pix", alignHoriz = "left")
feedback = visual.TextStim(win, units = "pix")
scoreText = visual.TextStim(win, text = "SCORE: " + str(startingScore), pos = [-250,250], height = 20, units = "pix")

timer = core.CountdownTimer()
progressBar = visual.Rect(win, size = [winWidth*2,20], units = "pix", fillColor = "red", lineColor = None, pos = [0,-300], autoDraw = False)

posList = [[0,150], [200,0], [200,0]]
probList = [lowProb, highProb]

def drawCanon():
    canonBody.draw()
    canonBarrel.draw()

def drawTarget():
    targetOuter.draw()
    targetMiddle.draw()
    targetInner.draw()

def drawPrism():
    prismHoriz.draw()
    prismVert.draw()

################
##  Training  ##
################

if tutorial == True:
    score = startingScore
    
    ## Explaining the canon and target. ##
    event.clearEvents()
    message.text = "Welcome to our experiment! In this experiment, you will operate a laser canon to shoot a target.\n\n Press ENTER to continue."
    message.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    message.text = "This is what the laser canon looks like.\n\nPress ENTER to continue."
    message.draw()
    drawCanon()
    win.flip()
    event.waitKeys(keyList = "return")

    message.text = "This is your target.\n\nPress ENTER to continue."
    message.draw()
    drawTarget()
    win.flip()
    event.waitKeys(keyList = "return")

    ## How to fire the laser. ##
    event.clearEvents()
    message.text = ("You can hit the target by pressing SPACE every time your laser canon is displayed.\n\n" +
                      "Press ENTER to continue and then press SPACE to fire the laser.")
    message.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    drawCanon()
    drawTarget()
    win.flip()
    event.waitKeys(keyList = "space")
    drawTarget()
    laserVert.draw()
    drawCanon()
    win.flip()
    core.wait(1)

    ## How to get more points. ##
    event.clearEvents()
    message.text = ("Good job! Every time you hit a target, you will receive some points.\n\n" +
                      "You can see your score balance in the top left corner of the screen.\n\n" +
                      "Press ENTER to continue.")

    timer.reset(t = 3)
    while timer.getTime() > 0:
        if int(timer.getTime()*10)%10 < 5:
            scoreText.draw()
        message.draw()
        win.flip()
    event.waitKeys(keyList = "return")

    message.text = ("If you hit a target, you will receive a certain amount of points.\n\n" +
                      "In this trial, you will get 75 points for hitting the target. " +
                      "During the trial, notice that you can also see a cue reminding you of the reward for hitting the target.\n\n" +
                      "Press ENTER to continue and then press SPACE to fire the laser.")
    scoreText.draw()
    message.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    instr.text = "\nHit:\n\n"
    values.text = "\n75\n\n"
    instr.draw()
    values.draw()
    scoreText.draw()
    drawCanon()
    drawTarget()
    win.flip()
    event.waitKeys(keyList = "space")

    instr.draw()
    values.draw()
    score += 75
    scoreText.color = "green"
    scoreText.text = "SCORE: " + str(score)
    scoreText.draw()
    drawTarget()
    laserVert.draw()
    drawCanon()
    win.flip()
    core.wait(1)

    feedback.text = "You HIT the target and receive 75 points.\n\nPress ENTER to continue."
    feedback.draw()
    scoreText.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    ## How to lose points. ##
    event.clearEvents()
    message.text = ("Sometimes, the target will appear misaligned with your shot. " +
                     "Firing the laser when the target is misaligned will result in a miss.\n\n" +
                     "In this trial, if you miss the target, you will lose 25 points. " +
                     "You will also see a cue showing how many points you would get if you hit the target, but that is not possible in this trial.\n\n" +
                     "Press ENTER to continue and then try firing the laser by pressing SPACE.")
    scoreText.color = "white"
    scoreText.draw()
    message.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    thisPos = posList[1]
    targetOuter.pos = thisPos
    targetMiddle.pos = thisPos
    targetInner.pos = thisPos
    
    instr.text = "\nHit:\nMiss:\n"
    values.text = "\n50\n-25\n"
    instr.draw()
    values.draw()
    scoreText.draw()
    drawCanon()
    drawTarget()
    win.flip()
    event.waitKeys(keyList = "space")

    instr.draw()
    values.draw()
    score -= 25
    scoreText.color = "red"
    scoreText.text = "SCORE: " + str(score)
    scoreText.draw()
    drawTarget()
    laserVert.draw()
    drawCanon()
    win.flip()
    core.wait(1)

    feedback.text = "You MISSED the target and lose 25 points.\n\nPress ENTER to continue."
    feedback.draw()
    scoreText.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    ## How prism works. ##
    event.clearEvents()
    message.text = ("Luckily for you, sometimes, there might be an invisible prism in front of your canon that would split the beam, so that you can hit the target even when it is misaligned. " +
                    "However, the prism will be hidden throughout the trial and you will not see it until you fire.\n\n" +
                    "In this trial, the target is misaligned but the prism will appear as soon as you fire the laser. You will get 150 points for hitting the target.\n\n" +
                    "Press ENTER to continue and then fire the laser by pressing SPACE.")
    scoreText.color = "white"
    scoreText.draw()
    message.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    thisPos = posList[1]
    targetOuter.pos = thisPos
    targetMiddle.pos = thisPos
    targetInner.pos = thisPos
    
    instr.text = "Prism %:\nHit:\nMiss:\n"
    values.text = "HIGH\n150\n-40\n"
    instr.draw()
    values.draw()
    scoreText.draw()
    drawCanon()
    drawTarget()
    win.flip()
    event.waitKeys(keyList = "space")

    instr.draw()
    values.draw()
    score += 150
    scoreText.color = "green"
    scoreText.text = "SCORE: " + str(score)
    scoreText.draw()
    drawTarget()
    laserVert.draw()
    laserHoriz.draw()
    drawPrism()
    drawCanon()
    win.flip()
    core.wait(1)

    feedback.text = "You HIT the target and receive 150 points.\n\nPress ENTER to continue."
    feedback.draw()
    scoreText.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    ## How prism probability works - high probability. ##
    event.clearEvents()
    message.text = ("The prism will NOT appear after every shot.\n\n" +
                    "Nevertheless, in each trial, you will see a cue telling you whether the probability of the prism's presence is HIGH or LOW.\n\n" +
                    "In this trial, the probability of the prism appearing is HIGH and you can get 21 points for hitting the target.\n\n" +
                    "Press ENTER to continue and then try firing the laser by pressing SPACE.")
    scoreText.color = "white"
    scoreText.draw()
    message.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    thisPos = posList[1]
    targetOuter.pos = thisPos
    targetMiddle.pos = thisPos
    targetInner.pos = thisPos
    
    instr.text = "Prism %:\nHit:\nMiss:\n"
    values.text = "HIGH\n21\n-38\n"
    instr.draw()
    values.draw()
    scoreText.draw()
    drawCanon()
    drawTarget()
    win.flip()
    event.waitKeys(keyList = "space")

    instr.draw()
    values.draw()
    score += 21
    scoreText.color = "green"
    scoreText.text = "SCORE: " + str(score)
    scoreText.draw()
    drawTarget()
    laserVert.draw()
    laserHoriz.draw()
    drawPrism()
    drawCanon()
    win.flip()
    core.wait(1)

    feedback.text = "You HIT the target and receive 21 points.\n\nPress ENTER to continue."
    feedback.draw()
    scoreText.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    ## How prism probability works - low probability. ##
    event.clearEvents()
    message.text = ("In some trial, the probability of the prism might also be LOW.\n\n" +
                    "Press ENTER to continue and then try firing the laser by pressing SPACE.")
    scoreText.color = "white"
    scoreText.draw()
    message.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    thisPos = posList[1]
    targetOuter.pos = thisPos
    targetMiddle.pos = thisPos
    targetInner.pos = thisPos
    
    instr.text = "Prism %:\nHit:\nMiss:\n"
    values.text = "LOW\n61\n-21\n"
    instr.draw()
    values.draw()
    scoreText.draw()
    drawCanon()
    drawTarget()
    win.flip()
    event.waitKeys(keyList = "space")

    instr.draw()
    values.draw()
    score -= 21
    scoreText.color = "red"
    scoreText.text = "SCORE: " + str(score)
    scoreText.draw()
    drawTarget()
    laserVert.draw()
    drawCanon()
    win.flip()
    core.wait(1)

    feedback.text = "You MISSED the target and lose 21 points.\n\nPress ENTER to continue."
    feedback.draw()
    scoreText.draw()
    win.flip()
    event.waitKeys(keyList = "return")
    
    ## How waiting works. ##
    event.clearEvents()
    message.text = ("Keep in mind that HIGH probability does not guarantee a HIT and LOW probability does not guarantee a MISS.\n\n" +
                      "Also, remember that if the target is aligned with the canon, you will ALWAYS hit it, regardless of whether the prism appears or not.\n\n" +
                      "Press ENTER to continue.")
    message.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    event.clearEvents()
    message.text = ("If you decide that you do not want to fire the laser, you can skip a trial by waiting until the trial ends. " +
                     "In every trial from now on, you will see a red line on the bottom of the screen that will shrink over time. " +
                     "If it shrinks so much that it disappears, the trial ends without firing the laser.\n\n" +
                     "In this trial, try waiting until the end of the trial.\n\n" +
                     "Press ENTER to continue and then wait for the trial to end.")
    scoreText.color = "white"
    scoreText.draw()
    message.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    thisPos = posList[1]
    targetOuter.pos = thisPos
    targetMiddle.pos = thisPos
    targetInner.pos = thisPos
    
    instr.text = "Prism %:\nHit:\nMiss:"
    values.text = "LOW\n10\n-48"
    trialDone = False
    timer.reset(t = trialLimit)
    while not trialDone:
        progressBarWidth = (timer.getTime()/trialLimit)*winWidth*2
        progressBar.size = [progressBarWidth,20]
        progressBar.draw()
        scoreText.draw()
        instr.draw()
        values.draw()
        drawTarget()
        drawCanon()
        win.flip()

        if timer.getTime() < 0:
            event.clearEvents()
            feedback.text = "You did not fire the laser.\n\nYou did not lose any points.\n\nPress ENTER to continue."
            scoreText.text = "SCORE: " + str(score)
            scoreText.draw()
            feedback.draw()
            win.flip()
            event.waitKeys(keyList = "return")
            trialDone = True

    ## Why waiting can be dangerous. ##
    event.clearEvents()
    message.text = ("Very good.\n\n" +
                    "Skipping a trial without firing the laser will usually cost you no points. However, every time you skip a trial, there is a small probability that you will lose " + str(abs(skipPenalty)) + " points!\n\n" +
                    "Try waiting until the end of the trial again.\n\n" +
                    "Press ENTER to continue and then wait for the trial to end.")
    scoreText.color = "white"
    scoreText.draw()
    message.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    thisPos = posList[1]
    targetOuter.pos = thisPos
    targetMiddle.pos = thisPos
    targetInner.pos = thisPos
    
    instr.text = "Prism %:\nHit:\nMiss:"
    values.text = "LOW\n6\n-68"
    trialDone = False
    timer.reset(t = trialLimit)
    while not trialDone:
        progressBarWidth = (timer.getTime()/trialLimit)*winWidth*2
        progressBar.size = [progressBarWidth,20]
        progressBar.draw()
        scoreText.draw()
        instr.draw()
        values.draw()
        drawTarget()
        drawCanon()
        win.flip()

        if timer.getTime() < 0:
            event.clearEvents()
            feedback.text = "You did not fire the laser.\n\nUnfortunately, you lost " + str(abs(skipPenalty)) + " points.\n\nPress ENTER to continue."
            score += skipPenalty
            scoreText.color = "red"
            scoreText.text = "SCORE: " + str(score)
            scoreText.draw()
            feedback.draw()
            win.flip()
            event.waitKeys(keyList = "return")
            trialDone = True

    ## Explaining the scale. ##
    event.clearEvents()
    message.text = ("After firing the laser, you will see two questions with a scale 1-7. " +
                    "The program will ask you (1) whether you think that your decision was GOOD or BAD and (2) whether you felt SURPRISED by what you saw.\n\n" +
                    "You can answer the questions by pressing a corresponding NUMBER key and confirm your choice by pressing ENTER.\n\n" +
                    "In the next trial, fire the laser. After that, you will see the two scales. Answer them according to your experience.\n\n" +
                    "Press ENTER to continue, then fire the laser and reply to the questions.")
    scoreText.color = "white"
    scoreText.draw()
    message.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    thisPos = posList[0]
    targetOuter.pos = thisPos
    targetMiddle.pos = thisPos
    targetInner.pos = thisPos
    
    instr.text = "Prism %:\nHit:\nMiss:"
    values.text = "LOW\n52\n-14"
    trialDone = False
    timer.reset(t = trialLimit)
    while not trialDone:
        progressBarWidth = (timer.getTime()/trialLimit)*winWidth*2
        progressBar.size = [progressBarWidth,20]
        progressBar.draw()
        scoreText.draw()
        instr.draw()
        values.draw()
        drawTarget()
        drawCanon()
        win.flip()

        if event.getKeys(keyList = "space"):    
            drawTarget()
            laserVert.draw()
            drawCanon()
            laserHoriz.draw()
            drawPrism()
            feedback.text = "You HIT the target and receive 52 points."
            score += 52
            scoreText.color = "green"
            scoreText.text = "SCORE: " + str(score)
            scoreText.draw()
            instr.draw()
            values.draw()
            win.flip()

            core.wait(0.5)

            feedback.draw()
            scoreText.draw()
            win.flip()

            core.wait(2)
            trialDone = True

            questionList = ["error", "surprise"]
            for thisQuestion in questionList:
                if thisQuestion == "error":
                    questionMsg = visual.TextStim(win, text = "How GOOD or BAD do you think your decision was?")
                    scale = visual.RatingScale(win, choices = [1,2,3,4,5,6,7], respKeys = ["1","2","3","4","5","6","7"],
                                               scale = "1 = very bad . . . . . . . . . . . 7 = very good", markerStart = None,
                                               showAccept = True, showValue = False, acceptPreText = "Select with NUMBERS", low = 1, high = 7,
                                               acceptText = "Confirm with ENTER", acceptSize = 2.5, minTime=0, leftKeys = None, rightKeys = None)
                if thisQuestion == "surprise":
                    questionMsg = visual.TextStim(win, text = "How much SURPRISED were you by what you saw?")
                    scale = visual.RatingScale(win, choices = [1,2,3,4,5,6,7], respKeys = ["1","2","3","4","5","6","7"],
                                               scale = "1 = not surprised . . . . . . . . . . . 7 = very surprised", markerStart = None,
                                               showAccept = True, showValue = False, acceptPreText = "Select with NUMBERS", low = 1, high = 7,
                                               acceptText = "Confirm with ENTER", acceptSize = 2.5, minTime=0, leftKeys = None, rightKeys = None)
                event.clearEvents()
                while scale.noResponse:
                    questionMsg.draw()
                    scale.draw()
                    win.flip()
                    if event.getKeys(keyList = "escape"):
                        end()
        
        if timer.getTime() < 0 and not trialDone == True:
            event.clearEvents()
            feedback.text = ("You did not fire the laser.\n\n" +
                             "In this trial, you have to fire the laser.\n\n" +
                             "Press ENTER to try again.")
            scoreText.text = "SCORE: " + str(score)
            scoreText.draw()
            feedback.draw()
            win.flip()
            event.waitKeys(keyList = "return")
            timer.reset(t = trialLimit)
            
    ## Summary. ##
    event.clearEvents()
    message.text = ("This is the end of the training. To summarize:\n" +
                      "- In every trial, you have to decide whether to fire the laser by pressing SPACE or wait until the end of the trial.\n" +
                      "- Before and during each trial, you will see (1) the probability of the prism, (2) reward for hitting the target, (3) penalty for missing.\n" +
                      "- In each trial, your task is to evaluate the potential rewards and decide whether it is better to fire the laser or not.\n" +
                      "- If you fire the laser, you will always answer the question about how good your decision was and whether you were surprised by what you saw.\n\n" +
                      "Press ENTER to continue.")
    message.draw()
    win.flip()
    event.waitKeys(keyList = "return")


###########################
## Block and trial setup ##
###########################

for thisBlock in blockList:
    if thisBlock == 0:
        score = startingScore
        trials = range(0,10)
        message.text = ("In the following block of trials, you can practice what you learned during the tutorial.\n\n" +
                          "Your score will be nullified at the end of this block. Feel free to experiment!\n\n" +
                          "Press ENTER to start.")
        
    else:
        trials = range(0,nTrials)
        if thisBlock == 1:
            score = startingScore
            message.text = ("Your score is now " + str(startingScore) + " points.\n\n" +
                              "Let's start the experiment now.\n\n" +
                              "Press ENTER to start.")
        else:
            message.text = ("You can take a break now.\n\n" +
                              "Press ENTER to continue.")
    message.draw()
    scoreText.text = "SCORE: " + str(score)
    scoreText.draw()
    win.flip()
    event.waitKeys(keyList = "return")

    for thisTrial in trials:
        event.clearEvents()
        progressBarWidth = winWidth*2
        progressBar.size = [progressBarWidth,20]
        
        ## Target position setup ##
        thisPos = random.choice(posList)
        if thisPos == posList[0]:
            position = "aligned"
        else:
            position = "misaligned"
        targetOuter.pos = thisPos
        targetMiddle.pos = thisPos
        targetInner.pos = thisPos

        ## Prism probability setup ##
        thisProb = random.choice(probList)
        roll = random.randrange(0,100)
        if roll <= thisProb:
            prismOccurs = True
        else:
            prismOccurs = False

        ## Reward/penalty setup ##
        reward = 0
        penalty = 0
        if thisProb == lowProb:
            rewardMu = 40
            penaltyMu = -10
        elif thisProb == highProb:
            rewardMu = 10
            penaltyMu = -40
        if score < 0:
            rewardMu = 50 # This ensures that the subjects gets out of the negative score quickly.
        rewardSigma = abs(rewardMu)/2
        penaltySigma = abs(penaltyMu)/2
        while reward <= 0 or reward >= 100 or penalty >= 0 or penalty <= -100: # This ensures that reward is always positive and penalty always negative and that none of those has three digits.
            reward = int(np.random.normal(rewardMu, rewardSigma, 1)[0])
            penalty = int(np.random.normal(penaltyMu, penaltySigma, 1)[0])

        ## Instruction setup ##
        if thisProb <= 50:
            probText = "LOW"
        else:
            probText = "HIGH"
        s = "\n"
        values.text = s.join([str(probText), str(reward), str(penalty)])

#######################
## Trial progression ##
#######################

        timer.reset(t = instrLimit + trialLimit)
        reaction = None
        RT = None
        trialDone = False
        scoreText.color = "white"
        
        while not trialDone:        
            while timer.getTime() > trialLimit:
                if event.getKeys(keyList = "escape"):
                    end()

                scoreText.draw()
                instr.draw()
                values.draw()
                win.flip()
            
            event.clearEvents()
            progressBarWidth = (timer.getTime()/trialLimit)*winWidth*2
            progressBar.size = [progressBarWidth,20]
            progressBar.draw()
            scoreText.draw()
            instr.draw()
            values.draw()
            drawTarget()
            drawCanon()
            win.flip()

            
            if event.getKeys(keyList = "escape"):
                end()
            
            if event.getKeys(keyList = "space"):    
                reaction = "press"
                RT = 10 - timer.getTime()
                
                
                drawTarget()
                laserVert.draw()
                drawCanon()
                
                if prismOccurs == True: # Automatically means a HIT.
                    laserHoriz.draw()
                    drawPrism()
                    feedback.text = "You HIT the target and receive " + str(reward) + " points."
                    score += reward
                    scoreText.color = "green"
                    outcome = "hit"
                elif thisPos == posList[0]: # I.e. if the target is alligned. Automatically means a HIT.
                    feedback.text = "You HIT the target and receive " + str(reward) + " points."
                    score += reward
                    scoreText.color = "green"
                    outcome = "hit"
                else: # The remaining situation (prismOccurs == False and thisPos != posList[0]) means a MISS.
                    feedback.text = "You MISSED the target and lose " + str(abs(penalty)) + " points."
                    score += penalty
                    scoreText.color = "red"
                    outcome = "miss"
                
                scoreText.text = "SCORE: " + str(score)
                scoreText.draw()
                instr.draw()
                values.draw()
                win.flip()

                core.wait(0.5)

                feedback.draw()
                scoreText.draw()
                win.flip()

                core.wait(2)
                trialDone = True

                questionList = ["error", "surprise"]
                for thisQuestion in questionList:
                    if thisQuestion == "error":
                        questionMsg = visual.TextStim(win, text = "How GOOD or BAD do you think your decision was?")
                        scale = visual.RatingScale(win, choices = [1,2,3,4,5,6,7], respKeys = ["1","2","3","4","5","6","7"],
                                                   scale = "1 = very bad . . . . . . . . . . . 7 = very good", markerStart = None,
                                                   showAccept = True, showValue = False, acceptPreText = "Select with NUMBERS", low = 1, high = 7,
                                                   acceptText = "Confirm with ENTER", acceptSize = 2.5, minTime=0, leftKeys = None, rightKeys = None)
                    if thisQuestion == "surprise":
                        questionMsg = visual.TextStim(win, text = "How much SURPRISED were you by what you saw?")
                        scale = visual.RatingScale(win, choices = [1,2,3,4,5,6,7], respKeys = ["1","2","3","4","5","6","7"],
                                                   scale = "1 = not surprised . . . . . . . . . . . 7 = very surprised", markerStart = None,
                                                   showAccept = True, showValue = False, acceptPreText = "Select with NUMBERS", low = 1, high = 7,
                                                   acceptText = "Confirm with ENTER", acceptSize = 2.5, minTime=0, leftKeys = None, rightKeys = None)
                    event.clearEvents()
                    while scale.noResponse:
                        questionMsg.draw()
                        scale.draw()
                        scoreText.draw()
                        win.flip()
                        if event.getKeys(keyList = "escape"):
                            end()
                    if thisQuestion == "error":
                        errorScResp = scale.getRating()
                        errorScRT = scale.getRT()
                    if thisQuestion == "surprise":
                        surpriseScResp = scale.getRating()
                        surpriseScRT = scale.getRT()
                
            elif timer.getTime() < 0 and not trialDone == True:
                reaction = "wait"
                RT = "N/A"
                errorScResp = "N/A"
                errorScRT = "N/A"
                surpriseScResp = "N/A"
                surpriseScRT = "N/A"
                questionList = ["N/A","N/A"] ## This is a list, because the log looks separately at the first and the second element.
                            
                roll = random.randrange(0,100)
                if roll < 10:
                    feedback.text = "You did not fire the laser.\n\nUnfortunately, you lost " + str(abs(skipPenalty)) + " points."
                    score += skipPenalty
                    scoreText.color = "red"
                    outcome = "skip_penalty"
                else:
                    feedback.text = "You did not fire the laser.\n\nFortunately, you did not lose any points."
                    outcome = "skip_free"
                scoreText.text = "SCORE: " + str(score)
                scoreText.draw()
                feedback.draw()
                win.flip()
                core.wait(2)
                trialDone = True
        log.write(",".join([str(thisBlock),str(thisTrial + 1),str(reward),str(penalty),str(position),str(thisProb),
                            str(prismOccurs),str(reaction),str(RT),str(outcome),str(score),str(errorScResp),str(errorScRT),
                            str(surpriseScResp),str(surpriseScRT),"\n"]))

log.close()

if score > 0:
    message.text = "This is the end of the experiment.\n\nYour final score is " + str(score) + ". That is not bad at all!\n\nThank you for your time!\n\nFinish the experiment by pressing ESCAPE."
else:
    message.text = "This is the end of the experiment.\n\nYour final score is " + str(score) + ". Don't feel bad about it, this task was not easy.\n\nThank you for your time!\n\nFinish the experiment by pressing ESCAPE."
message.draw()
win.flip()
event.waitKeys(keyList = "escape")

win.close()
core.quit()
