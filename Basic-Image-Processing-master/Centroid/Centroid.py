import cv2

img = cv2.imread("signature.png", 0)
'''
函数：cv2.imread(filename,flags)
参数：filename:读入文件的完整路径。
     flags:标志位，{1,0,-1}
           1：默认参数，读入一副彩色图片，忽略alpha通道
           
'''
# print(img)

ret, binary = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)


def findBB(im):
    h, w = im.shape[0], im.shape[1]
    left, top = w, h
    right, bottom = 0, 0

    for x in range(h):
        for y in range(w):
            if im[x, y] == 0:
                right = x if x > right else right
                left = x if x < left else left
                bottom = y if y > bottom else bottom
                top = y if y < top else top

    return left, right, top, bottom


def findCentroid(im):
    h, w = im.shape[0], im.shape[1]
    cx, cy, n = 0, 0, 0
    for x in range(h):
        for y in range(w):
            if im[x, y] == 0:
                cx += x
                cy += y
                n += 1
    cx /= n
    cy /= n
    cx, cy = int(cx), int(cy)
    return cx, cy


def divideImgIntoFour(im, cent):
    h, w = im.shape[0], im.shape[1]
    cx, cy = cent
    img1 = im[0:cx, 0:cy]
    img2 = im[0:cx, cy:w]
    img3 = im[cx:h, 0:cy]
    img4 = im[cx:h, cy:w]
    return [img1, img2, img3, img4]


def calculateTransitions(im):
    h, w = im.shape[0], im.shape[1]
    prev = im[0, 0]
    n = 0
    for x in range(1, h):
        for y in range(1, w):
            curr = im[x, y]
            # check if the is black to white transition
            n = n + 1 if curr == 255 and prev == 0 else n
            prev = curr
    return n


boundingBox = findBB(binary)
cropImg = binary[boundingBox[0]:boundingBox[1], boundingBox[2]:boundingBox[3]]
centroid = findCentroid(cropImg)
segments = divideImgIntoFour(cropImg, centroid)
transitions = [calculateTransitions(seg) for seg in segments]

print("Bounding Box:", boundingBox)
print("Coordinates of centroid:", centroid)
print("Black to white transitions (4 segments):", transitions)

cv2.imshow("TopLeft", segments[0])
cv2.imwrite("TopLeft.png", segments[0])
cv2.imshow("TopRight", segments[1])
cv2.imwrite("TopRight.png", segments[1])
cv2.imshow("BottomLeft", segments[2])
cv2.imwrite("BottomLeft.png", segments[2])
cv2.imshow("BottomRight", segments[3])
cv2.imwrite("BottomRight.png", segments[3])
cv2.waitKey(0)
