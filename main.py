import time
import cv2
import torch
from Class_yolov5 import Detect
from ObjectDetection.utils.general import scale_coords
from config import *
from helpMethod import *
from BirdView import BirdView


if __name__ == '__main__':
    cap = cv2.VideoCapture(VIDEO_IN) 
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (width, height)
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    result = cv2.VideoWriter(VIDEO_OUT,fourcc, fps, (width,height))

    # init Bird view
    region = np.float32([REGION_P1, REGION_P2, [width, height], [0, height]])
    dst = np.float32([[0, 0], [width, 0], [width, 3*width], [0, 3*width]])
    BirdV = BirdView(region, dst, size, circle_mode=CIRCLE_MODE)

    # load model
    Det = Detect(WEIGHT, IMG_SIZE_YOLO, DEVICE)
    
    # load old points 
    points = loadPointPolygon(PATH_POINTS_POLYGON)
    
    
    detect, dis = False, False
    pre_time_alert = 0
    window_name="Warning"
    colors_p = colors_o = ""
    
    polygon_mode = False
    bird_view_mode = False
    while True:
        with torch.no_grad(): 
            ret,frame = cap.read()   
            if not ret:
                break
            if detect:             
                st = time.time()
                # Object detection with YOLO
                pred = Det.detect(frame ,conf_thres = CONFIDENT_THRES, iou_thres=IOU_THRES)
                if pred != torch.tensor([]) and list(pred[0]) != []:
                    # Handle bounding boxes
                    pred_rescale = scale_coords(Det.img_size_detect[2:], torch.tensor(pred[0]), frame.shape).round()
                    centerbottom = Det.get_foot_object(pred_rescale)[:,:2]
                    labels = pred[0].numpy()[:,5]
                    list_peo, list_baby, list_obj = split_object(centerbottom, labels)

                    # Check for danger with Bird view
                    if bird_view_mode:
                        isCollis, colors_p, colors_o = checkCollided2List(BirdV, list_peo, list_obj)
                        # Draw
                        draw_circle(frame, list_peo, PEOPLE_COLOR)
                        draw_circle(frame, list_obj, OBJECT_COLOR)
                        frame = BirdV.showObjs(frame, list_peo, colors_p)
                        frame = BirdV.showObjs(frame, list_obj, colors_o)
                    else: isCollis = False

                    # Check object in polygon
                    if polygon_mode:
                        if len(points) < 4:
                            points = setup_points(frame, window_name, PATH_POINTS_POLYGON)
                        inPolygon, colors_p  = isInPolygon(points, list_peo, colors_p)
                        frame = Det.draw_all_box(frame, pred)
                    else: inPolygon = False

                    # Alert
                    if (isCollis or inPolygon):
                        if time.time() - pre_time_alert  > TIME_WAITING_ALERT:
                            pre_time_alert = time.time()
                            alertDangerous(frame)
                            print("Dangerous!")
                        putText(frame, "Dangerous!", (10, 50), FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                print('time per frame: ',time.time()-st)


            event =  cv2.waitKey(1)
            if event== ord('q'):
                break
            elif event == ord('1'):
                detect = True
                bird_view_mode = not bird_view_mode
            elif event == ord('2'):
                detect = True
                polygon_mode = not polygon_mode
            elif event == ord('3'):
                points = setup_points(frame, window_name, PATH_POINTS_POLYGON)
            elif event == ord('4'):
                putText(frame, "Pause!", (int(width/2-50), int(height/2-10)), FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow(window_name, frame)  
                cv2.waitKey(-1)
            elif event == ord('5'):
                detect = False
                
            
            if bird_view_mode:
                frame = BirdV.showRegion(frame)
            if polygon_mode:
                frame = draw_polygon(frame, points)
            
            result.write(frame)
            cv2.imshow(window_name, frame)            
    # When everything done, release the capture
    cap.release()
    result.release()
    cv2.destroyAllWindows()


