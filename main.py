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
    setText = font.render("Set!", True, (255,255,255))

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
    
    color = False
    number = False
    density = False
    shape = False

    hand = []

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
                        hand.append(pressed)
                        print(pressed)
                        break

        if len(hand) == 3:
            for i in range(4):
                if (hand[0][i] == hand[1][i] == hand[2][i]) or (hand[0][i] != hand[1][i] != hand[2][i]):
                    if i == 0:
                        color = True
                    elif i == 1:
                        number = True
                    elif i == 2:
                        density = True
                    elif i == 3:
                        shape = True
            print(color, number,density, shape)
        if color == True and number == True and density == True and shape == True:
            # currentTime = pygame.time.get_ticks()
            window.blit(setText, (hSize/2, 50))
            score += 1
            color = False
            number = False
            density = False
            shape = False
            hand = []

        scoreText = font.render("Number of Sets: " + str(score), True, (255,255,255))

        allSprites.draw(window)
        window.blit(scoreText, (10,10))
        pygame.display.update()

if __name__ == "__main__":
    main()
