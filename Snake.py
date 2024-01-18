import pygame
from sys import exit
from random import randint

add_pts, pts = 0, 0

ssq = 10
X0, Y0 = 100, 100
mx , my = 24 , 16

X1, Y1 = ssq*mx, ssq*my

fps = 10

map = []
level = None

lv = 1
mode = ''
path_hs = ''
highscore = 0

class Snake:
    def __init__(self,cx = mx//2,cy = my//2):
        """
            can have value 1,-1, and 0 in coordenates
            uv is a unitary vector
            define direction
        """
        self.length = 1
        self.coord =  (cx,cy)
        self.body = [self.rect(cx,cy)]
        self.head = self.body[0]
        self.uv = (1,0)

    def changeDirection(self,u,v):
        if ((u+self.uv[0],v+self.uv[1])!=(0,0)):
            self.uv = (u,v)
            
    def rect(self,x,y):
        return pygame.Rect((X0+x*ssq,Y0+y*ssq,ssq,ssq))

    def move(self):
        def sum(v1,v2):
            return ((v1[0]+v2[0])%mx,(v1[1]+v2[1])%my)  
        self.coord = sum(self.coord,self.uv)
        self.head = self.rect(self.coord[0],self.coord[1])
        self.body.append(self.head)
        self.tail = self.body.pop(0)

    def checkColSnake(self):
        for i in range(0,self.length-1):
            if pygame.Rect.colliderect(self.head,self.body[i]):
                return True
        return False

    def checkColFood(self,food):
        global pts, add_pts
        if pygame.Rect.colliderect(self.body[self.length-1],food.rect):
            food.new()
            self.length += 1
            self.body.insert(0,self.tail)
            pygame.mixer.Sound('sounds/food.mp3').play()
            pts += add_pts
            
    def checkColBlock(self):
        for i in range(0,my):
            for j in range(0,mx):
                if level.isBlock(self.coord[0],self.coord[1]):
                    return True
        return False
        
    def youLose(self):
        return (self.checkColBlock() or self.checkColSnake())
        
    def canSpawn(self,food):
        for i in self.body:
            if pygame.Rect.colliderect(i,food):
                return False
        return True
        


class Food:
    def __init__(self,snake):
        self.snake = snake
        self.new()

    def new(self):
        while True:
            rx = randint(0,mx-1)
            ry = randint(0,my-1)
            if level.isBlock(rx,ry):
                continue
            r = pygame.Rect(X0+rx*ssq,Y0+ry*ssq,ssq,ssq)
            if self.snake.canSpawn(r):
                break
        self.rect = r
        
class Level:
    global map
    def __init__(self):
        fp = open('levels/level'+str(lv)+'.lv','r')
        self.map = fp.readlines()
        fp.close()
                    
    def rect(self,i,j):
        return pygame.Rect(X0+ssq*j,Y0+ssq*i,ssq,ssq)
        
    def isBlock(self,i,j):
        return self.map[j][i]=='#'
                    
               


class Game:
    def __init__(self, md, colors, l, vel):
        global add_pts, pts, fps, level, path_hs, highscore, lv, mode
        
        self.colors = colors
        
        self.dim = (600,600)
        
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.dim)
        pygame. display.set_caption("SNAKE")
        pygame.display.flip()

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        
        fps = vel
        lv = l
        mode = md
        
        path_hs = 'highscore/'+mode+'/level'+str(lv)+".num"
        highscore = ((((open(path_hs,'r+')).readlines())[0]).split('\n'))[0]
        
        add_pts = fps
        pts = 0
        level = Level()
        self.snake=Snake()
        self.food = Food(self.snake)

        self.start()

    def start(self):
        global pts

        
        on = True
        lose = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit(lose)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.snake.changeDirection(0,1)
                    elif event.key == pygame.K_UP:
                        self.snake.changeDirection(0,-1)
                    elif event.key == pygame.K_LEFT:
                        self.snake.changeDirection(-1,0)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.changeDirection(1,0)
                    elif event.key == pygame.K_p:
                        on = not on
                    elif event.key == pygame.K_q:
                        self.quit(lose)
            if on:
                self.snake.move()
                self.snake.checkColFood(self.food)
                if self.snake.youLose():
                    pygame.mixer.Sound('sounds/game-over.mp3').play()
                    on = False
                    lose = True
                    self.updateHighscore()
                    continue
                self.draw()
                self.clock.tick(fps)
            elif lose:
                self.draw_game_over()
        
        
    def updateHighscore(self):
        fp = open(path_hs,'r+')
        hs = fp.readlines()
        fp.close()
        hs.append(str(pts)+'\n')
        for i in range(len(hs)):
            hs[i] = (hs[i].split('\n'))[0]
        hs.sort(reverse=True)
        hs = hs[0:10]
        for i in range(len(hs)):
            hs[i] = str(hs[i])+'\n'
        fp = open(path_hs,'w')
        fp.writelines(hs)
        fp.close()
        
    def quit(self,lose):
        if not lose:
            self.updateHighscore()
        pygame.quit()
        exit()

    def draw(self):
        
        self.screen.fill(self.colors['void'])
        
        border = pygame.Rect(X0-ssq,Y0-ssq,X1+2*ssq,Y1+2*ssq)
        pygame.draw.rect(self.screen,self.colors['bord'],border,ssq)
        
        field = pygame.Rect(X0,Y0,X1,Y1)
        pygame.draw.rect(self.screen,self.colors['field'],field)
        
        for i in range(0,mx):
            for j in range(0,my):
                r = pygame.Rect(X0+ssq*i,Y0+ssq*j,ssq,ssq)
                pygame.draw.rect(self.screen,(255,255,255),r,1)
        
        pygame.draw.rect(self.screen,self.colors['food'],self.food.rect)
        pygame.draw.rect(self.screen,self.colors['shape_food'],self.food.rect,1)
        
        for i in range(0,my):
            for j in range(0,mx):
                if level.isBlock(j,i):
                    r = level.rect(i,j)
                    pygame.draw.rect(self.screen,self.colors['block'],r,0)
                    pygame.draw.rect(self.screen,self.colors['shape_block'],r,1)
        
        for i in self.snake.body:
            pygame.draw.rect(self.screen,self.colors['snake'],i,0)
            pygame.draw.rect(self.screen,self.colors['shape_snake'],i,1)

        text_score = self.font.render('SCORE : '+str(pts), True, self.colors['text'])
        text_high = self.font.render('HIGHSCORE : '+str(highscore), True,self.colors['text'])
        text_level = self.font.render('Level : '+str(lv), True, self.colors['text'])
        text_vel = self.font.render('Velocity : '+str(fps), True,self.colors['text'])
        text_mode = self.font.render('Mode : '+str(mode), True, self.colors['text'])
        
        c = pygame.time.get_ticks()
        
        text_time = self.font.render('Time : '+str(int(c/1000)),True,self.colors['text'])
        
        self.screen.blit(text_high, (0,0))
        self.screen.blit(text_score, (400,0))
        self.screen.blit(text_level, (0,500))
        self.screen.blit(text_vel, (400,500))
        self.screen.blit(text_mode, (0,550))
        self.screen.blit(text_time, (400,550))
            
        pygame.display.update()

    def draw_game_over(self):
        self.screen.fill((255,255,255))
        text = self.font.render('GAME OVER', True, self.colors['text'])
        text_score = self.font.render('SCORE : '+str(pts), True, self.colors['text'])
        rect = text.get_rect(center=(self.dim[0]//2, self.dim[1]//2))
        self.screen.blit(text, rect)
        self.screen.blit(text_score, (0,0))
            
        pygame.display.update()
