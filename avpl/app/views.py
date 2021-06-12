from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from random import randint
from django.contrib.auth.hashers import make_password
import razorpay
import re
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import geocoder
import googlemaps
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from django.conf import settings
from avpl.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.


def base(request):
    search = Category.objects.all()
    print(search)
    return {'cat':search}

def cart_count_show(request):
    if request.user.is_authenticated:
        cart_count = UserCart.objects.filter(user=request.user)
        cart = cart_count.count()
        print(cart)
        return {'cart_count':cart}
    else:
        cart_count = UserCart.objects.all()
        return {'cart_count': cart_count}
############################################## USER SECTION ALL WORK DONE HERE ##########################################


####################### For  addres to get store #####################

def addres_for_shop(request):
    banner = Banner.objects.all()
    if request.user.is_authenticated:
        print('datayha tk chlega hii..')
        if request.method == "POST":
            category = request.POST.get('category')
            address = request.POST.get('adrs')
            if address != '':
                gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
                add_lat_long = gmaps.geocode(address)
                user_lat = add_lat_long[0]['geometry']['location']['lat']
                user_lng = add_lat_long[0]['geometry']['location']['lng']
                user_instance = User.objects.get(username = request.user.username)
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
                    return redirect('/')
            obj = User.objects.get(username = request.user.username)
            adrs = random_address.objects.get(user=obj)
            lat = adrs.latitude
            lng = adrs.longitude
            obj = Vendor_Store_detail.objects.all()
            newport_ri = (lat, lng)
            li = []
            print('code run hua yha tk ab pta  nhi....')
            for x in obj:
                # print(x.store_latitude,x.store_longitude)

                cleveland_oh = (x.store_latitude, x.store_longitude)
                c = geodesic(newport_ri, cleveland_oh).miles
                Km = c / 0.62137
                if Km <= 10:
                    user_instance = User.objects.get(username=x.user)
                    li.append(user_instance)
            shop = Vendor_Store_detail.objects.filter(user__in=li).filter(store_category=category)
            if shop:
                category = Category.objects.all()
                return render(request, 'home.html', {'ob': shop, 'category': category,'banner':banner})
            else:
                category = Category.objects.all()
                messages.error(request,'No shop found in your provided range!!')
                return render(request, 'home.html',{'category':category,'banner':banner})
        else:
            return redirect('/')
    else:
        if request.method == "POST":
            category = request.POST.get('category')
            address = request.POST.get('adrs')
            if address != '':
                gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
                add_lat_long = gmaps.geocode(address)
                user_lat = add_lat_long[0]['geometry']['location']['lat']
                user_lng = add_lat_long[0]['geometry']['location']['lng']
                newport_ri = (user_lat,user_lng)

                vendor_addres_get = Vendor_Store_detail.objects.all()
                li=[]
                for x in vendor_addres_get:
                    cleveland_oh=(x.store_latitude,x.store_longitude)
                    c=geodesic(newport_ri,cleveland_oh).miles
                    km = c/0.62137
                    if km <=10:
                        user_instance = User.objects.get(username=x.user)
                        li.append(user_instance)
                #user_instance = User.objects.get(username = x.user)
                #li.append(user_instance)
                vnedor_store_featch = Vendor_Store_detail.objects.filter(user__in=li).filter(store_category=category)
                if vnedor_store_featch:
                    category = Category.objects.all()
                    return render(request,'home.html',{'ob':vnedor_store_featch,'category':category,'banner':banner})
                else:
                    category = Category.objects.all()
                    messages.error(request,'No store found Search any other address.')
                    return render(request, 'home.html', {'category': category,'banner':banner})
            else:
                pass
        else:
            return redirect('/')



####################################################################

############################# home module work here ########################################
def home(request):
    banner = Banner.objects.all()
    #cat =Category.objects.all()
    #subcat = Subcategory.objects.all()
    #prod = Product.objects.all().order_by('id')
    #paginator = Paginator(prod, 6)
    #print(paginator)
    #page = request.GET.get('page')
    #try:
    #    page_obj = paginator.get_page(page)
    #except PageNotAnInteger:
     #   page_obj=paginator.page(1)
    #except EmptyPage:
     #   page_obj=paginator.page(paginator.num_pages)
    try:
        if request.user.is_authenticated:

            user_instance = User.objects.get(username=request.user.username)
            ob = random_address.objects.get(user=user_instance)
            obj = Vendor_Store_detail.objects.all()
            newport_ri = (ob.latitude, ob.longitude)
            li=[]
            for x in obj:
                #print(x.store_latitude,x.store_longitude)

                cleveland_oh = (x.store_latitude,x.store_longitude)
                c = geodesic(newport_ri, cleveland_oh).miles
                Km = c / 0.62137
                if Km <= 10:
                    user_instance = User.objects.get(username=x.user)
                    li.append(user_instance)

            category = Category.objects.all()
            prod = Product.objects.all()
            shop = Vendor_Store_detail.objects.filter(user__in=li)
            if shop:
                return render(request,'home.html',{'ob':shop,'product': prod, 'category': category,'banner':banner})
            else:
                messages.error(request,'No shop found in your range Please Search Shop.')
                return render(request,'home.html',{'category': category,'banner':banner})
        else:
            ob = Vendor_Store_detail.objects.all()
            category = Category.objects.all()
            prod = Product.objects.all()
            return render(request, 'home.html', {'ob': ob, 'category': category,'banner':banner})
    except:

        ob =Vendor_Store_detail.objects.all()
        category = Category.objects.all()
        prod = Product.objects.all()
        return render(request,'home.html',{'ob':ob,'category':category,'banner':banner})
    ################################## home end here ##########################################

########################## Product View Page ########################

def product_view_page(request,id):

    product_data = Product.objects.get(id=id)
    varient = Variants.objects.filter(product=product_data)
    print(varient,'ye vari hai..')
    c = []
    s = []
    for i in varient:
        if i.color:
            c.append(i.color.id)
        else:
            pass
        if i.size:
            s.append(i.size.id)
        else:
            pass
    cl = list(set(c))
    sl = list(set(s))
    color = Color.objects.filter(id__in=cl)
    if cl:
        size = Variants.objects.filter(product=id, color=cl[0])
    else:
        size = Variants.objects.filter(product=id)
    if request.method == 'POST':
        col_id1 = request.POST.get('color')
        size_id1 = request.POST.get("size")
        print(col_id1, size_id1, id)
        if col_id1!=None:
            size = Variants.objects.filter(product=id,color=col_id1)
        else:
            size=Variants.objects.filter(product=id)

        print(size)
        if col_id1 != None:
            col_id = int(col_id1)
        else:
            col_id = None
        if size_id1 != None:
            size_id = int(size_id1)
            l = []
            for k in size:
                l.append(k.size.id)
            if int(size_id1) in l:
                size_id = int(size_id1)
            else:
                if l:
                    size_id = l[0]
                else:
                    size_id = None
        else:
            if size[0].size:
                size_id = size[0].size.id
            else:
                size_id = None
    else:
        if cl:
            col_id = cl[0]
        else:
            col_id = None
        if sl:
            size_id = sl[0]
        else:
            size_id = None
    print(id, col_id, size_id)
    if col_id and size_id:
        for_price = Variants.objects.filter(product=id,color=col_id, size=size_id)
    elif col_id:
        for_price = Variants.objects.filter(product=id, color=col_id)
    else:
        for_price = Variants.objects.filter(product=id, size = size_id)
    print(for_price,'ye for pr')

    if for_price:
        price = for_price[0].price
        varient_id = for_price[0].id
    else:
        price = None
        varient_id = None

    print(varient_id, 'ye varient data hai..')
    for_image = Variants.objects.get(id=varient_id)

    context = {
        'prod': product_data,
        'varient': varient,
        'col_id': col_id,
        'color': color,
        'size': size,
        "size_id": size_id,
        'price': price,
        'varient_id':varient_id,
        'image':for_image,
    }
    print("**********************")


    return render(request,'product_view.html',context)


####################### End Product View page ######################

############################### Shop Section #####################################
def shop(request):
    if request.user.is_authenticated:
        randomm_address = random_address.objects.all()

    else:
        ob=Vendor_Store_detail.objects.all()
        return render(request,'shop.html',{'ob':ob})

############################### shop end here #################################



################################ Change Password User #########################
def ChangePassword(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            current_password=request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user=authenticate(username=request.user.username,password=current_password)
            if user is not None:
                if new_password==confirm_password:
                    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
                    # compiling regex
                    match_re = re.compile(reg)
                    # searching regex
                    res = re.search(match_re, new_password)
                    if res:
                        user_instance = User.objects.get(username=request.user.username)
                        user_instance.password=make_password(new_password)
                        user_instance.save()
                        messages.success(request,'Password Chnange Successfully..')
                        return render(request, 'change_password_dash.html')
                    else:
                        messages.error(request,'Password must be strong, Invalid Password..')
                        return render(request, 'change_password_dash.html')
                else:
                    messages.error(request,'New Password and Confirm Password not matched..')
                    return render(request, 'change_password_dash.html')
            else:
                messages.error(request,'Current Password Not valid..')
        return render(request,'change_password_dash.html')
    else:
        return redirect('/login')
############################## Change Password end here #########################


####################### User Dashboard Section #############################
def user_Dashboard(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            print('done done')
            profile_pic= request.FILES['pic']

            user=User.objects.get(username=request.user.username)
            print(user)
            ob = User_register.objects.get(user=user)
            print(ob)
            ob.profile_pic=profile_pic
            ob.save()


            print("done")
        return render(request,'user_profile_view.html')
    else:
        return redirect('/login')
######################### End User Dashboard Section #######################

# ###################### user profile edit end here #########################
#
def profile_edit(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            obj = User_register.objects.get(user=request.user)
            address = request.POST.get('adrs')
            print(address)
            gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
            add_lat_long = gmaps.geocode(address)
            user_lat = add_lat_long[0]['geometry']['location']['lat']
            user_lng = add_lat_long[0]['geometry']['location']['lng']
            obj.address=address
            obj.latitude = user_lat
            obj.longitude = user_lng
            obj.mobile = request.POST.get('mobile')
            obj.save()
            obb = User.objects.get(username=request.user)
            obb.first_name = request.POST.get('first_name')
            obb.last_name = request.POST.get('last_name')
            obb.save()
            return redirect('/userdashboard')
        else:
            #ob = User_register.objects.get(user=request.user)
            #print(ob.address)
            return render(request,'user_edit_profile.html')
    else:
        return redirect('/login')
#
# ##################### user profile end here #################


################################# Contact Form Work Done Here #################################

def Contact(request):
    if request.method == "POST":
        name= request.POST.get('name')
        email= request.POST.get('email')
        messaage= request.POST.get('message')
        phone= request.POST.get('phone')
        obj = contact(name=name,email=email,mobile=phone,message=messaage)
        obj.save()
        messages.success(request,'Your form has been submitted successfully')
    return render(request,'contact.html')

################################# End Contact Form Work Done Here #################################


################################# User Registration work done here #######################

def UserRegister(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            ########### session set here ################
            request.session['first_name']= request.POST.get('first_name')
            request.session['last_name']= request.POST.get('last_name')
            request.session['email']=request.POST.get('email')
            request.session['password1']=request.POST.get('password1')
            request.session['password2']=request.POST.get('password2')
            # request.session['question']=request.POST.get('name')
            # request.session['answer']=request.POST.get('answer')
            request.session['gender']=request.POST.get('gender')
            request.session['mobile']=request.POST.get('phone')
            request.session['address']=request.POST.get('adrs')
            ############ session get here##############
            email = request.session.get('email')
            password1 = request.session.get('password1')
            password2 = request.session.get('password2')
            try:
                exist = User.objects.get(username=email)
                messages.info(request,'This email is already exists try another email.')
                return redirect('/registration')
            except:
                if password1 == password2:
                    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
                    # compiling regex
                    match_re = re.compile(reg)
                    # searching regex
                    res = re.search(match_re, password1)

                    # validating conditions
                    if res:
                        otp = randint(1111, 9999)
                        try:
                            featch_otp = Otp.objects.get(email=email)
                            featch_otp.email=email
                            featch_otp.otp=otp
                            featch_otp.save()
                        except:
                            obb=Otp(email=email,otp=otp)
                            obb.save()

                        send_conformation_email(request,otp)
                        messages.success(request, 'OTP send on your register Email..Please Verify Email')
                        return render(request,"verify_gmail_otp.html")

                    else:
                        messages.error(request,'Password must be strong, Invalid Password')
                        print("Invalid Password")
                else:
                   messages.error(request,'Password and Confirm Password not matched..')
        return render(request,'user_registration.html')
#
# ########################### User Registration end here ###################

#
# ################################### mail sendin function ##################
def send_conformation_email(request,otp):
    email = request.session.get('email')
    print('codndition run here...')
    if email:
        print('here also run')
        subject = "Welcome To AVPL"
        message = "This is your OTP "+str(otp)
        recepient = str(email)
        #html_message = render_to_string('home/send_order_report.html', context)
        #plain_message = strip_tags(html_message)
        #from_email = settings.EMAIL_HOST_USER
        #to = email
        send_mail(subject, message,EMAIL_HOST_USER,[recepient],fail_silently=False)
    else:
        return False



################################### end mail sendin function ##################

################################ Gmail OTP VERIFY ##################

def gmail_otp(request):
    if request.method=="POST":
        first_name = request.session.get('first_name')
        last_name = request.session.get('last_name')
        password1 = request.session.get('password1')
        # question = request.session.get('question')
        gender = request.session.get('gender')
        # answer = request.session.get('answer')
        mobile = request.session.get('mobile')
        email=request.session.get('email')
        address = request.session.get('address')
        #user_instance = User.objects.get(username=email)
        #user_register_instance = User_register.objects.get(user=user_instance)
        otp_featch=Otp.objects.get(email=email)

        otp = request.POST.get('otp')

        if otp_featch.otp == str(otp):
            obj = User(username=email, first_name=first_name, last_name=last_name,password=make_password(password1))
            obj.save()  # here user save without refer
            ob = User.objects.get(username=obj.username)  # cretae instance for refercode saved
            gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
            add_lat_long = gmaps.geocode(address)
            user_lat = add_lat_long[0]['geometry']['location']['lat']
            user_lng = add_lat_long[0]['geometry']['location']['lng']
            obj = User_register(user=ob, mobile=mobile,gender=gender,otp=otp,status=True,address=address,latitude=user_lat,longitude=user_lng)
            obj.save()
            otp_featch.delete()
            randm_adrs=random_address(user=ob,latitude=user_lat,longitude=user_lng,address=address)
            randm_adrs.save()
            return redirect('/login')
        else:
            messages.error(request,'Invaild OTP..Please Provide Valid OTP')
            return render(request,'verify_gmail_otp.html')
    else:
        return redirect('/registration')


def resend_gmail_otp(request):
    email = request.session.get('email')
    #email = request.session.get('email')
    #user_instance = User.objects.get(username=email)
    #user_register_instance = User_register.objects.get(user=user_instance)
    otp = randint(1111, 9999)
    otp_update = Otp.objects.get(email=email)
    otp_update.otp=otp
    otp_update.save()

    send_conformation_email(request,otp)
    messages.success(request, 'Resend OTP Successfully on your register Email..Please Verify Email')
    return render(request, 'verify_gmail_otp.html')


############################ END GMAIL OTP VERIFY ################

######################### Change Password #########################



##################### End Change Password #######################

# ########################### Login module work done here #######################
def Login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            email=request.POST.get('email')
            print(email)
            password = request.POST.get('password')
            print('password--',password)
            print('yes yha tk chla 1')
            user = authenticate(username=email,password=password)
            print(user)
            print('yes yha tk chla 2')
            if user is not None:
                try:
                    user_instance = User_register.objects.get(user=user)
                    if user_instance.status==True:
                        login(request, user)
                        return redirect('/')
                    else:
                        messages.error(request, 'User Id or Password is Invalid..')
                        return render(request, 'login.html')
                except:
                    vendor_instance = Vendor_registration.objects.get(user=user)
                    if vendor_instance.vendor_status==True:
                        login(request, user)
                        return redirect('/')
                    else:
                        messages.error(request, 'User Id or Password is Invalid..')
                        return render(request, 'login.html')

                #messages.success(request,'login successfully..')
            else:
                messages.error(request,'User Id or Password is Invalid..')
        return render(request,'login.html')

# ########################### Login end here ##########################

# ######################## Logout module work done here ###############
def user_logout(request):
    logout(request)
    return redirect('/login')
#
# ######################## Logout end here ###########################


# ################################################# VENDOR ALL WORK DONE HERE ##################################################


###################### Vendor Registration ########################
#
def VendorRegister(request):
    if request.method=='POST':
        ########### session set here ################
        request.session['first_name'] = request.POST.get('first_name')
        request.session['last_name'] = request.POST.get('last_name')
        request.session['email'] = request.POST.get('email')
        request.session['password1'] = request.POST.get('password1')
        request.session['password2'] = request.POST.get('password2')

        request.session['gender'] = request.POST.get('gender')
        request.session['mobile'] = request.POST.get('phone')
        ############ session get here##############
        ############ session get here##############
        email = request.session.get('email')
        password1 = request.session.get('password1')
        password2 = request.session.get('password2')
        try:
            exist = User.objects.get(username=email)
            messages.info(request, 'This email is already exists try another email.')
            return redirect('/vendorregistration')
        except:
            if password1 == password2:
                reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
                # compiling regex
                match_re = re.compile(reg)
                # searching regex
                res = re.search(match_re, password1)

                # validating conditions
                if res:
                    otp = randint(1111, 9999)
                    try:
                        featch_otp = Otp.objects.get(email=email)
                        featch_otp.email = email
                        featch_otp.otp = otp
                        featch_otp.save()
                    except:
                        obb = Otp(email=email, otp=otp)
                        obb.save()

                    send_conformation_email(request,otp)
                    messages.success(request, 'OTP send on your register Email..Please Verify Email')
                    return render(request, "vendor_gmail_otp_verify.html")

                else:
                    messages.error(request, 'Password must be strong, Invalid Password')
                    print("Invalid Password")
            else:
                messages.error(request, 'Password and Confirm Password not matched..')
    return render(request,'vendor_registration.html')


###################### End vendor Registration ###################

################## Vendor gmail otp #############################
def vendor_otp(request):
    if request.method == "POST":
        first_name = request.session.get('first_name')
        last_name = request.session.get('last_name')
        password1 = request.session.get('password1')

        gender = request.session.get('gender')
        mobile = request.session.get('mobile')
        email = request.session.get('email')
        # user_instance = User.objects.get(username=email)
        # user_register_instance = User_register.objects.get(user=user_instance)
        otp_featch = Otp.objects.get(email=email)

        otp = request.POST.get('otp')

        if otp_featch.otp == str(otp):
            obj = User(username=email, first_name=first_name, last_name=last_name, password=make_password(password1))
            obj.save()  # here user save without refer
            ob = User.objects.get(username=obj.username)  # cretae instance for refercode saved
            obj = Vendor_registration(user=ob, store_mobile=mobile,profile_pic='tree_user_img.jpg', gender=gender,vendor_status=True)
            obj.save()
            otp_featch.delete()
            return redirect('/login')
        else:
            messages.error(request, 'Invaild OTP..Please Provide Valid OTP')
            return render(request, 'vendor_gmail_otp_verify.html')


################# vendor gmail otp end #######################

################### Vendor Resend Gmail OTP ##############
def vendor_resend_gmail_otp(request):
    email = request.session.get('email')
    #email = request.session.get('email')
    #user_instance = User.objects.get(username=email)
    #user_register_instance = User_register.objects.get(user=user_instance)
    otp = randint(1111, 9999)
    otp_update = Otp.objects.get(email=email)
    otp_update.otp=otp
    otp_update.save()

    send_conformation_email(request,otp)
    messages.success(request, 'Resend OTP Successfully on your register Email..Please Verify Email')
    return render(request, 'vendor_gmail_otp_verify.html')


###################vendor resend Gmail OTP ###############

##################### Vendor Register Store Detail ######################

def Vendor_register_store_detail(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            store_name = request.POST.get('store_name')
            store_address = request.POST.get('address')
            store_description = request.POST.get('store_description')
            store_logo = request.FILES['store_logo']
            store_banner = request.FILES['store_banner']
            store_image = request.FILES['store_image']
            store_category = request.POST.get('category')
            store_opening_time = request.POST.get('store_open_time')
            store_close_time = request.POST.get('store_close_time')
            store_cloasing_day = request.POST.get('store_day')
            store_registration_number = request.POST.get('store_registration_number')
            zipcode = request.POST.get('zipcode')
            user_instance = User.objects.get(username=request.user.username)
            vendor_reg_inst = Vendor_registration.objects.get(user=user_instance)
            gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
            if store_address:
                print('condition yha bhi aya hai..')
                add_lat_long = gmaps.geocode(store_address)
                user_lat = add_lat_long[0]['geometry']['location']['lat']
                user_lng = add_lat_long[0]['geometry']['location']['lng']
                print('condition ye bhi run..')
                store_detail = Vendor_Store_detail(user=user_instance,vendor=vendor_reg_inst,store_zipcode=zipcode,store_registration_number=store_registration_number,store_name=store_name,
                                               store_description=store_description,store_category=store_category,store_address = store_address,
                                               store_logo=store_logo,store_banner=store_banner,store_image=store_image,store_latitude=user_lat,store_longitude=user_lng,
                                               store_closing_day=store_cloasing_day,store_closing_time=store_close_time,store_opening_time=store_opening_time)
                print('condition yha tk chla..')
                store_detail.save()

                return redirect('/vendorregistrationstoredocumentdetail')

        category = Category.objects.all()
        return render(request,'vendor_register_store_detail.html',{'category':category})
    else:
        return redirect('/login')

####################### Vendor Register Store Detail End Here #############

#################### Vendor Register Store Document Detail #####################
def Vendor_register_store_document_detail(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            store_seller_aadhar = request.POST.get('aadhar_number')
            store_seller_front_aadhar_image = request.FILES['aadhar_image_front']
            store_seller_back_aadhar_image = request.FILES['aadhar_image_back']
            store_seller_pancard = request.POST.get('pancard_number')
            store_seller_pancard_image = request.FILES['pancard_image']
            try:
                store_shiping_policy = request.FILES['store_shiping_policy']
            except:
                store_shiping_policy=None
            store_seller_gst = request.POST.get('store_gst')
            try:
                store_return_policy = request.FILES['store_return_policy']
            except:
                store_return_policy = None

            store_bank_account_number = request.POST.get('bank_account_number')
            store_bank_name = request.POST.get('bank_name')
            store_bank_ifsc = request.POST.get('bank_ifsc')
            store_bank_passbook = request.FILES['bank_passbook_image']
            store_seller_razorpay_id = request.POST.get('razorpay_id')
            user_instance = User.objects.get(username=request.user.username)
            store_document = Vendor_store_document(user=user_instance,store_seller_aadhar=store_seller_aadhar,store_seller_front_aadhar_image=store_seller_front_aadhar_image,
                                                  store_seller_back_aadhar_image=store_seller_back_aadhar_image,store_seller_pancard=store_seller_pancard,
                                                   store_seller_pancard_image=store_seller_pancard_image,store_shiping_policy=store_shiping_policy,store_seller_gst=store_seller_gst,
                                                  store_return_policy=store_return_policy,store_bank_account_number=store_bank_account_number,store_bank_name=store_bank_name,
                                                  store_bank_ifsc=store_bank_ifsc,store_bank_passbook=store_bank_passbook,store_seller_razorpay_id=store_seller_razorpay_id)
            store_document.save()
            messages.info(request,'Waiting for Admin Approval..After Approval you eligible for manage your store , Thank You !')
            return render(request,'vendor_waiting.html')
        else:
            return render(request,'vendor_register_store_document_detail.html')
    else:
        return redirect('/login')

################## Vendor Register Store Document Detail End here #############

########################Vendor Profile View ########################
def vendor_profile(request):
    if request.user.is_authenticated:
        if request.user.vendor_registration.store_status == True:
            if request.method=="POST":
                print('done done')
                profile_pic= request.FILES['pic']
                user=User.objects.get(username=request.user.username)
                print(user)
                ob = Vendor_registration.objects.get(user=user)
                print(ob)
                ob.profile_pic=profile_pic
                ob.save()
            return render(request,'vendor_profile_view.html')
        else:
            try:
                user_instance = User.objects.get(username=request.user.username)
                obj = Vendor_Store_detail.objects.get(user=user_instance)
                try:
                    if request.user.vendor_store_document.user:
                        messages.info(request,
                                      'Waiting for Admin Approved..After Approved you eligible for manage your store , Thank You !')
                        return render(request, 'vendor_waiting.html')
                except:
                    print('yha chla hai...')
                    user_instance = User.objects.get(username=request.user.username)
                    obj=Vendor_Store_detail.objects.get(user=user_instance)
                    return render(request,'vendor_register_store_document_detail.html')
            except:

                category = Category.objects.all()
                return render(request,'vendor_register_store_detail.html',{'category':category})
    else:
        return redirect('/login')

#################### Vendor Profile View End ####################

def vendor_edit_profile(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            obj = Vendor_registration.objects.get(user=request.user)
            obj.address = request.POST.get('address')
            obj.mobile = request.POST.get('mobile')
            obj.save()
            obb = User.objects.get(username=request.user)
            obb.first_name = request.POST.get('first_name')
            obb.last_name = request.POST.get('last_name')
            obb.save()
            return redirect('/vendor_edit_profile')
        else:
            #ob = User_register.objects.get(user=request.user)
            #print(ob.address)
            return render(request,'vendor_edit_profile.html')
    else:
        return redirect('/login')
####################### Vendor Prodile Edit End ################


################## Vendor shop to product page ############

def product_page(request):
    z=request.GET.get('title')
    print('title,',z)
    vendor=request.GET.get('vendor')
    print('vendor,',vendor)
    brandd = request.GET.get('brand')

    min_price = request.GET.get('price_min')
    max_price = request.GET.get('price_max')

    subcat_instance = Subcategory.objects.get(name=z)
    print(subcat_instance,'subcat_instance hai..')
    user_instance = User.objects.get(id=vendor)
    print(user_instance,'user_instance hai..')
    if request.method=="POST":
        text = request.POST.get('text')
        product_featchh = Product.objects.filter(user=user_instance, subcategory=subcat_instance)
        variant_featch = Variants.objects.filter(product__in=product_featchh,after_discount_price__range=(min_price, max_price),variant_show_status=True)
    if brandd:
        brand_instance = Brands.objects.get(name=brandd)
        print('ab dta yha sae gya...')
        product_featchh = Product.objects.filter(user=user_instance, subcategory=subcat_instance,brand_name=brand_instance)
        variant_featch = Variants.objects.filter(product__in=product_featchh,variant_show_status=True)
    elif min_price:
        product_featchh = Product.objects.filter(user=user_instance, subcategory=subcat_instance)
        variant_featch = Variants.objects.filter(product__in=product_featchh,after_discount_price__range =(min_price,max_price),variant_show_status=True)
    else:
        product_featchh = Product.objects.filter(user=user_instance, subcategory=subcat_instance)
        variant_featch = Variants.objects.filter(product__in=product_featchh,variant_show_status=True)#### yha sae variant fetach kiya or bheja
        print('ye var ab sahi hai',variant_featch)
    prod_for_brand = Product.objects.filter(user=user_instance, subcategory=subcat_instance)
    brand = []
    for x in prod_for_brand:
        if x.brand_name not in brand:
            brand.append(x.brand_name)
    vendor_instance_create = Vendor_Store_detail.objects.get(user=user_instance)
    c = vendor_instance_create.user.id
    print('ye user id hai...', c)
    cat_instance = Category.objects.get(name=vendor_instance_create.store_category)
    subcat_instance = Subcategory.objects.filter(category=cat_instance)
    subcat = []

    for x in subcat_instance:###############
        # product_featch = Product.objects.filter(user=vendor_instance_create.user,SubCategory=x)
        product_featch = Product.objects.filter(user=vendor_instance_create.user, subcategory__name=x)
        for x in product_featch:
            if x.subcategory not in subcat:
                subcat.append(x.subcategory)
    print('title_hai',z)


    return render(request, 'category_by_product.html', {'product': variant_featch,'store':user_instance,'subcat':subcat,'brand':brand,'vendor':vendor,'title':z})
################## Vendor shop to product page end ############

############################# Store Brand Filter ############################





############################ end Store brand filter ####################


#################### Vendor Change Password ##################

def Vendor_changepassword(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            current_password=request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            user=authenticate(username=request.user.username,password=current_password)
            if user is not None:
                if new_password==confirm_password:
                    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,18}$"
                    # compiling regex
                    match_re = re.compile(reg)
                    # searching regex
                    res = re.search(match_re, new_password)
                    if res:
                        user_instance = User.objects.get(username=request.user.username)
                        user_instance.password=make_password(new_password)
                        user_instance.save()
                        messages.success(request,'Password Chnange Successfully..')
                        return render(request, 'vendor_changepassword.html')
                    else:
                        messages.error(request,'Password must be strong, Invalid Password..')
                        return render(request, 'vendor_changepassword.html')
                else:
                    messages.error(request,'New Password and Confirm Password not matched..')
                    return render(request, 'vendor_changepassword.html')
            else:
                messages.error(request,'Current Password Not valid..')
        else:
            return render(request, 'vendor_changepassword.html')
    else:
        return redirect('/login')

#################### Vendor change password end #############

################### Vendor Add Product ####################
def Vendor_add_product(request):
    if request.user.is_authenticated:
        user_instance = User.objects.get(username=request.user.username)
        vendor_categroy = Vendor_Store_detail.objects.get(user=user_instance)
        category_instance = Category.objects.get(name=vendor_categroy.store_category)
        subcategory_instance = Subcategory.objects.filter(category=category_instance)
        li=[]
        for x in subcategory_instance:
            li.append(x)
        subsubcategory_instance = Brands.objects.filter(subcategory__in=li)
        print(subsubcategory_instance)
        if request.method=="POST":
            product_category = request.POST.get('select_product')
            product_brand = request.POST.get('select_brand')
            product_title = request.POST.get('title')
            product_price = request.POST.get('price')
            front_image = request.FILES['front_image']
            gst = request.POST.get('gst')
            discount = request.POST.get('discount')
            variant_available =request.POST.get('value')
            subcat = Subcategory.objects.get(id=product_category)
            brand = Brands.objects.get(id=product_brand)
            if discount == '':
                product_add_vendor = Product(user=user_instance, stor_details=vendor_categroy,
                                             category=category_instance, subcategory=subcat,
                                             brand_name=brand, title=product_title, price=product_price,
                                             gst_percent=gst, variant=variant_available, image=front_image, status=True)
                product_add_vendor.save()
            else:
                product_add_vendor = Product(user=user_instance,stor_details=vendor_categroy,category=category_instance,subcategory=subcat,
                                             brand_name=brand,title=product_title,price=product_price,discount_percent=discount,
                                             gst_percent=gst,variant=variant_available,image=front_image,status=True)
                product_add_vendor.save()
            messages.success(request,'Product add successfully know add variants of this product.')
            return redirect('/add_product')


        return render(request,'add_product.html',{'subcategory':subcategory_instance,'brand':subsubcategory_instance,'cat':vendor_categroy.store_category})
    else:
        return redirect('/login')


#################### Vendor Add Product End ##################

########### product varient ##################
def Product_varient(request):
    if request.user.is_authenticated:
        user_instance = User.objects.get(username = request.user.username)
        product_featch = Product.objects.filter(user = user_instance)
        c=user_instance.vendor_store_detail.store_category
        color_featch= Color.objects.all()
        size = Size.objects.all()
        if request.method=="POST":
            product = request.POST.get('select_product')
            variant_title = request.POST.get('variant_title')
            variant_price = request.POST.get('variant_price')
            variant_discount = request.POST.get('variant_discount')
            if c !='Grocery':
                variant_color = request.POST.get('select_color')
                color_inst = Color.objects.get(id=variant_color)
            else:
                variant_color=None
                color_inst =None
            variant_size = request.POST.get('select_size')
            description = request.POST.get('description')
            variant_quantity=request.POST.get('quantity')

            image_fornt =request.FILES['image_fornt']
            image_back = request.FILES['image_back']
            image_side=request.FILES['image_side']
            prod_inst = Product.objects.get(id=product)
            print(prod_inst.discount_percent,'ye discount hai...')
            # color_inst = Color.objects.get(id=variant_color)
            size_inst = Size.objects.get(id=variant_size)
            pv_set = PVset.objects.get(Subcategory=prod_inst.subcategory)
            point_value=(pv_set.PV*float(variant_price))/100
            if prod_inst.discount_percent:
                gst_fix = (prod_inst.gst_percent*float(variant_price))/100
                include_gst_price = gst_fix+float(variant_price)
                discount_add = (prod_inst.discount_percent*include_gst_price)/100
                final_pric = include_gst_price-discount_add
                final_price = round(final_pric,2)
                variant_data_save = Variants(product=prod_inst,title=variant_title,description=description,quantity=variant_quantity,
                                         image_fornt=image_fornt,image_back=image_back,image_side=image_side,price=variant_price,
                                         point_value=point_value,color=color_inst,size=size_inst,after_discount_price=final_price,variant_show_status=True)
                variant_data_save.save()
                prod_inst.ecommerce_show_data=True
                prod_inst.save()
                messages.success(request,'Your variant added successfully..')
                return redirect('/product_varient')
            if variant_discount:
                gst_fix = (prod_inst.gst_percent  * float(variant_price))/100
                include_gst_price = gst_fix + float(variant_price)
                discount_add = (float(variant_discount) * include_gst_price)/100
                final_pric = include_gst_price - discount_add
                final_price = round(final_pric, 2)
                variant_data_save = Variants(product=prod_inst, title=variant_title, description=description,
                                             image_fornt=image_fornt,image_back=image_back,image_side=image_side,quantity=variant_quantity,
                                             price=variant_price, variant_discount=variant_discount,
                                             point_value=point_value, color=color_inst, size=size_inst,
                                             after_discount_price=final_price,variant_show_status=True)
                variant_data_save.save()
                prod_inst.ecommerce_show_data = True
                prod_inst.save()
                messages.success(request, 'Your variant added successfully..')
                return redirect('/product_varient')
            else:
                gst_fix = (prod_inst.gst_percent * float(variant_price))/100
                include_gst_pric = gst_fix + float(variant_price)
                include_gst_price = round(include_gst_pric,2)
                variant_data_save = Variants(product=prod_inst, title=variant_title, description=description,
                                             image_fornt=image_fornt,image_back=image_back,image_side=image_side,quantity=variant_quantity,
                                             price=variant_price,
                                             point_value=point_value, color=color_inst, size=size_inst,
                                             after_discount_price=include_gst_price,variant_show_status=True)
                variant_data_save.save()
                prod_inst.ecommerce_show_data = True
                prod_inst.save()
                messages.success(request, 'Your variant added successfully..')
                return redirect('/product_varient')

        return render(request,'product_varient.html',{'product':product_featch,'c':c,'color':color_featch,'size':size})
    else:
        return redirect('/login')

########## product varient end #############
########## Store View #####################
def store_view(request):
    if request.user.is_authenticated:
        user_inst = User.objects.get(username = request.user.username)
        store_featch = Vendor_Store_detail.objects.get(user = user_inst)
        return render(request,'store_view.html',{'store':store_featch})
    else:
        return redirect('/login')

########## Store View End #####################

############ store update ###################
def store_update(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            store_name = request.POST.get('store_name')
            store_description = request.POST.get('store_description')
            #store_address = request.POST.get('store_address')
            store_closing_time = request.POST.get('store_closing_time')
            store_opening_time = request.POST.get('store_opening_time')
            store_closing_day = request.POST.get('store_closing_day')
            user_inst = User.objects.get(username = request.user.username)
            store_featch = Vendor_Store_detail.objects.get(user=user_inst)
            store_featch.store_name = store_name
            store_featch.store_description = store_description
            store_featch.store_closing_time=store_closing_time
            store_featch.store_opening_time=store_opening_time
            store_featch.store_closing_day=store_closing_day
            store_featch.save()
            return redirect('/store_view')
        user_inst = User.objects.get(username=request.user.username)
        store_featch = Vendor_Store_detail.objects.get(user=user_inst)
        return render(request, 'store_update.html', {'store': store_featch})
    else:
        return redirect('/login')

##############store update end ###############
#
# ####################################### FOR ALL USER, VENDOR ###############################################


################### forget password  take email #############
def forget_password(request):
    if request.method=='POST':
        request.session['email'] = request.POST.get('email')
        email = request.session.get('email')
        print(email)
        try:
            check_email = User.objects.get(username=email)
            otp = randint(1111, 9999)
            print('condition run')
            if check_email:
                try:
                    OTP = Otp.objects.get(email=email)
                    OTP.otp = otp
                    OTP.save()
                except:
                    OTP = Otp(email=email, otp=otp)
                    OTP.save()
                print('yha bhi run')
                send_conformation_email(request,otp)
                print('send email work')
                return render(request,'forget_password_otp.html')
        except:
            messages.error(request,'Invaild email id try another')
    return render(request,'forget_password.html')



############### end forget password ##############



############ forget password verify otp ############

def forget_password_verify_otp(request):
    email = request.session.get('email')
    if request.method=="POST":
        otp = request.POST.get('otp')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        otp_featch = Otp.objects.get(email=email)
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
                    messages.success(request,'password changed successfully..')
                    return redirect('/login')
                else:
                    messages.error(request,'Passowrd must be strong..or min 8 char')
                    return render(request,'forget_password_otp.html')
            else:
                messages.error(request,'Password and confirm password not match..')
                return render(request, 'forget_password_otp.html')
        else:
            messages.error(request,'Otp not Vaild..')
            return render(request, 'forget_password_otp.html')


############forget password verify otp end ##########

############# forget password resend otp ###########

def forget_password_resend_otp(request):
    email = request.session.get('email')
    otp = randint(1111, 9999)
    otp_update = Otp.objects.get(email=email)
    otp_update.otp = otp
    otp_update.save()
    send_conformation_email(request,otp)
    messages.success(request, 'Resend OTP Successfully on your register Email..')
    return render(request,'forget_password_otp.html')


################### end forget resend otp #######
#

#
#
#
#
# def AddChainRegister(request):
#     obj = Product.objects.all()
#     return render(request,'addchain.html',{'pro':obj})
#
#
# def BuySponser(request,id):
#     try:
#         obb=buy_sponser.objects.get(username=request.user.username)
#         if obb:
#             inst_usr=User.objects.get(username=request.user.username)
#             try:
#                 tree_check = TreeChain.objects.get(user=inst_usr)
#                 messages.error(request,'Sorry you are already part of tree')
#                 obj = Product.objects.all()
#                 return render(request, 'addchain.html', {'pro': obj})
#             except:
#                 obj = Product.objects.get(pk=id)
#                 obb.product_name=obj.title
#                 obb.username=request.user.username
#                 obb.price = obj.price
#                 obb.image = obj.pic
#                 ob_updt = buy_sponser(product_name=obb.product_name,username=obb.username,price=obb.price,image=obb.image)
#                 obb.save()
#                 return render(request, 'sponser_info.html')
#
#
#     except:
#         obj = Product.objects.get(pk=id)
#         ob = buy_sponser(product_name=obj.title,username=request.user.username,price=obj.price,image=obj.pic)
#         ob.save()
#     return render(request,'sponser_info.html')
#
#
#
#
# ####################################################### Tree Chain Code ###############################################################
#
# ################################################HERE RIGHT CHECK FUNCTION WRITE#############################################

def right_check(request,obb,new_user_object,left,right,refer_by):
    for x in obb:
        if x.right == True:
            print('times of print----------',x.user)
            #obb = TreeChain.objects.filter(parent=x.id)
            obj = User.objects.get(username=x.user)
            print(obj, '.........')
            objb = TreeChain.objects.get(user=obj)
            obb = objb.get_children()
            obbj = TreeChain.objects.get(user=x.user)
            c=obbj.get_children()
            print('print hua hai---',c)
            if obbj.is_leaf_node() == True:
                print('jai hanuman')
                o = TreeChain(user=new_user_object, left=left, right=right, parent=obbj,refer_by=refer_by)  # condition ok
                #messages.success(request, 'User add in Chain successfully..')
                o.save()
                return True
            else:
                print('chla hai')
                return right_check(request,obb,new_user_object,left,right,refer_by)
    else:
        print('########',obb)
        obbj = TreeChain.objects.get(user=obb[0].user)
        print('$$$$$44444----',obbj.get_ancestors(ascending=False, include_self=False))
        c=obbj.get_ancestors(ascending=False, include_self=False)
        d=len(c)
        f=c[d-1]
        obb = User.objects.get(username=f)
        obbbj = TreeChain.objects.get(user=obb.id)
        print('ye obbbbj hai----------',obbbj)
        o = TreeChain(user=new_user_object, left=left, right=right, parent=obbbj,refer_by=refer_by)  # condition ok
        #messages.success(request, 'User add in Chain successfully..')
        o.save()
        return True
# ########################################################RIGHT CHECK FUNCTION END###########################################
#
# ###########################################HERE LEFT CHECK FUNCTION WRITE##############################################
#
def left_check(request,obb,new_user_object,left,right,refer_by):
    for x in obb:
        if x.left == True:
            print('times of print----------', x.user)
            # obb = TreeChain.objects.filter(parent=x.id)
            obj = User.objects.get(username=x.user)
            print(obj, '.........')
            objb = TreeChain.objects.get(user=obj)
            obb = objb.get_children()
            obbj = TreeChain.objects.get(user=x.user)
            print('ye obbj hai..@@##',obbj)
            c = obbj.get_children()
            print('print hua hai---', c)
            if obbj.is_leaf_node() == True:
                print('jai hanuman')
                o = TreeChain(user=new_user_object, left=left, right=right, parent=obbj,refer_by=refer_by)  # condition ok
                #messages.success(request, 'User add in Chain successfully..')
                o.save()
                return True
            else:
                print('chla hai')
                return left_check(request, obb, new_user_object, left, right,refer_by)
    else:
        print('########', obb)
        obbj = TreeChain.objects.get(user=obb[0].user)
        print('$$$$$44444----', obbj.get_ancestors(ascending=False, include_self=False))
        c = obbj.get_ancestors(ascending=False, include_self=False)
        d = len(c)
        f = c[d-1]
        obb = User.objects.get(username=f)
        obbbj = TreeChain.objects.get(user=obb.id)
        print('ye obbbbj hai----------', obbbj)
        o = TreeChain(user=new_user_object, left=left, right=right, parent=obbbj,refer_by=refer_by)  # condition ok
        #messages.success(request, 'User add in Chain successfully..')
        o.save()
        return True

#
#
#
# #########################################END LEFT CHECK FUNCTION#####################################################


def tree_adding(request,obb,new_user_object,parent,left,right,refer_by):
    print('yha code chla hai outer function...')
    if obb.count() == 2:
        if left == True:
            x = left_check(request, obb, new_user_object, left, right,refer_by)
            if x == True:
                return redirect('/')
        else:
            print('oobb count 2 ka right chla hai')
            x = right_check(request, obb, new_user_object, left, right,refer_by)
            if x == True:
                return redirect('/')

    if obb.count() == 1:
        for x in obb:
            if x.left == True:
                if right == True:  # same it run when user choose opposite node and node are free
                    o = TreeChain(user=new_user_object, left=left, right=right, parent=parent,refer_by=refer_by)
                    #messages.success(request, 'User add in Chain successfully..')
                    o.save()
                if left == True:
                    print('huma huma huma huma..')
                    print('x------user hai---',x.user)
                    #obb = TreeChain.objects.filter(parent=x.id)
                    obbj = TreeChain.objects.get(user=x.user)
                    if obbj.is_leaf_node() == True:
                        print('latest---left')
                        o = TreeChain(user=new_user_object, left=left, right=right, parent=obbj,refer_by=refer_by)
                        #messages.success(request, 'User add in Chain successfully..')
                        o.save()
                    else:
                        x = left_check(request,obb,new_user_object,left,right,refer_by)
                        if x == True:
                            return redirect('/')

            if x.right == True:
                if left == True:  # it run when node free user choose opposite node
                    o = TreeChain(user=new_user_object, left=left, right=right, parent=parent,refer_by=refer_by)
                    #messages.success(request, 'User add in Chain successfully..')
                    o.save()
                if right == True:
                    #obb = TreeChain.objects.filter(parent=x.id)
                    obbj = TreeChain.objects.get(user=x.user)
                    if obbj.is_leaf_node() == True:
                        print('latest---right')
                        o = TreeChain(user=new_user_object, left=left, right=right, parent=obbj,refer_by=refer_by)
                        messages.success(request, 'User add in Chain successfully..')
                        o.save()
                    else:
                        x = right_check(request,obb,new_user_object,left,right,refer_by)
                        if x == True:
                            return redirect('/')

    else:
        print('yes here running....')
        print(new_user_object,'--------------------')
        print(left,'--------------------')
        print(right,'--------------------')
        print(parent,'--------------------')
        print(refer_by,'--------------------')

        o = TreeChain(user=new_user_object,parent=parent, left=left, right=right, refer_by=refer_by)

        #messages.success(request, 'User add in Chain successfully..')
        o.save()


#
#
#
#
#
#
#
#
#
#
#
#
# def Sponser_address_chain(request):
#     if request.method == 'POST':
#         request.session['refer'] = request.POST.get('refer')
#         request.session['position'] = request.POST.get('value')
#         request.session['address1'] = request.POST.get('address1')
#         request.session['address2'] = request.POST.get('address2')
#         request.session['city'] = request.POST.get('city')
#         request.session['zipcode'] = request.POST.get('zipcode')
#         request.session['username']=request.user.username
#         request.session['name'] = request.user.first_name + request.user.last_name
#
#
#         refer=request.session.get('refer')
#         position=request.session.get('position')
#         address1=request.session.get('address1')
#         address2=request.session.get('address2')
#         city=request.session.get('city')
#         zipcode=request.session.get('zipcode')
#         username=request.session.get('username')
#         name=request.session.get('name')
#         try:
#             ob = Refer_code.objects.get(refercode=refer)
#             if ob:
#                 print('data run hua yha')
#                 print('code run run run..')
#                 print(request.user.username)
#                 prod = buy_sponser.objects.get(username=request.user.username)
#                 print('code yha run hua hai....')
#                 all_detail={'refer':refer,'position':position,'address1':address1,'address2':address2,'city':city,'zipcode':zipcode,'username':username,'name':name,'prod':prod}
#                 print('run..')
#                 amount = buy_sponser.objects.get(username=request.user.username)
#                 amt = int(amount.price * 100)
#                 print('run....')
#                 client = razorpay.Client(auth=("rzp_test_dR2Pg3t4eyAlsO", "QhGXjC9RqAKukJCDZ8LBcQKZ"))
#                 payment = client.order.create({'amount': amt, 'currency': 'INR', 'payment_capture': '1'})
#                 print(payment)
#                 print('run.....')
#                 print('ye client hau',client)
#                 obj = Sponser_user_address(username=username, sponserid=refer, position=position, address=address1,
#                                            address2=address2, city=city, zipcode=zipcode, name=name, amount=amt,
#                                            payment_id=payment['id'])
#                 return render(request, 'sponser_product_detail.html', {'detail': all_detail, 'payment': payment})
#         except:
#             messages.error(request,'Refer Code not matched !!!')
#
#
#     print('ye last run hua hai..')
#     return render(request,'sponser_info.html')
#
#
# def Payment_sucess(request):
#     if request.method=="POST":
#         a=request.POST
#
#         data={}
#         for key ,val in a.items():
#             if key == 'razorpay_order_id':
#                 data['razorpay_order_id'] = val
#             elif key == 'razorpay_payment_id':
#                 data['razorpay_payment_id'] = val
#             elif key == 'razorpay_signature' :
#                 data['razorpay_signature'] = val
#         print('ye data hai...',data)
#
#         refer = request.session.get('refer')
#         position = request.session.get('position')
#         address1 = request.session.get('address1')
#         address2 = request.session.get('address2')
#         city = request.session.get('city')
#         zipcode = request.session.get('zipcode')
#         username = request.session.get('username')
#         #name = request.session.get('name')
#         amount=buy_sponser.objects.get(username=request.user.username)
#         #print(amount)
#         #amt=int(amount.price*100)
#         client = razorpay.Client(auth=("rzp_test_dR2Pg3t4eyAlsO","QhGXjC9RqAKukJCDZ8LBcQKZ"))
#         check = client.utility.verify_payment_signature(data)
#         print(check)
#         if check:
#             pass
#         else:
#             #payment=client.order.create({'amount':amt,'currency':'INR','payment_capture':'1'})
#             name = request.user.first_name +' '+request.user.last_name
#             obj = Sponser_user_address(username=username,sponserid=refer,position=position,address=address1,address2=address2,city=city,zipcode=zipcode,name=name,amount=amount.price,payment_id=data['razorpay_payment_id'],order_id=data['razorpay_order_id'],signature=data['razorpay_signature'],product_name=amount.product_name,Paid=True)
#             obj.save()
#
#             try:
#                 ob = Refer_code.objects.get(refercode=refer)
#                 refer_by = ob.user  # this is only created for get refer user name
#                 if ob:
#
#                     new_user_object = User.objects.get(username=obj.username)
#                     parent = TreeChain.objects.get(user=ob.user)  # create exist user instance in tree
#                     print('ye obbj hai....', parent)
#                     if position == 'left':
#                         print('yha bhi chla hai--')
#                         print(ob.user)
#                         obj = User.objects.get(username=ob.user)
#                         print(obj, '.........')
#                         objb = TreeChain.objects.get(user=obj)
#                         # obb = TreeChain.objects.filter(parent__id=obj.id)
#                         # print('ye obb hi...', obb)
#                         obb = objb.get_children()
#                         print(obb.count())
#                         print('ye children hai...', objb.get_children())
#                         left = True
#                         right = False
#                         tree_adding(request, obb, new_user_object, parent, left, right, refer_by)
#                         print('yes left running')
#                         ##################################Refer Code generate Here ######################
#                         c = randint(0000, 9999)
#                         ob = User.objects.get(username=request.user.username)
#                         d = 'AVPL' + str(ob.id) + str(c)  # refercode generate here...............
#                         obj = Refer_code(user=ob, refercode=d)
#                         obj.save()
#
#                         ###################### Direct Refer amount Saved Here ############################
#                         prod_rate = buy_sponser.objects.get(username=request.user.username)
#                         amt = prod_rate.price * (25 / 100)
#                         print(amt)
#                         c = 'Direct Refer Urned By' + ' ' + request.user.first_name + ' ' + request.user.last_name
#                         print(c)
#                         print('ye objb hai-------', objb)
#                         drct_rfr = Direct_refer_statements(username=objb, amount=amt, desc=c)
#                         print('code yha chla hai')
#                         drct_rfr.save()
#                         return render(request,'success.html')
#                     else:
#                         obj = User.objects.get(username=ob.user)
#                         print(obj, '.........')
#                         objb = TreeChain.objects.get(user=obj)
#                         # obb = TreeChain.objects.filter(parent__id=obj.id)
#                         # print('ye obb hi...', obb)
#                         obb = objb.get_children()
#                         print(obb.count())
#                         print('ye children hai...', objb.get_children())
#                         for x in obb:
#                             print(x.user)
#                             if x.left == True:
#                                 print(x.left)
#
#                         left = False
#                         right = True
#                         tree_adding(request, obb, new_user_object, parent, left, right, refer_by)
#                         print('yes right running')
#
#                         ##################################Refer Code generate Here ######################
#                         c = randint(0000, 9999)
#                         ob = User.objects.get(username=request.user.username)
#                         d = 'AVPL' + str(ob.id) + str(c)  # refercode generate here...............
#                         obj = Refer_code(user=ob, refercode=d)
#                         obj.save()
#                         ###################### Direct Refer amount Saved Here ############################
#
#                         prod_rate = buy_sponser.objects.get(username=request.user.username)
#                         amt = prod_rate.price * (25 / 100)
#                         print(amt)
#                         c = 'Direct Refer Urned By' + ' ' + request.user.first_name + ' ' + request.user.last_name
#                         print(c)
#                         print('ye objb hai-------', objb)
#                         drct_rfr = Direct_refer_statements(username=objb, amount=amt, desc=c)
#                         print('code yha chla hai')
#                         drct_rfr.save()
#                         return render(request, 'success.html')
#
#             except:
#
#                 messages.error(request, 'Refer Code not matched...')
#                 print('code not matched..')
#
#
#
#     #obb = buy_sponser.objects.get(username=request.user.username)
#     #print(obb.price)
#     return render(request,'sponser_product_detail.html')
#
# ######################################################### TREE View############################################################
#
# def Tree_view(request):
#
#     if request.method=='POST':
#         name = request.POST['name']
#
#         try:
#             obj=User.objects.get(username=name)
#             obbj=TreeChain.objects.get(user=obj.id)
#             child=obbj.get_descendants(include_self=False)
#             print(child )
#             left_count=0
#             right_count=0
#             for x in child:
#                 if x.right==True:
#                     right_count=right_count + 1
#                 if x.left == True:
#                     left_count = left_count + 1
#
#
#             print('*************************')
# ################################### Uper part ka hai main start #########################
#             lv_1=obbj.get_children()
#             li=[]
#             print(lv_1.count())
#             if lv_1.count() == 1:
#                 print('y')
#                 for x in lv_1:
#                     if x.left==True:
#                         print('yes')
#                         li.insert(0,x.user)
#                         li.insert(1,' ')
#                     else:
#                         if not li:
#                             li.insert(0,' ')
#                             li.insert(1, x.user)
#                         else:
#                             li.insert(1, x.user)
#             if lv_1.count() == 2:
#                 for x in lv_1:
#                     if x.left==True:
#                         li.insert(0,x.user)
#                     else:
#                         li.insert(1, x.user)
#             print('ye li hai...',li)
# ##########################################check start here of lv_1 ###########################
#             if lv_1.count():
#                 if li[0] != ' ' and li[1] != ' ':
#                     print('under bunder bich samunder....')
#                     tre_inst = TreeChain.objects.get(user=li[0])
#                     print('tre',tre_inst)
#                     tre_inst2 = TreeChain.objects.get(user=li[1])
#                     print('yes',tre_inst2)
#                     print('mae hu...')
#                     lv_1_child=tre_inst.get_children()
#                     print('child do..')
#                     li_1 = []
#                     print('ye lv_1 child hqi',lv_1_child)
#
#                     if lv_1_child.count() == 1:
#                         for x in lv_1_child:
#                             if x.left == True:
#                                 li_1.insert(0, x.user)
#                                 li_1.insert(1,' ')
#                             else:
#                                 if not li_1:
#                                     li_1.insert(0, ' ')
#                                     li_1.insert(1, x.user)
#                                 else:
#                                     li_1.insert(1, x.user)
#                     if lv_1_child.count() == 2:
#                         for x in lv_1_child:
#                             if x.left == True:
#                                 li_1.insert(0, x.user)
#                             else:
#                                 li_1.insert(1, x.user)
#                     lv_2_child=tre_inst2.get_children()
#                     li_2 = []
#                     if lv_2_child.count() == 1:
#                         for x in lv_2_child:
#                             if x.left == True:
#                                 li_2.insert(0, x.user)
#                                 li_2.insert(1,' ')
#                             else:
#                                 if not li_2:
#                                     li_2.insert(0, ' ')
#                                     li_2.insert(1, x.user)
#                                 else:
#                                     li_2.insert(1, x.user)
#                     if lv_2_child.count() == 2:
#                         for x in lv_2_child:
#                             if x.left == True:
#                                 li_2.insert(0, x.user)
#                             else:
#                                 li_2.insert(1, x.user)
#                     print('condition 2 run hua')
#
#                     return render(request, 'tree_view.html',{'obb': li, 'obj': obj, 'left': left_count, 'right': right_count,'lv_1_child':li_1,'lv_2_child':li_2})
#                 if li[0] !=' ' and li[1] == ' ':
#                     li_1=[]
#                     print('ye lo not equal space')
#                     tre_inst = TreeChain.objects.get(user=li[0])
#                     lv_1_child = tre_inst.get_children()
#                     if lv_1_child.count() == 1:
#                         for x in lv_1_child:
#                             if x.left == True:
#                                 li_1.insert(0, x.user)
#                                 li_1.insert(1,' ')
#                             else:
#                                 if not li_1:
#                                     li_1.insert(0, ' ')
#                                     li_1.insert(1, x.user)
#                                 else:
#                                     li_1.insert(1, x.user)
#                     if lv_1_child.count() == 2:
#                         for x in lv_1_child:
#                             if x.left == True:
#                                 li_1.insert(0, x.user)
#                             else:
#                                 li_1.insert(1, x.user)
#                     li_2=[' ',' ']
#                     return render(request, 'tree_view.html',{'obb': li, 'obj': obj, 'left': left_count, 'right': right_count, 'lv_1_child': li_1,'lv_2_child': li_2})
#
#
#                 if li[0] ==' ' and li[1] != ' ':
#                     print('yes l1 not equal free space')
#                     li_2 = []
#                     print('ye lo not equal space')
#                     tre_inst = TreeChain.objects.get(user=li[1])
#                     lv_2_child = tre_inst.get_children()
#                     if lv_2_child.count() == 1:
#                         for x in lv_2_child:
#                             if x.left == True:
#                                 li_2.insert(0, x.user)
#                                 li_2.insert(1,' ')
#                             else:
#                                 if not li_2:
#                                     li_2.insert(0, ' ')
#                                     li_2.insert(1, x.user)
#                                 else:
#                                     li_2.insert(1, x.user)
#                     if lv_2_child.count() == 2:
#                         for x in lv_2_child:
#                             if x.left == True:
#                                 li_2.insert(0, x.user)
#                             else:
#                                 li_2.insert(1, x.user)
#
#                     li_1=[' ',' ']
#                     return render(request, 'tree_view.html',{'obb': li, 'obj': obj, 'left': left_count, 'right': right_count, 'lv_1_child': li_1,'lv_2_child': li_2})
#             else:
#                 print('condition else run hua hai')
#                 return render(request, 'tree_view.html',{'obj': obj, 'left': left_count, 'right': right_count})
#         except:
#             messages.error(request,'Invaild Sponsor ID')
#
#
#     return render(request,'tree_view.html')
#
# ########################################################### Cart Logics ################################################
def cart_show(request):
    if request.user.is_authenticated:
        user_instance = User.objects.get(username=request.user.username)
        cart_featch = UserCart.objects.filter(user=user_instance,cart_status=False)
        l2=[]
        li=[]
        sub_total_price = 0
        for x in cart_featch:
            product = Variants.objects.get(id=x.variant_id.id)
            li.append(product)
            l2.append(product.image)
            sub_total_price = x.final_price + sub_total_price

        shipping =15.0

        grand_total = sub_total_price + shipping
        grand = round(grand_total,2)
        subtotal=round(sub_total_price,2)
        cart = zip(cart_featch,li)
        return render(request, 'cart.html', {'cart': cart,'sub_total':subtotal,'shipping':shipping,"grand_total":grand,'cart_featch':cart_featch})
    else:
        return redirect('/login')


def Cart(request):
    if request.user.is_authenticated:
        data = request.GET.get('var_id')
        if request.method=="POST":
            data = request.POST.get('id')
            quantity = request.POST.get('quantity')

        print('yhi id hai...',data)
        varient_featch=Variants.objects.get(id=data)
        vendor_inst_by_user = User.objects.get(username=varient_featch.product.user)
        vendor_store_detail_inst = Vendor_Store_detail.objects.get(user=vendor_inst_by_user)
        user_instace = User.objects.get(username=request.user.username)
        cart_data_featch = UserCart.objects.filter(user=user_instace,cart_status=False)
        print('ye cart deta featch hai',cart_data_featch)
        if cart_data_featch:
            ct_fatch=UserCart.objects.filter(store_user = vendor_store_detail_inst)
            print(ct_fatch,'ye ct fatch hai..')

            if ct_fatch:
                if varient_featch.quantity >= int(1):

                    try:
                        print('ye data hai...')
                        cart_featch = UserCart.objects.get(variant_id = varient_featch,user=request.user,cart_status=False)
                        print('ab data yha hai..')

                        if cart_featch.cart_status == False:
                            if cart_featch.quantity < varient_featch.quantity:
                                print('ye condition run hua..')
                                cart_featch.quantity = cart_featch.quantity + int(1)
                                cart_featch.final_price = round(cart_featch.quantity * varient_featch.after_discount_price,2)
                                cart_featch.save()
                                return redirect('/cart_page')
                            else:
                                messages.error(request,'You Already added maximum quantity..')
                                return redirect('/cart_page')
                        else:
                            print('ye condition run hua hai...')
                            final_price = int(1) * varient_featch.after_discount_price
                            cart = UserCart(user=user_instace, variant_id=varient_featch, quantity=1,
                                            store_user=vendor_store_detail_inst, final_price=final_price)
                            cart.save()
                            return redirect('/cart_page')
                    except:
                        final_price =int(1) * varient_featch.after_discount_price
                        cart = UserCart(user=user_instace,variant_id=varient_featch,quantity=1,store_user=vendor_store_detail_inst,final_price=final_price)
                        cart.save()
                        return redirect('/cart_page')
                else:
                    messages.info(request,'You select maximum quantity select between left quantity')
                    return redirect('/product_view_page'+str(varient_featch.product.id))
            else:
                messages.error(request,"First you need to cart clear then you shop by another store")
                return redirect('/product_view_page'+str(varient_featch.product.id))
        else:
            print('statements run here...')
            final_price = round(int(1) * varient_featch.after_discount_price,2)
            cart = UserCart(user=user_instace, variant_id=varient_featch, quantity=1,
                            store_user=vendor_store_detail_inst, final_price=final_price)
            cart.save()
            return redirect('/cart_page')
    else:
        return redirect('/login')
# #
def cart_remove(request,id):
    if request.user.is_authenticated:
        ct =UserCart.objects.get(pk=id)
        ct.delete()
        return redirect('/cart_page')
    else:
        return redirect('/login')
#
def cart_plus(request,id):
    if request.user.is_authenticated:
        user_instance = User.objects.get(username = request.user.username)
        carts = UserCart.objects.filter(user=user_instance,cart_status=False).get(variant_id=id)
        product_featch = Variants.objects.get(id=id)
        print(product_featch.quantity,'ye vari quanti hai...')
        if product_featch.quantity > carts.quantity:
            carts.quantity = carts.quantity + 1
            carts.final_price = round(carts.quantity * product_featch.after_discount_price,2)
            carts.save()
            return redirect('/cart_page')
        else:
            messages.info(request,'You already add maximum quantity.')
            return redirect('/cart_page')
    else:
        return redirect('/login')
#
def cart_minus(request,id):
    print('yes this is runing')
    if request.user.is_authenticated:
        user_instance = User.objects.get(username=request.user.username)
        carts = UserCart.objects.filter(user=user_instance,cart_status=False).get(variant_id=id)
        product_featch = Variants.objects.get(id=id)
        if carts.quantity >= 2:
            carts.quantity = carts.quantity - 1
            carts.final_price = round(carts.quantity * product_featch.after_discount_price,2)
            carts.save()
            return redirect('/cart_page')
        else:
            carts.delete()
            return redirect('/cart_page')
    else:
        return redirect('/login')

################################# Self Picking/By delivery all payment ###############################

def self_picking_mode(request):
    if request.user.is_authenticated:
        cart_featch = UserCart.objects.filter(user=request.user, cart_status=False)
        total_pay = 0
        store_user = ''
        for x in cart_featch:
            total_pay = total_pay + x.final_price
            store_user = x.store_user
        from datetime import date
        import calendar
        my_date = date.today()
        obj = calendar.day_name[my_date.weekday()]
        slot_featch = vendor_time_slot.objects.filter(vendor_store=store_user, day=obj)
        print(slot_featch, 'ye slot featch hai..')
        if request.method=="POST":
            order_mode = request.POST.get('order_mode')
            time_slot = request.POST.get('time_slot')
            refer = request.POST.get('refer_code')
            position = request.POST.get('value')
            payment_mode = request.POST.get('payment')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            address = request.POST.get('address')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            locality = request.POST.get('locality')
            landmark = request.POST.get('landmark')
            alternate_mobile = request.POST.get('alternate_phone')
            if order_mode == 'Self_Picking':
                if refer:

                    try:
                        refer_featch = Refer_code.objects.get(refercode=refer)
                        try:
                            refer_store_featch = Refer_id_store.objects.get(user=request.user)
                        except:
                            refer_store_table = Refer_id_store(user=request.user,refer_code=refer,position=position,)
                            refer_store_table.save()
                    except:
                        from datetime import date
                        import calendar
                        my_date = date.today()
                        obj = calendar.day_name[my_date.weekday()]
                        slot_featch = vendor_time_slot.objects.filter(vendor_store=store_user, day=obj)
                        messages.error(request, 'Invalid Refer Code Please provide valid refer code..')

                        return render(request,'time_slot.html',{'order_mode':order_mode, 'slot': slot_featch})
                if time_slot and payment_mode:
                    if payment_mode=='Wallet':
                        pass
                    elif payment_mode =='Razorpay':
                        amt = int(total_pay * 100)
                        print(amt)
                        print('run....')
                        client = razorpay.Client(auth=("rzp_test_oh9NnzT3WLdH8D", "2cVCx2C2jgbv9YVe5p3WiSlr"))
                        order = client.order.create({'amount': amt, 'currency': 'INR', 'payment_capture': '1'})
                        context = {
                            'cart_featch': cart_featch,
                            'order': order,
                            'total_pay': total_pay,
                            'time_slot': time_slot,
                            'order_mode':order_mode,
                            'payment_mode': payment_mode,
                        }

                        return render(request, 'preview_payment.html', context)
                    elif payment_mode == 'COD':
                        context = {
                            'cart_featch': cart_featch,
                            'total_pay': total_pay,
                            'time_slot': time_slot,
                            'order_mode':order_mode,
                            'payment_mode': payment_mode,
                        }
                        return render(request, 'preview_payment_cod.html', context)
                if order_mode:
                    return render(request,'time_slot.html',{'order_mode':order_mode,'slot': slot_featch})
                else:
                    return redirect('/cart_page')

            if order_mode == 'By_Delivery':
                if address:
                    print('code run here')
                    gmaps = googlemaps.Client(key='AIzaSyC5m-C32piW2yiT3kevVbvLfHXsLsPTWik')
                    add_lat_long = gmaps.geocode(address)
                    user_lat = add_lat_long[0]['geometry']['location']['lat']
                    user_lng = add_lat_long[0]['geometry']['location']['lng']
                    newport_ri = (user_lat, user_lng)
                    cleveland_oh = (store_user.store_latitude, store_user.store_longitude)
                    c = geodesic(newport_ri, cleveland_oh).miles
                    km = c / 0.62137
                    if km <= 10:
                        if refer:
                            print('condition yha tk chla')
                            try:
                                refer_featch = Refer_code.objects.get(refercode=refer)
                                try:
                                    refer_store_featch = Refer_id_store.objects.get(user=request.user)
                                except:
                                    refer_store_table = Refer_id_store(user=request.user, refer_code=refer,
                                                                       position=position, )
                                    refer_store_table.save()
                            except:
                                context={

                                       'name': name,
                                       'phone': phone,
                                       'email': email,
                                       'address': address,
                                       'city': city,
                                       'pincode': pincode,
                                       'locality': locality,
                                       'landmark': landmark,
                                       'alternate_mobile': alternate_mobile,
                                        'order_mode': order_mode
                                }
                                print('ab yha chla')
                                messages.error(request, 'Invalid Refer Code Please provide valid refer code..')
                                return render(request, 'payment_address.html', context)
                        if payment_mode:
                            if payment_mode == 'Wallet':
                                pass
                            elif payment_mode == 'Razorpay':
                                amt = int(total_pay * 100)
                                print(amt)
                                print('run....')
                                client = razorpay.Client(auth=("rzp_test_oh9NnzT3WLdH8D", "2cVCx2C2jgbv9YVe5p3WiSlr"))
                                order = client.order.create({'amount': amt, 'currency': 'INR', 'payment_capture': '1'})
                                context = {
                                    'cart_featch': cart_featch,
                                    'order': order,
                                    'total_pay': total_pay,
                                    'time_slot': time_slot,
                                    'payment_mode': payment_mode,
                                    'name': name,
                                    'phone': phone,
                                    'email': email,
                                    'address': address,
                                    'city': city,
                                    'pincode': pincode,
                                    'locality': locality,
                                    'landmark': landmark,
                                    'refer':refer,
                                    'position':position,
                                    'order_mode': order_mode,
                                    'alternate_mobile': alternate_mobile,
                                }

                                return render(request, 'preview_payment.html', context)
                            elif payment_mode=='COD':
                                context = {
                                    'cart_featch': cart_featch,
                                    'total_pay': total_pay,
                                    'time_slot': time_slot,
                                    'payment_mode': payment_mode,
                                    'name': name,
                                    'phone': phone,
                                    'email': email,
                                    'address': address,
                                    'city': city,
                                    'pincode': pincode,
                                    'locality': locality,
                                    'landmark': landmark,
                                    'refer': refer,
                                    'position': position,
                                    'order_mode': order_mode,
                                    'alternate_mobile': alternate_mobile,
                                }
                                return render(request, 'preview_payment_cod.html', context)
                    else:
                        context = {

                            'name': name,
                            'phone': phone,
                            'email': email,
                            'address': address,
                            'city': city,
                            'pincode': pincode,
                            'locality': locality,
                            'landmark': landmark,
                            'alternate_mobile': alternate_mobile,
                            'order_mode': order_mode
                        }
                        messages.error(request,'Delivery are not available to your provided area')
                        return render(request,'payment_address.html',context)
                else:
                    return render(request,'payment_address.html',{'order_mode':order_mode})
        else:
            return redirect('/cart_page')
    else:
        return redirect('/login')


######################### end self picking #########################












################################# Success Payment / Razorpay #############
def succcess_payment_razorpay(request):
    if request.user.is_authenticated:
        cart_featch = UserCart.objects.filter(user=request.user,cart_status=False)
        total_pay = 0
        store_user = ''
        for x in cart_featch:
            total_pay = total_pay + x.final_price
            store_user = x.store_user

        if request.method=="POST":
            a=request.POST
            time_slot = request.POST.get('time_slot')
            payment_mode = request.POST.get('payment_mode')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            address = request.POST.get('address')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            locality = request.POST.get('locality')
            landmark = request.POST.get('landmark')
            alternate_mobile = request.POST.get('alternate_phone')
            order_mode = request.POST.get('order_mode')
            data={}
            for key ,val in a.items():
                if key == 'razorpay_order_id':
                    data['razorpay_order_id'] = val
                elif key == 'razorpay_payment_id':
                    data['razorpay_payment_id'] = val
                elif key == 'razorpay_signature' :
                    data['razorpay_signature'] = val
            print('ye data hai...',data)
            client = razorpay.Client(auth=("rzp_test_oh9NnzT3WLdH8D", "2cVCx2C2jgbv9YVe5p3WiSlr"))
            check = client.utility.verify_payment_signature(data)
            if check:
                pass
            else:

                print('payment_mode',payment_mode)
                # print(address_inst)
                if order_mode=='Self_Picking':
                    order_save = Order_detail(user=request.user,payment_mode=payment_mode,payment_id=data['razorpay_payment_id'],
                                              order_id=data['razorpay_order_id'],signature=data['razorpay_signature'],
                                              price=total_pay,store_user=store_user,time_slot=time_slot,
                                              order_mode='Self_Picking')
                    order_save.save()
                elif order_mode=='By_Delivery':
                    deli_address = Delivery_address(user=request.user, full_name=name,
                                                        phone=phone, email=email, address=address, city=city,
                                                        pincode=pincode,
                                                        locality=locality, landmark=landmark,
                                                        alternate_mobile=alternate_mobile)
                    deli_address.save()
                    order_save = Order_detail(user=request.user, payment_mode=payment_mode,
                                              payment_id=data['razorpay_payment_id'],
                                              order_id=data['razorpay_order_id'], signature=data['razorpay_signature'],
                                               price=total_pay, store_user=store_user,
                                               delivery_address=deli_address,order_mode='By_Delivery')
                    order_save.save()
                #order_save.item.set(cart_featch)
                for x in cart_featch:
                    prod_fake = Product_fake(Buyer=request.user,stor_details=x.store_user,category=x.variant_id.product.category,subcategory=x.variant_id.product.subcategory,
                                       brand_name=x.variant_id.product.brand_name,title=x.variant_id.product.title,price=x.variant_id.product.price,
                                       discount_percent=x.variant_id.product.discount_percent,gst_percent=x.variant_id.product.gst_percent,variant=x.variant_id.product.variant,
                                       image=x.variant_id.product.image)
                    prod_fake.save()
                    var_fake = Variants_fake(title=x.variant_id.title,real_var_id=x.variant_id.id,product=prod_fake,color=x.variant_id.color,size=x.variant_id.size,description=x.variant_id.description,
                                             image_fornt=x.variant_id.image_fornt,image_back=x.variant_id.image_back,image_side=x.variant_id.image_side,
                                             quantity=x.quantity,price=x.variant_id.price,point_value=x.variant_id.point_value,after_discount_price=x.variant_id.after_discount_price,
                                             variant_discount=x.variant_id.variant_discount)
                    var_fake.save()
                    order_save.item.add(var_fake)
                    var_featch=Variants.objects.get(id=x.variant_id.id)
                    var_featch.quantity=var_featch.quantity-x.quantity
                    var_featch.save()
                    # x.cart_status = True
                    # x.save()
                cart_featch.delete()
                return render(request,'success.html')
    else:
        return redirect('/login')




################################# End Success Payment / Razorpay #############

######################### Payment by COD ########################

def Payment_by_cod(request):
    if request.user.is_authenticated:
        print('code yha hai..')
        cart_featch = UserCart.objects.filter(user=request.user, cart_status=False)
        total_pay = 0
        store_user = ''
        for x in cart_featch:
            total_pay = total_pay + x.final_price
            store_user = x.store_user
        if request.method=="POST":
            print('ab code yha hai..')
            time_slot = request.POST.get('time_slot')
            payment_mode = request.POST.get('payment_mode')
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            address = request.POST.get('address')
            city = request.POST.get('city')
            pincode = request.POST.get('pincode')
            locality = request.POST.get('locality')
            landmark = request.POST.get('landmark')
            alternate_mobile = request.POST.get('alternate_phone')
            order_mode = request.POST.get('order_mode')


            order_id = 'Cod_order'+ str(randint(1111,4444))
            if order_mode=="Self_Picking":
                print('code time slot mae hai..')
                order_save = Order_detail(user=request.user, payment_mode=payment_mode,
                                           price=total_pay, store_user=store_user, time_slot=time_slot,
                                          order_mode='Self_Picking')
                order_save.save()
                obj=order_id+str(order_save.id)
                order_save.order_id=obj
                order_save.save()
            elif order_mode=='By_Delivery':
                deli_address = Delivery_address(user=request.user, full_name=name,
                                                phone=phone, email=email, address=address, city=city,
                                                pincode=pincode,
                                                locality=locality, landmark=landmark,
                                                alternate_mobile=alternate_mobile)
                deli_address.save()
                order_save = Order_detail(user=request.user, payment_mode=payment_mode,
                                           price=total_pay, store_user=store_user,
                                          delivery_address=deli_address,order_mode=order_mode)
                order_save.save()
                obj = order_id + str(order_save.id)
                order_save.order_id = obj
                order_save.save()

            for x in cart_featch:
                prod_fake = Product_fake(Buyer=request.user, stor_details=x.store_user,
                                         category=x.variant_id.product.category,
                                         subcategory=x.variant_id.product.subcategory,
                                         brand_name=x.variant_id.product.brand_name, title=x.variant_id.product.title,
                                         price=x.variant_id.product.price,
                                         discount_percent=x.variant_id.product.discount_percent,
                                         gst_percent=x.variant_id.product.gst_percent,
                                         variant=x.variant_id.product.variant,
                                         image=x.variant_id.product.image)
                prod_fake.save()
                var_fake = Variants_fake(title=x.variant_id.title, product=prod_fake, color=x.variant_id.color,
                                         real_var_id=x.variant_id.id,size=x.variant_id.size, description=x.variant_id.description,
                                         image_fornt=x.variant_id.image_fornt, image_back=x.variant_id.image_back,
                                         image_side=x.variant_id.image_side,
                                         quantity=x.quantity, price=x.variant_id.price,
                                         point_value=x.variant_id.point_value,
                                         after_discount_price=x.variant_id.after_discount_price,
                                         variant_discount=x.variant_id.variant_discount)
                var_fake.save()
                order_save.item.add(var_fake)
                var_featch = Variants.objects.get(id=x.variant_id.id)
                var_featch.quantity = var_featch.quantity - x.quantity
                var_featch.save()
                # x.cart_status = True
                # x.save()
            cart_featch.delete()
            return render(request, 'success.html')
    else:
        return redirect('/login')

##################################################################



################################## Wishlist ###############################

def wishlist(request):
    if request.user.is_authenticated:
        user_instance = User.objects.get(username = request.user.username)
        whishlist_featch = Wishlist.objects.filter(user = user_instance)
        li=[]
        for x in whishlist_featch:
            product_featch = Variants.objects.get(id=x.variant_id.id)
            li.append(product_featch)
        quantiy = 1
        li = zip(li,whishlist_featch)
        return render(request,'wishlist.html',{'li':li,'quantity':quantiy})
    else:
        return redirect('/login')

def wishlist_user(request,id):
    if request.user.is_authenticated:
        user_instance = User.objects.get(username=request.user.username)
        product_instance = Variants.objects.get(id=id)
        # print('ye prod inst hai..',product_instance.product.user)
        vendro_inst = User.objects.get(username=product_instance.product.user)
        vendro_store_inst = Vendor_Store_detail.objects.get(user=vendro_inst)
        try:
            print('code ye chal rha hai')
            whislist_featch = Wishlist.objects.get(variant_id=product_instance)
            print('ab code chal rha hai..')
            messages.info(request,'This product already add in your wishlist..')
            return redirect('/wishlist')
        except:
            print('know here run..')
            whishlist = Wishlist(user=user_instance,variant_id=product_instance,store_user=vendro_store_inst)
            whishlist.save()
            return redirect('/wishlist')
    else:
        return redirect('/login')

def wishlist_remove(request,id):
    if request.user.is_authenticated:
        whishlist_featch = Wishlist.objects.get(id=id)
        whishlist_featch.delete()
        return redirect("/wishlist")
    else:
        return redirect('/login')


def all_prod_cat(request,id):
    vendor_instance_create = Vendor_Store_detail.objects.get(id=id)
    c=vendor_instance_create.user.id
    print('ye user id hai...',c)
    cat_instance = Category.objects.get(name=vendor_instance_create.store_category)
    subcat_instance = Subcategory.objects.filter(category=cat_instance)
    li=[]
    l2=[]
    for x in subcat_instance:
        # product_featch = Product.objects.filter(user=vendor_instance_create.user,SubCategory=x)
        product_featch = Product.objects.filter(user=vendor_instance_create.user,subcategory__name=x,ecommerce_show_data=True)
        li.append(product_featch)
        for x in product_featch:
            if x.subcategory not in l2:
                l2.append(x.subcategory)
    print(l2)
    print(li,'ye l1 hai')
    subcat=zip(l2,li)

    return render(request,'cat_by_pro_or_store.html',{'subcat':subcat,'vendor':c,'store_detail':vendor_instance_create})


################################## Payment_address #####################

def payment_address(request):
    return render(request,'payment_address.html')



########################## end payment Address ##########################



##################### Your Order ##############################
def your_order_detail(request):
    if request.user.is_authenticated:
        order_featch = Order_detail.objects.filter(user=request.user,delivery_status=False).order_by('-date_time')


        return render(request,'your_order.html',{'order_featch':order_featch})
    else:
        return redirect('/login')


################ End Your Order ##############################

########################### Order Cancel #############

def order_cancel(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            order_idd = request.POST.get('order_id')
            reason = request.POST.get('reason')
            order_cacel_featch = Order_detail.objects.get(order_id = order_idd )
            order_cacel_featch.order_status='Cancel'
            order_cacel_featch.oreder_cancel_reason=reason
            x=datetime.datetime.now()
            date_time=x.strftime("%B") + ' ' + x.strftime("%d") + ',' + x.strftime("%Y") + ',' + x.strftime(
                "%I") + ':' + x.strftime("%M") + ' ' + x.strftime("%p")
            order_cacel_featch.cancel_date=date_time
            order_cacel_featch.save()
            for x in order_cacel_featch.item.all():
                real_variant_featch = Variants.objects.get(id=x.real_var_id)
                real_variant_featch.quantity = real_variant_featch.quantity + x.quantity
                real_variant_featch.save()
            return redirect('/your_order')
    else:
        return redirect('/login')

########################### End Order Cancel #############

############################################################ Vendor order related work ######################################

##################Self picking Pending Order ##################
def self_picking_pending_order(request):
    if request.user.is_authenticated:

        if request.method=="POST":
            order_idd = request.POST.get('order_id')
            ordr_featch = Order_detail.objects.get(order_id=order_idd)
            ordr_featch.order_status = 'Deliver'
            ordr_featch.save()
            try:
                new_user_object = User.objects.get(username=ordr_featch.user)
                refer_store_table_featch = Refer_id_store.objects.get(useer = new_user_object)
                try:
                    check_user_part_tree = TreeChain.objects.get(user=new_user_object)
                except:
                    if refer_store_table_featch.position == 'left':
                        print('code now here')
                        refer_generate_table = Refer_code.objects.get(refercode=refer_store_table_featch.refer_code)

                        objb = User.objects.get(
                            username=refer_generate_table.user)  # exist user in tree create instance
                        print(objb, '.........')
                        refer_by = objb
                        parent = TreeChain.objects.get(user=objb)
                        obb = parent.get_children()
                        print(obb.count())
                        # print('ye children hai...', objb.get_children())
                        left = True
                        right = False
                        print('yes yes you to close')
                        tree_adding(request, obb, new_user_object, parent, left, right, refer_by)

                        ##################### generaate refer code for new user ###################
                        print('ho gya kam')
                        c = randint(0000, 9999)
                        d = 'AVPL' + str(new_user_object.id) + str(c)  # refercode generate here...............
                        obj = Refer_code(user=new_user_object, refercode=d)
                        obj.save()

                        ################### Direct refer amount generate ########################
                        total_pv = 0
                        for x in ordr_featch.item.all():
                            total_pv = total_pv + x.point_value
                        desc = 'This PV is Earn By ' + str(new_user_object)
                        direct_refer_save = Direct_refer_statements(username=refer_by, desc=desc, amount=total_pv)
                        direct_refer_save.save()

                        ################### Direct refer amount end ##########################

                    if refer_store_table_featch.position == 'right':
                        refer_generate_table = Refer_code.objects.get(refercode=refer_store_table_featch.refer_code)

                        objb = User.objects.get(
                            username=refer_generate_table.user)  # exist user in tree create instance
                        print(objb, '.........')
                        refer_by = objb
                        parent = TreeChain.objects.get(user=objb)
                        obb = parent.get_children()
                        print(obb.count())
                        left = False
                        right = True
                        tree_adding(request, obb, new_user_object, parent, left, right, refer_by)
                        ##################### generaate refer code for new user ###################
                        c = randint(0000, 9999)
                        d = 'AVPL' + str(new_user_object.id) + str(c)  # refercode generate here...............
                        obj = Refer_code(user=new_user_object, refercode=d)
                        obj.save()

                        ###################### Direct refer save ######################
                        total_pv = 0
                        for x in ordr_featch.item.all():
                            total_pv = total_pv + x.point_value
                        desc = 'This PV is Earn By ' + str(new_user_object)
                        direct_refer_save = Direct_refer_statements(username=refer_by, desc=desc, amount=total_pv)
                        direct_refer_save.save()

                        ######################End Direct refer save ######################

            except:
                pass
            return redirect('/pending_order')
        user_inst = User.objects.get(username=request.user)
        vendor_inst = Vendor_Store_detail.objects.get(user=user_inst)
        order_featch = Order_detail.objects.filter(store_user=vendor_inst, order_status='Booked',
                                                   order_mode='Self_Picking').order_by('-date_time')
        print(order_featch)
        return render(request,'pending_order.html',{'order_featch':order_featch})

    else:
        return redirect('/login')

############### End Pending Order #################


################# Self picking cancle order ######

def self_picking_cancle_order(request):
    if request.user.is_authenticated:
        print('cond run here..')
        user_inst = User.objects.get(username=request.user)
        vendor_inst = Vendor_Store_detail.objects.get(user=user_inst)
        print(vendor_inst)
        order_featch = Order_detail.objects.filter(store_user=vendor_inst, order_status='Cancel',
                                                   order_mode='Self_Picking').order_by('-date_time')
        print(order_featch)
        return render(request,'pending_order.html',{'order_featch':order_featch})
    else:
        return redirect('/login')
################ end self picking cancle order ######

################## self_picking_deliver_order ###############
def self_picking_deliver_order(request):
    if request.user.is_authenticated:
        user_inst = User.objects.get(username=request.user)
        vendor_inst = Vendor_Store_detail.objects.get(user=user_inst)
        print(vendor_inst)
        order_featch = Order_detail.objects.filter(store_user=vendor_inst, order_status='Deliver',
                                                   order_mode='Self_Picking').order_by('-date_time')
        print(order_featch)
        return render(request, 'pending_order.html', {'order_featch': order_featch})
    else:
        return redirect('/login')
################### end self picking deliver_order_end #################



##################### by deliver /pending order ################

def deliver_pending_order(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            order_idd = request.POST.get('order_id')
            ordr_featch = Order_detail.objects.get(order_id=order_idd)
            ordr_featch.order_status = 'Deliver'
            ordr_featch.save()
            try:
                print('code')
                new_user_object = User.objects.get(username=ordr_featch.user)
                print('yes ')
                print(new_user_object,'new user hai...')
                refer_store_table_featch = Refer_id_store.objects.get(user = new_user_object)
                print(refer_store_table_featch,'ye bhi thik hai..')
                try:
                    print('code yha bhi')
                    check_user_part_tree = TreeChain.objects.get(user=new_user_object)


                except:
                    print('ab yha code')
                    if refer_store_table_featch.position == 'left':
                        print('code now here')
                        refer_generate_table = Refer_code.objects.get(refercode=refer_store_table_featch.refer_code)

                        objb = User.objects.get(username=refer_generate_table.user)# exist user in tree create instance
                        print(objb, '.........')
                        refer_by=objb
                        parent = TreeChain.objects.get(user=objb)
                        obb = parent.get_children()
                        print(obb.count())
                        # print('ye children hai...', objb.get_children())
                        left = True
                        right = False
                        print('yes yes you to close')
                        tree_adding(request, obb, new_user_object, parent, left, right, refer_by)

                        ##################### generaate refer code for new user ###################
                        print('ho gya kam')
                        c = randint(0000, 9999)
                        d = 'AVPL' + str(new_user_object.id) + str(c)  # refercode generate here...............
                        obj = Refer_code(user=new_user_object, refercode=d)
                        obj.save()

                        ################### Direct refer amount generate ########################
                        print('yes hum bhi run hue..')
                        total_pv = 0
                        for x in ordr_featch.item.all():
                            print('hum loop mae hai ab...')
                            total_pv = total_pv + x.point_value
                        print('loop kae bhar agya...')
                        desc = 'This PV is Earn By '+str(new_user_object)
                        print('apka desc bhi create kr rha..')
                        direct_refer_save = Direct_refer_statements(username = refer_by,desc=desc,amount=total_pv,status='Credit')
                        print('bus success mil hee gya...')
                        direct_refer_save.save()


                        ################### Direct refer amount end ##########################


                    if refer_store_table_featch.position == 'right':
                        refer_generate_table = Refer_code.objects.get(refercode=refer_store_table_featch.refer_code)

                        objb = User.objects.get(
                            username=refer_generate_table.user)  # exist user in tree create instance
                        print(objb, '.........')
                        refer_by = objb
                        parent = TreeChain.objects.get(user=objb)
                        obb = parent.get_children()
                        print(obb.count())
                        left = False
                        right = True
                        tree_adding(request, obb, new_user_object, parent, left, right, refer_by)
                        ##################### generaate refer code for new user ###################
                        c = randint(0000, 9999)
                        d = 'AVPL' + str(new_user_object.id) + str(c)  # refercode generate here...............
                        obj = Refer_code(user=new_user_object, refercode=d)
                        obj.save()

                        ###################### Direct refer save ######################
                        total_pv = 0
                        for x in ordr_featch.item.all():
                            total_pv = total_pv + x.point_value
                        desc = 'This PV is Earn By ' + str(new_user_object)
                        direct_refer_save = Direct_refer_statements(username=refer_by, desc=desc, amount=total_pv)
                        direct_refer_save.save()

                        ######################End Direct refer save ######################

            except:
                print('ye chl gya o no..')
            return redirect('/delivery_pending')
        user_inst = User.objects.get(username=request.user)
        vendor_inst = Vendor_Store_detail.objects.get(user=user_inst)
        print(vendor_inst)
        order_featch = Order_detail.objects.filter(store_user=vendor_inst, order_status='Booked',
                                                   order_mode='By_Delivery').order_by('-date_time')
        print(order_featch)
        return render(request, 'pending_order.html', {'order_featch': order_featch})
    else:
        return redirect('/login')


################## end by deliver/pending_order #########

################## by delivery / Cancle order ###############
def deliver_cancle_order(request):
    if request.user.is_authenticated:
        user_inst = User.objects.get(username=request.user)
        vendor_inst = Vendor_Store_detail.objects.get(user=user_inst)
        print(vendor_inst)
        order_featch = Order_detail.objects.filter(store_user=vendor_inst, order_status='Cancel',
                                                   order_mode='By_Delivery').order_by('-date_time')
        print(order_featch)
        return render(request, 'pending_order.html', {'order_featch': order_featch})
    else:
        return redirect('/login')

################### end by delivery / cancle order ########

######################## by delivery /Booked order ########
def deliver_confirm_order(request):
    if request.user.is_authenticated:
        user_inst = User.objects.get(username=request.user)
        vendor_inst = Vendor_Store_detail.objects.get(user=user_inst)
        print(vendor_inst)
        order_featch = Order_detail.objects.filter(store_user=vendor_inst, order_status='Deliver',
                                                   order_mode='By_Delivery').order_by('-date_time')
        print(order_featch)
        return render(request, 'pending_order.html', {'order_featch': order_featch})
    else:
        return redirect('/login')


##################### end by delivery / Booked order #####

########################## All Product Show ################

def all_product_vendor_dashboard(request):
    if request.user.is_authenticated:
        user_inst = User.objects.get(username=request.user)
        prod_inst = Product.objects.filter(user =user_inst,status=True)

        return render(request,'all_product.html',{'product':prod_inst})
    else:
        return redirect('/login')


###################### end all product show ####################

################# All variant data show ###################

def all_variant(request):
    if request.user.is_authenticated:
        data =request.GET.get('a')
        prod_inst =Product.objects.get(id=data)
        varinant_featch = Variants.objects.filter(product=prod_inst,variant_show_status=True)
        print(varinant_featch)
        return render(request,'all_variant.html',{'variant':varinant_featch,'data':data})
    else:
        return redirect('/login')

#################### end all variant data show ##############

############# Remove Variant #######################
def remove_variant(request):
    if request.user.is_authenticated:
        var_id =request.GET.get('ab')
        prod_id = request.GET.get('data')
        variant_featch = Variants.objects.get(id=var_id)
        variant_featch.variant_show_status=False
        variant_featch.save()
        var_featch = Variants.objects.filter(product=variant_featch.product,variant_show_status=True)
        print(var_featch.count())
        if var_featch.count()==0:
            print('code inside run..')
            variant_featch.product.ecommerce_show_data=False
            variant_featch.product.save()
        return redirect('/all_variant?a='+str(prod_id))
    else:
        return redirect('/login')


############ End remove variant ###############

############### Product Remove ############

def remove_product(request):
    if request.user.is_authenticated:
        data = request.GET.get('a')
        product_inst = Product.objects.get(id=data)
        product_inst.status =False
        product_inst.ecommerce_show_data=False
        product_inst.save()
        varint_inst =Variants.objects.filter(product=product_inst)
        for x in varint_inst:
            x.variant_show_status=False
            x.save()
        return redirect('/all_product')
    else:
        return redirect('/login')


################ End Product Remove ######

########################## Product Edit ###########################

def product_edit(request):
    if request.user.is_authenticated:
        id = request.GET.get('data')
        product_featch =Product.objects.get(id=id)
        variant_featch = Variants.objects.filter(product=product_featch)
        if request.user.is_authenticated:
            if request.method=="POST":
                title = request.POST.get('title')
                price = request.POST.get('price')
                gst = request.POST.get('gst')
                discount =request.POST.get('discount')
                x = datetime.datetime.now()
                date_time = x.strftime("%B") + ' ' + x.strftime("%d") + ',' + x.strftime("%Y") + ',' + x.strftime(
                    "%I") + ':' + x.strftime("%M") + ' ' + x.strftime("%p")
                product_featch.update_date = date_time
                product_featch.save()
                try:
                    image = request.FILES['front_image']
                    if discount:
                        product_featch.title=title
                        product_featch.price =price
                        product_featch.gst_percent=gst
                        product_featch.image = image
                        product_featch.discount_percent=discount
                        product_featch.save()

                        if variant_featch.count() != 0:
                            for x in variant_featch:
                                gst_fix = (float(gst) * float(x.price)) / 100
                                include_gst_price = gst_fix + float(x.price)
                                discount_add = (float(discount) * include_gst_price) / 100
                                final_pric = include_gst_price - discount_add
                                final_price = round(final_pric, 2)
                                x.after_discount_price = final_price
                                x.save()
                        messages.success(request,'Product update Successfully..')
                        return redirect('/edit_product/?data='+str(id))
                    else:
                        print('discount not')
                        product_featch.title = title
                        product_featch.price = price
                        product_featch.gst_percent = gst
                        product_featch.discount_percent = 0.0
                        product_featch.image = image
                        product_featch.save()
                        if variant_featch.count() != 0:
                            for x in variant_featch:
                                if x.variant_discount:
                                    gst_fix = (float(gst) * float(x.price)) / 100
                                    include_gst_price = gst_fix + float(x.price)
                                    discount_add = (float(x.variant_discount)* include_gst_price) / 100
                                    final_pric = include_gst_price - discount_add
                                    final_price = round(final_pric, 2)
                                    x.after_discount_price = final_price
                                    x.save()
                                else:
                                    gst_fix = (float(gst) * float(x.price)) / 100
                                    include_gst_price = gst_fix + float(x.price)
                                    final_price = round(include_gst_price, 2)
                                    x.after_discount_price = final_price
                                    x.save()
                        messages.success(request, 'Product update Successfully..')
                        return redirect('/edit_product/?data='+str(id))

                except:
                    if discount:
                        product_featch.title = title
                        product_featch.price = price
                        product_featch.gst_percent = gst
                        product_featch.discount_percent = discount
                        product_featch.save()

                        if variant_featch.count() != 0:
                            for x in variant_featch:
                                gst_fix = (float(gst) * float(x.price)) / 100
                                include_gst_price = gst_fix + float(x.price)
                                discount_add = (float(discount) * include_gst_price) / 100
                                final_pric = include_gst_price - discount_add
                                final_price = round(final_pric, 2)
                                x.after_discount_price = final_price
                                x.save()
                        messages.success(request, 'Product update Successfully..')
                        return redirect('/edit_product/?data='+str(id))
                    else:
                        print('discount not')
                        product_featch.title = title
                        product_featch.price = price
                        product_featch.gst_percent = gst
                        product_featch.discount_percent = 0.0
                        product_featch.save()
                        if variant_featch.count() != 0:
                            for x in variant_featch:
                                if x.variant_discount:
                                    gst_fix = (float(gst) * float(x.price)) / 100
                                    include_gst_price = gst_fix + float(x.price)
                                    discount_add = (float(x.variant_discount) * include_gst_price) / 100
                                    final_pric = include_gst_price - discount_add
                                    final_price = round(final_pric, 2)
                                    x.after_discount_price = final_price
                                    x.save()
                                else:
                                    gst_fix = (float(gst) * float(x.price)) / 100
                                    include_gst_price = gst_fix + float(x.price)
                                    final_price = round(include_gst_price, 2)
                                    x.after_discount_price = final_price
                                    x.save()
                        messages.success(request, 'Product update Successfully..')
                        return redirect('/edit_product/?data='+str(id))

        return render(request,'product_edit.html',{'product':product_featch})
    else:
        return redirect('/login')

####################### Product End #######################

########################## Edit variant ################

def variant_edit(request):
    if request.user.is_authenticated:
        id = request.GET.get('data')
        variant_featch = Variants.objects.get(id=id)
        if request.method == "POST":
            title = request.POST.get('title')
            price = request.POST.get('price')
            discount = request.POST.get('discount')
            description = request.POST.get('description')
            try:
                front_image = request.FILES['front_image']
            except:
                front_image = None
            try:
                back_image = request.FILES['back_image']
            except:
                back_image = None
            try:
                side_image = request.FILES['side_image']
            except:
                side_image=None

            pv_featch = PVset.objects.get(Subcategory=variant_featch.product.subcategory)
            pvset = (float(pv_featch.PV)*float(price))/100
            pv = round(pvset,2)
            variant_featch.point_value = pv
            variant_featch.save()
            x = datetime.datetime.now()
            date_time = x.strftime("%B") + ' ' + x.strftime("%d") + ',' + x.strftime("%Y") + ',' + x.strftime(
                "%I") + ':' + x.strftime("%M") + ' ' + x.strftime("%p")
            variant_featch.update_date_time = date_time
            variant_featch.save()
            if discount:
                if variant_featch.product.discount_percent:
                    variant_featch.title = title
                    variant_featch.price = price
                    variant_featch.description =description
                    variant_featch.save()
                    gst_fix = (float(variant_featch.product.gst_percent) * float(price)) / 100
                    include_gst_price = gst_fix + float(price)
                    discount_add = (float(variant_featch.product.discount_percent) * include_gst_price) / 100
                    final_pric = include_gst_price - discount_add
                    final_price = round(final_pric, 2)
                    variant_featch.after_discount_price = final_price
                    variant_featch.save()

                    if front_image !=None:
                        variant_featch.image_fornt=front_image
                        variant_featch.save()
                    if back_image !=None:
                        variant_featch.image_back =back_image
                        variant_featch.save()
                    if side_image != None:
                        variant_featch.image_side = side_image
                        variant_featch.save()
                    messages.success(request,'Your Variant Update successfully but discount not add first you need to remove product discount for apply variant discount..')
                    return redirect('/variant_edit/?data='+str(id))
                else:
                    variant_featch.title = title
                    variant_featch.price = price
                    variant_featch.description = description
                    variant_featch.variant_discount = discount
                    variant_featch.save()
                    gst_fix = (float(variant_featch.product.gst_percent) * float(price)) / 100
                    include_gst_price = gst_fix + float(price)
                    discount_add = (float(discount) * include_gst_price) / 100
                    final_pric = include_gst_price - discount_add
                    final_price = round(final_pric, 2)
                    variant_featch.after_discount_price = final_price
                    variant_featch.save()

                    if front_image != None:
                        variant_featch.image_fornt = front_image
                        variant_featch.save()
                    if back_image != None:
                        variant_featch.image_back = back_image
                        variant_featch.save()
                    if side_image != None:
                        variant_featch.image_side = side_image
                        variant_featch.save()
                    messages.success(request,'Variant updated Successfully...')
                    return redirect('/variant_edit/?data=' + str(id))
            else:
                if variant_featch.product.discount_percent:
                    variant_featch.title = title
                    variant_featch.price = price
                    variant_featch.description =description
                    variant_featch.save()
                    gst_fix = (float(variant_featch.product.gst_percent) * float(price)) / 100
                    include_gst_price = gst_fix + float(price)
                    discount_add = (float(variant_featch.product.discount_percent) * include_gst_price) / 100
                    final_pric = include_gst_price - discount_add
                    final_price = round(final_pric, 2)
                    variant_featch.after_discount_price = final_price
                    variant_featch.save()

                    if front_image !=None:
                        variant_featch.image_fornt=front_image
                        variant_featch.save()
                    if back_image !=None:
                        variant_featch.image_back =back_image
                        variant_featch.save()
                    if side_image != None:
                        variant_featch.image_side = side_image
                        variant_featch.save()
                    messages.success(request,'Variant updated Successfully with product discount..')
                    return redirect('/variant_edit/?data=' + str(id))
                else:
                    variant_featch.title = title
                    variant_featch.price = price
                    variant_featch.description = description
                    variant_featch.save()
                    gst_fix = (float(variant_featch.product.gst_percent) * float(price)) / 100
                    include_gst_price = gst_fix + float(price)
                    final_price = round(include_gst_price, 2)
                    variant_featch.after_discount_price = final_price
                    variant_featch.save()

                    if front_image != None:
                        variant_featch.image_fornt = front_image
                        variant_featch.save()
                    if back_image != None:
                        variant_featch.image_back = back_image
                        variant_featch.save()
                    if side_image != None:
                        variant_featch.image_side = side_image
                        variant_featch.save()
                    messages.success(request, 'Variant updated Successfully...')
                    return redirect('/variant_edit/?data=' + str(id))

        return render(request,'edit_variant.html',{'variant':variant_featch})
    else:
        return redirect('/login')
##################### end edit variant ###############


################# Time Slot ####################

def vendor_time_create(request):
    if request.user.is_authenticated:

        if request.method=='POST':
            from_time = request.POST.get('from_time')
            to_time = request.POST.get('to_time')
            day = request.POST.get('day')
            vendor_store_featch = Vendor_Store_detail.objects.get(user=request.user)
            slot =vendor_time_slot(from_time=from_time,to_time=to_time,day=day,user=request.user,vendor_store=vendor_store_featch)
            slot.save()
            return redirect('/vendor_time_create')
        else:
            time_slot_featch =vendor_time_slot.objects.filter(user=request.user)
            return render(request,'time_slot_create.html',{'time_slot':time_slot_featch})
    else:
        return redirect('/login')

################## End Time Slot ##############

################## remove time slot #########

def remove_slot(request):
    if request.user.is_authenticated:
        id = request.GET.get('data')
        slot_featch = vendor_time_slot.objects.get(id=id)
        slot_featch.delete()
        return redirect('/vendor_time_create')
    else:
        return redirect('/login')
############# end remove time slot #############


############# MLM Tree View ############

def mlm_tree(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST['name']

            try:
                refer_featch = Refer_code.objects.get(refercode=name)
                obj=User.objects.get(username=refer_featch.user)
                obbj=TreeChain.objects.get(user=obj.id)
                child=obbj.get_descendants(include_self=False)
                print(child )
                left_count=0
                right_count=0
                for x in child:
                    if x.right==True:
                        right_count=right_count + 1
                    if x.left == True:
                        left_count = left_count + 1


                print('*************************')
    ################################### Uper part ka hai main start #########################
                lv_1=obbj.get_children()

                li=[]
                print(lv_1.count())
                if lv_1.count() == 1:
                    print('y')
                    for x in lv_1:
                        if x.left==True:
                            print('yes')
                            refer_code_featch = Refer_code.objects.get(user=x.user)
                            li.insert(0,refer_code_featch.refercode)
                            li.insert(1,' ')
                        else:
                            if not li:
                                li.insert(0,' ')
                                refer_code_featch = Refer_code.objects.get(user=x.user)
                                li.insert(1, refer_code_featch.refercode)
                            else:
                                refer_code_featch = Refer_code.objects.get(user=x.user)
                                li.insert(1, refer_code_featch.refercode)
                if lv_1.count() == 2:
                    for x in lv_1:
                        if x.left==True:
                            refer_code_featch = Refer_code.objects.get(user=x.user)
                            li.insert(0,refer_code_featch.refercode)
                        else:
                            refer_code_featch = Refer_code.objects.get(user=x.user)
                            li.insert(1, refer_code_featch.refercode)
                print('ye li fdfdhai...',li)
    ##########################################check start here of lv_1 ###########################
                if lv_1.count():
                    if li[0] != ' ' and li[1] != ' ':
                        print('under bunder bich samunder....')
                        refer_return_make_user = Refer_code.objects.get(refercode=li[0])
                        tre_inst = TreeChain.objects.get(user=refer_return_make_user.user.treechain.user)
                        print('tre',tre_inst)
                        refer_return_make_user = Refer_code.objects.get(refercode=li[1])
                        tre_inst2 = TreeChain.objects.get(user=refer_return_make_user.user.treechain.user)
                        print('yes',tre_inst2)
                        print('mae hu...')
                        lv_1_child=tre_inst.get_children()
                        print('child do..')
                        li_1 = []
                        print('ye lv_1 child hqi',lv_1_child)

                        if lv_1_child.count() == 1:
                            for x in lv_1_child:
                                if x.left == True:
                                    refer_code_featch = Refer_code.objects.get(user=x.user)
                                    li_1.insert(0, refer_code_featch.refercode)
                                    li_1.insert(1,' ')
                                else:
                                    if not li_1:
                                        li_1.insert(0, ' ')
                                        refer_code_featch = Refer_code.objects.get(user=x.user)
                                        li_1.insert(1, refer_code_featch.refercode)
                                    else:
                                        refer_code_featch = Refer_code.objects.get(user=x.user)
                                        li_1.insert(1, refer_code_featch.refercode)
                        if lv_1_child.count() == 2:
                            for x in lv_1_child:
                                if x.left == True:
                                    refer_code_featch = Refer_code.objects.get(user=x.user)
                                    li_1.insert(0,refer_code_featch.refercode)
                                else:
                                    refer_code_featch = Refer_code.objects.get(user=x.user)
                                    li_1.insert(1,refer_code_featch.refercode)
                        lv_2_child=tre_inst2.get_children()
                        li_2 = []
                        if lv_2_child.count() == 1:
                            for x in lv_2_child:
                                if x.left == True:
                                    refer_code_featch = Refer_code.objects.get(user=x.user)
                                    li_2.insert(0, refer_code_featch.refercode)
                                    li_2.insert(1,' ')
                                else:
                                    if not li_2:
                                        li_2.insert(0, ' ')
                                        refer_code_featch = Refer_code.objects.get(user=x.user)
                                        li_2.insert(1, refer_code_featch.refercode)
                                    else:
                                        refer_code_featch = Refer_code.objects.get(user=x.user)
                                        li_2.insert(1, refer_code_featch.refercode)
                        if lv_2_child.count() == 2:
                            for x in lv_2_child:
                                if x.left == True:
                                    refer_code_featch = Refer_code.objects.get(user=x.user)
                                    li_2.insert(0, refer_code_featch.refercode)
                                else:
                                    refer_code_featch = Refer_code.objects.get(user=x.user)
                                    li_2.insert(1, refer_code_featch.refercode)
                        print('condition 2 run hua')

                        return render(request, 'tree_view.html',{'obb': li, 'obj': refer_featch.refercode, 'left': left_count, 'right': right_count,'lv_1_child':li_1,'lv_2_child':li_2})
                    if li[0] !=' ' and li[1] == ' ':
                        li_1=[]
                        print('ye lo not equal space')
                        refer_return_make_user = Refer_code.objects.get(refercode=li[0])

                        # user_inst = User.objects.get()
                        tre_inst = TreeChain.objects.get(user=refer_return_make_user.user.treechain.user)
                        print('ha ab thik hai..')
                        lv_1_child = tre_inst.get_children()
                        if lv_1_child.count() == 1:
                            for x in lv_1_child:
                                if x.left == True:
                                    refer_code_featch = Refer_code.objects.get(user=x.user)
                                    li_1.insert(0, refer_code_featch.refercode)
                                    li_1.insert(1,' ')
                                else:
                                    if not li_1:
                                        li_1.insert(0, ' ')
                                        refer_code_featch = Refer_code.objects.get(user=x.user)
                                        li_1.insert(1, refer_code_featch.refercode)
                                    else:
                                        refer_code_featch = Refer_code.objects.get(user=x.user)
                                        li_1.insert(1, refer_code_featch.refercode)
                        if lv_1_child.count() == 2:
                            for x in lv_1_child:
                                if x.left == True:
                                    refer_code_featch = Refer_code.objects.get(user=x.user)
                                    li_1.insert(0, refer_code_featch.refercode)
                                else:
                                    refer_code_featch = Refer_code.objects.get(user=x.user)
                                    li_1.insert(1, refer_code_featch.refercode)
                        li_2=[' ',' ']
                        return render(request, 'tree_view.html',{'obb': li, 'obj': refer_featch.refercode, 'left': left_count, 'right': right_count, 'lv_1_child': li_1,'lv_2_child': li_2})


                    if li[0] ==' ' and li[1] != ' ':
                        print('yes l1 not equal free space')
                        li_2 = []
                        print('ye lo not equal space')
                        refer_return_make_user = Refer_code.objects.get(refercode=li[1])
                        tre_inst = TreeChain.objects.get(user=refer_return_make_user.user.treechain.user)
                        lv_2_child = tre_inst.get_children()
                        if lv_2_child.count() == 1:
                            for x in lv_2_child:
                                if x.left == True:
                                    refer_code_featch = Refer_code.objects.get(user=x.user)
                                    li_2.insert(0, refer_code_featch.refercode)
                                    li_2.insert(1,' ')
                                else:
                                    if not li_2:
                                        li_2.insert(0, ' ')
                                        refer_code_featch = Refer_code.objects.get(user=x.user)
                                        li_2.insert(1, refer_code_featch.refercode)
                                    else:
                                        refer_code_featch = Refer_code.objects.get(user=x.user)
                                        li_2.insert(1, refer_code_featch.refercode)
                        if lv_2_child.count() == 2:
                            for x in lv_2_child:
                                if x.left == True:
                                    refer_code_featch = Refer_code.objects.get(user=x.user)
                                    li_2.insert(0, refer_code_featch.refercode)
                                else:
                                    refer_code_featch = Refer_code.objects.get(user=x.user)
                                    li_2.insert(1, refer_code_featch.refercode)

                        li_1=[' ',' ']
                        return render(request, 'tree_view.html',{'obb': li, 'obj': refer_featch.refercode, 'left': left_count, 'right': right_count, 'lv_1_child': li_1,'lv_2_child': li_2})
                else:
                    print('condition else run hua hai')
                    return render(request, 'tree_view.html',{'obj': refer_featch.refercode, 'left': left_count, 'right': right_count})
            except:
                messages.error(request,'Invaild Refer Code')




        return render(request,'tree_view.html')
    else:
        return redirect('/login')

########### End MLM Tree View ##########

################### mlm_pannel #################

def mlm_pannel(request):
    if request.user.is_authenticated:
        direct_refer_featch = Direct_refer_statements.objects.filter(username=request.user).order_by('-date_time')
        direct_refer_pv = 0
        for x in direct_refer_featch:
            direct_refer_pv = direct_refer_pv + x.amount
        return render(request,'mlm_pannel.html',{'direct_refer':direct_refer_featch,'direct_refer_pv':direct_refer_pv})
    else:
        return redirect('/login')


################# end mlm pannel ################

def user_wallet(request):
    if request.user.is_authenticated:
        direct_refer_featch = Direct_refer_statements.objects.filter(username=request.user).order_by('-date_time')
        direct_refer_pv = 0
        for x in direct_refer_featch:
            direct_refer_pv = direct_refer_pv + x.amount
        return render(request,'wallet.html',{'direct_refer_pv':direct_refer_pv})
    else:
        return redirect('/login')


############################## User Complain #############################

def new_user_complain(request):
    return render(request,'new_complain.html')



######################### end user complain ##########################

########################## user chat complain #######################

def chat_complian(request):
    return render(request,'chat_complain.html')

#################### end user chat complain #######################