import pygame
import random
import time

pygame.init()
largeur, hauteur = 800, 600
ecran = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu du Raton Laveur")

blanc = (255, 255, 255)
noir = (0, 0, 0)

raton_laveur = pygame.image.load("racoon.png")
raton_laveur = pygame.transform.scale(raton_laveur, (128, 128)) 
piece = pygame.image.load("gold.png")
piece = pygame.transform.scale(piece, (32, 32)) 
bombe = pygame.image.load("bomb.png")
bombe = pygame.transform.scale(bombe, (32, 32))  
raton_x = largeur // 2
raton_y = hauteur - 160  
objets = []

score = 0
game_over = False
game_over_time = 0

font = pygame.font.Font(None, 36)

def ajouter_objet():
    objet_x = random.randint(64, largeur - 64)
    objet_y = 0
    objet_image = piece if random.random() < 0.8 else bombe
    objet_vitesse = random.randint(2, 6)
    objets.append((objet_x, objet_y, objet_image, objet_vitesse))

for _ in range(10):
    ajouter_objet()

def collision(rect1, rect2):
    margin = 10 
    return (rect1.left + margin < rect2.right - margin and
            rect1.right - margin > rect2.left + margin and
            rect1.top < rect2.bottom and
            rect1.bottom > rect2.top)

clock = pygame.time.Clock()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and raton_x > 0:
        raton_x -= 15
    if keys[pygame.K_RIGHT] and raton_x < largeur - 128:
        raton_x += 15

    for i in range(len(objets)):
        objet_x, objet_y, objet_image, objet_vitesse = objets[i]
        objets[i] = (objet_x, objet_y + objet_vitesse, objet_image, objet_vitesse)
        if objet_y > hauteur:
            objets.remove(objets[i])
            ajouter_objet()

    ecran.fill(blanc)
    ecran.blit(raton_laveur, (raton_x, raton_y))
    raton_rect = pygame.Rect(raton_x, raton_y, 128, 128)

    for objet_x, objet_y, image, _ in objets:
        objet_rect = pygame.Rect(objet_x, objet_y, 32, 32)
        if collision(raton_rect, objet_rect):
            if image == piece:
                score += 1
            else:
                game_over_text = font.render("GAME OVER", True, noir)
                ecran.blit(game_over_text, (largeur // 2 - 100, hauteur // 2 - 50))
                pygame.display.update()
                game_over_time = time.time()
                game_over = True
            objets.remove((objet_x, objet_y, image, _))

        ecran.blit(image, (objet_x, objet_y))

    score_text = font.render(f"Score: {score}", True, noir)
    ecran.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)

if game_over_time > 0:
    while time.time() - game_over_time < 30:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

pygame.quit()
