from cv2 import putText,setMouseCallback,waitKey, polylines, line, imshow, imwrite, circle, resize, FONT_HERSHEY_SIMPLEX, EVENT_LBUTTONDOWN
import numpy as np
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import telegram
from config import *
import os
from threading import Thread
def draw_circle(image, pos, color = (0,0,255)):
    for i in pos:
        circle(image,(int(i[0]),int(i[1])),4, color, 5)

def isInside(points, centroid):
    polygon = Polygon(points)
    centroid = Point(centroid)
    return polygon.contains(centroid)


def send_warning(photo_path=IMG_DG_PATH):
    try:
        bot = telegram.Bot(token=TOKEN)
        bot.send_photo(chat_id= CHAT_ID,photo=open(photo_path, "rb"), caption="Baby Dangerous!!") 
        print("Send Success!")
    except Exception as ex:
        print("Can not send warning! ", ex)

def alertDangerous(img):
    imwrite(IMG_DG_PATH, resize(img, dsize=(920,640), fx=0.2, fy=0.2))
    thread = Thread(target=send_warning(IMG_DG_PATH))
    thread.start()
    return img

def split_object(centerbottom, labels):
    
    list_peo = []
    list_baby = []
    list_obj = []
    # classification people and objects into list_peo and list_obj
    for j in range(labels.shape[0]):
        pos = [int(centerbottom[j][0]),int(centerbottom[j][1])]
        if(int(labels[j]) ==4):
            list_peo.append(pos)
            # if Det.sInside(points,center_peo):
            #     frame = Det.alert(frame)
        elif(int(labels[j]) ==6):
            list_baby.append(pos)
        else:
            list_obj.append(pos)
    return list_peo, list_baby, list_obj

def writePointPolygon(path, points):
    data = ""
    for i in points:
        data+= f"{i[0]} {i[1]}\n"
    f = open(path, "w")
    f.write(data)
    f.close()
def loadPointPolygon(path):
    points = []
    if os.path.isfile(path):
        f=open(path, "r")
        data = f.read().split("\n")[:-1]
        f.close()
        for i in data:
            value = i.split(" ")
            points.append([int(value[0]), int(value[1])])
    return points


def handle_left_click(event, x, y,flags, points):
    if event == EVENT_LBUTTONDOWN:
        points.append([x, y])

def setup_points(img_bg, window_name, path_save):
    points = []
    border = np.ones(((55,410,3)),dtype=np.uint8)*255
    x_ofs = 200
    y_ofs = 10
    img_bg[y_ofs:y_ofs+border.shape[0], x_ofs:x_ofs+border.shape[1]] = border
    while True:
        setMouseCallback(window_name, handle_left_click, points)
        if waitKey(1) == ord("q"):
            break
        putText(img_bg, "Click left mouse to draw polygon (least 4 points).", (x_ofs+5, y_ofs+20), FONT_HERSHEY_SIMPLEX, 0.5, (105, 155, 0), 2)
        putText(img_bg, "Press \"q\" to save points and continue", (x_ofs+5, y_ofs+40), FONT_HERSHEY_SIMPLEX, 0.5, (105, 155, 0), 2)
        for point in points:
            img_bg = circle( img_bg, (point[0], point[1]), 5, (0,0,255), -1)
        img_bg = polylines(img_bg, [np.int32(points)], False, (255,0, 0), thickness=2)
        imshow(window_name, img_bg)
    writePointPolygon(path_save, points)
    return points

def draw_polygon (frame, points):
    for point in points:
        frame = circle( frame, (point[0], point[1]), 5, (0,0,255), -1)
    frame = polylines(frame, [np.int32(points)], False, (255,0, 0), thickness=2)
    if(len(points) > 2):
        frame = line(frame, tuple(points[0]), tuple(points[-1]),(255,0, 0), thickness=2)
    return frame

def distance(point1, point2):
    '''Calculate usual distance.'''
    x1, y1 = point1
    x2, y2 = point2
    return np.linalg.norm([x1 - x2, y1 - y2])

def createListColors(length, color):
    colors = []
    for i in range(length):
        colors.append(color)
    return colors

def checkCollided2List(BirdV, list1, list2, colors1="", colors2=""):
    if colors1 == "":
        colors1 = createListColors(len(list1), COLOR1_DEFAULT)
    if colors2 == "":
        colors2 = createListColors(len(list2), COLOR2_DEFAULT)
    collided = False
    for i in range(len(list1)):
        for j in range(len(list2)):
            if BirdV.isCollided(list1[i], list2[j]):
                colors1[i] = DANGEROUS_COLOR
                colors2[j] = DANGEROUS_COLOR
                collided = True
    return collided, colors1, colors2
def isInPolygon(points, lists, colors = ""):
    if colors == "":
        colors = createListColors(len(lists), COLOR1_DEFAULT)
    isIn = False
    for i in range(len(lists)):
        if isInside(points, lists[i]):
            isIn = True
            colors[i] = DANGEROUS_COLOR
    return isIn, colors