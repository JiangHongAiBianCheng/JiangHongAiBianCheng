# 导入一些需要的库
from random import *
from math import *
import pgzrun as pz

# 设置游戏屏幕的高度、宽度、标题
WIDTH: int = 800
HEIGHT: int = 600
TITLE: str = "game"

# 设置敌人在x轴和y轴上的速度
dx: float = uniform(-1, 1)
dy: float = uniform(-1, 1)

# 创建各个角色
player: Actor = Actor("player.png", [WIDTH//2, HEIGHT//2])
enemy: Actor = Actor("enemy.png", [randint(0, WIDTH), randint(0, HEIGHT)])
enemy.angle = degrees(atan2(-dy, dx))   # 计算敌人的角度
knife: Actor = Actor("knife.png", [400,100])

# 设置游戏是否结束、胜利、是否需要绘制刀子
end: bool = False
win: bool = False
drawKnife: bool = True

def set_dead() -> None:
    '''
    设置游戏结束
    '''
    global end
    end = True

def set_win() -> None:
    '''
    设置游戏胜利
    '''
    global win
    win = True

def get_degrees(x: float, y: float) -> float:
    '''
    计算pgzero里的角度
    '''
    return degrees(atan2(-y, x))                    # 计算并返回角度

def set_enemy_new_direction() -> None:
    '''
    设置敌人新的方向
    '''
    global dx, dy
    dx, dy = uniform(-1, 1), uniform(-1, 1)         # 设置敌人的x轴和y轴速度
    enemy.angle = get_degrees(dx, dy)               # 计算敌人的角度

def set_knife_new_position() -> None:
    '''
    设置刀子的新的位置
    '''
    knife.x = randint(0, WIDTH)                     # 设置刀子在x轴上的新位置
    knife.y = randint(0, HEIGHT)                    # 设置刀子在y轴上的新位置

clock.schedule_unique(set_win, 60)                  # 设置游戏在60秒后胜利
clock.schedule_interval(set_enemy_new_direction, 3) # 设置敌人每3秒改变一次方向
clock.schedule_interval(set_knife_new_position, 3)  # 设置刀子每3秒改变一次位置

def draw() -> None:
    '''
    绘制游戏画面
    '''
    screen.fill("white")                            # 设置背景颜色
    if not (end or win):                            # 如果游戏进行中
        player.draw()                               # 绘制玩家
        enemy.draw()                                # 绘制敌人
        if drawKnife:                               # 如果要绘制刀子
            knife.draw()                            # 绘制刀子
    if end:                                         # 如果游戏结束
        screen.draw.text("Game Over", center=(WIDTH//2, HEIGHT//2), fontsize=100, color="red")  # 绘制"Game Over"
        clock.schedule(exit, 3)                     # 3秒后退出
    if win:                                         # 如果游戏胜利
        screen.draw.text("You Win", center=(WIDTH//2, HEIGHT//2), fontsize=100, color="red")    # 绘制"You Win"
        clock.schedule(exit, 3)                     # 3秒后退出

def update() -> None:
    '''
    更新、计算游戏元素
    '''
    global drawKnife, dx, dy
    if not (end or win):                            # 如果游戏进行中
        if player.colliderect(enemy) and player.image != "player has knife":                    # 如果玩家撞到敌人并且没有持刀
            set_dead()                              # 设置玩家死亡
        elif player.colliderect(enemy) and player.image != "player":                            # 如果玩家撞到敌人并且持刀
            set_win()                               # 设置游戏胜利
        elif player.colliderect(knife) and player.image != "player has knife":                  # 如果玩家撞到刀子并且没有持刀
            player.image = "player has knife"       # 设置玩家持刀
            drawKnife = False                       # 设置不绘制刀子
        
        enemy.move_ip(dx, dy)                       # 移动敌人
        
        if enemy.x < 0 or enemy.x > WIDTH:          # 如果敌人超出x范围
            dx = -dx                                # 改变敌人x方向
            enemy.angle = get_degrees(dx, dy)       # 改变敌人角度
        if enemy.y < 0 or enemy.y > HEIGHT:         # 如果敌人超出y范围
            dy = -dy                                # 改变敌人y方向
            enemy.angle = get_degrees(dx, dy)       # 改变敌人角度

def on_key_down(key) -> None:
    '''
    当按键按下时调用
    '''
    if not (end or win):                            # 如果游戏进行中
        if key == keys.LEFT:                        # 如果按下左键
            player.x -= 20                          # 移动玩家
        if key == keys.RIGHT:                       # 如果按下右键
            player.x += 20                          # 移动玩家
        if key == keys.UP:                          # 如果按下上键
            player.y -= 20                          # 移动玩家
        if key == keys.DOWN:                        # 如果按下下键
            player.y += 20                          # 移动玩家

def main() -> None:
    pz.go()                                         # 运行游戏

if __name__ == 'pgzero.builtins':
    main()