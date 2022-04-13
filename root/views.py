from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
import pymysql

#start

import cv2
import imutils
import numpy as np
import pytesseract
import glob

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

#end
# Create your views here.

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
    # Users = User.objects.all()
    # print(Users)
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

        user = auth.authenticate(username=username,password=pswd)
        if user is not None:
            auth.login(request, user)
            name = user
            return render(request,'userWorkPage.html',{'name':name})
        else :
            messages.error(request,"Invalid username or password" )
            return redirect('startPage')

        


def validateWL(request):
    # return render(request, 'workerWorkPage.html')
    return render(request,'detectPage.html')

def debitCredits(request):
    number = request.POST.get('num','')
    messages.info(request,"Credits debited on vehicle "+ str(number))
    print("Redirecting...........................")
    return redirect('debit')
    # return render(request,'debitStat.html',{'status':stat})


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

        # saving the file

        # print("\n \n")
        # print(type(up))
        # print(up)
        # print(up.name)
        # print("\n \n")

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
            messages.info(request,"Dear "+ str(first_name) +", your account has been created : )  Now you can login" )
        # print("Redirecting...........................")
        return redirect('startPage')
    return redirect('startPage')




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

