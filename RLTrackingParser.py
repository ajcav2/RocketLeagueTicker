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
    if (gameMode == 1):
        horz = allTableInfo.split("Duel",1)[1]
        horz = horz.split("/tr",1)[0]
        pointsUpDown = re.findall(r'\~([^<]+)\<',horz)
    elif (gameMode == 2):
        horz = allTableInfo.split("Doubles",1)[1]
        horz = horz.split("/tr",1)[0]
        pointsUpDown = re.findall(r'\~([^<]+)\<',horz)
    elif (gameMode == 4):
        horz = allTableInfo.split("Solo Standard",1)[1]
        horz = horz.split("/tr",1)[0]
        pointsUpDown = re.findall(r'\~([^<]+)\<',horz)
    else:
        horz = allTableInfo.split("Ranked Standard",1)[1]
        horz = horz.split("/tr",1)[0]
        pointsUpDown = re.findall(r'\~([^<]+)\<',horz)

    if (len(pointsUpDown) == 2):
        pointsDown = pointsUpDown[0]
        pointsUp = pointsUpDown[1]
    else:
        pointsDown = 0
        pointsUp = 0

    return [pointsDown,pointsUp]
