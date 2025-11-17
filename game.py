import pgzrun
import random
import Personagem as p
import Enemy as e
from pgzero import clock

beep = tone.create('A3', 0.1)
################
# Music track: Majestic by Alegend
# Source: https://freetouse.com/music
# No Copyright Background Music
#################

character = p.Personagem(Actor('personagem1_stay'),'personagem1_stay', 'personagem1_hurt', 'personagem1_right', 'personagem1_right2', 'personagem1_left', 'personagem1_left2')
character.set_pos(2, 284)

enemy = e.Enemy(Actor('enemy'),0.5,0)
enemy.set_pos(90, 294)
enemy2 = e.Enemy(Actor('enemy2'),-1,0)
enemy2.set_pos(90, 62)
enemy2.actor.angle=180
enemy3 = e.Enemy(Actor('enemy3'),0,-2)
enemy3.set_pos(random.randint(160,200), 180)

enemy4 = e.Enemy(Actor('enemy'),0.5,0)
enemy4.set_pos(270, 294)
enemy5 = e.Enemy(Actor('enemy2'),-1,0)
enemy5.set_pos(210, 62)
enemy5.actor.angle=180
enemy6 = e.Enemy(Actor('enemy3'),0,-2)
enemy6.set_pos(random.randint(280,330), 220)
enemy7 = e.Enemy(Actor('enemy3'),0,-2)
enemy7.set_pos(random.randint(340,378), 150)
enemies = [enemy, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7]
obstacles = [enemy.actor, enemy2.actor, enemy3.actor, enemy4.actor, enemy5.actor, enemy6.actor, enemy7.actor]

# Botão de começar o jogo
start = Actor('botao_iniciar', center=(250, 100))
# Botão de desligar os sons
music = Actor('botao_musica', center=(250, 200))
# Botão de sair
exit_ = Actor('botao_sair', center=(250, 300))

sound_on = True
game_started = False
game_over = False
score = 0

WIDTH = 500
HEIGHT = 400

ground=[]

def create_map():
    global ground
    ground = []
    for i in range(0, WIDTH, 8):
        ground.append(Actor('chao', topleft=(0+i, 300)))
    ground.append(Actor('chao', topleft=(0, 292)))

    for i in range(0, WIDTH, 8):
        ground.append(Actor('teto', topleft=(0+i, 50)))
    ground.append(Actor('teto', topleft=(0, 58)))

    # Estacas no chão
    for i in range(5):
        if random.randint(0,9) < 1:
            continue
        for a in range(random.randint(5,10)):
            ground.append(Actor('reto1', topleft=(30+i*90, 300-a*8)))
        ground.append(Actor('quina1', topleft=(30+i*90, 300-(a+1)*8)))

    # Estacas no teto
    for i in range(7):
        if random.randint(0,9) < 1:
            continue
        for a in range(random.randint(5,10)):
            ground.append(Actor('reto1', topleft=(50+i*70, 50+a*8)))
        ground.append(Actor('quina2', topleft=(50+i*70, 50+(a+1)*8)))

    # Plataformas horizontais
    for i in range(6):
        if random.randint(0,9) < 1:
            continue
        x = random.randint(4, 8)
        y = random.randint(-6, 4)
        ground.append(Actor('quina3', topleft=(50+i*70, 200+y*8)))
        for a in range(x):
            ground.append(Actor('reto2', topleft=(58+a*8+i*70, 200+y*8)))
        ground.append(Actor('quina4', topleft=(58+(a+1)*8+i*70, 200+y*8)))

    # Plataformas verticais
    for i in range(8):
        if random.randint(0,9) < 1:
            continue
        x = random.randint(2, 5)
        y = random.randint(-2, 4)
        ground.append(Actor('quina1', topleft=(50+i*50, 150+y*8)))
        for a in range(x):
            ground.append(Actor('reto1', topleft=(50+i*50, 158+a*8+y*8)))
        ground.append(Actor('quina2', topleft=(50+i*50, 158+y*8+(a+1)*8)))

def draw():
    global game_started

    screen.fill((0, 0, 150))
    # Desenhar botões tela inicial
    if not game_started:
        start.draw()
        music.draw()
        exit_.draw()
    else:
        character.draw()
        for e in enemies:
            e.draw()
        
        for part in ground:
            part.draw()
        screen.draw.filled_rect(Rect((0,308),(500,400)), (95, 87, 79))
        screen.draw.filled_rect(Rect((0,0),(500,50)), (95, 87, 79))
        screen.draw.text("Score: "+str(score), (20, 20))

def update():
    global game_over, game_started, score

    if not game_started or game_over:
        return
    # Animação de movimento
    if character.vx < 0:
        character.animate_left()
    elif character.vx > 0:
        character.animate_right()
    else:
        character.set_actor_normal()

    movement(character)
    for e in enemies:
        movement(e)
    enemies[2].change_image("enemy3","enemy3_2")
    enemies[5].change_image("enemy3","enemy3_2")
    enemies[6].change_image("enemy3","enemy3_2")
    
    if character.actor.left > WIDTH:
        character.actor.right = 2
        create_map()
        score += 100

    if character.actor.collidelist(obstacles) != -1:
        character.set_actor_hurt()
        if sound_on and not game_over:
            sounds.explosion_crunch_000.play()
        if not game_over:
            character.vx = 0
            character.vy = -2
            clock.schedule_unique(reset, 3)
        game_over = True
    
def reset():
    global game_over, game_started, score
    if game_over:
        create_map()
        game_started = False
        game_over = False
        character.set_pos(2, 284)
        character.set_actor_normal()
        sounds.majestic.stop()
        score = 0

def movement(actor):
    ## Verificando colisões e adicionando movimento
    actor.actor.top -= actor.vy
    if actor.actor.collidelist(ground) != -1:
        actor.actor.top += actor.vy
        if str(type(actor)) == "<class 'Enemy.Enemy'>":
            actor.hit()
    
    actor.actor.left += actor.vx
    if actor.actor.collidelist(ground) != -1:
        actor.actor.left -= actor.vx
        if str(type(actor)) == "<class 'Enemy.Enemy'>":
            actor.hit()
    elif actor.actor.left < -4:
        actor.actor.left -= actor.vx
        
def on_mouse_down(pos):
    global sound_on, game_started
    # Verificar click nos botões da tela inicial
    if game_started:
        return
    elif start.collidepoint(pos):
        game_started = True
        if sound_on:
            sounds.majestic.play()
    elif music.collidepoint(pos):
        sound_on = not sound_on
        if sound_on:
            beep.play()
    elif exit_.collidepoint(pos):
        exit()

def on_key_down(key):
    if game_started and not game_over:
        if keys.D == key:
            character.vx += 2
        if keys.W == key:
            character.vy += 4
        if keys.A == key:
            character.vx += -2

def on_key_up(key):
    if game_started and not game_over:
        if keys.D == key:
            character.vx -= 2
        if keys.W == key:
            character.vy -= 4
        if keys.A == key:
            character.vx -= -2

create_map()
pgzrun.go()