import math
import random
import pygame as pg
from pygame.locals import *

MOVE_SPEED = 0.2
BULLET_SPEED = 0.3

pg.init()
screenWidth, screenHeight = 640, 480
pg.display.set_caption("games by -3-")
screen = pg.display.set_mode((screenWidth, screenHeight))
keys = [False, False, False, False]
playerPosition = [screenWidth / 2, screenHeight / 2]
bullets = []

playerImg = pg.image.load("./img/player.png")
bulletImg = pg.image.load("./img/bullet.png")

while True:
    screen.fill((188, 188, 188))
    # 旋转玩家
    mousePosition = pg.mouse.get_pos()
    angle = math.atan2(mousePosition[1] - playerPosition[1], mousePosition[0] - playerPosition[0])
    playerRotation = pg.transform.rotate(playerImg, 360 - angle * 57.29)
    playerPosition1 = [playerPosition[0] - playerRotation.get_rect().width / 2, playerPosition[1] - playerRotation.get_rect().height / 2]
    screen.blit(playerRotation, playerPosition1)
    # 移动玩家
    if keys[0]:
        playerPosition[1] -= MOVE_SPEED
    elif keys[2]:
        playerPosition[1] += MOVE_SPEED
    if keys[1]:
        playerPosition[0] -= MOVE_SPEED
    elif keys[3]:
        playerPosition[0] += MOVE_SPEED

    # 处理子弹
    for bullet in bullets:
        index = 0
        bullet[1] += math.cos(bullet[0]) * BULLET_SPEED
        bullet[2] += math.sin(bullet[0]) * BULLET_SPEED
        if bullet[1] < -8 or bullet[1] > screenWidth + 8 or bullet[2] < -8 or bullet[2] > screenHeight + 8:
            bullets.pop(index)
        index += 1
        screen.blit(bulletImg, (bullet[1], bullet[2]))

    # 处理事件
    for event in pg.event.get():
        # 退出事件
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        # 鼠标左键发射
        if event.type == pg.MOUSEBUTTONDOWN:
            bullets.append([angle, playerPosition[0], playerPosition[1]])
        # 键盘按下事件
        if event.type == pg.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
        # 键盘放开事件
        if event.type == pg.KEYUP:
            if event.key == K_w:
                keys[0] = False
            elif event.key == K_a:
                keys[1] = False
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_d:
                keys[3] = False

    # 绘制
    pg.display.flip()
