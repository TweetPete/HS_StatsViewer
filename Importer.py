import xml.etree.ElementTree as ET
from collections import defaultdict

def leaders(xs, top=10):
    counts = defaultdict(int)
    for x in xs:
        counts[x] += 1
    return sorted(counts.items(), reverse=True, key=lambda tup: tup[1])[:top]

def getOpponentList(): #encoded because of cyrillic letters
    OpponentList = [opponent.text.encode('utf8') for opponent in root.iter('OpponentName')\
                     if opponent.text is not None]
    for item in leaders(OpponentList, 5):
        print('%s - (%i)' % (item[0], item[1]))

def getOpponentStats(OpponentName='MichaELSvent'):
    winList = [game.find('Result').text for game in root.iter('Game') \
               if game.find('OpponentName').text == OpponentName]
    winCount = winList.count('Win')
    
    print('Opponent: %s' % OpponentName)
    print('Your Wins: %i/%i' % (winCount, len(winList)))
    print('Percentage: %.2f' % (winCount/len(winList)*100))
    
    print('\nMOST PLAYED CLASS:')
    
    heroList = [game.find('OpponentHero').text for game in root.iter('Game') \
                if game.find('OpponentName').text == OpponentName]
    for hero in leaders(heroList,3):
        print('-%s' % (hero[0]))

def getDeckList():
    pass

def getBestDeck():
    pass

def getDeckStats(DeckName = 'Kel\'step'):
    winList = [game.find('Result').text for game in root.iter('Game') \
               if game.find('DeckName').text == DeckName]
    winCount = winList.count('Win')
    
    print('Deck Name: %s' % DeckName)
    print('Wins: %i/%i' % (winCount, len(winList)))
    print('Percentage: %.2f' % (winCount/len(winList)*100))
    
    print('\nMATCHUPS:')
    heroList = [game.find('OpponentHero').text for game in root.iter('Game') \
                if game.find('DeckName').text == DeckName]
    for hero in sorted(set(heroList)):
        heroResult = [game.find('Result').text for game in root.iter('Game') \
                     if game.find('DeckName').text == DeckName and game.find('OpponentHero').text == hero]
        winCount = heroResult.count('Win')
        print('%s - %.2f' % (hero, winCount/len(heroResult)*100))
    
    
tree = ET.parse('xml/DeckStats.xml')
root = tree.getroot()
#getOpponentList()    
#getOpponentStats()
getDeckStats()