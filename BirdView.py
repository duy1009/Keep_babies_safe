from cv2 import perspectiveTransform,circle, addWeighted, flip, warpPerspective, getPerspectiveTransform, polylines, putText,LINE_AA, INTER_NEAREST, WARP_INVERSE_MAP, FONT_HERSHEY_SIMPLEX
import numpy as np
from helpMethod import *

class BirdView:
    def __init__(self, region, dst, size_frame, d_collis):
        self.region = region
        self.dst = dst
        self.region1 = np.array(region, dtype=np.int32).reshape((-1, 1, 2))
        self.M= getPerspectiveTransform(self.region, self.dst)
        self.d_collis = d_collis
        self.size_frame = size_frame

    def convert_to_bird(self,centers, M):
        '''Apply the perpective to the bird's-eye view.'''
        centers = [perspectiveTransform(np.float32([[center]]), M) for center in centers.copy()]
        centers = [list(center[0, 0]) for center in centers.copy()]
        return centers

    def distance_bv(self, img_pos_1, img_pos_2):
        bv_pos1 = perspectiveTransform(np.float32([[img_pos_1]]), self.M)[0][0]
        bv_pos2 = perspectiveTransform(np.float32([[img_pos_2]]), self.M)[0][0]
        return distance(bv_pos1, bv_pos2)

    def isCollided(self, img_pos_1, img_pos_2):
        return self.distance_bv(img_pos_1, img_pos_2) < self.d_collis
    
    def showObj(self, frame, point, color, d = -1):
        if d<0:
            d = self.d_collis
        x, y = perspectiveTransform(np.float32([[point]]), self.M)[0][0]

        overlay = np.zeros((5*self.size_frame[0], 4*self.size_frame[0], 3), np.uint8)
        if x >= int(d/2+15/2):
            overlay = circle(overlay, (x, y), int(d/2),
                                color, 15, lineType=LINE_AA)
        overlay = warpPerspective(overlay, self.M, self.size_frame,
                                    INTER_NEAREST, WARP_INVERSE_MAP)
        return addWeighted(frame, 1, overlay, 1, 0)
        
    def showObjs(self, frame, points, colors):
        for i in range(len(points)):
            frame = self.showObj(frame, points[i], colors[i])
        return frame

    def showRegion(self, frame, color = REGION_COLOR):
        return polylines(frame.copy(), [self.region1], True, color, 2)
    