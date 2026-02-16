import pygame, sys, os, random
from pygame.locals import *
from settings import *

window = pygame.display.set_mode((hSize,vSize), 0, 24)

class Card(pygame.sprite.Sprite):
    def __init__(self,cardImg,slot,tempCard):
        super().__init__()
        self.image = cardImg
        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect()
        self.slot = slot
        if slot <= 12:
            col = self.slot % 3 
            row = self.slot % 4
            self.rect.centerx = hSize//2 - 1.5*CARDSPACING + CARDSPACING * row
            self.rect.centery = vSize//2 - CARDSPACING + CARDSPACING * col
        elif slot <= 15:
            slot = slot - 12
            self.rect.centerx =  hSize//2 - 1.5*CARDSPACING + CARDSPACING * 4
            self.rect.centery = vSize//2 - CARDSPACING + CARDSPACING * (slot - 1)
        elif slot <= 18:
            slot = slot - 15
            self.rect.centerx =  hSize//2 - 1.5*CARDSPACING + CARDSPACING * -1
            self.rect.centery = vSize//2 - CARDSPACING + CARDSPACING * (slot - 1)


        self.value = tempCard[:4]
        self.selected = False

class Add(pygame.sprite.Sprite):
    def __init__(self,addImg):
        super().__init__()
        self.image = addImg
        self.image = pygame.transform.scale_by(self.image, 3)
        self.rect = self.image.get_rect()
        self.rect.topright = (hSize - 10, 10 )

def main():
    allSprites = pygame.sprite.Group()
    buttons = pygame.sprite.Group()
    
    score = 0
    setText = font.render("Set!", True, (255,255,255))

    cantAdd = font.render("Cannot Add More Cards", True, (255,255,255))

    freeSlots = list(range(12))

    addImage = pygame.image.load("addCard.png").convert_alpha()
    addCard = Add(addImage)
    buttons.add(addCard)

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
    cantAddCheck =  False
    addThree = False
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
                for button in buttons:
                    if button.rect.collidepoint(mousePosition):
                        addThree = True

        
        for card in allSprites:
            if card.selected:
                outline = card.rect.inflate(10,10)
                pygame.draw.rect(window,(0,0,0), outline, 0)

        if len(hand) == 3:
            for i in range(4):
                if (hand[0].value[i] == hand[1].value[i] == hand[2].value[i]) or ((hand[0].value[i] != hand[1].value[i]) and (hand[0].value[i] != hand[2].value[i]) and (hand[1].value[i] != hand[2].value[i])): #(hand[0].value[i] != hand[1].value[i] != hand[2].value[i]):
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
                if card.slot < 12:
                    freeSlots.append(card.slot)
            hand.clear()

        if setTextCheck == True:
            window.blit(setText, (hSize/2 - 10, 75))
            if duration < time - winTime:
                setTextCheck = False

        if cantAddCheck == True:
            window.blit(cantAdd, (hSize/2 - 175, vSize - 100))
            if duration < time - buttonTime:
                cantAddCheck = False
        
        if len(freeSlots) > 0:
            for i in range(len(freeSlots)):
                tempCard = random.choice(deck)
                cardImage = pygame.image.load("deck/" + tempCard).convert_alpha()
                slot = freeSlots[0]
                freeSlots.pop(0)
                card = Card(cardImage, slot, tempCard)
                allSprites.add(card)
                deck.remove(tempCard)
        if addThree == True:
            buttonTime = pygame.time.get_ticks()
            addThree = False
            if len(allSprites) <= 12:
                freeSlots = freeSlots + [13, 14, 15]
                addThree = False
            elif len(allSprites) <= 15:
                freeSlots = freeSlots + [16, 17, 18]
            elif len(allSprites) > 15:
                cantAddCheck = True

        scoreText = font.render("Sets: " + str(score), True, (255,255,255))

        cardsLeft = len(deck)
        leftText = font.render("Cards Remaining: " + str(cardsLeft), True, (255,255,255)) 

        allSprites.draw(window)
        buttons.draw(window)
        window.blit(scoreText, (10,50))
        window.blit(leftText, (10, 10))
        pygame.display.update()

if __name__ == "__main__":
    main()
