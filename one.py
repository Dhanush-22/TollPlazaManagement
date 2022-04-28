import imutils
import glob

import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def removeSpecialCharacter(s):
    j = 0
    while j < len(s):
        if (ord(s[j]) in range(97,123) ):
            # erase function to erase
            # the character
            x=chr(ord(s[j])-32)
            y= s[0:j]+x+s[j+1:]
            s=y
            j -= 1
        j += 1
    i=0
    while i < len(s):
        if not (ord(s[i]) in range(48,58) or ord(s[i]) in range(65,91) or  ord(s[i]) in range(97,123)):
            # erase function to erase
            # the character
            x= s[0:i]+s[i+1:]
            s=x
            i -= 1
        i += 1
    return "".join(s)

# for img in glob.glob("C:\/Users\dell\Documents\Cpp VS\myProject\media\*.jpg"):
for img in glob.glob("C:\\NIT AP\\EPICS\\DataSet\\w1\\*.jpg"):
        img = cv2.imread(img, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (600, 400))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray,7, 15, 15)  #11 17 17   7 15 15

        cv2.imshow('Check : ', img)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()

        edged = cv2.Canny(gray, 170, 200)  #170,200
        cv2.imshow('Check : ', edged)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10] #:30
        screenCnt = None

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)  #0.02

            if len(approx) == 4:
                screenCnt = approx
                break
        
        stat = "found"
        if screenCnt is None:
            detected = 0
        else:
            detected = 1

        if detected == 1:
            cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

        cv2.imshow('Check : ', img)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()


        mask = np.zeros(gray.shape, np.uint8)
        if detected==1:
            new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
        new_image = cv2.bitwise_and(img, img, mask=mask)


        cv2.imshow('Check : ', new_image)
        cv2.waitKey(5000)
        cv2.destroyAllWindows()


        (x, y) = np.where(mask == 255)
        if(len(x) == 0 or len(y)==0):
            print()
        else :
            (topx, topy) = (np.min(x), np.min(y))

            (bottomx, bottomy) = (np.max(x), np.max(y))
            Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

            cv2.imshow('Check : ', Cropped)
            cv2.waitKey(5000)
            cv2.destroyAllWindows()

            text = pytesseract.image_to_string(Cropped, config='--psm 11')
            if (len(text) >5):
                #print("programming_fever's License Plate Recognition\n")
                text = removeSpecialCharacter(text)
                print("Number :", text)
                stat = removeSpecialCharacter(text)
                img = cv2.resize(img, (500, 300))
                Cropped = cv2.resize(Cropped, (400, 200))
            else :
                print("Not found")