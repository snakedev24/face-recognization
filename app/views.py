from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password
from . models import *
from django.contrib import messages
from facedetect.settings import BASE_DIR
import os
import cv2
from datetime import datetime
import pytesseract

def user_login(request):
    if request.method == 'POST':
      
        username = request.POST['username']
        password = request.POST['password']
    
        user = authenticate(username=username, password=password)
        if user is not None:
         
            login(request, user)
           
            return redirect("success_login")
        else:
            messages.warning(request, 'Incorrect username and / or password.')
            return render(request, 'login.html')
    else:
     
        return render(request, 'login.html')


def signup(request):
    if request.method=="POST":
        username = request.POST['username']
        password = make_password(request.POST['password'])
        email = request.POST['email']
       
        newuser = User(
            username=username,
            password=password,
            email=email)
        newuser.save()



def home(request):
    print("enter in home page")
    return render(request,'login.html')


def success_login(request):
    final_data =[]
    final_list=[]

    # Assuming you have imported BASE_DIR from your Django settings
    img_dir = os.path.join(BASE_DIR, "media", "my_images")
    img_list = os.listdir(img_dir)

    for img_filename in img_list:
      
        img_path = os.path.join(img_dir, img_filename)
        image = cv2.imread(img_path)
        
        if image is not None:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

            rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

            dilation = cv2.dilate(thresh, rect_kernel, iterations=1)

            contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                cropped = image[y:y + h, x:x + w]
                text = pytesseract.image_to_string(cropped)                
               
                if "\n" in text:
                    smt = text.split('\n')
                    time_stamp = smt[0]
                    name = smt[1] 
                    final_data.append(time_stamp)
                    final_data.append(name)
                elif not '\n' in text:
                    final_data.append(text)
             

            for item_remove in final_data:
                cleaned_item = item_remove.strip()
                if cleaned_item != "":
                    final_list.append(cleaned_item)

            datetime_string = f"{final_list[1]} {final_list[0]}"
            datetime_object = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
           
            if ImageModel.objects.filter(image=f"my_images/{img_filename}", name_of_employee=final_list[2], datetime_field=datetime_object).exists():
                pass
            else:
   
                obj = ImageModel(image=f"my_images/{img_filename}", name_of_employee=final_list[2], datetime_field=datetime_object)
                obj.save()
           

    obj = ImageModel.objects.all()





    return render(request,'success_login.html',{'obj':obj})


