# RocketLeagueTicker
This project displays real-time Rocket League stat updates via a 16x2 LCD screen attached to a Raspberry Pi 3 Model B. Player information is stored in a DynamoDB database. These players are then looked up using a Rocket League API and by parsing the [Rocket League Tracking Network website](https://rocketleague.tracker.network/). Relevant information is then passed to the LCD screen for the user to enjoy.

## Getting Started
These instructions will help you to set up the Rocket League Ticker. Additionally, the required hardware and software will be listed here.

### Hardware
For this project, a Raspberry Pi Model B was used. Other models can work as well, though the GPIO numbering may be different. In addition to the Raspberry Pi, you will also need:
  1. 6 220 Ohm resistors
  2. 6 LED's
  3. Male:Female jumper wires
  4. Male:Male jumper wires
  5. 16x2 LCD panel
  6. 1 Potentiometer
  7. 2 Push buttons

### Software
There are a number of steps to setting up the required software and getting the required packages. These instructions assume that Python 2.7.9 is already installed on the Raspberry Pi.

#### DynamoDB
DynamoDB was utilized to store users names, screen names, and consoles. Register for an AWS account at [aws.amazon.com](aws.amazon.com). After creating an account, find the DynamoDB service and create a new table. Name the table `RocketLeagueTicker`, and enter `name` for the partition key (key should be type `String`). Create the table. Next, create an IAM role that allows full read/write access to the DynamoDB table, and generate an access key and secret key. Store these somewhere safe as you won't be able to see them again.

#### BeautifulSoup
BeautifulSoup is used to parse HTML found in the [Rocket League Tracking Network](https://rocketleague.tracker.network/). Values found here are used to calculate points required to change division. To install open a terminal on the Raspberry Pi and enter:
```
sudo apt-get install python-bs4
```
More information on BeautifulSoup can be found [here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)

#### Adafruit Python CharLCD
This library was used to communicate with the LCD panel. Installation instructions can be found [here](https://github.com/adafruit/Adafruit_Python_CharLCD)

### Setup
A Fritzing file can be found inside the repository that describes how to wire the LCD and Raspberry Pi. The setup is also shown below:
![alt text][schematic]

[schematic]: https://github.com/ajcav2/RocketLeagueTicker/blob/master/RocketLeagueTickerSchematic.PNG "Ticker Schematic"


## Additional Files
Download this repository onto a Raspberry Pi. Navigate inside the directory, and create two new files:
```
DDBCert.py
APIKey.py
```
Inside the DDBCert file, you must insert the access key and secret key from the IAM role created earlier. The file should look like:
```
accessKey = "sdff423fjsdf34w3f"
secretKey = "324bsdf8hk34h8shjhkfow348h/34f"
```
Inside the APIKey file, you must insert a rocket league API key. Instructions to obtain a key can be found [here](http://documentation.rocketleaguestats.com/#introduction). The file should look like:
```
key = "2345ndsfjkdsfhj34"
```
## First Run
Before running the program for the first time, you should add at least one player to the DynamoDB database. You can do this manually from the AWS website, or you can do it in the Raspberry Pi by navigating to the RocketLeagueTicker directory and running:
```
./addPlayer.sh
```
This shell script will call a python script to ask questions about the new user, and add them to the DynamoDB database when finished. In addition, there is also the option to remove a player `./removePlayer.sh` or to list the players you are currently streaming information about `./printPlayers.sh`. 

To start the software, run the main script:
```nohup sudo python main.py &```

## Features
This section details more specific features about the Rocket League Ticker

### LCD Screen
The program will display information about the players on the LCD screen. The format is as follows:
```
playerName                                         TierDivision       Points

gamesToDivisionDown|gamesToDivisionUp     pointsToDivisionDown|pointsToDivisionUp
```

For example, player Shelby has 570 points in singles. Shelby is ranked as Silver III Division III. Shelby would need to lose 8 points to be demoted to the previous division, and Shelby needs 13 points to move up one division. This corresponds to losing ~1 game to move down a division, or winning ~2 games to move up a division. When Shelby's stats are shown on the LCD screen, they will appear as follows:
```
Shelby  S3D3  570
1|2          8|13
```
### LED's and Buttons
The LED's connected to the Raspberry pi serve to provide information to the user that would otherwise take up too much screen real estate. The LED's connected to pins 16, 20, 21, and 26 indicate which game mode the user is streaming information about (i.e. 2 LED's lit signify doubles information is streaming). To change game modes, the user can press the button connected to pin 35. The user should see a short message on the LCD to indicate the change in game mode, and should see a change in the number of lit LED's.

The other button, connected to Pin 33, can be pressed to retrieve more information about the player that is currently being displayed (i.e. number of goals, MVP's, etc.). 

The two extra LED's indicate when the program is making a request to the API, and when it is opening the Rocket League Tracking Network.

While the program is running, the user does not need to stop the program to add or remove players. The player list can be modified while the program is running by using the approproate shell script to add or remove players. The user can also SSH into the Raspberry Pi from their smartphone so as to never need to use an external monitor to add or remove players.

## Authors
Alex Cavanaugh -- ajcav2@gmail.com

## Acknowledgments
+ Mike, for building the Rocket League API and providing a key
+ The creators of the Rocket League Tracking Network
+ Max Dribinsky, for helping parse API response
