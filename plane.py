import math
import random
import pygame as pg
from pygame.locals import *

# 参数
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MOVE_SPEED = 0.2
BULLET_SPEED = 0.3
SHOOT_TIME = 500
SHOOT_TRACK = 1
SHOOT_TRACK_GAP = 0.1
MONSTER_SPEED = 0.05
MONSTER_HP = 0
MONSTER_CREATE_TIME = 2000
MONSTER_CREATE_NUMBER = 1
MONSTER_STRONG_TIME = 10000
BUFF_TIME = 3000

# 初始化
pg.init()
pg.display.set_caption("games by -3-")
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
keys = [False, False, False, False]
playerPosition = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
bullets = []
shootTimer = SHOOT_TIME
monsters = []
monsterCreateTimer = MONSTER_CREATE_TIME
monsterStrongTimer = MONSTER_STRONG_TIME
buffs = []
buffTimer = BUFF_TIME
score = 0
gaming = True

# 加载图片
playerImg = pg.image.load("./img/player.png")
PLAYER_WIDTH = playerImg.get_rect().width
bulletImg = pg.image.load("./img/bullet.png")
BULLET_WIDTH = bulletImg.get_rect().width
monsterImgs= [pg.image.load("./img/monster0.png"), pg.image.load("./img/monster1.png"), pg.image.load("./img/monster2.png"), pg.image.load("./img/monster3.png"), pg.image.load("./img/monster4.png")]
MONSTER_WIDTH = monsterImgs[0].get_rect().width
buffImgs = [pg.image.load("./img/buff0.png"), pg.image.load("./img/buff1.png"), pg.image.load("./img/buff2.png"), pg.image.load("./img/buff3.png")]
BUFF_WIDTH = buffImgs[0].get_rect().width

while gaming:
    # 填充背景色覆盖上一帧画面
    screen.fill((131, 131, 131))

    # 旋转玩家
    mousePosition = pg.mouse.get_pos()
    playerAngle = math.atan2(mousePosition[1] - playerPosition[1], mousePosition[0] - playerPosition[0])
    playerRotation = pg.transform.rotate(playerImg, 360 - playerAngle * 57.29)
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

    # 玩家Rect
    playerRect = pg.Rect(playerImg.get_rect())
    playerRect.top = playerPosition[1]
    playerRect.left = playerPosition[0]

    # 发射子弹
    if shootTimer > 0:
        shootTimer -= 1
    else:
        shootTimer = SHOOT_TIME
        shootAngle = playerAngle - (SHOOT_TRACK - 1) / 2 * SHOOT_TRACK_GAP
        for i in range(SHOOT_TRACK):
            bullets.append([shootAngle, playerPosition[0], playerPosition[1]])
            shootAngle += SHOOT_TRACK_GAP

    # 生成怪物
    if monsterCreateTimer > 0:
        monsterCreateTimer -= 1
    else:
        monsterCreateTimer = MONSTER_CREATE_TIME
        for i in range(MONSTER_CREATE_NUMBER):
            wall = random.randint(1, 4)
            monsterPosition = ()
            if wall == 1: # 上
                monsterPosition = (random.randint(0, SCREEN_WIDTH), -MONSTER_WIDTH)
            elif wall == 2: # 下
                monsterPosition = (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + MONSTER_WIDTH)
            elif wall == 3: # 左
                monsterPosition = (-MONSTER_WIDTH, random.randint(0, SCREEN_HEIGHT))
            elif wall == 4: # 右
                monsterPosition = (SCREEN_WIDTH + MONSTER_WIDTH, random.randint(0, SCREEN_HEIGHT))
            monsterAngle = math.atan2(playerPosition[1] - monsterPosition[1], playerPosition[0] - monsterPosition[0])
            monsters.append([MONSTER_HP, monsterAngle, monsterPosition[0], monsterPosition[1]])

    # 生成buff
    if buffTimer > 0:
        buffTimer -= 1
    else:
        buffTimer = BUFF_TIME
        buffs.append([random.randint(0, 3), random.randint(SCREEN_WIDTH / 8, SCREEN_WIDTH / 8 * 7), random.randint(SCREEN_HEIGHT / 8, SCREEN_HEIGHT / 8 * 7)])

    # 绘制buff
    for buff in buffs:
        screen.blit(buffImgs[buff[0]], (buff[1], buff[2]))

    # 加强怪物
    if monsterStrongTimer > 0:
        monsterStrongTimer -= 1
    else:
        monsterStrongTimer = MONSTER_STRONG_TIME
        MONSTER_SPEED += 0.05
        MONSTER_HP = min(MONSTER_HP + 1, 4)
        MONSTER_CREATE_TIME = max(MONSTER_CREATE_TIME - 250, 125)
        MONSTER_CREATE_NUMBER += 1

    # 移动怪物
    index = 0
    for monster in monsters:
        monster[2] += math.cos(monster[1]) * MONSTER_SPEED
        monster[3] += math.sin(monster[1]) * MONSTER_SPEED
        if monster[2] < -MONSTER_WIDTH or monster[2] > SCREEN_WIDTH + MONSTER_WIDTH or monster[3] < -MONSTER_WIDTH or monster[3] > SCREEN_HEIGHT + MONSTER_WIDTH:
            monsters.pop(index)
        else:
            index += 1
        screen.blit(monsterImgs[monster[0]], (monster[2], monster[3]))

    # 移动子弹
    index = 0
    for bullet in bullets:
        bullet[1] += math.cos(bullet[0]) * BULLET_SPEED
        bullet[2] += math.sin(bullet[0]) * BULLET_SPEED
        if bullet[1] < -BULLET_WIDTH or bullet[1] > SCREEN_WIDTH + BULLET_WIDTH or bullet[2] < -BULLET_WIDTH or bullet[2] > SCREEN_HEIGHT + BULLET_WIDTH:
            bullets.pop(index)
        else:
            index += 1
        screen.blit(bulletImg, (bullet[1], bullet[2]))

    # HUD
    scoreFont = pg.font.SysFont('arial', 24)
    scoreText = scoreFont.render("score: " + str(score), 1, (0, 0, 0))
    scoreRect = scoreText.get_rect()
    scoreRect.topleft = [10, 10]
    screen.blit(scoreText, scoreRect)

    buffFont = pg.font.SysFont('arial', 18)
    buff0Text = buffFont.render("speed: " + str(round(MOVE_SPEED, 1)), 1, (231, 33, 40))
    buff0Rect = buff0Text.get_rect()
    buff0Rect.topright = [SCREEN_WIDTH - 10, 10]
    buff1Text = buffFont.render("shoot gap: " + str(SHOOT_TIME), 1, (231, 231, 33))
    buff1Rect = buff1Text.get_rect()
    buff1Rect.topright = [SCREEN_WIDTH - 10, 30]
    buff2Text = buffFont.render("shoot speed: " + str(round(BULLET_SPEED, 1)), 1, (80, 231, 33))
    buff2Rect = buff2Text.get_rect()
    buff2Rect.topright = [SCREEN_WIDTH - 10, 50]
    buff3Text = buffFont.render("bullet: " + str(SHOOT_TRACK), 1, (33, 116, 231))
    buff3Rect = buff3Text.get_rect()
    buff3Rect.topright = [SCREEN_WIDTH - 10, 70]
    screen.blit(buff0Text, buff0Rect)
    screen.blit(buff1Text, buff1Rect)
    screen.blit(buff2Text, buff2Rect)
    screen.blit(buff3Text, buff3Rect)

    # 处理键盘事件
    for event in pg.event.get():
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
            elif event.key == K_ESCAPE or event.key == K_q:
                pg.quit()
                exit()
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

    # 处理怪物碰撞事件
    index_monster = 0
    for monster in monsters:
        monsterRect = pg.Rect(monsterImgs[monster[0]].get_rect())
        monsterRect.top = monster[3]
        monsterRect.left = monster[2]
        # 与玩家的碰撞
        if monsterRect.colliderect(playerRect):
            gaming = False
        # 与子弹的碰撞
        index_bullet = 0
        for bullet in bullets:
            bulletRect = pg.Rect(bulletImg.get_rect())
            bulletRect.top = bullet[2]
            bulletRect.left = bullet[1]
            if monsterRect.colliderect(bulletRect):
                score += 1
                bullets.pop(index_bullet)
                monster[0] -= 1
                if monster[0] < 0:
                    monsters.pop(index_monster)
                    index_monster -= 1
                    break
            else:
                index_bullet += 1
        index_monster += 1

    # 处理buff与玩家的碰撞
    index = 0
    for buff in buffs:
        buffRect = pg.Rect(buffImgs[buff[0]].get_rect())
        buffRect.top = buff[2]
        buffRect.left = buff[1]
        if buffRect.colliderect(playerRect):
            buffs.pop(index)
            if buff[0] == 0: # 0.2
                MOVE_SPEED += 0.1
            elif buff[0] == 1: # 500
                SHOOT_TIME = max(SHOOT_TIME - 100, 50)
            elif buff[0] == 2: # 0.3
                BULLET_SPEED += 0.2
            elif buff[0] == 3: # 1
                SHOOT_TRACK += 2
        else:
            index += 1

    # 绘制
    pg.display.flip()

# 失败
screen.fill((0, 0, 0))
loseFont = pg.font.SysFont('arial', 60)
loseText = loseFont.render("you lose  score: " + str(score), 1, (255, 0, 0))
loseRect = loseText.get_rect()
loseRect.centerx = screen.get_rect().centerx
loseRect.centery = screen.get_rect().centery
screen.blit(loseText, loseRect)
pg.display.flip()

while True:
    for event in pg.event.get():
        if event.type == pg.KEYDOWN and (event.key == K_ESCAPE or event.key == K_q):
            pg.quit()
            exit()
