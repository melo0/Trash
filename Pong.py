import pygame, sys, time
from pygame.locals import *

FPS = 150
window_width = 400
window_height = 300
line_thickness = 10
paddle_size = 30
paddle_offset = 30
black = (0, 0, 0)
white = (255, 255, 255)
ballX = window_width / 2 - line_thickness / 2
ballY = window_height / 2 - line_thickness / 2


def drawArena():
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, white, ((0, 0), (window_width, window_height)), line_thickness * 2)
    pygame.draw.line(screen, white, ((int(window_width / 2), 0)), ((int(window_width / 2)), window_height)), (int(line_thickness) / 4)

def drawPaddle(paddle):
    if paddle.bottom > window_height - line_thickness:
        paddle.bottom = window_height - line_thickness
    elif paddle.top < line_thickness:
        paddle.top = line_thickness
    pygame.draw.rect(screen, white, paddle)

def drawBall(ball):
    #pygame.draw.ellipse(screen, white, ball)
    ballImg = pygame.image.load('ball.png')
    screen.blit(ballImg, ball)

def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (line_thickness) or ball.bottom == (window_height - line_thickness):
        ballDirY = ballDirY * -1
    if ball.left == (line_thickness) or ball.right == (window_width - line_thickness):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else:
        return 1

def artifialIntelligence(ball, ballDirX, paddle2):
    if ballDirX == -1:
        if paddle2.centery < (window_height / 2):
            paddle2.y += 1
        elif paddle2.centery > (window_height / 2):
            paddle2.y -= 1
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -= 1
    return paddle2

def checkPointScored(paddle1, ball, score, ballDirX):
    if ball.left == line_thickness:
        return 0
    elif ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        score += 1
        return score
    elif ball.right == window_width - line_thickness:
        score += 5
        return score
    else:
        return score

def checkPointScored_cpu(paddle2, ball, score_cpu, ballDirX):
    if ball.right == window_width - line_thickness:
        return 0
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        score_cpu +=1
        return score_cpu
    else:
        return score_cpu

def displayScore(score):
    resultSurf = basicFont.render('Score = %s' %(score), True, white)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (window_width - 350, 25)
    screen.blit(resultSurf, resultRect)

def displayScore_cpu(score_cpu):
    resultSurf = basicFont.render('CPU = %s' %(score_cpu), True, white)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (window_width - 150, 25)
    screen.blit(resultSurf, resultRect)

def showResult(score, score_cpu):
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, white, ((0, 0), (window_width, window_height)), line_thickness * 2)
    Result = basicFont.render('Wynik %s : %s' %(score, score_cpu),True, white)
    ResultRect = Result.get_rect()
    ResultRect.center = (window_width/2, window_height/2)
    screen.blit(Result, ResultRect)
    pygame.display.update()
    time.sleep(3)
    main()



def main():
    pygame.init()
    global screen
    global basicFont, basicFontSize
    fpsClock = pygame.time.Clock()
    basicFontSize = 20
    basicFont = pygame.font.Font('freesansbold.ttf', basicFontSize)
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Pong')
    ballDirX = -1
    ballDirY = -1
    playerOnePosition = (window_height - paddle_size) / 2
    playerTwoPosition = (window_height - paddle_size) / 2
    paddle1 = pygame.Rect(paddle_offset, playerOnePosition, line_thickness, paddle_size)
    paddle2 = pygame.Rect(window_width - paddle_offset - line_thickness, playerTwoPosition, line_thickness, paddle_size)
    ball = pygame.Rect(ballX, ballY, line_thickness, line_thickness)
    score = 0
    score_cpu = 0
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)
    pygame.mouse.set_visible(1)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if (score > score_cpu +1 ) and (score > 3):
                showResult(score, score_cpu)
            if (score_cpu > score + 1) and (score_cpu > 5):
                showResult(score, score_cpu)
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey
        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)
        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        score = checkPointScored(paddle1, ball, score, ballDirX)
        score_cpu = checkPointScored_cpu(paddle2, ball, score_cpu, ballDirX)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
        paddle2 = artifialIntelligence(ball, ballDirX, paddle2)
        displayScore(score)
        displayScore_cpu(score_cpu)
        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
