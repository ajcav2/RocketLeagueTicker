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
        streak = re.findall(r'\:([^"]+)\"',horz)
    elif (gameMode == 4):
        horz = allTableInfo.split("Solo Standard",1)[1]
        horz = horz.split("/tr",1)[0]
        pointsUpDown = re.findall(r'\~([^<]+)\<',horz)
        streak = re.findall(r'\:([^"]+)\"',horz)
    else:
        horz = allTableInfo.split("Ranked Standard",1)[1]
        horz = horz.split("/tr",1)[0]
        pointsUpDown = re.findall(r'\~([^<]+)\<',horz)
        streak = re.findall(r'\:([^"]+)\"',horz)

    if ("Win Streak" in horz):
        streakUpDown = "^"
    else:
        streakUpDown = "v"
        
    if ("Streak" in horz):
        streakString = horz.split("Streak: ",1)[1]
        streak = streakString.split(" ",1)[0]
    else:
        streak = "-"

    streak = "".join(streak.splitlines())
    
        
    # If length == 2, both point values were found
    if (len(pointsUpDown) == 2):
        pointsDown = pointsUpDown[0]
        pointsUp = pointsUpDown[1]
    elif ("color:red" in horz and len(pointsUpDown) == 1): # Only points down was found
        pointsDown = pointsUpDown[0]
        pointsUp = 0
    elif ("color:green" in horz and len(pointsUpDown) == 1): # Only points up was found
        pointsUp = pointsUpDown[0]
        pointsDown = 0
    else: # No points were found for division changes
        pointsDown = 0
        pointsUp = 0

    return [pointsDown,pointsUp,streak,streakUpDown]
