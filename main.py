import pygame, sys, os, random
from pygame.locals import *
from settings import *

window = pygame.display.set_mode((hSize,vSize), 0, 24)

class Card(pygame.sprite.Sprite):
    def __init__(self,cardImg,slot,tempCard):
        super().__init__()
        self.image = cardImg
        self.image = pygame.transform.scale_by(self.image, 2)
        self.rect = self.image.get_rect()
        # cardWidth = self.image.get_width()
        # cardHeight = self.image.get_height()
        self.slot = slot
        col = self.slot % 3 
        row = self.slot % 4
        self.rect.centerx = hSize//2 - 1.5*CARDSPACING + CARDSPACING * row
        self.rect.centery = vSize//2 - CARDSPACING + CARDSPACING * col
        self.value = tempCard[:4]
        self.selected = False

def main():
    allSprites = pygame.sprite.Group()
    
    score = 0
    setText = font.render("Set!", True, (255,255,255))

    freeSlots = list(range(12))

    deck = os.listdir("/home/zeus/Projects/set/deck")
    for i in range(len(freeSlots)):
            tempCard = random.choice(deck)
            cardImage = pygame.image.load("deck/" + tempCard).convert_alpha()
            slot = freeSlots[0]
            freeSlots.pop(0)
            card = Card(cardImage, slot, tempCard)
            allSprites.add(card)
            deck.remove(tempCard)
    
    #While Loop Variables
    color = False
    number = False
    density = False
    shape = False
    setTextCheck = False
    winTime = 0
    duration = 1500
    
    hand = []

    clock = pygame.time.Clock()
    while True:
        window.fill(TABLE_RED)
        clock.tick(60)
        time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePosition = pygame.mouse.get_pos()
                for card in allSprites:
                    if card.rect.collidepoint(mousePosition):
                        if card not in hand:
                            hand.append(card)
                            card.selected = True
                            print(card.value)
                        break
        
        for card in allSprites:
            if card.selected:
                outline = card.rect.inflate(10,10)
                pygame.draw.rect(window,(0,0,0), outline, 0)

        if len(hand) == 3:
            for i in range(4):
                if (hand[0].value[i] == hand[1].value[i] == hand[2].value[i]) or (hand[0].value[i] != hand[1].value[i] != hand[2].value[i]):
                    if i == 0:
                        color = True
                    elif i == 1:
                        number = True
                    elif i == 2:
                        density = True
                    elif i == 3:
                        shape = True
                else:
                    hand = []
                    color = False
                    number = False
                    density = False
                    shape = False
                    for card in allSprites:
                        card.selected = False
                    break

        if color == True and number == True and density == True and shape == True:
            score += 1
            color = False
            number = False
            density = False
            shape = False
            setTextCheck = True
            winTime = pygame.time.get_ticks()
            for card in hand:
                card.kill()
                freeSlots.append(card.slot)
            hand.clear()

        if setTextCheck == True:
            window.blit(setText, (hSize/2, 50))
            if duration < time - winTime:
                setTextCheck = False
        
        if len(freeSlots) > 0:
            for i in range(len(freeSlots)):
                tempCard = random.choice(deck)
                cardImage = pygame.image.load("deck/" + tempCard).convert_alpha()
                slot = freeSlots[0]
                freeSlots.pop(0)
                card = Card(cardImage, slot, tempCard)
                allSprites.add(card)
                deck.remove(tempCard)

        scoreText = font.render("Number of Sets: " + str(score), True, (255,255,255))

        allSprites.draw(window)
        window.blit(scoreText, (10,10))
        pygame.display.update()

if __name__ == "__main__":
    main()
