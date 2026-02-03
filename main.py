import pygame, sys, os, random
from pygame.locals import *
from settings import *

window = pygame.display.set_mode((hSize,vSize), 0, 24)

class Card(pygame.sprite.Sprite):
    def __init__(self,cardImg,col,row,tempCard):
        super().__init__()
        self.image = cardImg
        self.image = pygame.transform.scale_by(self.image, 2)
        self.rect = self.image.get_rect()
        cardWidth = self.image.get_width()
        cardHeight = self.image.get_height()
        # self.rect.centerx = hSize//2 - cardWidth + (cardWidth/2) * row
        # self.rect.centery = vSize//2 - cardHeight + (cardHeight/2) * col
        self.rect.centerx = hSize//2 - 200 + 100 * row
        self.rect.centery = vSize//2 - 200 + 100 * col
        self.value = tempCard[:4]
        # rowNum = row - 1
        # cardID = rowNum * 3 + col
        # filled = False

def main():
    allSprites = pygame.sprite.Group()
    
    score = 0
    scoreText = font.render("Number of Sets: " + str(score), True, (255,255,255))

    tableOfCards = []

    row = [1,2,3] # esnures the correct spacing using LOC variables in cards
    #column = [1,2,3]

    deck = os.listdir("/home/zeus/Projects/set/deck")
    for i in range(len(row)):
        count = 0
        for j in range(3):
            count += 1
            tempCard = random.choice(deck)
            cardImage = pygame.image.load("deck/" + tempCard).convert_alpha()
            tableOfCards.append(tempCard[:4])
            # cardImage = pygame.image.load("deck/p1fo.png").convert_alpha()
            card = Card(cardImage, row[i], count, tempCard)
            allSprites.add(card)
            deck.remove(tempCard)
    print(tableOfCards) # TEMPORARY USED TO CHECK THE CARDS
    clock = pygame.time.Clock()
    while True:
        window.fill(TABLE_RED)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                for card in allSprites:
                    if card.rect.collidepoint(mousePosition):
                        pressed = card.value
                        print(pressed)
                        break

        allSprites.draw(window)
        window.blit(scoreText, (10,10))
        pygame.display.update()

if __name__ == "__main__":
    main()
