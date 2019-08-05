import math
import random
import pygame as pg
from pygame.locals import *

# 参数
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MOVE_SPEED = 0.1
BULLET_SPEED = 0.3
SHOOT_TIME = 500
MONSTER_SPEED = 0.05
MONSTER_TIME = 2000

# 初始化
pg.init()
pg.display.set_caption("games by -3-")
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
keys = [False, False, False, False]
playerPosition = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
bullets = []
shootTimer = SHOOT_TIME
monsters = []
monsterTimer = MONSTER_TIME
score = 0
gaming = True

# 加载图片
playerImg = pg.image.load("./img/player.png")
PLAYER_WIDTH = playerImg.get_rect().width
bulletImg = pg.image.load("./img/bullet.png")
BULLET_WIDTH = bulletImg.get_rect().width
monsterImg = pg.image.load("./img/monster.png")
MONSTER_WIDTH = monsterImg.get_rect().width

while gaming:
    # 填充背景色覆盖上一帧画面
    screen.fill((188, 188, 188))

    # HUD
    scoreFont = pg.font.Font(None, 36)
    scoreText = scoreFont.render(str(score), 1, (0, 0, 0))
    scoreRect = scoreText.get_rect()
    scoreRect.topleft = [10, 10]
    screen.blit(scoreText, scoreRect)

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

    # 发射子弹
    if shootTimer > 0:
        shootTimer -= 1
    else:
        shootTimer = SHOOT_TIME
        bullets.append([playerAngle, playerPosition[0], playerPosition[1]])

    # 生成怪物
    if monsterTimer > 0:
        monsterTimer -= 1
    else:
        monsterTimer = MONSTER_TIME
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
        monsters.append([monsterAngle, monsterPosition[0], monsterPosition[1]])

    # 移动怪物
    index = 0
    for monster in monsters:
        monster[1] += math.cos(monster[0]) * MONSTER_SPEED
        monster[2] += math.sin(monster[0]) * MONSTER_SPEED
        if monster[1] < -MONSTER_WIDTH or monster[1] > SCREEN_WIDTH + MONSTER_WIDTH or monster[2] < -MONSTER_WIDTH or monster[2] > SCREEN_HEIGHT + MONSTER_WIDTH:
            monsters.pop(index)
        else:
            index += 1
        screen.blit(monsterImg, (monster[1], monster[2]))

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

    # 处理鼠标键盘事件
    for event in pg.event.get():
        # 退出事件
        if event.type == pg.K_ESCAPE:
            pg.quit()
            exit()
        # 鼠标左键发射
        # if event.type == pg.MOUSEBUTTONDOWN:
        #     bullets.append([playerAngle, playerPosition[0], playerPosition[1]])
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

    # 处理碰撞事件
    index_monster = 0
    for monster in monsters:
        monsterRect = pg.Rect(monsterImg.get_rect())
        monsterRect.top = monster[2]
        monsterRect.left = monster[1]
        # 与子弹的碰撞
        index_bullet = 0
        for bullet in bullets:
            bulletRect = pg.Rect(bulletImg.get_rect())
            bulletRect.top = bullet[2]
            bulletRect.left = bullet[1]
            if monsterRect.colliderect(bulletRect):
                score += 1
                monsters.pop(index_monster)
                bullets.pop(index_bullet)
                index_monster -= 1
                break
            index_bullet += 1

        # 与玩家的碰撞
        playerRect = pg.Rect(playerImg.get_rect())
        playerRect.top = playerPosition[1]
        playerRect.left = playerPosition[0]
        if monsterRect.colliderect(playerRect):
            gaming = False
        index_monster += 1

    # 绘制
    pg.display.flip()

# 失败
screen.fill((188, 188, 188))
loseFont = pg.font.Font(None, 36)
loseText = loseFont.render("you lose", 1, (0, 0, 0))
loseRect = loseText.get_rect()
loseRect.centerx = screen.get_rect().centerx
loseRect.centery = screen.get_rect().centery
screen.blit(loseText, loseRect)
pg.display.flip()

while True:
    for event in pg.event.get():
        if event.type == pg.K_ESCAPE:
            pg.quit()
            exit()
