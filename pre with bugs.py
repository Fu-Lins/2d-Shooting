
import pygame
pygame.init()

win = pygame.display.set_mode((1211,693))

pygame.display.set_caption("ilk oyun")

walkRight = [pygame.image.load('r1.png'), pygame.image.load('r2.png'), pygame.image.load('r3.png'), pygame.image.load('r4.png'), pygame.image.load('r5.png'), pygame.image.load('r6.png'), pygame.image.load('r7.png'), pygame.image.load('r8.png')]
walkLeft = [pygame.image.load('l1.png'), pygame.image.load('l2.png'), pygame.image.load('l3.png'), pygame.image.load('l4.png'), pygame.image.load('l5.png'), pygame.image.load('l6.png'), pygame.image.load('l7.png'), pygame.image.load('l8.png')]
#death = [pygame.image.load('death1.png'),pygame.image.load('death2.png'),pygame.image.load('death3.png'),pygame.image.load('death4.png'),pygame.image.load('death5.png'),pygame.image.load('death6.png'),pygame.image.load('death7.png'),pygame.image.load('death8.png'),pygame.image.load('death9.png'),pygame.image.load('death10.png'),pygame.image.load('death11.png'),pygame.image.load('death12.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.jpg')
shooting_animation = [pygame.image.load('shooting0.jpg'),pygame.image.load('shooting1.jpg'),pygame.image.load('shooting2.jpg'),pygame.image.load('shooting3.jpg'),pygame.image.load('shooting4.jpg')]
shooting_animation_left = [pygame.image.load('shootl1.png'),pygame.image.load('shootl2.png'),pygame.image.load('shootl3.png'),pygame.image.load('shootl4.png'),pygame.image.load('shootl5.png')]
bullet_animation = [pygame.image.load('bullet.png'),pygame.image.load('bullet.png'),pygame.image.load('bullet.png'),pygame.image.load('bullet.png'),pygame.image.load('bullet.png')]
bullet_anim_index = 0
pygame.display.update()
clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('bullet.mp3')
hitSound = pygame.mixer.Sound('hit.mp3')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 50, 52)
        self.visible = True
        self.shooting_animation = []  # Ateş etme animasyonunu saklamak için bir değişken ekleyin
        self.shooting_animation_left = []
        self.bullet_anim_index = 0  # Mermi animasyon çerçeve indeksi
        self.shooting = False  # Ateş etme durumu
        
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//4], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//4], (self.x,self.y))
                self.walkCount +=1
            else:
                if self.right:
                    win.blit(walkRight[0], (self.x, self.y))
                else:
                    win.blit(walkLeft[0], (self.x, self.y))
            self.hitbox = (self.x + 17, self.y + 11, 50, 52)
        if self.shooting_animation is not None:
            # Ateş etme animasyonunu kullan
            if self.bullet_anim_index < len(self.shooting_animation):
                win.blit(self.shooting_animation[self.bullet_anim_index], (self.x, self.y))
                self.bullet_anim_index += 1
            self.standing = False  # Ateş etme animasyonunu gösterirken standing'i False yapın
        else:
            if self.left:
                win.blit(walkLeft[self.walkCount // 4], (self.x, self.y))
            else:
                win.blit(walkRight[self.walkCount // 4], (self.x, self.y))
            self.walkCount += 1  # Her ateş etme işlemi sırasında çerçeve geçişini artır
        self.walkCount += 1  # Her çerçeve geçişini artır
        if self.bullet_anim_index == 0:  # Animasyon tamamlandığında, ateş etme durumunu sıfırla
            self.shooting = False

        #pygame.draw.rect(win, (255,0,0), goblin.hitbox,2)
    def shoot(self):
        if not self.shooting:  # Karakter ateş etmiyorsa, ateş etme animasyonunu başlat
            self.shooting = True

            # Karakter sağa bakıyorsa shooting_animation kullan, aksi takdirde shooting_animation_left'i kullan
            if self.right:
                self.shooting_animation = shooting_animation
            else:
                self.shooting_animation = shooting_animation_left

        if self.shooting_animation is not None:
            # Ateş etme animasyonunu kullan
            win.blit(self.shooting_animation[self.bullet_anim_index], (self.x, self.y))
            self.bullet_anim_index = (self.bullet_anim_index + 1) % len(self.shooting_animation)
        else:
            # Karakterin normal animasyonunu çiz
            if self.left:
                win.blit(walkLeft[self.walkCount // 4], (self.x, self.y))
            else:
                win.blit(walkRight[self.walkCount // 4], (self.x, self.y))
        self.walkCount += 1  # Her ateş etme işlemi sırasında çerçeve geçişini artır
        if self.bullet_anim_index == 0:  # Animasyon tamamlandığında, ateş etme durumunu sıfırla
            self.shooting = False

    def hit(goblin):
        goblin.isJump = True
        goblin.jumpCount = 10
        goblin.x = 100
        goblin.y = 500
        goblin.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 400)
        text = font1.render('-5', 1, (255,0,0))
        win.blit(text, (600 - (text.get_width()/2),50))
        #win.draw(death)
        pygame.display.update()
        i = 0
        while i < 200:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 201
                    pygame.quit()
                

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
        self.bullet_anim = 0
        self.bullet_animation = [pygame.image.load('bullet.png'), pygame.image.load('bullet.png'), pygame.image.load('bullet.png'), pygame.image.load('bullet.png'), pygame.image.load('bullet.png')]

    def draw(self,win):
        self.bullet_img = pygame.image.load('bullet.png')
        win.blit(self.bullet_img, (self.x - self.radius, self.y - self.radius))
        win.blit(self.bullet_animation[self.bullet_anim], (self.x - self.radius, self.y - self.radius))
        win.blit(self.bullet_animation[self.bullet_anim], (self.x - self.radius, self.y - self.radius))
        self.bullet_anim = (self.bullet_anim + 1) % len(self.bullet_animation)
        #pygame.draw.circle(win, self.color, (self.x,self.y), self.radius) eski mermi


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]


    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 90, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
        
    def draw(self,win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount += 2
            
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount += 2
            

            pygame.draw.rect(win, (135,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (255,8,8), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 50, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), goblin.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        if self.health == 0:
            self.visible = False
            goblin2.health = 10
            goblin2.hitbox = (goblin2.x + 50, goblin2.y + 2, 31, 57)
            goblin2.visible = True

        
class enemy2(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    
    def __init__(self2, x, y, width, height, end):
        self2.x = x
        self2.y = y
        self2.width = width
        self2.height = height
        self2.end = end
        self2.path = [self2.x, self2.end]
        self2.walkCount = 0         
        self2.vel = 3
        self2.hitbox = (self2.x + 90, self2.y + 2, 31, 57)
        self2.health = 10
        self2.visible = False
        
    def draw(self2,win):
        self2.move()
        if self2.visible:
            if self2.walkCount + 1 >= 33:
                self2.walkCount = 0

            if self2.vel > 0:
                win.blit(self2.walkRight[self2.walkCount //3], (self2.x, self2.y))
                self2.walkCount += 2
            else:
                win.blit(self2.walkLeft[self2.walkCount //3], (self2.x, self2.y))
                self2.walkCount += 2

            pygame.draw.rect(win, (135,0,0), (self2.hitbox[0], self2.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (255,8,8), (self2.hitbox[0], self2.hitbox[1] - 20, 50 - (5 * (10 - self2.health)), 10))
            self2.hitbox = (self2.x + 50, self2.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), goblin.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
    def hit(self):
        if self.health >0:
            self.health -= 1
            if self.health == 0:
                self.visible = False
                goblin.health = 10  # Goblin'in canını geri yükle
                goblin.hitbox = (goblin.x + 50, goblin.y + 2, 31, 57)  # Goblin'in hitboxunu ayarla
                goblin.visible = True 
        print('hit')



def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (1000, 10))
    man.draw(win)
    goblin.draw(win)
    if goblin.health == 0:
        goblin.visible = False
        goblin2.draw(win)
        goblin2.visible = True
    if goblin2.health == 0:
        goblin2.visible = False
        goblin.draw(win)
        goblin.visible = True
    for bullet in bullets:
        bullet.draw(win)
        
        
    
    pygame.display.update()


#mainloop
font = pygame.font.SysFont('comicsans', 30, True)
man = player(200, 500, 150,150)
goblin = enemy(0, 515, 150, 150, 1120)
goblin2 = enemy2(0, 515, 150, 150, 1120)

shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)
    
    if goblin.visible == True:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5
    
    if goblin2.visible == True:
         if man.hitbox[1] < goblin2.hitbox[1] + goblin2.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin2.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin2.hitbox[0] and man.hitbox[0] < goblin2.hitbox[0] + goblin2.hitbox[2]:
                man.hit()
                score -= 5

    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 8:
        shootLoop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    for bullet in bullets:
        
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                if goblin.visible:
                    hitSound.play()
                    goblin.hit()
                    score += 1
                    bullets.remove(bullet)
                   
                    #bullets.pop(bullets.remove(bullet))

        if bullet.y - bullet.radius < goblin2.hitbox[1] + goblin2.hitbox[3] and bullet.y + bullet.radius > goblin2.hitbox[1]:
            if bullet.x + bullet.radius > goblin2.hitbox[0] and bullet.x - bullet.radius < goblin2.hitbox[0] + goblin2.hitbox[2]:
                if goblin2.visible:
                    hitSound.play()
                    goblin2.hit()
                    score += 1
                    bullets.remove(bullet)

            if 0 < bullet.x < 1211:  # mermiyi ekrandan çıkınca silme
                bullet.x += bullet.vel
            else:
                bullets.remove(bullet)
                    
            

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        man.shoot()
        if man.left:
            facing = -1
            
        else:
            facing = 1
            
        if len(bullets) > 0:
            for bullet in bullets:
                # Mermi animasyonunu her mermi için çiz
                
                win.blit(bullet_animation[bullet_anim_index], (bullet.x - bullet.radius, bullet.y - bullet.radius))
                bullet_anim_index = (bullet_anim_index + 1) % len(bullet_animation)
        if len(bullets) < 5:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 9, (0, 0, 0), facing))
        # Mermi animasyonunu çerçevesini göster
            

        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 1170 - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()