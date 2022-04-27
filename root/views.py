from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
from .models import *
import pymysql
import razorpay

import imutils
import glob

import cv2
import numpy as np
import pytesseract
import requests
import base64
import json



pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def detectAndDebit(request):
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
    
    if request.method == 'POST' and request.FILES['Upload']:
        upload = request.FILES['Upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        stat = "not found"
        for img in glob.glob("C:\/Users\dell\Documents\Cpp VS\myProject\media\*.jpg"):
            name = ""
            i = len(img)-1
            while (img[i] != '\\'):
                name = img[i]+name
                i=i-1 
            if (name == file) :
                img = cv2.imread(img, cv2.IMREAD_COLOR)
                img = cv2.resize(img, (600, 400))
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.bilateralFilter(gray,7, 15, 15)  #11 17 17   7 15 15

                '''cv2.imshow('Check : ', img)
                cv2.waitKey(5000)
                cv2.destroyAllWindows()'''
                edged = cv2.Canny(gray, 170, 200)  #170,200
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


                mask = np.zeros(gray.shape, np.uint8)
                if detected==1:
                    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
                new_image = cv2.bitwise_and(img, img, mask=mask)


                (x, y) = np.where(mask == 255)
                if(len(x) == 0 or len(y)==0):
                    print()
                else :
                    (topx, topy) = (np.min(x), np.min(y))

                    (bottomx, bottomy) = (np.max(x), np.max(y))
                    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

                    text = pytesseract.image_to_string(Cropped, config='--psm 11')
                    if (len(text) >5):
                        #print("programming_fever's License Plate Recognition\n")
                        #removeSpecialCharacter(text)
                        # print("Number :", text)
                        stat = removeSpecialCharacter(text)
                        img = cv2.resize(img, (500, 300))
                        Cropped = cv2.resize(Cropped, (400, 200))
                        return render(request,'debitStat.html',{'status':stat})
                    return render(request,'debitStat.html',{'status':stat})
    return render(request, 'upload.html')    

def test(request):
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

    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']

        # print("\n \n")
        # print(type(upload))
        # print(upload)
        # print(upload.name)
        # print("\n \n")

        fss = FileSystemStorage()
        print(type(fss))
        print(fss)


        file = fss.save(upload.name, upload)
        stat = "not found"

        for img in glob.glob("C:\/Users\dell\Documents\Cpp VS\myProject\media\*.jpg"):
            name = ""
            i = len(img)-1
            while (img[i] != '\\'):
                name = img[i]+name
                i=i-1 
            if (name == file) :
                img = cv2.imread(img, cv2.IMREAD_COLOR)
                img = cv2.resize(img, (600, 400))
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.bilateralFilter(gray,7, 15, 15)  #11 17 17   7 15 15

                '''cv2.imshow('Check : ', img)
                cv2.waitKey(5000)
                cv2.destroyAllWindows()'''
                edged = cv2.Canny(gray, 170, 200)  #170,200
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


                mask = np.zeros(gray.shape, np.uint8)
                if detected==1:
                    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
                new_image = cv2.bitwise_and(img, img, mask=mask)


                (x, y) = np.where(mask == 255)
                if(len(x) == 0 or len(y)==0):
                    print()
                else :
                    (topx, topy) = (np.min(x), np.min(y))

                    (bottomx, bottomy) = (np.max(x), np.max(y))
                    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

                    text = pytesseract.image_to_string(Cropped, config='--psm 11')
                    if (len(text) >5):
                        #print("programming_fever's License Plate Recognition\n")
                        #removeSpecialCharacter(text)
                        # print("Number :", text)
                        stat = removeSpecialCharacter(text)
                        img = cv2.resize(img, (500, 300))
                        Cropped = cv2.resize(Cropped, (400, 200))
                        return render(request,'debitStat.html',{'status':stat})
                    return render(request,'debitStat.html',{'status':stat})
    return render(request, 'upload.html')



def displayHome(request):
    return render(request,'rootBase1.html') 

def displayNew(request):
    return render(request, 'rootBase1.html')

def displayIndex(request):
    return render(request, 'index.html')

def displaySignup(request):
    return render(request,'signupPage.html')

def displayAdminLogin(request):
    return render(request, 'test1.html')

def displayUserLogin(request):
    return render(request, 'userLoginPage.html')

def displayWorkerLogin(request):
    return render(request,'workerLoginPage.html')

def validateAL(request):
    newUsers = []
    UserExtras = User_Extra.objects.all()

    for user in UserExtras:
        if(user.is_verified==0):
            newUsers = newUsers + [user]   
    print("\n \n")
    print(newUsers)
    return render(request, 'adminWorkPage.html', {'newUsers' : newUsers})


def validateUL(request):
    if request.method == "POST":
        username = request.POST['uname1']
        pswd = request.POST['psw1']
        isValid = 0
        user = auth.authenticate(username=username,password=pswd)
        f_name = username
        if user is not None:
            auth.login(request, user)
            name = user
            f_name,l_name = username.split("_")
            this_users = User_Extra.objects.filter(First_Name=f_name,Last_Name=l_name)
            print(this_users)
            user_vehicles = []
            for u in this_users:
                veh_obj = Vehicle.objects.get(veh_no=str(u.Vehicle_Number))
                isValid = u.is_verified
                user_vehicles.append(veh_obj)
            print("\n \n")
            return render(request,'userWorkPage.html',{'name':f_name, 'veh_list':user_vehicles, 'isValidUser':isValid})
        else :
            messages.error(request,"Invalid username or password" )
            return redirect('startPage')

        
def validateWL(request):
    return render(request,'detectPage.html')

def debitCredit(request):
    number = request.POST.get('num','')
    veh_obj = Vehicle.objects.filter(veh_no = number)
    # a = int(input("Enter the value : "))
    if len(veh_obj) >0 :
        veh_obj = Vehicle.objects.get(veh_no = number)
        credits = veh_obj.balance
        tax = 50
        stat = "Success"
        if tax>credits :
            stat = "No enough credits"
        else:
            credits = credits-tax
            veh_obj.balance = credits
            veh_obj.save()
    else:
        stat = "Vehicle not yet registered."
    return render(request,'debitStat.html',{'status':stat})


def registerNew(request):
    if request.method == 'POST' and request.FILES['upload1']:
        up = request.FILES['upload1']
        first_name = request.POST.get('first','default')
        last_name = request.POST.get('last','default')
        email = request.POST.get('email','default')
        phone = request.POST.get('phone','default')
        veh_num = request.POST.get('veh_num','default')
        veh_name = request.POST.get('vehName','default')
        license_num = request.POST.get('license_num','default')
        pswd = request.POST.get('psw','default')
        username = first_name + "_"+ last_name


        #To check whether username exists or not
        if User.objects.filter(username=username).exists():
            messages.info(request,"Oops! username already exists" )
        
        else:
            fss = FileSystemStorage()
            file = fss.save(up.name, up)
        
            # Create a User object after validating the abouve stuff
            newUser = User.objects.create_user(username = username, password = pswd, email=email, first_name=first_name,
            last_name=last_name)
            newUserExtra = User_Extra.objects.create(First_Name=first_name, Last_Name = last_name, License_num = license_num
            , Vehicle_Number=veh_num, Vehicle_Name = veh_name, is_verified=0,License_img=up.name)
            full_name = first_name + " "+ last_name
            newVehicle = Vehicle.objects.create(owner_name=full_name, veh_no = veh_num, balance=0)
            newUser.save()
            newUserExtra.save()
            newVehicle.save()
            # print("\n \n Both saved successfully \n \n")
            messages.info(request,"Dear "+ str(first_name) +", your account has been created : )  Now you can login using " +str(username) + " as username." )
        # print("Redirecting...........................")
        return redirect('startPage')
    return redirect('startPage')




def doPayment(request):
    if request.method == "POST":
        # order_amount = 200
        order_amount = request.POST['amt']
        order_amount = order_amount + "00"
        print(type(order_amount))
        order_amount = int(order_amount)
        vehicle_num = request.POST['vehNo']
        print(order_amount)
        print(vehicle_num)
        order_currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_aQdqNW0mKjsYkA','A7BHFuErU1PKBcMDM7ZT0MRC'))
        payment = client.order.create({'amount':order_amount, 'currency':'INR', 'payment_capture':'1'})
    return render(request,'PaymentPage.html',{'payment':payment})



def DetectAndDebit(request):  
    if request.method != "POST" : 
        return HttpResponse("Try again detect and debit")

    frameWidth = 640  # Frame Width
    franeHeight = 480  # Frame Height
    plateCascade = cv2.CascadeClassifier("C:\\Users\\dell\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\cv2\\data\\haarcascade_russian_plate_number.xml")
    minArea = 500

    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, franeHeight)
    cap.set(10, 150)
    count = 0

    detectedList = []

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
                # print(text)
                flag = Vehicle.objects.filter(veh_no = text).exists()
                if(flag):
                    veh_obj = Vehicle.objects.get(veh_no = text)
                    detectedList.append(veh_obj)
                    credits = veh_obj.balance
                    tax = 50
                    stat = "Success"
                    if tax>credits :
                        stat = "No enough credits"
                    else:
                        print(text)
                        credits = credits-tax
                        veh_obj.balance = credits
                        veh_obj.save()
            except:
                print("No number plate found")
        elif k % 256 == 27:
            print("Escape hit, closing...")
            break
    
    print(detectedList)
    return render(request,'result_page.html',{'list':detectedList})
    # return HttpResponse("Hey there")






'''
 # db = pymysql.connect(host="localhost",user="root",password="dhanush@123")
    # database = "vehInfo"
    # open = "use " + database
    # cur = db.cursor()
    # cur.execute(open)
    # print("Connected!")
    # print("Connected!")
    # print("\n")
    # print("\n")
    # print("Connected!")
    # tax = 80
    # vehicleNo = number
    # flag = 0

    # cur.execute('select * from credits where number = %s',vehicleNo)
    # rows = cur.fetchall()
    # for row in rows :
    #     stat = "Found"
    #     if(row[1] == vehicleNo):
    #         flag = 1
    #         l1 = 'Vehicle found\n'
    #         l2 = 'Vehicle name : %s\n' %(row[2])
    #         l3 = 'Credits : %d<br>' %(row[3])
    #         l4 = 'Tax = %d\n' %(tax)
    #         a = row[3] - tax
    #         if(a >= 0):
    #             sql = "UPDATE CREDITS SET balance = %d where number = '%s'" %(a,vehicleNo)
    #             cur.execute(sql)
    #             l5 = "Debited \nGenerating reciept..\n"
    #             l6 = "Credits left : %d\n"%(a)
    #             l7 = "<br>Happy Journey :)\n"
    #             stat = "success"
    #         else:
    #             l5 = "Process Cancelled\n"
    #             l6 = "No enough credits, make payment by cash if possible\n"
    #             stat = "Invalid"
    #         db.commit()
    # if (flag == 0):
    #     stat = "Vehicle not yet registered with Instant"
    # db.commit()
    # db.close()
    '''

