import pygame, sys, random;
from pygame.locals import *;

WINDOWWIDTH=640;
WINDOWHEIGHT=480;

CARDHEIGHT=120;
CARDWIDTH=90;
BOARDSIZEWIDTH=4;
BOARDSIZEHEIGHT=3;

WHOTCARDNUM=5;
CARDSHAPES=[ 'square', 'circle', 'diamond', 'lines'];
SHAPECARDSNUM=12
SHAPESNUM=4;

GAP=30;

BASICFONTSIZE=30;
MEGAFONTSIZE=100;

SHAPESIZE=30;
#R G B
BLACK=(0, 0, 0);
WHITE=(255, 255, 255);
RED=(255, 0, 0);
GREEN=(0, 128, 0);
BLUE=(0, 0, 255);
BROWN=(165,42,42);

SQUARE='square';
CIRCLE='circle';
LINES='lines';
DIAMOND='diamond'

BGCOLOR=GREEN;

RIGHT='right';
LEFT='left'
UP='up'
DOWN='down'

CARDMAX=4;



FPS=30;

XMARGIN=int((WINDOWWIDTH - (BOARDSIZEWIDTH * ((CARDWIDTH + GAP))))/2)
YMARGIN=int((WINDOWHEIGHT - (BOARDSIZEHEIGHT * ((CARDHEIGHT + GAP))))/2);
PLAYERPOSY=int(( (CARDHEIGHT + GAP))) + YMARGIN;
COMPUTERPOSY=int(( (CARDHEIGHT + GAP))) + YMARGIN

MARKETCARDY=YMARGIN + CARDHEIGHT + GAP
STARTCARDX=int((BOARDSIZEWIDTH * (CARDWIDTH + GAP))) + XMARGIN - CARDWIDTH;

def main():
    global BASICFONT, DISPLAYSURF, FPSCLOCK, animSpeed;
    pygame.init()
    FPSCLOCK=pygame.time.Clock();
    DISPLAYSURF=pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT));
    BASICFONT=pygame.font.Font('freesansbold.ttf', BASICFONTSIZE );
    animSpeed=10;
    DISPLAYSURF.fill(BGCOLOR);
    cards=generateCards();
    playerCards=getFourCards(cards);
    computerCards=getFourCards(cards);
    startingCard=cards[random.randint(0, len(cards) - 1)];
    #startingCard={'shape':'square', 'number':'2'}
    playedCards=[];
    mouseClicked=False;
    mousex=0
    mousey=0
    x=0;
    b=4;
    marketRect=pygame.Rect(XMARGIN, MARKETCARDY, CARDWIDTH, CARDHEIGHT);
    defaultCard={'shape':'square', 'number':'4'}
    startingCardIsSpecial=isSpecialCard(startingCard);
    turn='player'
    startGameAnimation();
    sharingCardsAnimation(cards,playerCards, computerCards);
    
    while True:
        DISPLAYSURF.fill(BGCOLOR);
        if len(playerCards) < 4:
            x=0;
        if len(playerCards) > 4:
            next=drawNext();
            if next.collidepoint(mousex, mousey) and mouseClicked:
                if x + CARDMAX <= 0:
                    x += CARDMAX;
                x -= 1;
                mouseClicked=False;
        drawTextForBoard(startingCard['shape'], 280, 180)
        drawSeperateCards(playerCards, False, PLAYERPOSY + CARDHEIGHT + GAP, x)
        drawText(len(playerCards), XMARGIN - 60, PLAYERPOSY + CARDHEIGHT + GAP);
        drawMarket(cards);
        drawText(len(cards), XMARGIN - 60, MARKETCARDY)
        drawSeperateCardsCom(computerCards, True, YMARGIN)
        drawText(len(computerCards), XMARGIN - 60, YMARGIN)
        
        drawCard(startingCard, STARTCARDX, MARKETCARDY, BROWN, False, 0, 0)
        drawText(len(playedCards), STARTCARDX+120, MARKETCARDY);
        
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate();
            if event.type==MOUSEBUTTONUP:
                mouseClicked=True;
                mousex, mousey=event.pos;
        box=boardCoords(playerCards,PLAYERPOSY + CARDHEIGHT + GAP, mousex, mousey );
        
        if turn=='player':
            #textt=BASICFONT.render('Player', True, WHITE);
            #texttRect=textt.get_rect();
            #texttRect.center=(200, 300);
            #DISPLAYSURF.blit(textt, texttRect)
            if mouseClicked:
                if box!= None:
                    if isValidMove(playerCards[box + x], startingCard):
                        makeMove(playerCards, playedCards, mousex, mousey, PLAYERPOSY + CARDHEIGHT + GAP, x )
                        startingCard=playerCards[box + x];
                        del playerCards[box + x];
                        if len(playerCards)==0:
                            gameStateAnimation('You Won');
                            cards=generateCards()
                            playerCards=getFourCards(cards)
                            computerCards=getFourCards(cards)
                            startingCard=cards[random.randint(0, len(cards) - 1)];
                            playedCards=[];
                        if isSpecialCard(startingCard):
                            runSpecialCard(startingCard, computerCards, cards, turn);
                            #turn='computer';
                        elif startingCard['number']=='20':
                            startingCard=random.choice(playerCards);
                            turn='computer';
                        else:
                            turn='computer';
                        mouseClicked=False;
                    else:
                        correctCardText=BASICFONT.render('Select the appropriate card', True, WHITE);
                        correctCardTextRect=correctCardText.get_rect();
                        correctCardTextRect.center=(WINDOWWIDTH/2, WINDOWHEIGHT);
                        DISPLAYSURF.blit(correctCardText, correctCardTextRect);
                elif marketRect.collidepoint(mousex, mousey):
                    if len(cards) > 1:
                        slideAnimation(cards[0],XMARGIN, MARKETCARDY, XMARGIN + CARDWIDTH, PLAYERPOSY, DOWN, False)
                        playerCards.append(cards[0]);
                        del cards[0];
                        mousex=0;
                        mousey=0;
                        turn='computer';
                    else:
                        for i in playedCards:
                            cards.append(i);
                        random.shuffle(cards);
                        playedCards=[startingCard];
        elif turn=='computer':
            box=compMove(computerCards, playerCards, startingCard);
            if box != None:
                slideAnimation(computerCards[box], XMARGIN + (box * (CARDWIDTH + GAP)) , COMPUTERPOSY, STARTCARDX, MARKETCARDY, DOWN, False)
                startingCard=computerCards[box];
                playedCards.append(computerCards[box]);
                del computerCards[box];
                if len(computerCards)==0:
                            gameStateAnimation('You Lost');
                            cards=generateCards()
                            playerCards=getFourCards(cards)
                            computerCards=getFourCards(cards)
                            startingCard=cards[random.randint(0, len(cards) - 1)];
                            playedCards=[];
                if isSpecialCard(startingCard):
                    runSpecialCard(startingCard, playerCards, cards,  turn);
                elif startingCard['number']=='20':
                    startingCard=random.choice(computerCards);
                    turn='player';
                else:
                    turn='player';
            else:
                if len(cards) > 1:
                    slideAnimation(cards[0], XMARGIN, MARKETCARDY,  XMARGIN + CARDWIDTH, COMPUTERPOSY, UP, False)
                    computerCards.append(cards[0]);
                    del cards[0];
                    turn='player';
                else:
                    for i in playedCards:
                        cards.append(i);
                    random.shuffle(cards);
                    playedCards=[startingCard];
        pygame.display.update();
        FPSCLOCK.tick();
        
        
def generateCards():
    cardDeck=[];
    for i in range(WHOTCARDNUM):
        cardDeck.append({'shape':'whot', 'number':'20'});
    for i in range(SHAPECARDSNUM):
        for i in range(SHAPESNUM):
            number=str(random.randint(1, 14));
            shape=CARDSHAPES[i];
            cardDeck.append({'shape':shape, 'number':number});
    cardDeck.append({'shape':'square', 'number':'14'});
    random.shuffle(cardDeck);
    assert len(cardDeck) == 54 ;
    return cardDeck;
    
def startGameAnimation():
    Font=pygame.font.Font('freesansbold.ttf', MEGAFONTSIZE);
    Font1Text=Font.render('Whot', True, WHITE);
    Font1Rect=Font1Text.get_rect();
    Font1Rect.center=(WINDOWWIDTH/2, WINDOWHEIGHT/2)
    DISPLAYSURF.blit(Font1Text, Font1Rect);
    
    Font2Text=Font.render('Whot', True, WHITE);
    Font2Rect=Font2Text.get_rect();
    Font2Rect.center=(WINDOWWIDTH/2, WINDOWHEIGHT/2 + 100);
    DISPLAYSURF.blit(Font2Text, Font2Rect);
    
    Font3Text=BASICFONT.render('Tap the screen to start', True, WHITE);
    Font3Rect=Font3Text.get_rect();
    Font3Rect.center=(WINDOWWIDTH/2, WINDOWHEIGHT/2 + 200);    
    DISPLAYSURF.blit(Font3Text, Font3Rect)
    
    while checkForKeyPress()==None:
        pygame.display.update();
        FPSCLOCK.tick(FPS);
    
def checkForKeyPress():
    for event in pygame.event.get():
        if event.type==QUIT:
            terminate();
        if event.type==MOUSEBUTTONUP:
            return event.type
        else:
            return None

def terminate():
    pygame.quit();
    sys.exit();
    
def drawCard(cardObj, left, top, color, covered, adjx, adjy):
    if not covered:
        pygame.draw.rect(DISPLAYSURF, BROWN, (left + adjx, top + adjy, CARDWIDTH, CARDHEIGHT), 5 );
        pygame.draw.rect(DISPLAYSURF, WHITE, (left + adjx , top + adjy, CARDWIDTH, CARDHEIGHT) );
        text=BASICFONT.render(cardObj['number'], True, BROWN);
        textRect=text.get_rect()
        textRect.center=(left + adjx + CARDWIDTH/2, top + adjy + CARDHEIGHT/2);
        DISPLAYSURF.blit(text, textRect);
    
        quarter = SHAPESIZE * 0.25# syntactic sugar

        half = SHAPESIZE * 0.5# syntactic sugar
        SHAPEPOSX=5;
        SHAPEPOSY=5;
    # Draw the shapes
        if cardObj['shape']== SQUARE:
            pygame.draw.rect(DISPLAYSURF, color, (left + adjx + quarter, top + adjy + quarter, SHAPESIZE, SHAPESIZE))

        elif cardObj['shape']== DIAMOND:

            pygame.draw.polygon(DISPLAYSURF, color, ((left +adjx+ half, top+adjy), (left +adjx+ SHAPESIZE - 1, top +adjy+ half), (left +adjx+ half, top +adjy+ SHAPESIZE - 1), (left + adjx, top +adjy + 
half)))

        elif cardObj['shape'] == LINES:

            for i in range(0, SHAPESIZE, 4):

                pygame.draw.line(DISPLAYSURF, color, (left + adjx , top +adjy+ i), (left +adjx + 
i, top + adjy))
                pygame.draw.line(DISPLAYSURF, color, (left + adjx + i, top + adjy), (left + adjx, top + adjy + i))
        elif cardObj['shape'] == CIRCLE:
            pygame.draw.circle(DISPLAYSURF, color, (left +adjx  + half, top + adjy + half), half - 5)

            pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + adjx + half, top + adjy + half), quarter - 5)
        elif cardObj['shape']=='whot':
            Font2=pygame.font.Font('freesansbold.ttf', 18);
            text=Font2.render('Whot', True, BROWN);
            textRect=text.get_rect()
            textRect.center=(left + adjx + half + quarter, top+ adjy + half);
            DISPLAYSURF.blit(text, textRect);
    else:
        pygame.draw.rect(DISPLAYSURF, BROWN, (left + adjx , top + adjy , CARDWIDTH, CARDHEIGHT) );
        text=BASICFONT.render('Whot', True, WHITE);
        textRect=text.get_rect()
        textRect.center=(left + adjx + CARDWIDTH/2, top+ adjy + CARDHEIGHT/2);
        DISPLAYSURF.blit(text, textRect);
def slideAnimation(cardObj, left, top, toX, toY, dir, covered):
    
    baseSurf=DISPLAYSURF.copy();
    if dir==RIGHT:
        for i in range(0, toX, animSpeed):
            #checkForQuit();
            DISPLAYSURF.blit(baseSurf, (0,0));
            drawCard(cardObj, left, top, BROWN, covered,  i, 0);
            pygame.display.update();
            FPSCLOCK.tick(FPS);
    if dir==DOWN:
        for i in range(0, toY, animSpeed):
            #checkForQuit();
            DISPLAYSURF.blit(baseSurf, (0,0));
            drawCard(cardObj, left, top, BROWN, covered,  0, i);
            pygame.display.update();
            FPSCLOCK.tick(FPS);
    if dir==UP:
        for i in range(0, toY, animSpeed):
            #checkForQuit();
            DISPLAYSURF.blit(baseSurf, (0,0));
            drawCard(cardObj, left, top, BROWN, covered,  0, -i);
            pygame.display.update();
            FPSCLOCK.tick(FPS);
    if dir==LEFT:
        for i in range(0, toY, animSpeed):
            #checkForQuit();
            DISPLAYSURF.blit(baseSurf, (0,0));
            drawCard(cardObj, left, top, BROWN, covered,  -i, 0);
            pygame.display.update();
            FPSCLOCK.tick(FPS);
def sharingCardsAnimation(cards,playerCards, computerCards):
    DISPLAYSURF.fill(BGCOLOR)
    drawMarket(cards)
    for i in range(len(playerCards)):
        slideAnimation(playerCards[i], XMARGIN, MARKETCARDY, 0, PLAYERPOSY, DOWN, False);
        pygame.time.wait(200)
    for i in range(len(computerCards)):
        slideAnimation(playerCards[i], XMARGIN, MARKETCARDY, 0, COMPUTERPOSY, UP, True);
        pygame.time.wait(200)
def getFourCards(cards):
    Cards=[];
    for i in range(CARDMAX):
        card=cards[i];
        Cards.append(card);
        del cards[i];
    return Cards;
def drawMarket(cards):
    for i in range(len(cards)):
            drawCard(cards[i], XMARGIN, MARKETCARDY, BROWN, True, 0, 0);
            
def drawSeperateCards(cards, covered,top, x):
    loopter=4;
    if len(cards)<4:
        loopter=len(cards);
    for i in range(0, loopter):
        drawCard(cards[i + x], XMARGIN + (i * (CARDWIDTH + GAP)) , top, BROWN, covered, 0,0);

def drawSeperateCardsCom(cards, covered,top):
    loopter=4;
    if len(cards)<4:
        loopter=len(cards);
    for i in range(0, loopter):
        drawCard(cards[i], XMARGIN + (i * (CARDWIDTH + GAP)) , top, BROWN, covered, 0,0); 

def isSpecialCard(cardObj):
    if cardObj['number']=='1':
        return 'hold on';
    elif cardObj['number']=='8':
        return 'suspension';
    elif cardObj['number']=='14':
        return 'general market';
    elif cardObj['number']=='5':
        return 'pick three';
    elif cardObj['number']=='2':
        return 'pick two';
    else:
        return False;
        
def isLastCard(cards):
    if len(card) + 1==1:
        return True;
    return False;
    
def whoGoesFirst():
    if random.randint(0, 1)==0:
        return 'player';
    else:
        return 'computer';
        
def runSpecialCard(cardObj, pCards, cards, player):
    if player=='player':
        Xplayer='computer';
    elif player=='computer':
        Xplayer='player'
    if cardObj['number']=='1':
        turn=player;
    elif cardObj['number']=='8':
        turn=player;
    elif cardObj['number']=='14':
        if len(cards) > 1:
            pCards.append(cards[0]);
            del cards[0];
        turn=player;
    elif cardObj['number']=='5':
        for i in range(3):
            if len(cards) > 1:
                pCards.append(cards[0]);
                del cards[0];
        turn=player;
    elif cardObj['number']=='2':
        for i in range(2):
            if len(cards) > 1:
                pCards.append(cards[0]);
                del cards[0];
        turn=player;
        
def checkForKeyPress():
    for event in pygame.event.get():
        if event.type==QUIT:
            terminate()
        if event.type==MOUSEBUTTONUP:
            return event.pos;
    return None;
        
def demandedShape(x, y):
    drawShapesButton()
    cards=shapeButton()
    for i in range(len(cards)):
        boxRect=cards[i];
        if boxRect.collidepoint(x, y):
            return CARDSHAPES[i];
    return None;
def shapeButton():
    btnSize=50;
    shpSize=20;
    top=500;
    squareRect=pygame.Rect( XMARGIN, top, btnSize, btnSize);
    
    diamondRect=pygame.Rect( XMARGIN + GAP + btnSize, top, btnSize, btnSize);
    
    circleRect=pygame.Rect( XMARGIN + ((GAP + btnSize) * 2), top, btnSize, btnSize);
    
    lineRect=pygame.Rect( XMARGIN + ((GAP + btnSize) * 3), top, btnSize, btnSize);
    return [squareRect, circleRect, diamondRect, lineRect];
def drawShapesButton():
    btnSize=50;
    shpSize=20;
    top=500;
    squareRect=pygame.Rect( XMARGIN, top, btnSize, btnSize);
    pygame.draw.rect(DISPLAYSURF, WHITE, squareRect);
    pygame.draw.rect(DISPLAYSURF, BROWN, (XMARGIN + btnSize/4, top + btnSize/4, shpSize, shpSize));
    
    diamondRect=pygame.Rect( XMARGIN + GAP + btnSize, top, btnSize, btnSize);
    pygame.draw.rect(DISPLAYSURF, WHITE, diamondRect);
    pygame.draw.polygon(DISPLAYSURF, BROWN, ((XMARGIN + GAP + btnSize + btnSize/2, top), (XMARGIN + GAP + btnSize+ btnSize - 1, top + btnSize/2), ( XMARGIN + GAP + btnSize + btnSize/2, top + btnSize - 1), (XMARGIN + GAP + btnSize, top + btnSize/2)))
    
    circleRect=pygame.Rect( XMARGIN + ((GAP + btnSize) * 2), top, btnSize, btnSize);
    pygame.draw.rect(DISPLAYSURF, WHITE, circleRect);
    pygame.draw.circle(DISPLAYSURF, BROWN, (XMARGIN + ((GAP + btnSize) * 2) + btnSize/2, top + btnSize/2), 
btnSize/2 - 5)

    pygame.draw.circle(DISPLAYSURF, WHITE, ( XMARGIN + ((GAP + btnSize) * 2) + btnSize/2,  top + 
btnSize/2),  btnSize/4 - 5)
    
    lineRect=pygame.Rect( XMARGIN + ((GAP + btnSize) * 3), top, btnSize, btnSize);
    pygame.draw.rect(DISPLAYSURF, WHITE, lineRect);
    for i in range(0, btnSize, 4):

        pygame.draw.line(DISPLAYSURF, BROWN,(XMARGIN + ((GAP + btnSize) * 3), top + i), (XMARGIN + ((GAP + btnSize) * 3)+ 

i, top))

        pygame.draw.line(DISPLAYSURF, BROWN, ( XMARGIN + ((GAP + btnSize) * 3) + i, top + btnSize

- 1), (XMARGIN + ((GAP + btnSize) * 3) + btnSize - 1, top + i))
    
    
def drawNext():
    Rect=pygame.Rect(600, YMARGIN ,100, 100);
    text=BASICFONT.render('NEXT', True, BLUE)
    textRect=text.get_rect();
    textRect.center=(600 + 100/2, YMARGIN + 100/2);
    
    pygame.draw.rect(DISPLAYSURF, WHITE, Rect);
    DISPLAYSURF.blit(text, textRect);
    return Rect;
def boardCoords(cards, top, x, y):
    for i in range(len(cards)):
        boxRect=pygame.Rect(XMARGIN + (i * (CARDWIDTH + GAP)), top, CARDWIDTH, CARDHEIGHT);
        if boxRect.collidepoint(x, y):
            return i 
    return None;
            
def makeMove(cards, playedCards,x, y, top, add):
    box=boardCoords(cards, top, x, y);
    playedCards.append(cards[box + add]);
    slideAnimation(cards[box + add], XMARGIN + (box * (CARDWIDTH + GAP)) , PLAYERPOSY + CARDHEIGHT + GAP, STARTCARDX, MARKETCARDY, UP, False)
        
def isValidMove(card, comCard):
    if card['number']==comCard['number'] or card['shape']==comCard['shape'] or card['number']=='20':
        return True;
    else:
        return False;
        
def compMove(compCards, playCards, startingCard):
    possibleMoves=[];
    if len(playCards) <= 1:
        for i in range(len(compCards)):
            if compCards[i]['number'] in ['2', '5']:
                if isValidMove(compCards[i], startingCard):
                    return i;
            elif compCards[i]['number'] in ['1', '8']:
                if isValidMove(compCards[i], startingCard):
                    return i;
    elif len(possibleMoves) == 0:
        for i in range(len(compCards)):
            if int(compCards[i]['number'] ) > 8:
                if isValidMove(compCards[i], startingCard):
                    return i;
            elif compCards[i]['number'] in ['1', '8']:
                if isValidMove(compCards[i], startingCard):
                    return i;
            elif compCards[i]['number'] in ['2', '5']:
                if isValidMove(compCards[i], startingCard):
                    return i;
    else:
        for i in range(len(compCards)):
            if isValidMove(compCards[i], startingCard):
                possibleMove.append(i);
        return random.choice(possibleMove);
    return None;
def drawText(text, left, top):
    rectSize=50;
    Rect=pygame.Rect(left, top, rectSize , rectSize);
    text=BASICFONT.render(str(text), True, BROWN)
    textRect=text.get_rect();
    textRect.center=(left + rectSize/2,  top + rectSize/2);
    pygame.draw.rect(DISPLAYSURF, WHITE, Rect);
    pygame.draw.rect(DISPLAYSURF, BROWN, Rect, 5);
    DISPLAYSURF.blit(text, textRect)
def drawTextForBoard(text, left, top):
    rectWidth=140;
    rectHeight=50;
    Rect=pygame.Rect(left, top, rectWidth , rectHeight);
    text=BASICFONT.render(str(text), True, BROWN)
    textRect=text.get_rect();
    textRect.center=(left + rectWidth/2,  top + rectHeight/2);
    pygame.draw.rect(DISPLAYSURF, WHITE, Rect);
    pygame.draw.rect(DISPLAYSURF, BROWN, Rect, 5);
    DISPLAYSURF.blit(text, textRect)
    
def isWinner(cards):
    if len(cards)==0:
        return True;
    return False;
    
    
def gameStateAnimation(text):
    DISPLAYSURF.fill(BGCOLOR)
    Font=pygame.font.Font('freesansbold.ttf', 120)
    text=Font.render(text, True, WHITE)
    textRect=text.get_rect();
    textRect.center=(WINDOWWIDTH/2,  WINDOWHEIGHT/2);
    textRect2=text.get_rect();
    textRect2.center=(WINDOWWIDTH/2 + 3,  WINDOWHEIGHT/2 + 3);
    text2=BASICFONT.render('Tap The Screen To Play Again', True, WHITE);
    textRect3=text2.get_rect()
    textRect3.center=(WINDOWWIDTH/2, WINDOWHEIGHT/2 + 100);
    while checkForKeyPress()==None:
        DISPLAYSURF.blit(text, textRect)
        DISPLAYSURF.blit(text, textRect2)
        DISPLAYSURF.blit(text2, textRect3)
        pygame.display.update()
if __name__=='__main__':
    main();