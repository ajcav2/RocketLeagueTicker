# RocketLeagueTicker
This project aims to give real-time updates on Rocket League user stats. The project user can add/remove players that they wish to stream stats about from a DynamoDB database using a Raspberry Pi. The project utilizes and API and HTML parsing to obtain stats for users, then displays them on a 16x2 LCD screen.

## Getting Started
These instructions will get you started using the Rocket League Ticker. Additionally, the required hardware and software will be listed here.

### Hardware
For this project, a Raspberry Pi Model B was used. Other models can work as well, though the GPIO numbering may be different. In addition to the Raspberry Pi, you will also need:
  1.) 6 220 Ohm resistors
  2.) 6 LED's
  3.) Male:Female jumper wires
  4.) Male:Male jumper wires
  5.) 16x2 LCD panel
  6.) 1 Potentiometer
  7.) 2 Push buttons

### Software
There are a number of steps to setting up the required software and getting the required packages. This project assumes Python 2.7.9 is already installed on the Raspberry Pi.

#### DynamoDB
DynamoDB was utilized to store users names, screen names, and consoles. Register for an AWS account at [aws.amazon.com](aws.amazon.com). After creating an account, find the DynamoDB service and create a new table. Name the table "RocketLeagueTicker", and enter "name" for the partition key (key should be type String). Create the table. Next, create an IAM role that allows full read/write access to the DynamoDB table, and generate an access key and secret key. Store these somewhere safe as you won't be able to see them again.

#### BeautifulSoup
BeautifulSoup is used to parse HTML found in the [Rocket League Tracking Network] (https://rocketleague.tracker.network/). Values found here are used to calculate points required to change division. To install open a terminal on the Raspberry Pi and enter:
```
sudo apt-get install python-bs4
```
More information on BeautifulSoup can be found [here](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)

#### Adafruit Python CharLCD
This library was used to communicate with the LCD panel. Installation instructions can be found [here] (https://github.com/adafruit/Adafruit_Python_CharLCD)

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
Inside the APIKey file, you must insert a rocket league API key. Instructions to obtain a key can be found [here] (http://documentation.rocketleaguestats.com/#introduction). The file should look like:
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
The program will display information about the players on the LCD screen. The format is as follows:
```
playerName                                         TierDivision      Points
gamesToDivisionDown|gamesToDivisionUp     pointsToDivisionDown|pointsToDivisionUp
```
In addition, there are two buttons connected to the Raspberry Pi. The button connected to Pin 35 can be pressed to change the game mode. After pressing it, the LED's should indicate a change in game mode, along with a brief message on the LCD screen. 

The other button, connected to Pin 33, can be pressed to retrieve more information about the player that is currently being displayed (i.e. number of goals, MVP's, etc.). 

The two extra LED's indicate when the program is making a request to the API, and when it is opening the Rocket League Tracking Network. 

## Authors
Alex Cavanaugh -- ajcav2@gmail.com

## Acknowledgments
+ Mike, for building the Rocket League API and providing a key
+ The creators of the Rocket League Tracking Network
+ Max Dribinsky, for helping parse API response
