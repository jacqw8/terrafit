import cv2
import os

def cam():
    cam = cv2.VideoCapture(0)

    img_counter = 0

    while (True):
        ret, frame = cam.read()

        cv2.imshow('frame', frame)

        if not ret:
            break
        k=cv2.waitKey(1)

        if k%256==32:
            #space
            img_name = f"image_{img_counter}.png"
            path = os.getcwd() + '/ml_clothes/new/' + img_name
            cv2.imwrite(path, frame)
            img_counter += 1
            break

    cam.release()
    cv2.destroyAllWindows()
