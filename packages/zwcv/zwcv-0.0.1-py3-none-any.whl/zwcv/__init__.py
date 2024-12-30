import cv2
import numpy as np


def cvshow(img, title='cvshow'):
    cv2.namedWindow(title, 0)
    cv2.imshow(title, img)

def cvwait():
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def cvread(pth):
    return cv2.imdecode(np.fromfile(pth, dtype=np.uint8), cv2.IMREAD_COLOR)

def cvwrite(img, pth, fmt='.png'):
    cv2.imencode(fmt, img)[1].tofile(pth)

###############################################################################
# cvMSER
###############################################################################
def cvMSER(pth):
    # 读取图片
    imagePath = pth
    img = cv2.imread(imagePath)
    # 灰度化
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    vis = img.copy()
    orig = img.copy()
    # 调用 MSER 算法
    mser = cv2.MSER_create(min_area=30)
    regions, _ = mser.detectRegions(gray) # 获取文本区域
    hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions] # 绘制文本区域
    cv2.polylines(img, hulls, 1, (0, 255, 0))
    # cv2.imshow('img', img)
    # 将不规则检测框处理成矩形框
    keep = []
    for c in hulls:
        x, y, w, h = cv2.boundingRect(c)
        keep.append([x, y, x + w, y + h])
        cv2.rectangle(vis, (x, y), (x + w, y + h), (255, 255, 0), 1)
    # cv2.imshow("hulls", vis)

    # 筛选不重复的矩形框
    keep2=np.array(keep)
    pick = nms_fast(keep2, 0.5)
    for (startX, startY, endX, endY) in pick:
        cv2.rectangle(orig, (startX, startY), (endX, endY), (255, 185, 120), 2)
    cv2.imshow("After NMS", orig)

def nms_fast(boxes, overlapThresh=0.5):
    # 空数组检测
    if len(boxes) == 0:
        return []
 
    # 将类型转为float
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")
 
    pick = []
    # 四个坐标数组
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]
 
    area = (x2 - x1 + 1) * (y2 - y1 + 1) # 计算面积数组
    idxs = np.argsort(y2) # 返回的是右下角坐标从小到大的索引值
 
    # 开始遍历删除重复的框
    while len(idxs) > 0:
        # 将最右下方的框放入pick数组
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)
 
        # 找到剩下的其余框中最大的坐标x1y1，和最小的坐标x2y2,
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])
 
        # 计算重叠面积占对应框的比例
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        overlap = (w * h) / area[idxs[:last]]
 
        # 如果占比大于阈值，则删除
        idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))

    return boxes[pick].astype("int")

###############################################################################
# distorCorrect
###############################################################################
def distorCorrect(pth):
    img = cv2.imread(pth)
    # 图片二值化
    matGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, matBin = cv2.threshold(matGray, 127, 255, cv2.THRESH_BINARY)
    # 高斯降噪
    matBlured = cv2.GaussianBlur(matBin, ksize=(3, 3), sigmaX=2, sigmaY=2)
    matCanny = cv2.Canny(matBlured, threshold1=20, threshold2=60, apertureSize=3, L2gradient=False)
    # 寻找轮廓
    contours, hierarchy = cv2.findContours(matCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # 在众多轮廓中选择凸多边形且定点数为四个的轮廓（找梯形）
    rect_contours = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02*perimeter, True)
        if len(approx) == 4:
            rect_contours.append(approx)

    # 寻找面积最大的轮廓
    areas = []
    for c in rect_contours:
        areas.append(cv2.contourArea(c))
    contour_idx = areas.index(max(areas))
    contour_max = rect_contours[contour_idx]

    # 获得最大轮廓对应的正方形（debug用）
    x, y, w, h = cv2.boundingRect(contour_max)
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,0,255), 3)
    matCropped= img[y+2:y+h-2,x+2:x+w-2]

    if contour_max is None:
        return

    # 绘制最大轮廓顶点（debug用）
    top_left = None
    top_right = None
    bottom_right = None
    bottom_left = None
    points = contour_max.reshape(4, 2)
    rect = np.zeros((4, 2), dtype=np.float32)
    s = points.sum(axis=1)
    rect[0] = points[np.argmin(s)]
    rect[2] = points[np.argmax(s)]
    diff = np.diff(points, axis=1)
    rect[1] = points[np.argmin(diff)]
    rect[3] = points[np.argmax(diff)]
    
    top_left = tuple(rect[0])
    top_right = tuple(rect[1])
    bottom_right = tuple(rect[2])
    bottom_left = tuple(rect[3])

    top_left        = (int(top_left[0]), int(top_left[1]))
    top_right       = (int(top_right[0]), int(top_right[1]))
    bottom_right    = (int(bottom_right[0]), int(bottom_right[1]))
    bottom_left      = (int(bottom_left[0]), int(bottom_left[1]))
    cv2.circle(img, top_left,5,(0,255,0),-1)
    cv2.circle(img, top_right, 5,(0,255,0), -1)
    cv2.circle(img, bottom_right, 5, (0,255,0), -1)
    cv2.circle(img, bottom_left,5,(0,255,0), -1)

    # 通过透视完成畸形矫正
    warped = four_point_transform(img, rect)

    cvshow('(1)binary', matBin)
    cvshow('(2)edge detect', matCanny)
    cvshow('(3)max rect', img)
    cvshow('(4)cropped', matCropped)
    cvshow('(5)transformed', warped)
    cvwait()

def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")
 
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
 
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
 
    # return the ordered coordinates
    return rect

def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    # rect = order_points(pts)
    rect = pts
    (tl, tr, br, bl) = rect
 
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
 
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
 
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
 
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
 
    # return the warped image
    return warped

###############################################################################
# 
###############################################################################