from rest_framework import serializers
from app.models import *
from django.contrib.auth.models import User

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['id','username','first_name','last_name']
class UserRegisterSerializers(serializers.ModelSerializer):
    # user=UserSerializers()
    class Meta:
        model=User_register
        # fields = ['user','mobile','gender','address']
        fields='__all__'



class VendorRegisterSerializers(serializers.ModelSerializer):
        user=UserSerializers()
        class Meta:
            model=Vendor_registration
            # fields = ['user','store_mobile','gender','store_address']
            fields='__all__'
class VendorStoreDetailSerializers(serializers.ModelSerializer):
    # user=UserSerializers()
    class Meta:
        model=Vendor_Store_detail()
        fields='__all__'


class VendorRegStodcuDetSerializers(serializers.ModelSerializer):
    user=UserSerializers()
    class Meta:
        model=Vendor_store_document()
        # fields=['user','store_seller_aadhar','store_seller_gst','store_seller_front_aadhar_image','store_seller_back_aadhar_image',
        #         'store_seller_pancard','store_seller_pancard_image','store_shiping_policy',
        #           'store_return_policy','store_bank_account_number','store_bank_name','store_bank_ifsc',
        #            'store_bank_passbook','store_seller_razorpay_id','created']
        fields='__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=contact
        # fields=['name','email','mobile','message','datetime']
        fields='__all__'
############################################################ filter######
##all in one me views and url bana padega
class ProductSerialize(serializers.ModelSerializer):
    class Meta:
        model=Product
        # fields=['title','description','retailer_price','price','gst_percent','discount_percent','quantity']
        fields='__all__'

class SubSubcategorySerializer(serializers.ModelSerializer):
    # subcategory=SubcategorySerializer()
    product=ProductSerialize(many=True)
    class Meta:
        model=Brands
        fields=['name','product']#'subcategory',


class SubcategorySerializer(serializers.ModelSerializer):
    # category=CategorySerializer()
    subsubcategory=SubSubcategorySerializer(many=True)
    class Meta:
        model=Subcategory
        fields=['name','subsubcategory']#'category',
#reverse me jaye ga data,CategorySerializer se all list ayega
class CategorySerializer(serializers.ModelSerializer): 
    subcategory=SubcategorySerializer(many=True)
    
    class Meta:
        model=Category
        fields=['name','subcategory']


# https://www.youtube.com/watch?v=EyMFf9O6E60
######### only catgery list#########

class CategorySerializer_only(serializers.ModelSerializer):
    
    class Meta:
        model=Category
        # fields=['id','name','image']
        fields='__all__'

class SubcategorySerializer_only(serializers.ModelSerializer):
    class Meta:
        model=Subcategory
        fields=['category_id','id','name','image']
class SubSubcategorySerializer_only(serializers.ModelSerializer):
    
    class Meta:
        model=Brands
        fields=['subcategory_id','id','name','image']
        # fields='__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banner
        # fields=['id','image','title','description']
        fields='__all__'
        

class Bottom_BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bottom_Banner
        # fields=['id','image','title','description']
        fields='__all__'



class ProductSerializeALL(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Images
        fields='__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Color
        fields='__all__'






