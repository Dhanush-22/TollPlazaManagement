import cv2
import numpy as np
import pytesseract
import requests
import base64
import json
import imutils


frameWidth = 640  # Frame Width
franeHeight = 480  # Frame Height
plateCascade = cv2.CascadeClassifier("C:\\Users\\dell\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_russian_plate_number.xml")
minArea = 500

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, franeHeight)
cap.set(10, 150)
count = 0

while True:
    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)

    for (x, y, w, h) in numberPlates:
        area = w * h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "NumberPlate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            imgRoi = img[y:y + h, x:x + w]
            cv2.imshow("ROI", imgRoi)
    cv2.imshow("Result", img)
    k=cv2.waitKey(100)
    if k%256==32:
        img_name = "C:\\license_plates\\car_image_{}.jpg".format(count)
        cv2.imwrite(img_name, imgRoi)
        cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Scan Saved", (15, 265), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
        cv2.waitKey(500)
        count += 1

        SECRET_KEY = 'sk_13e457114d7cbf9fd86db7ff'
        with open(img_name, 'rb') as image_file:
            img_base64 = base64.b64encode(image_file.read())

        url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=ind&secret_key=%s' % (SECRET_KEY)
        r = requests.post(url, data=img_base64)
        try:
            text=r.json()['results'][0]['plate']
            print(text)

        except:
            print("No number plate found")
    elif k % 256 == 27:
        print("Escape hit, closing...")
        break

