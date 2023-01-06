# Import Libaries 
import pygame, sys
from pygame.locals import *
pygame.init()
from pygame import mixer


clock = pygame.time.Clock()
# Creates window for the game
pygame.display.set_caption('   CONTRA-versial')
WIDTH = 900
HEIGHT = 500
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
tile_size = 50
bullet_size = (20,10)
PLAYER_WIDTH, PLAYER_HEIGHT = 30, 50

pygame.font.init()
myfont = pygame.font.SysFont('monospace', 10)

######Defining all images used and scales them to fit on WINDOW#####

BACKGROUND = pygame.image.load('Assets/Map_Tiles/backround.jpg').convert_alpha()
BACKGROUND = pygame.transform.scale(BACKGROUND,(WIDTH,HEIGHT))

Wall1 = pygame.image.load('Assets/Map_Tiles/MetalGrate.jpg').convert_alpha()
Wall1 = pygame.transform.scale(Wall1,(tile_size,tile_size))

Wall2 = pygame.image.load('Assets/Map_Tiles/ShipPlating(1).png').convert_alpha()
Wall2 = pygame.transform.scale(Wall2,(tile_size,tile_size))

Floor1 = pygame.image.load('Assets/Map_Tiles/MetalFloor1.jpg').convert_alpha()
Floor1 = pygame.transform.scale(Floor1, (tile_size,tile_size))

Tech1 = pygame.image.load('Assets/Map_Tiles/Control.jpg').convert_alpha()
Tech1 = pygame.transform.scale(Tech1, (tile_size,tile_size))

Tech2 = pygame.image.load('Assets/Map_Tiles/Energy.jpg').convert_alpha()
Tech2 = pygame.transform.scale(Tech2, (tile_size,tile_size))

Tech3 = pygame.image.load('Assets/Map_Tiles/Rockets!.jpg').convert_alpha()
Tech3 = pygame.transform.scale(Tech3, (tile_size,tile_size))

Door1 = pygame.image.load('Assets/Map_Tiles/BrokenBlastdoor.jpg').convert_alpha()
Door1 = pygame.transform.scale(Door1, (tile_size,tile_size))

GLASS = pygame.image.load('Assets/Map_Tiles/glassstain.png').convert_alpha()
GLASS = pygame.transform.scale(GLASS, (tile_size,tile_size))


PLAYER = pygame.image.load('Assets/Character_Sprites/thisisaguy.png').convert_alpha()
PLAYER = pygame.transform.scale(PLAYER, (PLAYER_WIDTH, PLAYER_HEIGHT))

PLAYERBULLET = pygame.image.load('Assets/Character_Sprites/redpewpew.png').convert_alpha()
PLAYERBULLET = pygame.transform.scale(PLAYERBULLET,bullet_size)

ENEMYBULLET = pygame.image.load('Assets/Character_Sprites/bluepewpew.png').convert_alpha()
ENEMYBULLET = pygame.transform.scale(ENEMYBULLET,bullet_size)

shot_delay = 30

rightwalk = [pygame.transform.scale(pygame.image.load('Assets/Animations/Playerspriteanimations/pixil-frame-'+str(i)+'.png').convert_alpha(),(PLAYER_WIDTH, PLAYER_HEIGHT)) for i in range(6)]

leftwalk = [pygame.transform.scale(pygame.image.load('Assets/Animations/Playerspriteanimationleft/pixil-frame-'+str(i)+'L.png').convert_alpha(),(PLAYER_WIDTH, PLAYER_HEIGHT)) for i in range(6)]


#########
scroll_x = 0

class enemy:
  def __init__(self, health, sprite_l, sprite_r, pos):
    instances.append(self)
    self.faceleft = False
    self.health = health
    self.sprite_l = pygame.transform.scale(pygame.image.load(sprite_l).convert_alpha(),(tile_size,tile_size))
    self.sprite_r = pygame.transform.scale(pygame.image.load(sprite_r).convert_alpha(),(tile_size,tile_size))
    self.pos = pos
    self.shot_delay = 200
    self.delay = 0

  def rect(self):
    return pygame.Rect(self.pos[0]+scroll_x, self.pos[1], tile_size, tile_size)

  def damage(self,num):
    self.health -= num
    mixer.music.load('Assets/Sounds/hitrobot.mp3')
    mixer.music.set_volume(1)
    mixer.music.play()
    if self.health <=1: 
      instances.remove(self)
      global killcount
      killcount+=1
      mixer.music.load('Assets/Sounds/explosion.mp3')
      mixer.music.set_volume(1)
      mixer.music.play()

  def dostuff(self):
    if self.rect().x < PLAYER_RECT.x:
      self.faceleft = False
    else: self.faceleft = True
    if self.delay < self.shot_delay:
      self.delay +=1
    else:
      self.delay = 0
      shoot(self.faceleft,False,(self.pos[0]+scroll_x,self.pos[1]))
def closehit(rect1, rect2):
  if abs(rect1.x - rect2.x) < 5 and abs(rect1.y - rect2.y) < 5: return True
  return False


def load_map(path):
    global instances, bullets, scroll_x, PLAYER_RECT
    instances=[]
    bullets = []
    f = open(path, 'r')
    game_map = [list(row) for row in f.read().split('\n')]
    f.close
    scroll_x = 0
    y = 0
    for row in game_map:
      x = 0
      for tile in row:
        if tile == '3':
          instances.append(enemy(12,'Assets/Character_Sprites/robotl.png','Assets/Character_Sprites/robotr.png',(x*tile_size+scroll_x, y*tile_size)))
        x += 1
      y += 1
    PLAYER_RECT = pygame.Rect(410,250,PLAYER_WIDTH,PLAYER_HEIGHT)
    return game_map

start_health = 12
health = start_health
def damage(num):
  global health
  health -= num
  if health <= 0:
    die()
  
#Loads map file
game_map = load_map('Maps/fall.txt')
'''

HERE

'''
levelsbackup = ['Maps/tutorial.txt','Maps/test.txt', 'Maps/debris.txt','Maps/pray.txt', 'Maps/win.txt']
levels = levelsbackup

def die():
  global game_map, health, start_health, levels, levelsbackup
  game_map = load_map('Maps/ded.txt')
  health = start_health
  levels = levelsbackup

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {
        'top': False,
        'bottom': False,
        'right': False,
        'left': False
    }
    global scroll_x
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return collision_types

bullets = []
bullet_speed = 5

def shoot(left, player, posi):
  pos = [posi[0] - scroll_x,posi[1]]
  bullets.append([left, player, pos])

def movepewpew():
  for i in bullets:
    if i[0]: i[2][0] -= bullet_speed
    else: i[2][0] += bullet_speed

def renderpewpew():
  for i in bullets:
    if i[1]:
      WINDOW.blit(PLAYERBULLET,(i[2][0] + scroll_x, i[2][1]+10))
    else:
      WINDOW.blit(ENEMYBULLET,(i[2][0] + scroll_x, i[2][1]+10))

def pewpewcollide():
  for i in bullets:
    collider = pygame.Rect(i[2][0] + scroll_x, i[2][1]+10, bullet_size[0], bullet_size[1])
    if i[1]:
      collides = collision_test(collider, tile_rects)
      if len(collides) > 0:
        try: bullets.remove(i)
        except: pass
        for x in instances:
          for j in collides:
            if closehit(j,x.rect()): x.damage(1)
    else:

      def isrobot():
        for x in instances:
          for j in collides:
            if closehit(j,x.rect()): return True
        return False

      
      collides = collision_test(collider, tile_rects)
      if len(collides) > 0:
        if not isrobot(): 
          try:bullets.remove(i)
          except: pass
      if collider.colliderect(PLAYER_RECT):
        try:
          bullets.remove(i)
          damage(1)
        except: pass
      
#Presets values for player movement/jumping
PLAYER_right = False
PLAYER_left = False
PLAYER_y_momentum = 0
PLAYER_air_timer = 0
face_right = False

killcount, walkframe = 0,0

instances = []


delay=shot_delay

# Game Loop
while True:
  
    if delay <= shot_delay: delay += 1

  
    tile_rects = []

    WINDOW.blit(BACKGROUND, (0, 0))
  
  #Makes map from the map.txt file
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
              WINDOW.blit(Wall1, (x*tile_size+scroll_x, y*tile_size)) 
            elif tile == '2':
              WINDOW.blit(Floor1, (x*tile_size+scroll_x, y*tile_size))
            elif tile == '4':
              WINDOW.blit(Tech1, (x*tile_size+scroll_x,y*tile_size))
            elif tile == '5':
              WINDOW.blit(Tech2, (x*tile_size+scroll_x, y*tile_size))
            elif tile == '6':
              WINDOW.blit(Door1, (x*tile_size+scroll_x, y*tile_size))
            elif tile == '0' or tile == '3':
              WINDOW.blit(GLASS, (x*tile_size+scroll_x, y*tile_size))
            elif tile == '7':
              WINDOW.blit(Tech3, (x*tile_size+scroll_x, y*tile_size))
            elif tile == '8':
              WINDOW.blit(Wall2, (x*tile_size+scroll_x, y*tile_size))
          
            if tile == '2' or tile == '8':
              tile_rects.append(pygame.Rect(x * tile_size + scroll_x, y * tile_size, tile_size, tile_size))

            x += 1
        y += 1

    for i in instances:
      tile_rects.append(i.rect())
      i.dostuff()
  # player movement & collisions
    PLAYER_movement = [0, 0]
    if PLAYER_right:
        PLAYER_movement[0] += 3
        face_right = True
    if PLAYER_left:
        PLAYER_movement[0] -= 3
        face_right = False
    PLAYER_movement[1] += PLAYER_y_momentum
    PLAYER_y_momentum += 0.15
    if PLAYER_y_momentum > 3:
        PLAYER_y_momentum = 3

    PLAYER_collisions = move(PLAYER_RECT, PLAYER_movement, tile_rects)

    if PLAYER_collisions['bottom']:
        PLAYER_y_momentum = 0
        PLAYER_air_timer = 0
    else:
        PLAYER_air_timer += 1

    if PLAYER_collisions['top']:
        PLAYER_y_momentum = 0

    if (not (PLAYER_collisions['right'])) and (not (PLAYER_collisions['left'])):
      scroll_x -= PLAYER_movement[0]

  #Defines which keys move the characters 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.VIDEORESIZE:
            WINDOW=pygame.display.set_mode(event.size)

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                PLAYER_right = True
                PLAYER = pygame.transform.scale(pygame.image.load('Assets/Character_Sprites/thisisaguy.png').convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
            if event.key == K_LEFT:
                PLAYER_left = True
                PLAYER = pygame.transform.scale(pygame.image.load('Assets/Character_Sprites/thisisaguyleft.png').convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
            if event.key == K_UP:
                if PLAYER_air_timer < 10:
                    PLAYER_y_momentum = -5
            if event.key == K_SPACE:
              if delay >= shot_delay:
                delay = 0
                shoot(not face_right, True, [PLAYER_RECT.x, PLAYER_RECT.y])
                mixer.music.load('Assets/Sounds/pewpew.mp3')
                mixer.music.set_volume(1)
                mixer.music.play()
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                PLAYER_right = False
            if event.key == K_LEFT:
                PLAYER_left = False
    if PLAYER_RECT.x > 410:
      PLAYER_RECT.x -= 1
      scroll_x -= 1
    if PLAYER_RECT.x < 410:
      PLAYER_RECT.x += 1
      scroll_x += 1

    movepewpew()
    renderpewpew()
    pewpewcollide()

    for i in instances: 
      if i.faceleft: WINDOW.blit(i.sprite_l,(i.pos[0] + scroll_x, i.pos[1]))
      else: WINDOW.blit(i.sprite_r,(i.pos[0] + scroll_x, i.pos[1]))
    xval = myfont.render(str(health), False,(0,0,0) )
    shotbar = pygame.Rect(PLAYER_RECT.x,PLAYER_RECT.y+50,(delay / shot_delay * 50), 10)
    if delay < shot_delay: pygame.draw.rect(WINDOW,(255,255,255),shotbar)
    pygame.draw.rect(WINDOW,(0,0,0),pygame.Rect(7,7,start_health*5+2,17))
    pygame.draw.rect(WINDOW,(255,0,0),pygame.Rect(8,8,health*5,15))
    WINDOW.blit(xval,(10,10))
    #Projects everything onto the WINDOW
    if PLAYER_RECT.y > WINDOW.get_height(): 
      game_map = load_map(levels[0])
      levels = levels[1:]
    if walkframe >= 5:
      walkframe = 0
    else: walkframe +=0.1
    if PLAYER_right: 
      WINDOW.blit(rightwalk[int(walkframe)], (PLAYER_RECT.x,PLAYER_RECT.y))
    elif PLAYER_left:
      WINDOW.blit(leftwalk[int(walkframe)], (PLAYER_RECT.x,PLAYER_RECT.y))
    else: 
      WINDOW.blit(PLAYER, (PLAYER_RECT.x, PLAYER_RECT.y))
    pygame.draw.rect(WINDOW,(0,0,0),pygame.Rect(7,29,22,14))
    pygame.draw.rect(WINDOW,(255,255,255),pygame.Rect(8,30,20,12))
    WINDOW.blit(myfont.render(str(int(killcount / 2)), False,(0,0,0) ), (10,30))
    WINDOW_SIZE=(WINDOW.get_width(),WINDOW.get_height())
    pygame.display.update()
    clock.tick(60)