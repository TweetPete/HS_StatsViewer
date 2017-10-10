import xml.etree.ElementTree as ET
from collections import defaultdict
import matplotlib.pyplot as plt
import os

def leaders(xs, top=10):
    counts = defaultdict(int)
    for x in xs:
        counts[x] += 1
    return sorted(counts.items(), reverse=True, key=lambda tup: tup[1])[:top]

def getOpponentList(): #encoded because of cyrillic letters
    OpponentList = [opponent.text.encode('utf8') for opponent in root.iter('OpponentName')\
                     if opponent.text is not None]
    for item in leaders(OpponentList, 10):
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
    deckList = [deck.text for deck in root.iter('DeckName') if 'Arena' not in deck.text]
    #print(set(deckList))
    return set(deckList)

def getBestDeck():
    bestDeck = 'None'
    bestRate = 0
    for Deck in getDeckList():
        winList = [game.find('Result').text for game in root.iter('Game') \
                   if game.find('DeckName').text == Deck]
        winCount = winList.count('Win')
        winNr = len(winList)
        rate = winCount/winNr*100
        
        if rate > bestRate and winNr >10:
            bestDeck = Deck
            bestRate = rate
    print('\nBest Deck: %s\nWinrate: %.2f' % (bestDeck, bestRate))

def getDeckStats(DeckName = 'Kel\'step'):
    winList = [game.find('Result').text for game in root.iter('Game') \
               if game.find('DeckName').text == DeckName]
    winCount = winList.count('Win')
    
    print('\nDeck Name: %s' % DeckName)
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
    
def getMatchesByRank(mode = 'Wild', season = '47'): 
    gameList = [game.find('Rank').text for game in root.iter('Game') if game.find('GameMode').text == 'Ranked' \
     and game.find('Format').text == mode and game.find('RankedSeasonId').text == season]
    return leaders(gameList, 26)

def plotRanks(array):
    x = [int(pair[0]) for pair in array]
    y = [int(pair[1]) for pair in array]        
    plt.bar(x,y)
    plt.gca().invert_xaxis()
    plt.show()
            
#tree = ET.parse('xml/DeckStats.xml')
roamingpath = os.getenv('AppData')
tree = ET.parse(roamingpath + '/HearthstoneDeckTracker/DeckStats.xml')
root = tree.getroot()
#getOpponentList()    
getOpponentStats()
#getDeckStats('Kel\'step')
#print(getDeckList())
#getBestDeck()
#plotRanks(getMatchesByRank('Wild','47'))