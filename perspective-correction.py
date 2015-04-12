import numpy as np
import cv2
from shapely.geometry import Polygon


# accepts vertices in any order
class Quadrilateral:
    def __init__(self, verts):
        if len(verts) != 4:
            raise NameError('only 4 vertices allowed in a quadrilateral!')
        # note that the origin is the top left of the image
        highest = 0
        secondHighest = 0
        for vert in verts:
            if vert[1] >= highest:
                secondHighest = highest
                highest = vert[1]
            elif vert[1] >= secondHighest:
                secondHighest = vert[1]

        top = []
        bottom = []
        #drawAndDisplayBox(verts[0], verts[1], verts[3], verts[2])

        for vert in verts:
            if vert[1] == highest or vert[1] == secondHighest:
                top.append(vert)
            else:
                bottom.append(vert)

        if len(top) > 2:
            raise NameError('this is not a quadrilateral!')
        if len(bottom) > 2:
            raise NameError('this is not a quadrilateral!')

        if top[0][0] > top[1][0]:
            self.topLeft = top[1]
            self.topRight = top[0]
        else:
            self.topLeft = top[0]
            self.topRight = top[1]

        if bottom[0][0] > bottom[1][0]:
            self.bottomLeft = bottom[1]
            self.bottomRight = bottom[0]
        else:
            self.bottomLeft = bottom[0]
            self.bottomRight = bottom[1]

    def getSize(self):
        return Polygon([self.topLeft, self.topRight,
                        self.bottomRight, self.bottomLeft]).area


def computeIntersect(a, b):
    x1 = a[0][0]
    y1 = a[0][1]
    x2 = a[1][0]
    y2 = a[1][1]

    x3 = b[0][0]
    y3 = b[0][1]
    x4 = b[1][0]
    y4 = b[1][1]

    d = (1.0 * (x1-x2)) * (y3-y4) - (1.0 * (y1-y2)) * (x3-x4)
    if d == 0:
        return (-1, -1)

    x = ((x1 * y2 - y1 * x2) * (x3 - x4) -
         (x1 - x2) * (x3 * y4 - y3 * x4)) / d
    y = ((x1 * y2 - y1 * x2) * (y3 - y4) -
         (y1 - y2) * (x3 * y4 - y3 * x4)) / d
    return (x, y)


# find all lines that close the box started by the first three arguments
# note: modifies intersections to remove used lines
def findRectangles(originalLine, intersectingLineStruct,
                   secondIntersectingLineStruct, intersections):
    intersectingLine = intersectingLineStruct[0]
    secondIntersectingLine = secondIntersectingLineStruct[0]
    vert1 = intersectingLineStruct[1]
    vert2 = secondIntersectingLineStruct[1]
    rectangles = []
    validLines = intersections[secondIntersectingLine]
    for lineStruct in intersections[intersectingLine]:
        for validLineStruct in validLines:  # could be a dict i guess
            if lineStruct[0] == validLineStruct[0]:
                try:
                    rectangles.append(Quadrilateral([vert1, vert2, lineStruct[1], validLineStruct[1]]))
                except:
                    continue

    # removing entries as we go along to avoid duplicate rectangles
    #originalLineEntry = (originalLine, vert1)
    #intersectingLineEntries = intersections[intersectingLine]
    #if originalLineEntry in intersectingLineEntries:
        #intersectingLineEntries.remove(originalyLineEntry)
    #originalLineEntry = (originalLine, vert2)
    #if originalLineEntry in validLines:
        #validLines.remove(originalyLineEntry)

    return rectangles


def findOutermostCorners(linesDefinedByPoints, img):
    # first find all intersections within the picture
    intersections = {}
    height, width = img.shape[:2]
    for line in linesDefinedByPoints:
        intersections[line] = []
        for otherLine in linesDefinedByPoints:
            if line == otherLine:
                continue
            intersection = computeIntersect(line, otherLine)
            # make sure the intersection is within the image
            if intersection[0] > width or intersection[0] < 0:
                continue
            if intersection[1] > height or intersection[1] < 0:
                continue
            intersections[line].append((otherLine, intersection))

    # for each line, try all pairs of lines that intersect with it
    # if that pair share another line they intersect with, record the vertices
    rectangles = []
    for line, others in intersections.iteritems():
        if len(others) < 2:
            continue
        for intersectingLineStruct in others:
            #img = cv2.imread(filename) # to ignore previous lines
            #drawLine(img, line[0], line[1])
            #drawLine(img, intersectingLineStruct[0][0], intersectingLineStruct[0][1])
            #cv2.imshow('box', img)
            #if cv2.waitKey(0):
                #cv2.destroyAllWindows()

            for secondIntersectingLineStruct in others:
                if intersectingLineStruct == secondIntersectingLineStruct:
                    continue
                rectangles.extend(
                    findRectangles(
                        line, intersectingLineStruct,
                        secondIntersectingLineStruct, intersections))

    # compare the sizes of rectangles and return the largest
    maxRectSize = 0
    maxRect = None
    for quad in rectangles:
        if quad.getSize() > maxRectSize:
            maxRectSize = quad.getSize()
            maxRect = quad

    return maxRect

def drawAndDisplayBoxFromQuad(quad):
    drawAndDisplayBox(quad.topLeft, quad.topRight, quad.bottomRight, quad.bottomLeft)

def drawAndDisplayBox(topLeft, topRight, bottomRight, bottomLeft):
    global tries
    img = cv2.imread(filename) # to ignore previous lines
    drawLine(img, topLeft, topRight)
    drawLine(img, topLeft, bottomLeft)
    drawLine(img, bottomRight, topRight)
    drawLine(img, bottomLeft, bottomRight)
    cv2.imwrite('tries/try:' + str(tries) + '.jpg', img)
    tries += 1
    #cv2.imshow('box', img)
    #if cv2.waitKey(0):
        #cv2.destroyAllWindows()

def drawLine(img, vert1, vert2):
    cv2.line(img, (int(vert1[0]), int(vert1[1])), (int(vert2[0]), int(vert2[1])), (0, 0, 255), 2)

tries = 0
# print computeIntersect([(1, 1), (2, 1)], [(1, 1), (2, 2)])
#filename = './perspective-quadrilateral-src-img.jpg'
filename = './test-images-4-12/test-image-upload-0.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#commented out awaken
edges = cv2.Canny(gray, 150, 300, apertureSize=3)
#edges = cv2.Canny(gray, 100, 100, apertureSize=3)

cv2.imshow('edges', edges)
if cv2.waitKey(0):
    cv2.destroyAllWindows()

#commented out awaken
lines = cv2.HoughLines(edges, 1, np.pi/180, 150)
#lines = cv2.HoughLines(edges, 1, np.pi/180, 70, 30, 10)



# easier format to reason about.  ((x1, y1), (x2, y2))
linesDefinedByPoints = []
for line in lines:
    rho, theta = line[0]  # double-packed for no discernable reason
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))
    linesDefinedByPoints.append(((x1, y1), (x2, y2)))

    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imshow('lines', img)
if cv2.waitKey(0):
    cv2.destroyAllWindows()

# using the outermost lines. might not be the most effective, but cleans up well
quad = findOutermostCorners(linesDefinedByPoints, img)

print quad.topLeft
print quad.topRight
print quad.bottomLeft
print quad.bottomRight
drawAndDisplayBoxFromQuad(quad)

#try to straighten the picture out
src = np.array([quad.topLeft, quad.topRight, quad.bottomRight, quad.bottomLeft], np.float32)
dst = np.array([[0, 810], [560, 810], [560, 0], [0, 0]], np.float32)

matrix = cv2.getPerspectiveTransform(src, dst)
print matrix

img = cv2.imread(filename) # to ignore previous lines
result = cv2.warpPerspective(img, matrix, (560, 810))

cv2.imshow('result', result)
if cv2.waitKey(0):
    cv2.destroyAllWindows()

cv2.imwrite('perspective-corrected-suspension-field.jpg', result)
