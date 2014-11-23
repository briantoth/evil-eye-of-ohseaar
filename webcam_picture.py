import cv2
import serial

s = serial.Serial(port='/dev/tty.usbserial-DA013PLT', baudrate=9600)
if s.isOpen():
    print s.readline()
    capture = cv2.cv.CaptureFromCAM(1)
    if capture:
        cv2.cv.NamedWindow("cam_test", cv2.CV_WINDOW_AUTOSIZE)
        f=cv2.cv.QueryFrame(capture)
        if f:
            cv2.cv.ShowImage("cam_test",f)
            cv2.cv.WaitKey(0)
    cv2.cv.DestroyWindow("cam_test")
s.close()

