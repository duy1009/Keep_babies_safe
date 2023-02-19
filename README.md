# Keep_Babies_Safe
### Description

### Requirements
python >= 3.8
#### Install libraries
```
cd Keep_Babies_Safe
pip install -r requirements.txt
```
### Setup
Go to `config.py` file to setup the parameters
#### YOLO
You can modify the parameters of Yolo and weight files path on `line 2-6` 
#### Alert your telegram
Step 1: Get token and chat ID by following instructions: https://www.siteguarding.com/en/how-to-get-telegram-bot-api-token?fbclid=IwAR2Z0Yz2c2rLCOi6eA8BxjS2KB7flyR3C2Yil0nvo2Rg29GUrbXcZLq6Xbc

Step 2: Replace token and chat ID into `line 10-11`
#### Deployment on webcam camera
Step 1: Connect the camera and PC run this App to the same LAN network.

Step 2: Change path at line 15 to stream RTSP

For example:
`VIDEO_IN = 'rtsp://kt:kt123@192.168.11.11:554/cam/realmonitor?channel=1&subtype=1'`
#### Bird view plane
The bird view plane is a plane made up of 4 points on the image, two of which are set by default to the lower left corner and the lower right corner. You can correct 2 points on `lines 22-23`

### How to run
Run the main.py file with the following command:

```
cd Keep_Babies_Safe
python main.py
```

*Functions are enabled/disabled by pressing the following key:

- Press "1" : Bird view mode

- Press "2" : Polygon mode

- Press "3" : Setup points for polygon mode

- Press "4" : Pause screen

- Press "5" : Turn off AI

- Press "q" : Exit this program
