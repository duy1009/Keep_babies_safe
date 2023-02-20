# YOLO
IMG_SIZE_YOLO = 640
CONFIDENT_THRES = 0.5
IOU_THRES = 0.5
DEVICE = 'cpu'
WEIGHT = r'.\data\dan_items\bestshow.pt'

# Alert
TIME_WAITING_ALERT = 30        # second
TOKEN = '5811380057:AAG9duwWycJIukxAFeJ98m01wJjgHQEg_2s'
CHAT_ID = '5923323553'
IMG_DG_PATH =r".\data\alert.png"

# Input and output video
VIDEO_IN = r'.\videos\file3.mp4'
VIDEO_OUT = r'.\video\Video_output\output.mp4'

# Points polygon
PATH_POINTS_POLYGON = r".\data\points.txt"

# Bird view
REGION_P1 = [300, 210]
REGION_P2 = [520, 210]
DISTANCE_OBJECT = 250   # Circle mode
POLYGON_OBJECT =[[-120,0],[0,-120],[120,0],[0,120]] # Shape mode
CIRCLE_MODE = False

# Object colors
COLOR1_DEFAULT = (255,255,0)
COLOR2_DEFAULT = (0,255,255)
DANGEROUS_COLOR = (0,0,255)
REGION_COLOR = (0, 0, 255)
PEOPLE_COLOR = (255,0,0)
BABY_COLOR = (0,255,0)
OBJECT_COLOR = (0,0,255)


