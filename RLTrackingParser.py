from bs4 import BeautifulSoup
import urllib2
import math
import re

def getHTMLData(screenName,console,gameMode):
    # Get platform for URL
    if (console == 'ps4'):
        platform = 'ps'
    elif (console == 'pc'):
        platform = 'steam'
    else:
        platform = 'xbox'

    # Open URL with a fake agent to not be blocked    
    URL = 'https://rocketleague.tracker.network/profile/' + platform +'/' + screenName
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/5.0')]
    r = opener.open(URL)
    soup = BeautifulSoup(r)
    
    # Get a string that gives all HTML between 'tr' tags
    allTableInfo = str(soup.find_all("tr"))

    # Cut strings to find points up and points down in each playlist    
    horzSingles = allTableInfo.split("Duel",1)[1]
    horzSingles = horzSingles.split("/tr",1)[0]
    singlesPoints = re.findall(r'\~([^<]+)\<',horzSingles)

    horzDoubles = allTableInfo.split("Doubles",1)[1]
    horzDoubles = horzDoubles.split("/tr",1)[0]
    doublesPoints = re.findall(r'\~([^<]+)\<',horzDoubles)

    horzSoloStandard = allTableInfo.split("Solo Standard",1)[1]
    horzSoloStandard = horzSoloStandard.split("/tr",1)[0]
    soloStandardPoints = re.findall(r'\~([^<]+)\<',horzSoloStandard)

    horzStandard = allTableInfo.split("Ranked Standard",1)[1]
    horzStandard = horzStandard.split("/tr",1)[0]
    standardPoints = re.findall(r'\~([^<]+)\<',horzStandard)

    if (gameMode == 1):
        # Ensure that each entry has a value
        # (website sometimes misses entries)
        if (len(singlesPoints) == 2):
            pointsDown = singlesPoints[0]
            pointsUp = singlesPoints[1]
        else:
            pointsDown = 0
            pointsUp = 0
    elif (gameMode == 2):
        if (len(doublesPoints) == 2):
            pointsDown = doublesPoints[0]
            pointsUp = doublesPoints[1]
        else:
            pointsDown = 0
            pointsUp = 0
    elif (gameMode == 3):
        if (len(standardPoints) == 2):
            pointsDown = standardPoints[0]
            pointsUp = standardPoints[1]
        else:
            pointsDown = 0
            pointsUp = 0
    else:
        if (len(soloStandardPoints) == 2):
            pointsDown = soloStandardPoints[0]
            pointsUp = soloStandardPoints[1]
        else:
            pointsDown = 0
            pointsUp = 0

    return [pointsDown,pointsUp]
