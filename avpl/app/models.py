from django.db import models

from django.contrib.auth.models import User,AbstractUser
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
############################################# User Registration #######################################################
class User_register(models.Model):
    user =  models.OneToOneField(User,on_delete=models.CASCADE)
    mobile = models.IntegerField()
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    gender = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50,null=True)
    longitude = models.CharField(max_length=50,null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200,null=True)
    otp = models.CharField(max_length=20,null=True)
    profile_pic = models.ImageField(upload_to='profile_pic',null=True)
    utype = models.CharField(max_length=100,default='User')
    date_time = models.DateTimeField(auto_now_add=True, null=True)
    update_date_time = models.CharField(max_length=100, null=True)


# ########################################## Binary Tree ###############################################################3
class TreeChain(MPTTModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    refer_by = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    left = models.BooleanField()
    right = models.BooleanField()

    def __str__(self):
        return self.user.username
#
# ########################################### Refer Code ###############################################################
class Refer_code(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    refercode = models.CharField(max_length=300)
    date_time  = models.DateTimeField(auto_now_add=True,null=True)

#
# ########################################## Category And Sub Ctaegory #################################################
#
class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category',null=True)
    date_time = models.DateTimeField(auto_now_add=True, null=True)
    update_date_time = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name
class Subcategory(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='subcategory',null=True)
    date_time = models.DateTimeField(auto_now_add=True, null=True)
    update_date_time = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name
class Brands(models.Model):
    subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image=models.ImageField(upload_to='brand',null=True)
    date_time  = models.DateTimeField(auto_now_add=True,null=True)
    update_date_time = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name

# ########################################################## PV Set Here ##################################################
#
class PVset(models.Model):
    Subcategory = models.ForeignKey(Subcategory,on_delete=models.CASCADE)
    PV = models.FloatField()
#
# ###################################################### Prouct Model Here ########################################################
class Vendor_registration(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    store_mobile = models.IntegerField()
    vendor_status = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='vendor_profile_pic',null=True)
    store_status = models.BooleanField(default=False)
    store_remove = models.BooleanField(default=False)
    created= models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=10,null=True)
    utype = models.CharField(max_length=100, default='Vendor')
    update_date_time = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.user.username

class Vendor_Store_detail(models.Model):
    vendor = models.OneToOneField(Vendor_registration,on_delete=models.CASCADE,null=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    store_name = models.CharField(max_length=200)
    store_address = models.CharField(max_length=200,null=True)
    store_zipcode = models.CharField(max_length=20,null=True)
    store_latitude = models.CharField(max_length=200,null=True)
    store_longitude = models.CharField(max_length=200,null=True)
    store_description = models.TextField()
    store_registration_number = models.CharField(max_length=100,null=True)
    store_category = models.CharField(max_length=200)
    store_logo = models.ImageField(upload_to='store_logo')
    store_banner = models.ImageField(upload_to='store_banner')
    store_image = models.ImageField(upload_to='store_image')
    store_closing_day = models.CharField(max_length=200)
    store_closing_time = models.CharField(max_length=20)
    store_opening_time = models.CharField(max_length=20)
    store_created_at = models.DateTimeField(auto_now_add=True)
    store_update_at = models.DateTimeField(auto_now_add=True)

class Vendor_store_document(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    store_seller_aadhar = models.IntegerField()
    store_seller_gst = models.CharField(max_length=100)
    store_seller_front_aadhar_image = models.FileField(upload_to='store_seller_aadhar_image')
    store_seller_back_aadhar_image = models.FileField(upload_to='store_seller_aadhar_image',null=True)
    store_seller_pancard = models.CharField(max_length=100)
    store_seller_pancard_image = models.FileField(upload_to='store_seller_pancard_image')
    store_shiping_policy = models.FileField(upload_to='shiping_policy',null=True)
    store_return_policy = models.FileField(upload_to='return_policy',null=True)
    store_bank_account_number = models.CharField(max_length=300)
    store_bank_name = models.CharField(max_length=100)
    store_bank_ifsc = models.CharField(max_length=100)
    store_bank_passbook = models.FileField(upload_to='store_bank_passbook')
    store_seller_razorpay_id = models.CharField(max_length=200,null=True)
    created = models.DateTimeField(auto_now_add=True)
    update_date_time = models.CharField(max_length=100,null=True)


class Product(models.Model):
    VARIANTS = (
        ('Size', 'Size'),
        ('Color', 'Color'),
        ('Size-Color', 'Size-Color'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    stor_details=models.ForeignKey(Vendor_Store_detail,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand_name = models.ForeignKey(Brands, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_percent = models.FloatField(blank=True, null=True)
    gst_percent = models.FloatField(blank=True, null=True)
    variant = models.CharField(max_length=10, choices=VARIANTS, default='Size')
    image = models.ImageField(upload_to='product', null=True)
    status = models.BooleanField(default=False)
    created_date =models.DateTimeField(auto_now_add=True,null=True)
    update_date = models.CharField(max_length=100,null=True)
    ecommerce_show_data = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def amount_to_pay(self):
        return self.price - self.price * (self.discount_percent / 100)

    def amount_to_pay_retailer(self):
        return self.retailer_price - self.price * (self.discount_percent / 100)

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""


class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.URLField(max_length=6000, blank=True)

    def __str__(self):
        return self.title


# class Comment(models.Model):
#     STATUS = (
#         ('New', 'New'),
#         ('True', 'True'),
#         ('False', 'False'),
#     )
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     subject = models.CharField(max_length=50, blank=True)
#     comment = models.CharField(max_length=250, blank=True)
#     rate = models.IntegerField(default=1)
#     status = models.CharField(max_length=10, choices=STATUS, default='New')
#     create_at = models.DateTimeField(auto_now_add=True)
#     update_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.subject


class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}">Color </p>'.format(self.code))
        else:
            return ""


class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)
    date_time = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name


class Variants(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(null=True)
    image_fornt = models.ImageField(upload_to='image_front',null=True)
    image_back = models.ImageField(upload_to='image_back',null=True)
    image_side = models.ImageField(upload_to='image_side',null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    point_value = models.FloatField(null=True)
    after_discount_price = models.FloatField(null=True)
    variant_discount = models.FloatField(null=True)
    variant_show_status = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True,null=True)
    update_date_time = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""



###################### Fake product table only use for order######################

class Product_fake(models.Model):
    Buyer = models.ForeignKey(User,on_delete=models.CASCADE)
    stor_details=models.ForeignKey(Vendor_Store_detail,on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_percent = models.FloatField(blank=True, null=True)
    gst_percent = models.FloatField(blank=True, null=True)
    variant = models.CharField(max_length=10)
    image = models.ImageField(upload_to='product_fake', null=True)
    created_date =models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.title

    def amount_to_pay(self):
        return self.price - self.price * (self.discount_percent / 100)

    def amount_to_pay_retailer(self):
        return self.retailer_price - self.price * (self.discount_percent / 100)

    def image_tag(self):
        if self.image.url is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
        else:
            return ""

###################### end fake product table/only user for order ########################

######################## fake variant table ##################


class Variants_fake(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product_fake, on_delete=models.CASCADE)
    real_var_id = models.IntegerField(null=True)
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    description = models.TextField(null=True)
    image_fornt = models.ImageField(upload_to='image_front_fake',null=True)
    image_back = models.ImageField(upload_to='image_back_fake',null=True)
    image_side = models.ImageField(upload_to='image_side_fake',null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    point_value = models.FloatField(null=True)
    after_discount_price = models.FloatField(null=True)
    variant_discount = models.FloatField(null=True)
    date_time = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.title

    def image(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            varimage = img.image.url
        else:
            varimage = ""
        return varimage

    def image_tag(self):
        img = Images.objects.get(id=self.image_id)
        if img.id is not None:
            return mark_safe('<img src="{}" height="50"/>'.format(img.image.url))
        else:
            return ""



################### end fake variant table/only use for order ###############


# #####################################################Direct refer Statement genrate here############################################
#
class Direct_refer_statements(models.Model):
    username=models.ForeignKey(User,on_delete=models.CASCADE)
    desc = models.CharField(max_length=100)
    amount = models.FloatField()
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100,null=True)


################################################ Pv Earn By self ##########################################


class pv_earn_by_self(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    desc = models.CharField(max_length=200)
    amount = models.FloatField()
    date_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)



# ################################################ Cart ###############################################################
#
class UserCart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    variant_id = models.ForeignKey(Variants,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    store_user = models.ForeignKey(Vendor_Store_detail,on_delete=models.CASCADE)
    final_price = models.FloatField(default='0.0')
    cart_status = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True,null=True)
    update_date_time = models.CharField(max_length=100,null=True)

############################################# Contact Form #######################################

class contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    mobile = models.IntegerField()
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
############################################# For Otp matching #####################################3
class Otp(models.Model):
    email=models.CharField(max_length=100)
    otp=models.CharField(max_length=20)

########################################### Wishlist ################################################

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    store_user = models.ForeignKey(Vendor_Store_detail,on_delete=models.CASCADE)
    variant_id = models.OneToOneField(Variants,on_delete=models.CASCADE)
    date_time =models.DateTimeField(auto_now_add=True,null=True)
####################################  Randm address picker by user ################################

class random_address(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now_add=True,null=True)

################################ baneer model ##############################

class Banner(models.Model):
    image = models.ImageField(upload_to='banner')
    title = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.title


############################ Product Shipping Address #################

class Delivery_address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.PositiveIntegerField()
    email = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.PositiveIntegerField()
    locality = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200,null=True)
    alternate_mobile = models.IntegerField(null=True)
    house_number = models.CharField(max_length=100,null=True)
    date_time = models.DateTimeField(auto_now_add=True,null=True)


#################### order detail / History ###################################
class Order_detail(models.Model):
    order_stat = (
        ('Deliver', 'Deliver'),
        ('Booked', 'Booked'),
        ('Cancel', 'Cancel'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ManyToManyField(Variants_fake)
    store_user = models.ForeignKey(Vendor_Store_detail,on_delete=models.CASCADE)
    payment_mode = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=200)
    order_id = models.CharField(max_length=200)
    signature=models.CharField(max_length=200)
    order_status = models.CharField(default='Booked',choices=order_stat,max_length=100)
    delivery_status = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)
    cancel_date = models.CharField(max_length=50,null=True)
    delivery_address = models.ForeignKey(Delivery_address,on_delete=models.CASCADE,null=True)
    time_slot = models.CharField(max_length=100,null=True)
    order_mode = models.CharField(max_length=40)
    price = models.FloatField()
    oreder_cancel_reason = models.TextField(null=True)

# ############################End  Product Shipping Address #################


################ Bottom Banner ##############################


class Bottom_Banner(models.Model):
    image = models.ImageField(upload_to='bottom_banner')
    title = models.CharField(max_length=100)
    description = models.TextField()
    def __str__(self):
        return self.title




################# End Bottom banner ##########################


################refer_id_store/position#########################

class Refer_id_store(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    refer_code = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    status=models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True,null=True)


##################enn refere_id_sotre/position#################


class vendor_time_slot(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    vendor_store = models.ForeignKey(Vendor_Store_detail,on_delete=models.CASCADE)
    from_time = models.CharField(max_length=100)
    to_time = models.CharField(max_length=100)
    day = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)

############################ Wallet history #########################
# class wallet(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
#     desc = models.CharField(max_length=200)
#     status = models.CharField(max_length=100)
#     amount = models.FloatField()
#     date_time = models.DateTimeField(auto_now_add=True)



######################## End Wallet History ######################

##################### Complain Chat ##############################

class complain(models.Model):
    sender = models.CharField(max_length=200)
    recevier = models.CharField(max_length=200)
    mark_read = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)
    msg = models.TextField()


#################### end complain chat #########################