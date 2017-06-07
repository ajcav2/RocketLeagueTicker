import subprocess
import json
import APIKey

def getResponse(screenName,console,gameMode):
    # Get console ID
    if (console == 'pc'):
        platform_id = 1
    elif (console == 'ps4'):
        platform_id = 2
    else:
        platform_id = 3

    # Call the API
    URL = "https://api.rocketleaguestats.com/v1/player?unique_id=" + screenName + "&platform_id=" + str(platform_id)
    proc = subprocess.Popen(['curl',URL,'-H',"Authorization: Bearer " + APIKey.key], stdout=subprocess.PIPE)

    # Get the return string
    result = ''
    for line in iter(proc.stdout.readline, ''):
        result = line
    print (result)

    # Return the string, converted to json format
    return (json.loads(result))

    
