from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from app.models import *
from app.serializers import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from django.db import IntegrityError
from django.contrib.auth import authenticate,login,logout
import re
from random import randint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import geocoder
import googlemaps
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from rest_framework import status
from avpl.settings import EMAIL_HOST_USER
from django.core.mail import send_mail



class UserRegister(ViewSet):
    def list(self,request):
        query=User_register.objects.all()
        seriler=UserRegisterSerializers(query,many=True)
        users={'User_register':seriler.data,'response_code':200,'comments':'all list',"status": True}
        return Response(users)

    def create(self,request):
        data=request.data
        ###session set####
        request.session['first_name']=data.get('first_name')
        request.session['last_name']=data.get('last_name')
        request.session['password']=data.get('password')
        request.session['email']=data.get('email')
        request.session['mobile']=data.get('mobile')
        request.session['gender']=data.get('gender')
        request.session['address']=data.get('address')
        ####session get#####
        email1 = request.session.get('email')
        password1 = request.session.get('password')
        try:
            user_object=User.objects.get(username=email1)#instance username me email save ho rha
            response_data = {'response_code':200,'email':email1,'comments':'email is allredy exist',"status": False}
            return Response(response_data)
        except:
            rand_otp = randint(1111, 9999)
            try:
                otp_check=Otp.objects.get(email=email1)
                otp_check.email=email1
                otp_check.otp=rand_otp
                otp_check.save()
            except:
                otp_obj=Otp(otp=rand_otp,email=email1)
                otp_obj.save()
        
            send_conformation_email(request,rand_otp)
            response_data = {'response_code':200,'email':email1,'comments':'otp is send please veryfy',"status": True}
            return Response(response_data)
        
    
    def destroy(self,request,id=None):
        try:
            ts=User_register.objects.get(id=id)
            ts.delete()
            response_data = {'response_code':200,'comments':'User_register is succeefull deleted',"status": True}
            return Response(response_data)
        except User_register.DoesNotExist:
            response_data = {'response_code':200,'comments':'User_register is invalid',"status": False}
            return Response(response_data)
    def update(self,request,id=None):
        data=request.data
        email1=data.get('email')
        first_name1=data.get('first_name')
        last_name1=data.get('last_name')
        mobile1=data.get('mobile')
        address1=data.get('address')
        try:
            user_inst = User.objects.get(username=email1)#instance
            print(user_inst)
            obj = User_register.objects.get(user=user_inst)
            print(obj)
            gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
            add_lat_long = gmaps.geocode(address1)
            user_lat = add_lat_long[0]['geometry']['location']['lat']
            user_lng = add_lat_long[0]['geometry']['location']['lng']
            obj.address=address1
            obj.latitude = user_lat
            obj.longitude = user_lng
            obj.mobile = mobile1
            obj.save()
            obb = User.objects.get(username=email1)
            obb.first_name =first_name1
            obb.last_name =last_name1
            obb.save()
            response_data = {'response_code':200,'comments':'user is succeefull update',"status": True}
            return Response(response_data)
        except:
            response_data = {'response_code':200,'comments':'user not  register',"status": False}
            return Response(response_data)


class UserResendMailOtp(ViewSet):
    def create(self,request):
        email = request.data.get('email') 
        print(email)
        rand_otp = randint(1111, 9999)
        otp_update = Otp.objects.get(email=email)
        otp_update.otp=rand_otp
        print('otp_update',otp_update)
        otp_update.save()
        send_conformation_email(request,rand_otp)
        response_data = {'response_code':200,'comments':'Resend OTP Successfully on your register Email..Please Verify Email',"status": True}
        return Response(response_data)
class UserOtpVerify(ViewSet):
    def create(self,request):
        # data=request.data
        first_name1 = request.data.get('first_name')
        last_name1 = request.data.get('last_name')
        password1 = request.data.get('password')
        gender1 = request.data.get('gender')
        mobile1 = request.data.get('mobile')
        email1=request.data.get('email')
        address1 = request.data.get('address')
        otp_check=Otp.objects.get(email=email1)
        print(otp_check)
        print("yes run here..")
        otpByuser=request.data.get('otp')#ye postman me fildname rahega ,jsme gmail wala otp rega
        print(otpByuser)
        if otp_check.otp==str(otpByuser):
            usr_obj=User(username=email1,first_name=first_name1,last_name=last_name1,password=make_password(password1))
            usr_obj.save()
            user_inst=User.objects.get(username=email1)
            gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
            add_lat_long = gmaps.geocode(address1)
            user_lat = add_lat_long[0]['geometry']['location']['lat']
            user_lng = add_lat_long[0]['geometry']['location']['lng']
            rest_obj=User_register(user=user_inst,mobile=mobile1,gender=gender1,address=address1,latitude=user_lat,longitude=user_lng)
            rest_obj.save()
            otp_check.delete()
            response_data = {'response_code':200,'comments':'register is successful',"status": True}
            return Response(response_data)
        else:
            response_data = {'response_code':200,'comments':'give valid otp',"status": False}
            return Response(response_data)

class UserChangePwd(ViewSet):
    def create(self,request):
        datas=request.data
        email1=datas.get('email')
        current_pwd=datas.get('current_password')
        new_pwd=datas.get('new_password')
        confirm_pwd=datas.get('confirm_password')
        # print(email1,current_pwd,new_pwd,confirm_pwd)
        user=authenticate(username=email1,password=current_pwd)
        print(user)
        if user is not None:
            print('111',user)
            if new_pwd==confirm_pwd:
                pwd_re = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
                match_pwd = re.compile(pwd_re)
                res = re.search(match_pwd, new_pwd)
                if res:
                    user_inst=User.objects.get(username=email1)#update pwd
                    user_inst.password=make_password(new_pwd)
                    user_inst.save()
                else:
                    response_data = {'response_code':200,'comments':'password most be strong',"status":False}
                    return Response(response_data)
            else:
                response_data = {'response_code':200,'comments':'password not matched',"status":False}
                return Response(response_data)
        else:
            response_data = {'response_code':200,'comments':'user is not valide',"status":False}
            return Response(response_data)


        response_data = {'response_code':200,'comments':'Password Chnange Successfully',"status":True}
        return Response(response_data)




############################ start vendor register api ####################

class VendorRegister(ViewSet):
    def list(self,request):
        query=Vendor_registration.objects.all()
        seriler=VendorRegisterSerializers(query,many=True)
        vrdr={'Vendor_registration':seriler.data,'response_code':200,'comments':'all list',"status": True}
        return Response(vrdr)
    def create(self,request):
        data=request.data
        ###session set####
        request.session['first_name']=data.get('first_name')
        request.session['last_name']=data.get('last_name')
        request.session['password']=data.get('password')
        request.session['repassword']=data.get('repassword')
        request.session['email']=data.get('email')
        request.session['mobile']=data.get('mobile')
        request.session['gender']=data.get('gender')
        request.session['address']=data.get('address')
        request.session['zipcode']=data.get('zipcode')
        ####session get#####
        email1 = request.session.get('email')
        password1 = request.session.get('password')
        password2 = request.session.get('repassword')
        # print(email1,password1,password2)
        # return Response('ok')
        try:
            user_object=User.objects.get(username=email1)#instance username me email save ho rha
            return Response('email is allredy exist')
        except:
            if password1==password2:
                pwd_reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
                pwd_match_reg = re.compile(pwd_reg)
                # searching regex
                pwd = re.search(pwd_match_reg, password1)
                if pwd:
                    rand_otp = randint(1111, 9999)
                    try:
                        otp_check=Otp.objects.get(email=email1)
                        otp_check.email=email1
                        otp_check.otp=rand_otp
                        otp_check.save()
                    except:
                        otp_obj=Otp(otp=rand_otp,email=email1)
                        otp_obj.save()
                    #######
                    fromaddr='masterpython64@gmail.com'
                    toaddr=email1
                    msg=MIMEMultipart()
                    msg['From']=fromaddr
                    msg['To']=toaddr
                    msg['Subject']="otp for register"
                    body="Your OTP is,"+str(rand_otp)
                    msg.attach(MIMEText(body, 'plain'))
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    # start TLS for security
                    s.starttls()
                    # Authentication
                    s.login(fromaddr, "ashish@#2021")
                    # Converts the Multipart msg into a string
                    text = msg.as_string()
                    # sending the mail
                    s.sendmail(fromaddr, toaddr, text)
                    # terminating the session
                    s.quit()
                    response_data = {'response_code':200,'comments':'otp is send please veryfy',"status":True}
                    return Response(response_data)
                else:
                    response_data = {'response_code':200,'comments':'password invalid',"status":False}
                    return Response(response_data)                
            else:
                response_data = {'response_code':200,'comments':'password not match',"status":False}
                return Response(response_data)
    def update(self,request,id=None):
        data=request.data
        email1=data.get('email')
        first_name1=data.get('first_name')
        last_name1=data.get('last_name')
        mobile1=data.get('mobile')
        address1=data.get('address')
        try:
            user_inst = User.objects.get(username=email1)#instance
            print(user_inst)
            obj = Vendor_registration.objects.get(user=user_inst)
            print(obj)
            gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
            add_lat_long = gmaps.geocode(address1)
            user_lat = add_lat_long[0]['geometry']['location']['lat']
            user_lng = add_lat_long[0]['geometry']['location']['lng']
            obj.store_address=address1
            obj.store_latitude = user_lat
            obj.store_longitude = user_lng
            obj.store_mobile = mobile1
            obj.save()
            obb = User.objects.get(username=email1)
            obb.first_name =first_name1
            obb.last_name =last_name1
            obb.save()
            response_data = {'response_code':200,'comments':'user is succeefull update',"status": True}
            return Response(response_data)
        except:
            response_data = {'response_code':200,'comments':'user not  register',"status": False}
            return Response(response_data)

############################ end vendor register api ####################
class VendorResendMailOtp(ViewSet):
    def create(self,request):
        email = request.session.get('email')
        print(email)
        otp = randint(1111, 9999)
        print(ot)
        otp_update = Otp.objects.get(email=email)
        otp_update.otp=otp
        print(otp_update)
        otp_update.save()
        fromaddr = 'masterpython64@gmail.com'
        toaddr = email
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Testing For Otp"
        body = "Your OTP is," + str(otp)
        msg.attach(MIMEText(body, 'plain'))
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        s.login(fromaddr, "ashish@#2021")
        # Converts the Multipart msg into a string
        text = msg.as_string()
        # sending the mail
        s.sendmail(fromaddr, toaddr, text)
        # terminating the session
        s.quit()
        return Response('Resend OTP Successfully on your register Email..Please Verify Email')
############################ start VendorOtpVerify api ####################
class VendorOtpVerify(ViewSet):
    def create(self,request):
        data=request.data
        first_name1 = request.session.get('first_name')
        last_name1 = request.session.get('last_name')
        password1 = request.session.get('password')
        gender1 = request.session.get('gender')
        mobile1 = request.session.get('mobile')
        email1=request.session.get('email')
        address1 = request.session.get('address')
        zipcode1=request.session.get('zipcode')
        otp_check=Otp.objects.get(email=email1)
        print(otp_check)
        print("yes run here..")
        otpByuser=data.get('otp')#ye postman me fildname rahega ,jsme gmail wala otp rega
        print(otpByuser)
        if otp_check.otp==str(otpByuser):
            usr_obj=User(username=email1,first_name=first_name1,last_name=last_name1,password=make_password(password1))
            usr_obj.save()
            user_inst=User.objects.get(username=email1)
            gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
            if address1:
                add_lat_long = gmaps.geocode(address1)
                vendor_lat = add_lat_long[0]['geometry']['location']['lat']
                vendor_lng = add_lat_long[0]['geometry']['location']['lng']
                rest_obj=Vendor_registration(user=user_inst, store_mobile=mobile1,profile_pic='tree_user_img.jpg', gender=gender1, store_address=address1,store_zipcode=zipcode1,store_latitude=vendor_lat,store_longitude=vendor_lng)
                rest_obj.save()
                otp_check.delete()
                response_data = {'response_code':200,'comments':'register is successful',"status": True}
                return Response(response_data)
        else:
            response_data = {'response_code':200,'comments':'give valid otp',"status": False}
            return Response(response_data)

class VendorChangePwd(ViewSet):
    def create(self,request):
        datas=request.data
        email1=datas.get('email')
        current_pwd=datas.get('current_password')
        new_pwd=datas.get('new_password')
        confirm_pwd=datas.get('confirm_password')
        # print(email1,current_pwd,new_pwd,confirm_pwd)
        user=authenticate(username=email1,password=current_pwd)
        print(user)
        if user is not None:
            print('111',user)
            if new_pwd==confirm_pwd:
                pwd_re = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
                match_pwd = re.compile(pwd_re)
                res = re.search(match_pwd, new_pwd)
                if res:
                    user_inst=User.objects.get(username=email1)#update pwd
                    user_inst.password=make_password(new_pwd)
                    user_inst.save()
                else:
                    return Response({'message':'password most be strong'})
            else:
                return Response({'message':'password not matched'})
        else:
            return Response({'message':'user is not valide'})

        return Response({'message':'Password Chnange Successfully'})


class VendorRegisterStoreDetails(ViewSet):
    def list(self,request):
        query=Vendor_Store_detail.objects.all()
        vendr=Vendor_registration.objects.all()
        if query:

            dat_dict={}
            data_list=[]

            for x in query:
                dat_dict={'user_id':x.vendor.user.id,'username':x.vendor.user.username,'first_name':x.vendor.user.first_name,'last_name':x.vendor.user.last_name,
                'store_mobile':x.vendor.store_mobile,'vendor_status':x.vendor.vendor_status,'profile_pic':str(x.vendor.profile_pic),
                'store_status':x.vendor.store_status,'store_remove':x.vendor.store_remove,'created':x.vendor.created,
                'gender':x.vendor.gender,'utype':x.vendor.utype,
                'store_id':x.id,'store_name':x.store_name,
                'store_address':x.store_address,'store_zipcode':x.store_zipcode,'store_latitude':x.store_latitude,
                'store_longitude':x.store_longitude,'store_category':x.store_category,'store_description':x.store_description,'store_registration_number':x.store_registration_number,
                'store_image':str(x.store_image),'store_logo':str(x.store_logo),'store_banner':str(x.store_banner),
                'store_closing_day':x.store_closing_day,'store_closing_time':x.store_closing_time,'store_opening_time':x.store_opening_time
                ,'store_created_at':x.store_created_at,'store_update_at':x.store_update_at}
                data_list.append(dat_dict)
            shop_dict={"Vendor_shop_details":data_list,'response_code':200,'comments':'all list',"status": True}
           
            return Response(shop_dict)
        else:
            shop_dict={'response_code':200,'comments':'no details of shop',"status": False}
            return Response(shop_dict)


    def create(self,request):
        datas=request.data
        email=datas.get('email')
        store_name = datas.get('store_name')
        store_description = datas.get('store_description')
        store_logo = datas.get('store_logo')
        store_banner = datas.get('store_banner')
        store_image = datas.get('store_image')
        store_category = datas.get('category')
        store_opening_time =datas.get('store_open_time')
        store_close_time =datas.get('store_close_time')
        store_cloasing_day =datas.get('store_day')
        store_registration_number =datas.get('store_registration_number')
        print('11111')
        try:
            user_instance = User.objects.get(username=email)
            store_detail = Vendor_Store_detail(user=user_instance,store_registration_number=store_registration_number,store_name=store_name,store_description=store_description,store_category=store_category,store_logo=store_logo,store_banner=store_banner,store_image=store_image,store_closing_day=store_cloasing_day,store_closing_time=store_close_time,store_opening_time=store_opening_time)
            store_detail.save()
            response_data = {'response_code':status.HTTP_201_CREATED,'comments':'Store Details successful register',"status": True}
            return Response(response_data)
        except:

            response_data = {'response_code':status.HTTP_404_NOT_FOUND,'comments':'venodor is not register',"status": False}
            return Response(response_data)
    def update(self,request,id=None):
        datas=request.data
        email=datas.get('email')
        store_name1 = datas.get('store_name')
        store_description1 = datas.get('store_description')
        store_logo1 = datas.get('store_logo')
        store_banner1 = datas.get('store_banner')
        store_image1 = datas.get('store_image')
        store_opening_time1 =datas.get('store_open_time')
        store_close_time1 =datas.get('store_close_time')
        store_cloasing_day1 =datas.get('store_day')
        try:
            user_inst = User.objects.get(username=email1)#instance
            print(user_inst)
            obj = Vendor_Store_detail.objects.get(user=user_inst)
            print(obj)
            gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
            add_lat_long = gmaps.geocode(address1)
            user_lat = add_lat_long[0]['geometry']['location']['lat']
            user_lng = add_lat_long[0]['geometry']['location']['lng']
            obj.store_name=store_name1
            obj.store_description=store_description1
            obj.store_logo = store_logo1
            obj.store_banner = store_banner1
            obj.store_image = store_image1
            obj.store_closing_day=store_cloasing_day1
            obj.store_closing_time=store_close_time1
            obj.store_opening_time=store_opening_time1
            obj.save()
            
            response_data = {'response_code':200,'comments':'Store Details successful update',"status": True}
            return Response(response_data)
        except:
            response_data = {'response_code':200,'comments':'Store not  register',"status": False}
            return Response(response_data)




class VendorRegisterStoredcumentDetail(ViewSet):
    def list(self,request):
        query=Vendor_store_document.objects.all()
        serializer=VendorRegStodcuDetSerializers(query,many=True)
        vrd={'VendorRegisterStoredcumentDetail':serializer.data,'response_code':200,'comments':'all list',"status": True}
        return Response(vrd)
    def create(self,request):
        datas=request.data
        email=datas.get('email')
        store_seller_aadhar =datas.get('aadhar_number')
        store_seller_front_aadhar_image =datas.get('aadhar_image_front')
        store_seller_back_aadhar_image =datas.get('aadhar_image_back')
        store_seller_pancard =datas.get('pancard_number')
        store_seller_pancard_image = datas.get('pancard_image')
        try:
            store_shiping_policy =datas.get('store_shiping_policy')
        except:
            store_shiping_policy=None
        store_seller_gst =datas.get('store_gst')
        try:
            store_return_policy =datas.get('store_return_policy')
        except:
            store_return_policy = None

        store_bank_account_number =datas.get('bank_account_number')
        store_bank_name =datas.get('bank_name')
        store_bank_ifsc =datas.get('bank_ifsc')
        store_bank_passbook =datas.get('bank_passbook_image')
        store_seller_razorpay_id =datas.get('razorpay_id')
        store_seller_aadhar =datas.get('aadhar_number')
        store_seller_front_aadhar_image =datas.get('aadhar_image_front')
        store_seller_back_aadhar_image =datas.get('aadhar_image_back')
        store_seller_pancard =datas.get('pancard_number')
        store_seller_pancard_image =datas.get('pancard_image')
        try:
            store_shiping_policy =datas.get('store_shiping_policy')
        except:
            store_shiping_policy=None
        store_seller_gst =datas.get('store_gst')
        try:
            store_return_policy =datas.get('store_return_policy')
        except:
            store_return_policy = None

        store_bank_account_number =datas.get('bank_account_number')
        store_bank_name =datas.get('bank_name')
        store_bank_ifsc =datas.get('bank_ifsc')
        store_bank_passbook =datas.get('bank_passbook_image')
        store_seller_razorpay_id = datas.get('razorpay_id')
        try:

            user_instance = User.objects.get(username=email)
            store_document = Vendor_store_document(user=user_instance,store_seller_aadhar=store_seller_aadhar,store_seller_front_aadhar_image=store_seller_front_aadhar_image,
                                                  store_seller_back_aadhar_image=store_seller_back_aadhar_image,store_seller_pancard=store_seller_pancard,
                                                   store_seller_pancard_image=store_seller_pancard_image,store_shiping_policy=store_shiping_policy,store_seller_gst=store_seller_gst,
                                                  store_return_policy=store_return_policy,store_bank_account_number=store_bank_account_number,store_bank_name=store_bank_name,
                                                  store_bank_ifsc=store_bank_ifsc,store_bank_passbook=store_bank_passbook,store_seller_razorpay_id=store_seller_razorpay_id)
            store_document.save()
            response_data = {'response_code':status.HTTP_201_CREATED,'comments':'Store Details successful register',"status": True}
            return Response(response_data)

        except:
            response_data = {'response_code':status.HTTP_400_BAD_REQUEST,'comments':'Vendor is not register',"status": False}
            return Response(response_data)

###Category.objects.all() all list jayega
class CategoryALL(ViewSet):
    def list(self,request):
        query=Category.objects.all()
        serializers=CategorySerializer_only(query,many=True)
        cat={'category':serializers.data,'response_code':200,'comments':'all list',"status": True}
        return Response(cat)
    def create(self,request):
        name=request.data.get('name')
        if name=='':
            response_data = {'response_code':200,'comments':'Category is required',"status": False}
            return Response(response_data)
        else:
            cat=Category(name=name)
            cat.save()
            response_data = {'response_code':200,'comments':'Category Created',"status": True}
            return Response(response_data)
    
    def update(sel,request,id=None):
        name1=request.data.get('name')
        try:
            cat_inst=Category.objects.get(id=id)
            cat_inst.name=name1
            cat_inst.save()
            response_data = {'response_code':200,'comments':'Category updated',"status": True}
            return Response(response_data)
        except:
            response_data = {'response_code':200,'comments':'Category id not exist',"status": False}
            return Response(response_data)
    def destory(self,request,id=None):
        try:
            cat_inst=Category.objects.get(id=id)
            cat_inst.delete()
            response_data = {'response_code':200,'comments':'Category deleted',"status": True}
            return Response(response_data)
        except:
            response_data = {'response_code':200,'comments':'Category id not exist',"status": False}
            return Response(response_data)

class SubcategoryALL(ViewSet):
    def list(self,request):
        
        sub_obje=Subcategory.objects.all()
        serilizers=SubcategorySerializer_only(sub_obje,many=True)
        subcat={'subcategry':serilizers.data,'response_code':200,'comments':'all list',"status": True}
        return Response(subcat)
    def create(self,request):
        C_id=request.data.get('category_id')
        try:
            if C_id=='':
                response_data = {'response_code':200,'comments':'all fields are required',"status": True}
                return Response(response_data)
            else:
                cat_inst=Category.objects.filter(id__in=C_id)
                sub_obj=Subcategory.objects.filter(category__in=cat_inst)
                if sub_obj:
                    dat_dict={}
                    data_list=[]
                    for x in sub_obj:
                        dat_dict={'category_id':x.category.id,'category_name':x.category.name,
                        'subcategory_id':x.id,'subcategory_name':x.name,'subcategory_image':str(x.image)}
                        data_list.append(dat_dict)
                    shop_dict={"subcategory_details":data_list,'response_code':200,'comments':'all list',"status": True}
                    return Response(shop_dict)
                else:
                    response_data = {'response_code':200,'comments':'subcategory is not exsit',"status": False}
                    return Response(response_data)
        except:
            response_data = {'response_code':200,'comments':'Category is not exsit',"status": False}
            return Response(response_data)


class SubSubcategoryAll(ViewSet):
    def list(self,request):
        query=Brands.objects.all()
        ser=SubSubcategorySerializer_only(query,many=True)
        subsub={'brands_list':ser.data,'response_code':200,'comments':'all list',"status": True}
        return Response(subsub)
    def create(self,request):
        s_id=request.data.get('subcategory_id')
        try:
            if s_id=='':
                response_data = {'response_code':200,'comments':'all fields are required',"status": True}
                return Response(response_data)
            else:
                sub_obj=Subcategory.objects.filter(id__in=s_id)
                brand_obj=Brands.objects.filter(subcategory__in=sub_obj)
                if brand_obj:
                    dat_dict={}
                    data_list=[]
                    for x in brand_obj:
                        dat_dict={'subcategory_id':x.subcategory.id,'subcategory_name':x.subcategory.name,
                           'brand_id':x.id,'brand_name':x.name,'brand_image':str(x.image)}
                        data_list.append(dat_dict)
                    shop_dict={"products_details":data_list,'response_code':200,'comments':'all list',"status": True}
                    return Response(shop_dict)
                else:
                    response_data = {'response_code':200,'comments':'brand is not exsit',"status": False}
                    return Response(response_data)

        except:
            response_data = {'response_code':200,'comments':'subcategory is not exsit',"status": False}
            return Response(response_data)
        

        

############################start login api ####################
class Login_check(ViewSet):
    def create(self,request):
        data=request.data
        email1=data.get('email')
        password1=data.get('password')
        
        user1=authenticate(username=email1,password=password1)
        # if user1.check_password(password1):
        if user1 is not None:
            print('----')
            try:
                print('--#333--')
                user_instance = User_register.objects.get(user=user1)
                print('----')
                if user_instance.status==True:
                    user_det=User.objects.get(username=email1)
                    user_reg=User_register.objects.get(user=user_det)
                    sending_data=[]
                    userdata={'id':user_det.id,'email':user_det.username,'first_name':user_det.first_name,'last_name':user_det.last_name,'image':str(user_reg.profile_pic),'address':user_reg.address,'phone':user_reg.mobile,'status':user_reg.status,'gender':user_reg.gender,'latitude':user_reg.latitude,'longitude':user_reg.longitude}
                    sending_data.append(userdata)
                    response_data = {'user_data':sending_data,'response_code':200,'comments':'user exist',"status": True}
                    return Response(response_data) 
                else:
                    response_data = {'response_code':200,'comments':'You are Block by Admin',"status": False}
                    return Response(response_data)
            except:
                
                vendor_instance = Vendor_registration.objects.get(user=user1)
                if vendor_instance.store_status==True:

                    user_det=User.objects.get(username=email1)
                    vender=Vendor_registration.objects.get(user=user_det)
                    serdata=VendorRegisterSerializers(vender)
                    response_data = {'user_data':serdata.data,'response_code':200,'comments':'login is successful',"status": True}
                    return Response(response_data)
                else:
                    response_data = {'response_code':200,'comments':'You are Block by Admin',"status": False}
                    return Response(response_data)
        else:
            response_data = {'response_code':200,'comments':'user is not match',"status": False}
            return Response(response_data) 
        ####################end login api ####################
############################start logout api ####################


class Logout_check(ViewSet):
    def list(self,request):
        logout(request)
        response_data = {'response_code':200,'comments':'logout is successful',"status": True}
        return Response(response_data)     

class Contactall(ViewSet):
    def create(self,request):
        datas=request.data
        name1=datas.get('name')
        email1=datas.get('email')
        mobile1=datas.get('mobile')
        message1=datas.get('message')
        try:
            cont_qr=contact(name=name1,email=email1,mobile=mobile1,message=message1)
            cont_qr.save()
            response_data = {'response_code':200,'comments':'contact is created',"status": True}
            return Response(response_data)
        except:
            response_data = {'response_code':200,'comments':'contacts is not none',"status": False}
            return Response(response_data) 
    def list(self,request):
        query=contact.objects.all()
        serilizer=ContactSerializer(query,many=True)
        contact={'contact':serilizer.data,'response_code':200,'comments':'all list',"status": True}
        return Response(contact)
    def destory(self,request,id=None):
        try:
            dt=contact.objects.get(id=id)
            dt.delete()
            return Response('contact is deleted')
        except contact.DoesNotExist:
            return Response('contact is not available')


class BannerALL(ViewSet):
    def list(self,request):
        query=Banner.objects.all()
        ser=BannerSerializer(query,many=True)
        banner={'Banner':ser.data,'response_code':200,'comments':'all list',"status": True}
        return Response(banner)

class Bottom_BannerAll(ViewSet):
    def list(self,request):
        query=Bottom_Banner.objects.all()
        ser=Bottom_BannerSerializer(query,many=True)
        banner={'bottom_banner':ser.data,'response_code':200,'comments':'all list',"status": True}
        return Response(banner)




# ################################### mail sendin function ##################
def send_conformation_email(request,rand_otp):
    email = request.session.get('email')
    if email:
        subject = "Welcome To AVPL"
        message = "This is your OTP "+str(rand_otp)
        recepient = str(email)
        #html_message = render_to_string('home/send_order_report.html', context)
        #plain_message = strip_tags(html_message)
        #from_email = settings.EMAIL_HOST_USER
        #to = email
        send_mail(subject, message,EMAIL_HOST_USER,[recepient],fail_silently=False)
    else:
        return False



################################### end mail sendin function ##################


class Forget_password(ViewSet):
    def create(self,request):
        data=request.data
        request.session['email'] =data.get('email')
        email = request.session.get('email')
        print(email)
        try:

            check_email = User.objects.get(username=email)
            OTP = randint(1111, 9999)
            if check_email:
                    try:
                        otp = Otp.objects.get(email=email)
                        otp.otp = OTP
                        otp.save()
                    except:
                        otp = Otp(email=email, otp=OTP)
                        otp.save()
                    send_conformation_email(request,OTP)
                    response_data = {'response_code':200,'comments':'otp is send to mail',"status": True}
                    return Response(response_data)
        except:
            response_data = {'response_code':200,'comments':'email is not register',"status": True}
            return Response(response_data)

class Forget_Password_Verify_Otp(ViewSet):
    def create(self,request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        password1 = request.data.get('password')
        password2 = request.data.get('repassword')
        otp_featch = Otp.objects.get(email=email)
        print(password1,password2,otp,email)
        if otp_featch.otp == otp:
            if password1 == password2:
                reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
                # compiling regex
                match_re = re.compile(reg)
                # searching regex
                res = re.search(match_re, password1)
                if res:
                    user_featch  = User.objects.get(username=email)
                    user_featch.password = make_password(password1)
                    user_featch.save()
                    response_data = {'response_code':200,'comments':'password changed successfully..',"status": True}
                    return Response(response_data)
                else:
                    response_data = {'response_code':200,'comments':'Passowrd must be strong..or min 8 char',"status": False}
                    return Response(response_data)
            else:
                response_data = {'response_code':200,'comments':'Password and confirm password not match..',"status": False}
                return Response(response_data)
        else:
            response_data = {'response_code':200,'comments':'Otp not Vaild..',"status": False}
            return Response(response_data)

class Forget_Password_Resend_Otp(ViewSet):
    def create(self,request):
        email = request.session.get('email')
        try:
            otp = randint(1111, 9999)
            otp_update = Otp.objects.get(email=email)
            otp_update.otp = otp
            otp_update.save()
            send_conformation_email(request,otp)
            response_data = {'response_code':200,'comments':'Resend OTP Successfully on your register Email..',"status": True}
            return Response(response_data)
        except:
            response_data = {'response_code':200,'comments':'apply Forget_Password_Verify_Otp ',"status": False}
            return Response(response_data)



################### end forget resend otp #######



class Addres_Search_For_Shop(ViewSet):
    def create(self,request):
        category = request.data.get('category')
        address = request.data.get('address')
        if address != '':
                gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
                add_lat_long = gmaps.geocode(address)
                user_lat = add_lat_long[0]['geometry']['location']['lat']
                user_lng = add_lat_long[0]['geometry']['location']['lng']
                newport_ri = (user_lat, user_lng)
                print('useraddrs',newport_ri)
                li = []
                print('code run hua yha tk ab pta  nhi....')
                obj = Vendor_Store_detail.objects.all()
                for x in obj:
                    cleveland_oh = (x.store_latitude, x.store_longitude)
                    print('shop',cleveland_oh)
                    c = geodesic(newport_ri, cleveland_oh).miles
                    Km = c / 0.62137
                    print('km',Km)
                    if Km <=10:
                        user_instance = User.objects.get(username=x.user)
                        li.append(user_instance)
                if category:
                    shop = Vendor_Store_detail.objects.filter(user__in=li).filter(store_category=category)
                    if shop:
                        vend_serlizer=VendorStoreDetailSerializers(shop,many=True)
                        # category = Category.objects.all()
                        # serilizer=CategorySerializer_only(category,many=True)
                        dat={'shop':vend_serlizer.data,'response_code':200,'comments':'all list',"status": True}
                        return Response(dat)
                    else:
                        # category = Category.objects.all()
                        # serilizer=CategorySerializer_only(category,many=True)
                        dat={'response_code':200,'comments':'No store found Search any other address',"status": False}
                        return Response(dat)
                else:
                    shop = Vendor_Store_detail.objects.filter(user__in=li)
                    if shop:
                        vend_serlizer=VendorStoreDetailSerializers(shop,many=True)
                        # category = Category.objects.all()
                        # serilizer=CategorySerializer_only(category,many=True)
                        dat={'shop':vend_serlizer.data,'response_code':200,'comments':'all list',"status": True}
                        return Response(dat)
                    else:
                        # category = Category.objects.all()
                        # serilizer=CategorySerializer_only(category,many=True)
                        dat={'response_code':200,'comments':'No store found Search any other address',"status": False}
                        return Response(dat)

        else:
            dat={'response_code':200,'comments':'enter address',"status": False}
            return Response(dat)
    


class Addres_Search_For_Shop_after_Login(ViewSet):
    def create(self,request):
        email1=request.data.get('user_email')
        category = request.data.get('category')
        address = request.data.get('address')
        
        if address != '':
            gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
            add_lat_long = gmaps.geocode(address)
            user_lat = add_lat_long[0]['geometry']['location']['lat']
            user_lng = add_lat_long[0]['geometry']['location']['lng']
            try:

                user_instance = User.objects.get(username =email1)
                try: 
                    fatch_random_address = random_address.objects.get(user=user_instance)
                    if fatch_random_address:
                        fatch_random_address.address = address
                        fatch_random_address.latitude = user_lat
                        fatch_random_address.longitude = user_lng
                        fatch_random_address.save()
                        print('i am update')
                except:
                    raandom_address = random_address(user=user_instance,address=address,latitude=user_lat,longitude=user_lng)
                    raandom_address.save()
                    # return redirect('/')
                # obj = User.objects.get(username =email1)
                adrs = random_address.objects.get(user=user_instance)
                lat = adrs.latitude
                lng = adrs.longitude
                objs = Vendor_Store_detail.objects.all()
                newport_ri = (lat, lng)
                li = []
                print('code run hua yha tk ab pta  nhi....')
                for x in objs:
                    # print(x.store_latitude,x.store_longitude)

                    cleveland_oh = (x.store_latitude, x.store_longitude)
                    c = geodesic(newport_ri, cleveland_oh).miles
                    Km = c / 0.62137
                    if Km <=10:
                        user_instance = User.objects.get(username=x.user)
                        li.append(user_instance)
                if category:
                    shop = Vendor_Store_detail.objects.filter(user__in=li).filter(store_category=category)
                    if shop:
                        vend_serlizer=VendorStoreDetailSerializers(shop,many=True)
        
                        dat={'shop': vend_serlizer.data,'response_code':200,'comments':'all list',"status": True}
                        return Response(dat)
                    else:

                        dat={'response_code':200,'comments':'shop is not in your location',"status": False}
                        return Response(dat)
                else:
                    shop = Vendor_Store_detail.objects.filter(user__in=li)
                    if shop:
                        vend_serlizer=VendorStoreDetailSerializers(shop,many=True)
                        dat={'shop': vend_serlizer.data, 'response_code':200,'comments':'all list',"status": True}
                        return Response(dat)
                    else:
                        dat={'response_code':200,'comments':'shop is not in your location',"status": False}
                        return Response(dat)
            except:
                dat={'response_code':200,'comments':'user not exist',"status": False}
                return Response(dat)

        else:
            dat={'response_code':200,'comments':'enter address',"status": False}
            return Response(dat)








class ProductALL(ViewSet):
    def list(self,request):
        product_obj=Product.objects.all()
        if product_obj:

            dat_dict={}
            data_list=[]

            for x in product_obj:
                dat_dict={'vendor_id':x.user.id,'vendor_email':x.user.username,'first_name':x.user.first_name,'last_name':x.user.last_name,
                'category_id':x.category.id,'category_name':x.category.name,'subcategory_id':x.subcategory.id,'subcategory_name':x.subcategory.name,
                'brand_id':x.brand_name.id,'brand_name':x.brand_name.name,'product_id':x.id,'product_title':x.title,'product_price':x.price,'product_discount_percent':x.discount_percent,
                'product_gst_percent':x.gst_percent,'product_variant':x.variant,
                'product_image':str(x.image),'product_status':x.status
                }
                data_list.append(dat_dict)
            shop_dict={"product_details":data_list,'response_code':200,'comments':'all list',"status": True}
           
            return Response(shop_dict)
        else:
            shop_dict={'response_code':200,'comments':'no details of shop',"status": False}
            return Response(shop_dict)
    def create(self,request):
        stor_id=request.data.get('stor_id')
        dat_dict={}
        data_list=[]
        if stor_id:
            stor_inst=Vendor_Store_detail.objects.filter(id__in=stor_id)
            if stor_inst:
                product_obj=Product.objects.filter(stor_details__in=stor_inst)
                if product_obj:
                    for x in product_obj:
                        dat_dict={'vendor_id':x.user.id,'vendor_email':x.user.username,'first_name':x.user.first_name,'last_name':x.user.last_name,
                            'category_id':x.category.id,'category_name':x.category.name,'subcategory_id':x.subcategory.id,'subcategory_name':x.subcategory.name,
                            'brand_id':x.brand_name.id,'brand_name':x.brand_name.name,'product_id':x.id,'product_title':x.title,'product_price':x.price,'product_discount_percent':x.discount_percent,
                            'product_gst_percent':x.gst_percent,'product_variant':x.variant,
                                'product_image':str(x.image),'product_status':x.status}
                        data_list.append(dat_dict)
                    shop_dict={"products_details":data_list,'response_code':200,'comments':'all list',"status": True}
                    return Response(shop_dict)
                else:
                    response_data = {'response_code':200,'comments':'product is not exsit',"status": False}
                    return Response(response_data)
            else:
                response_data = {'response_code':200,'comments':'stor is not exsit',"status": False}
                return Response(response_data)

        else:
            response_data = {'response_code':200,'comments':'all fields required',"status": False}
            return Response(response_data)
        


    


        

class ImageAll(ViewSet):
    def list(self,request):
        image_obj=Images.objects.all()
        if image_obj:
            data_list=[]
            data_dict={}
            for x in image_obj:
                data_dict={'product_id':x.product.id,'image_id':x.id,'image_title':x.title,'image_url':x.image}
                data_list.append(data_dict)
            pt={'image_details':data_list,'response_code':200,'comments':'all list',"status": True}
            return Response(pt)
        else:
            res={'response_code':200,'comments':'no list',"status": False}
            return Response(res)


class ColorSizeBrandAll(ViewSet):
    def list(self,request):
        color_obj=Color.objects.all()
        size_obje=Size.objects.all()
        brand_obj=Brands.objects.all()
        color_dict={}
        color_list=[]
        size_dict={}
        size_list=[]
        brand_dict={}
        brand_list=[]
        for x in color_obj:
            color_dict={'color_id':x.id,'color_name':x.name,'color_code':x.code}
            color_list.append(color_dict)
        for y in size_obje:
            size_dict={'size_id':y.id,'size_name':y.name,'size_code':y.code}
            size_list.append(size_dict)
        for z in brand_obj:
            brand_dict={'brand_id':z.id,'brand_name':z.name,'brand_image':str(z.image)}
            brand_list.append(brand_dict)

        ct={'brand_details':brand_list,"color_details":color_list,'size_details':size_list,'response_code':200,'comments':'all list',"status": True}
        return Response(ct)
        

class VariantsAll(ViewSet):
    def create(self,request):
        brand_id=request.data.get('brand_id')
        size_id=request.data.get('size_id')
        color_id=request.data.get('color_id')
        try:
            brand_objet=Brands.objects.filter(id__in=brand_id)
            product_obj=Product.objects.filter(brand_name__in=brand_objet)
            size_obj=Size.objects.filter(id__in=size_id)
            color_obj=Color.objects.filter(id__in=color_id)
            data_dict={}
            data_list=[]
            if brand_id and size_id and color_id:
                vernt_obj=Variants.objects.filter(product__in=product_obj).filter(size__in=size_obj).filter(color__in=color_obj)
                if vernt_obj:
                    for x in vernt_obj:
                        data_dict={'variant_id':x.id,'variant_title':x.title,'variant_description':x.description,'variant_image_fornt':str(x.image_fornt),'variant_image_back':str(x.image_back),'variant_image_side':str(x.image_side),
                        'variant_quantity':x.quantity,'variant_price':x.price,'variant_weight':x.weight,'variant_point_value':x.point_value,
                        'product_id':x.product.id,'product_title':x.product.title,'product_price':x.product.price,'product_brand_id':x.product.brand_name.id,'product_brand_name':x.product.brand_name.name,'product_subcategory_id':x.product.subcategory.id,'product_subcategory_name':x.product.subcategory.name,'product_category_id':x.product.category.id,'product_category_name':x.product.category.name,'vandor_id':x.product.user.id,'vendor_email':x.product.user.username,
                         'variant_color_id':x.color.id,'variant_color_name':x.color.name,'variant_size_id':x.size.id,'variant_size_name':x.size.name
                        }
                        data_list.append(data_dict)
                    dt={'variant_details':data_list,'response_code':200,'comments':'all list',"status": True} 
                    return Response(dt)
                else:
                    dt={'response_code':200,'comments':'no list',"status": False} 
                    return Response(dt)

            elif brand_id and size_id:
                vernt_obj=Variants.objects.filter(product__in=product_obj).filter(size__in=size_obj)
                if vernt_obj:

                    for x in vernt_obj:
                        data_dict={'variant_id':x.id,'variant_title':x.title,'variant_description':x.description,'variant_image_fornt':str(x.image_fornt),'variant_image_back':str(x.image_back),'variant_image_side':str(x.image_side),
                        'variant_quantity':x.quantity,'variant_price':x.price,'variant_weight':x.weight,'variant_point_value':x.point_value,
                        'product_id':x.product.id,'product_title':x.product.title,'product_price':x.product.price,'product_brand_id':x.product.brand_name.id,'product_brand_name':x.product.brand_name.name,'product_subcategory_id':x.product.subcategory.id,'product_subcategory_name':x.product.subcategory.name,'product_category_id':x.product.category.id,'product_category_name':x.product.category.name,'vandor_id':x.product.user.id,'vendor_email':x.product.user.username,
                        'variant_color_id':x.color.id,'variant_color_name':x.color.name,'variant_size_id':x.size.id,'variant_size_name':x.size.name
                        }
                        data_list.append(data_dict)
                    dt={'variant_details':data_list,'response_code':200,'comments':'all list',"status": True} 
                    return Response(dt)
                else:
                    dt={'response_code':200,'comments':'no list',"status": False} 
                    return Response(dt)
            
            elif size_id and color_id:
                vernt_obj=Variants.objects.filter(size__in=size_obj).filter(color__in=color_obj)
                if vernt_obj:

                    for x in vernt_obj:
                        data_dict={'variant_id':x.id,'variant_title':x.title,'variant_description':x.description,'variant_image_fornt':str(x.image_fornt),'variant_image_back':str(x.image_back),'variant_image_side':str(x.image_side),
                        'variant_quantity':x.quantity,'variant_price':x.price,'variant_weight':x.weight,'variant_point_value':x.point_value,
                        'product_id':x.product.id,'product_title':x.product.title,'product_price':x.product.price,'product_brand_id':x.product.brand_name.id,'product_brand_name':x.product.brand_name.name,'product_subcategory_id':x.product.subcategory.id,'product_subcategory_name':x.product.subcategory.name,'product_category_id':x.product.category.id,'product_category_name':x.product.category.name,'vandor_id':x.product.user.id,'vendor_email':x.product.user.username,
                        'variant_color_id':x.color.id,'variant_color_name':x.color.name,'variant_size_id':x.size.id,'variant_size_name':x.size.name
                        }
                        data_list.append(data_dict)
                    dt={'variant_details':data_list,'response_code':200,'comments':'all list',"status": True} 
                    return Response(dt)
                else:
                    dt={'response_code':200,'comments':'no list',"status": False} 
                    return Response(dt)
                
            elif brand_id and color_id :
                vernt_obj=Variants.objects.filter(product__in=product_obj).filter(color__in=color_obj)
                if vernt_obj:

                    for x in vernt_obj:
                        data_dict={'variant_id':x.id,'variant_title':x.title,'variant_description':x.description,'variant_image_fornt':str(x.image_fornt),'variant_image_back':str(x.image_back),'variant_image_side':str(x.image_side),
                        'variant_quantity':x.quantity,'variant_price':x.price,'variant_weight':x.weight,'variant_point_value':x.point_value,
                        'product_id':x.product.id,'product_title':x.product.title,'product_price':x.product.price,'product_brand_id':x.product.brand_name.id,'product_brand_name':x.product.brand_name.name,'product_subcategory_id':x.product.subcategory.id,'product_subcategory_name':x.product.subcategory.name,'product_category_id':x.product.category.id,'product_category_name':x.product.category.name,'vandor_id':x.product.user.id,'vendor_email':x.product.user.username,
                        'variant_color_id':x.color.id,'variant_color_name':x.color.name,'variant_size_id':x.size.id,'variant_size_name':x.size.name
                        }
                        data_list.append(data_dict)
                    dt={'variant_details':data_list,'response_code':200,'comments':'all list',"status": True} 
                    return Response(dt)
                else:
                    dt={'response_code':200,'comments':'no list',"status": False} 
                    return Response(dt)
            elif brand_id:
                vernt_obj=Variants.objects.filter(product__in=product_obj)
                if vernt_obj:

                    for x in vernt_obj:
                        data_dict={'variant_id':x.id,'variant_title':x.title,'variant_description':x.description,'variant_image_fornt':str(x.image_fornt),'variant_image_back':str(x.image_back),'variant_image_side':str(x.image_side),
                        'variant_quantity':x.quantity,'variant_price':x.price,'variant_weight':x.weight,'variant_point_value':x.point_value,
                        'product_id':x.product.id,'product_title':x.product.title,'product_price':x.product.price,'product_brand_id':x.product.brand_name.id,'product_brand_name':x.product.brand_name.name,'product_subcategory_id':x.product.subcategory.id,'product_subcategory_name':x.product.subcategory.name,'product_category_id':x.product.category.id,'product_category_name':x.product.category.name,'vandor_id':x.product.user.id,'vendor_email':x.product.user.username,
                        'variant_color_id':x.color.id,'variant_color_name':x.color.name,'variant_size_id':x.size.id,'variant_size_name':x.size.name
                        }
                        data_list.append(data_dict)
                    dt={'variant_details':data_list,'response_code':200,'comments':'all list',"status": True} 
                    return Response(dt)
                else:
                    dt={'response_code':200,'comments':'no list',"status": False} 
                    return Response(dt)
            elif size_id:
                vernt_obj=Variants.objects.filter(size__in=size_obj)
                if vernt_obj:

                    for x in vernt_obj:
                        data_dict={'variant_id':x.id,'variant_title':x.title,'variant_description':x.description,'variant_image_fornt':str(x.image_fornt),'variant_image_back':str(x.image_back),'variant_image_side':str(x.image_side),
                        'variant_quantity':x.quantity,'variant_price':x.price,'variant_weight':x.weight,'variant_point_value':x.point_value,
                        'product_id':x.product.id,'product_title':x.product.title,'product_price':x.product.price,'product_brand_id':x.product.brand_name.id,'product_brand_name':x.product.brand_name.name,'product_subcategory_id':x.product.subcategory.id,'product_subcategory_name':x.product.subcategory.name,'product_category_id':x.product.category.id,'product_category_name':x.product.category.name,'vandor_id':x.product.user.id,'vendor_email':x.product.user.username,
                        'variant_color_id':x.color.id,'variant_color_name':x.color.name,'variant_size_id':x.size.id,'variant_size_name':x.size.name
                        }
                        data_list.append(data_dict)
                    dt={'variant_details':data_list,'response_code':200,'comments':'all list',"status": True} 
                    return Response(dt)
                else:
                    dt={'response_code':200,'comments':'no list',"status": False} 
                    return Response(dt)
            elif color_id:
                vernt_obj=Variants.objects.filter(color__in=color_obj)
                if vernt_obj:

                    for x in vernt_obj:
                        data_dict={'variant_id':x.id,'variant_title':x.title,'variant_description':x.description,'variant_image_fornt':str(x.image_fornt),'variant_image_back':str(x.image_back),'variant_image_side':str(x.image_side),
                        'variant_quantity':x.quantity,'variant_price':x.price,'variant_weight':x.weight,'variant_point_value':x.point_value,
                        'product_id':x.product.id,'product_title':x.product.title,'product_price':x.product.price,'product_brand_id':x.product.brand_name.id,'product_brand_name':x.product.brand_name.name,'product_subcategory_id':x.product.subcategory.id,'product_subcategory_name':x.product.subcategory.name,'product_category_id':x.product.category.id,'product_category_name':x.product.category.name,'vandor_id':x.product.user.id,'vendor_email':x.product.user.username,
                        'variant_color_id':x.color.id,'variant_color_name':x.color.name,'variant_size_id':x.size.id,'variant_size_name':x.size.name
                        }
                        data_list.append(data_dict)
                    dt={'variant_details':data_list,'response_code':200,'comments':'all list',"status": True} 
                    return Response(dt)
                else:
                    dt={'response_code':200,'comments':'no list',"status": False} 
                    return Response(dt)
            else:
                vernt_obj=Variants.objects.all()
                for x in vernt_obj:
                    data_dict={'variant_id':x.id,'variant_title':x.title,'variant_description':x.description,'variant_image_fornt':str(x.image_fornt),'variant_image_back':str(x.image_back),'variant_image_side':str(x.image_side),
                    'variant_quantity':x.quantity,'variant_price':x.price,'variant_weight':x.weight,'variant_point_value':x.point_value,
                    'product_id':x.product.id,'product_title':x.product.title,'product_price':x.product.price,'product_brand_id':x.product.brand_name.id,'product_brand_name':x.product.brand_name.name,'product_subcategory_id':x.product.subcategory.id,'product_subcategory_name':x.product.subcategory.name,'product_category_id':x.product.category.id,'product_category_name':x.product.category.name,'vandor_id':x.product.user.id,'vendor_email':x.product.user.username,
                    'variant_color_id':x.color.id,'variant_color_name':x.color.name,'variant_size_id':x.size.id,'variant_size_name':x.size.name
                    }
                    data_list.append(data_dict)
                dt={'variant_details':data_list,'response_code':200,'comments':'all list',"status": True} 
                return Response(dt)
        except:
            dt={'response_code':200,'comments':'no list',"status": False} 
            return Response(dt)

           
class VariantbySubcategryStor(ViewSet):
    def create(self,request):
        stor_id=request.data.get('stor_id')
        subcat_id=request.data.get('subcat_id')
        try:

            stor_inst=Vendor_Store_detail.objects.filter(id__in=stor_id)
            subcat_inst=Subcategory.objects.filter(id__in=subcat_id)
            data_dict={}
            data_list=[]
            if stor_id and subcat_id:
                product_obj=Product.objects.filter(stor_details__in=stor_inst).filter(subcategory__in=subcat_inst)
                vernt_obj=Variants.objects.filter(product__in=product_obj)
                if vernt_obj:
                    for x in vernt_obj:
                        data_dict={'variant_id':x.id,'variant_title':x.title,'variant_description':x.description,'variant_image_fornt':str(x.image_fornt),'variant_image_back':str(x.image_back),'variant_image_side':str(x.image_side),
                                'variant_quantity':x.quantity,'variant_price':x.price,'variant_weight':x.weight,'variant_point_value':x.point_value,
                                'product_id':x.product.id,'product_title':x.product.title,'product_price':x.product.price,'product_brand_id':x.product.brand_name.id,'product_brand_name':x.product.brand_name.name,'product_subcategory_id':x.product.subcategory.id,'product_subcategory_name':x.product.subcategory.name,'product_category_id':x.product.category.id,'product_category_name':x.product.category.name,'vandor_id':x.product.user.id,'vendor_email':x.product.user.username,
                                'variant_color_id':x.color.id,'variant_color_name':x.color.name,'variant_size_id':x.size.id,'variant_size_name':x.size.name
                                }
                        data_list.append(data_dict)
                    dt={'variant_details':data_list,'response_code':200,'comments':'all list',"status": True} 
                    return Response(dt)
                else:
                    dt={'response_code':200,'comments':'no list',"status": False} 
                    return Response(dt)
            elif stor_id:
                product_obj=Product.objects.filter(stor_details__in=stor_inst)
                vernt_obj=Variants.objects.filter(product__in=product_obj)
                if vernt_obj:
                    for x in vernt_obj:
                        data_dict={'variant_id':x.id,'variant_title':x.title,'variant_description':x.description,'variant_image_fornt':str(x.image_fornt),'variant_image_back':str(x.image_back),'variant_image_side':str(x.image_side),
                                'variant_quantity':x.quantity,'variant_price':x.price,'variant_weight':x.weight,'variant_point_value':x.point_value,
                                'product_id':x.product.id,'product_title':x.product.title,'product_price':x.product.price,'product_brand_id':x.product.brand_name.id,'product_brand_name':x.product.brand_name.name,'product_subcategory_id':x.product.subcategory.id,'product_subcategory_name':x.product.subcategory.name,'product_category_id':x.product.category.id,'product_category_name':x.product.category.name,'vandor_id':x.product.user.id,'vendor_email':x.product.user.username,
                                'variant_color_id':x.color.id,'variant_color_name':x.color.name,'variant_size_id':x.size.id,'variant_size_name':x.size.name
                                }
                        data_list.append(data_dict)
                    dt={'variant_details':data_list,'response_code':200,'comments':'all list',"status": True} 
                    return Response(dt)
                else:
                    dt={'response_code':200,'comments':'no list',"status": False} 
                    return Response(dt)
            elif subcat_id:
                product_obj=Product.objects.filter(subcategory__in=subcat_inst)
                vernt_obj=Variants.objects.filter(product__in=product_obj)
                if vernt_obj:
                    for x in vernt_obj:
                        data_dict={'variant_id':x.id,'variant_title':x.title,'variant_description':x.description,'variant_image_fornt':str(x.image_fornt),'variant_image_back':str(x.image_back),'variant_image_side':str(x.image_side),
                                'variant_quantity':x.quantity,'variant_price':x.price,'variant_weight':x.weight,'variant_point_value':x.point_value,
                                'product_id':x.product.id,'product_title':x.product.title,'product_price':x.product.price,'product_brand_id':x.product.brand_name.id,'product_brand_name':x.product.brand_name.name,'product_subcategory_id':x.product.subcategory.id,'product_subcategory_name':x.product.subcategory.name,'product_category_id':x.product.category.id,'product_category_name':x.product.category.name,'vandor_id':x.product.user.id,'vendor_email':x.product.user.username,
                                'variant_color_id':x.color.id,'variant_color_name':x.color.name,'variant_size_id':x.size.id,'variant_size_name':x.size.name
                                }
                        data_list.append(data_dict)
                    dt={'variant_details':data_list,'response_code':200,'comments':'all list',"status": True} 
                    return Response(dt)
            else:
                vernt_obj=Variants.objects.all()
                for x in vernt_obj:
                    data_dict={'variant_id':x.id,'variant_title':x.title,'variant_description':x.description,'variant_image_fornt':str(x.image_fornt),'variant_image_back':str(x.image_back),'variant_image_side':str(x.image_side),
                    'variant_quantity':x.quantity,'variant_price':x.price,'variant_weight':x.weight,'variant_point_value':x.point_value,
                    'product_id':x.product.id,'product_title':x.product.title,'product_price':x.product.price,'product_brand_id':x.product.brand_name.id,'product_brand_name':x.product.brand_name.name,'product_subcategory_id':x.product.subcategory.id,'product_subcategory_name':x.product.subcategory.name,'product_category_id':x.product.category.id,'product_category_name':x.product.category.name,'vandor_id':x.product.user.id,'vendor_email':x.product.user.username,
                    'variant_color_id':x.color.id,'variant_color_name':x.color.name,'variant_size_id':x.size.id,'variant_size_name':x.size.name
                    }
                    data_list.append(data_dict)
                dt={'variant_details':data_list,'response_code':200,'comments':'all list',"status": True} 
                return Response(dt)
        except:
            dt={'response_code':200,'comments':'no list',"status": False} 
            return Response(dt)

class VariantbySubcategry(ViewSet):
    def create(self, request):
        email1 = request.data.get('user_email')
        subcat_id = request.data.get('subcat_id')
        try:
            obj = User.objects.get(username=email1)
            adrs = random_address.objects.get(user=obj)
            lat = adrs.latitude
            lng = adrs.longitude
            newport_ri = (lat, lng)
            objs = Vendor_Store_detail.objects.all()
            li = []
            for x in objs:
                # print(x.store_latitude,x.store_longitude)
                cleveland_oh = (x.store_latitude, x.store_longitude)
                c = geodesic(newport_ri, cleveland_oh).miles
                Km = c / 0.62137
                if Km <= 10:
                    user_instance = User.objects.get(username=x.user)
                    li.append(user_instance)
            if subcat_id:
                shop = Vendor_Store_detail.objects.filter(user__in=li)
                try:
                    subcat_inst = Subcategory.objects.get(id=subcat_id)
                    data_dict = {}
                    data_list = []
                    if subcat_inst:
                        product_obj = Product.objects.filter(subcategory=subcat_inst).filter(stor_details__in=shop)
                        vernt_obj = Variants.objects.filter(product__in=product_obj)
                        if vernt_obj:
                            for x in vernt_obj:
                                data_dict = {'variant_id': x.id, 'variant_title': x.title,
                                             'variant_description': x.description,
                                             'variant_image_fornt': str(x.image_fornt),
                                             'variant_image_back': str(x.image_back),
                                             'variant_image_side': str(x.image_side),
                                             'variant_quantity': x.quantity, 'variant_price': x.price,
                                             'variant_weight': x.weight, 'variant_point_value': x.point_value,
                                             'product_id': x.product.id, 'product_title': x.product.title,
                                             'product_price': x.product.price,
                                             'product_brand_id': x.product.brand_name.id,
                                             'product_brand_name': x.product.brand_name.name,
                                             'product_subcategory_id': x.product.subcategory.id,
                                             'product_subcategory_name': x.product.subcategory.name,
                                             'product_category_id': x.product.category.id,
                                             'product_category_name': x.product.category.name,
                                             'vandor_id': x.product.user.id,
                                             'vendor_email': x.product.user.username,
                                             'variant_color_id': x.color.id, 'variant_color_name': x.color.name,
                                             'variant_size_id': x.size.id, 'variant_size_name': x.size.name
                                             }
                                data_list.append(data_dict)
                            dt = {'variant_details': data_list, 'response_code': 200, 'comments': 'all list',
                                  "status": True}
                            return Response(dt)
                        else:
                            dt = {'response_code': 200, 'comments': 'no variant list', "status": False}
                            return Response(dt)
                except:
                    dt = {'response_code': 200, 'comments': 'no  subcategry list', "status": False}
                    return Response(dt)

            else:
                dt = {'response_code': 200, 'comments': 'no   list', "status": False}
                return Response(dt)
        except:
            dt = {'response_code': 200, 'comments': 'no id', "status": False}
            return Response(dt)