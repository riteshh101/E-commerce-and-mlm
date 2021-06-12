from django.contrib import admin
from .models import *
from mptt.admin import DraggableMPTTAdmin
# Register your models here.

############################################################# Category #################################################
#
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]
#
@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Subcategory._meta.fields]
@admin.register(Brands)
class SubSubCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Brands._meta.fields]
#
# ################################################################## Product #################################################
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Product._meta.fields]

# #############################################################User Register Show Here ####################################
@admin.register(User_register)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User_register._meta.fields]
#
# ######################################################## Vendor Register Here ########################################
#
@admin.register(Vendor_registration)
class VendorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Vendor_registration._meta.fields]

@admin.register(Vendor_Store_detail)
class VendorStoreAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Vendor_Store_detail._meta.fields]

@admin.register(Vendor_store_document)
class VendorStoreDocumentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Vendor_store_document._meta.fields]

# ###################################################### Cart ###########################################################
#
@admin.register(UserCart)
class CartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserCart._meta.fields]
#
# ################################################### Buy Sponser Product Show#########################################
#
# @admin.register(buy_sponser)
# class BuySponserAdmin(admin.ModelAdmin):
#     list_display = ['id','username','product_name','price']
#
# ################################################# Sponser_user_address_Detail ###########################################
#
# @admin.register(Sponser_user_address)
# class SponserAddressAdmin(admin.ModelAdmin):
#     list_display = ['id','username','sponserid','position','city']
#
# ################################################## Refer_Code Detail #################################################
@admin.register(Refer_code)
class ReferCodeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Refer_code._meta.fields]
#
# ################################################### Direct Refer Statement #####################################
#
# @admin.register(Direct_refer_statements)
# class DirectreferAdmin(admin.ModelAdmin):
#     list_display = ['id','username','desc','amount','date_time']
#
# ###################################################### PV VALUE SET ############################################
#
@admin.register(PVset)
class PvAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PVset._meta.fields]
# ################################################## Tree Chain ######################################################
#
admin.site.register(
    TreeChain,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)

#

############################################# Contact#######################################
@admin.register(contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','mobile','message','datetime']

######################################### OTP ############################################
@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['id','email','otp']

##################################### Wishlist ########################################
@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Wishlist._meta.fields]

##################################### Random Address ##############################

@admin.register(random_address)
class RandomAddressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in random_address._meta.fields]

#################### refer_code_sotre/position ################

@admin.register(Refer_id_store)
class Refer_id_storeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Refer_id_store._meta.fields]


#################################################################

############################# Shipping Address ################
@admin.register(Delivery_address)
class Shipping_address_admin(admin.ModelAdmin):
    list_display = [field.name for field in Delivery_address._meta.fields]

###############################################################
############################ Order_detail #########################
@admin.register(Order_detail)
class Order_deatilAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order_detail._meta.fields]


###########################################################

# @admin.register(Product_image)
# class Product_imageAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Product_image._meta.fields]

############################# Bottom Banner ###########################

@admin.register(Bottom_Banner)
class BottomBannerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bottom_Banner._meta.fields]

########################## End bottom Banner #######################


################################## Top Banner ################################
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Banner._meta.fields]
######################### End Top Banner ##############################

############### Shubham Sir ka code ##########################

class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    #readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True

class ImagesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Images._meta.fields]

class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    list_filter = ['subcategory']
    #readonly_fields = ('image_tag',)
    inlines = [ProductImageInline,ProductVariantsInline]
    #prepopulated_fields = {'slug': ('title',)}
#
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ['subject','comment', 'status','create_at']
#     list_filter = ['status']
#     readonly_fields = ('subject','comment','user','product','rate','id')

class ColorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Color._meta.fields]

class SizeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Size._meta.fields]

# class ContectusmsgAdmin(admin.ModelAdmin):
#     list_display = ['name','email','topics']


class VariantsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Variants._meta.fields]


admin.site.register(Variants,VariantsAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Color,ColorAdmin)
admin.site.register(Size,SizeAdmin)
admin.site.register(Product,ProductAdmin)
#admin.site.register(Contectusmsg,ContectusmsgAdmin)

##########################################################


################# fake_product #################
@admin.register(Product_fake)
class product_fake_admin(admin.ModelAdmin):
    list_display = [field.name for field in Product_fake._meta.fields]



##############End Fake_product##################


############# fake_variant ##################

@admin.register(Variants_fake)
class variant_fake_admin(admin.ModelAdmin):
    list_display = [field.name for field in Variants_fake._meta.fields]

############## end fake variant ##########

@admin.register(vendor_time_slot)
class vendor_time_slot_admin(admin.ModelAdmin):
    list_display = [field.name for field in vendor_time_slot._meta.fields]

##################### Direct Refer_pv statements ##########

@admin.register(Direct_refer_statements)
class Direct_refer_admin(admin.ModelAdmin):
    list_display = [field.name for field in Direct_refer_statements._meta.fields]