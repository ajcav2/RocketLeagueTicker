import boto3
import DDBCert

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=DDBCert.accessKey,
                          aws_secret_access_key=DDBCert.secretKey,
                          region_name="us-west-2")

table = dynamodb.Table('RocketLeagueTicker')
ean = { "#n":"name", }


def addPlayer():
    global names

    # Get name of new player
    newPlayer = ''
    while len(newPlayer) < 1:
        newPlayer = raw_input('What is your name?: ')

    # Get console of new player
    newConsole = ''
    while ( newConsole != 'ps4' and newConsole != 'pc' and newConsole != 'xbox' ):
        newConsole = raw_input(newPlayer + ', what console do you play on? (ps4/pc/xbox): ')

    # Get screen name of new player
    newScreenName = ''
    while (len(newScreenName) < 1):
        newScreenName = raw_input('What is your ' + newConsole + ' screen name?: ')

    # Prompt user for confirmation
    answer = ''
    while (answer != 'y' and answer != 'n'):
        answer = raw_input('Would you like to save ' + newPlayer + 's screen name as ' + newScreenName + ' on ' + newConsole + '? (y/n): ')
    if (answer == 'y'):
        # Send information to DynamoDB
        table.put_item(
            Item={
                'name':newPlayer.lower(),
                'screenName':newScreenName,
                'console':newConsole
                }
            )
        print("Player " + newPlayer + " added.")
    print("Done.")


def removePlayer():
    global names
    
    # Get player name to remove
    nameToRemove = ''
    while (len(nameToRemove) < 1):
        nameToRemove = raw_input('Please enter a name to remove: ')

    # Prompt user for confirmation
    answer = ''
    while (answer != 'y' and answer != 'n'):
        answer = raw_input('Are you sure you would like to remove ' + nameToRemove + '? (y/n): ')
    if (answer == 'y'):
        # Send information to DynamoDB
        table.delete_item(
            Key={
                'name':nameToRemove.lower()
                }
            )
        print(nameToRemove + ' has been removed.')
    print("Done.")
    

def getPlayers():
    return table.scan(
        ProjectionExpression="#n",
        ExpressionAttributeNames=ean
        )
