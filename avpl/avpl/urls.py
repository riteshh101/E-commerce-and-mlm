"""avpl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app import views
from app import api_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(api_urls)),

    ####################### MLM all Urls #########################
    #
    path('tree_view/',views.mlm_tree,name='tree_view'),
    path('mlm_pannel/',views.mlm_pannel,name='mlm_pannel'),
    path('wallet_section/',views.user_wallet,name='wallet_section'),

    ####################### User all Urls #########################

    path('',views.home,name='home'),
    path('all_prod_cat_id/<int:id>',views.all_prod_cat,name='all_prod_cat_id'),
    path('all_prod_cat/',views.all_prod_cat,name='all_prod_cat'),
    path('show_shop_nearabout/',views.addres_for_shop,name='shop_near_about'),
    path('contact/',views.Contact,name='contact'),
    path('shop/',views.shop,name='shop'),
    path('userdashboard/',views.user_Dashboard,name='user_dashboard'),
    path('gmailotp/',views.gmail_otp,name='gmail_otp'),
    path('resend_gamil_otp/',views.resend_gmail_otp,name="resend_gmail_otp"),
    path('changepassword/',views.ChangePassword,name="change_password"),
    path('product_view_page<int:id>/',views.product_view_page,name='product_view_page'),
    path('forget_password_resend_otp/',views.forget_password_resend_otp,name="forget_password_resend_otp"),
    path('payment_sucess_razorpay/',views.succcess_payment_razorpay,name='payment_success_razorpay'),
    path('payment_by_cod/',views.Payment_by_cod,name='payment_success_cod'),
    path('cart/',views.Cart,name='cart'),
    path('registration/',views.UserRegister,name='registration'),
    path('profile_edit/',views.profile_edit,name='profile_edit'),
    path('cart_page/',views.cart_show,name='cart_show'),
    path('cart_remove<int:id>/',views.cart_remove,name='cart_remove'),
    path('wishlist<int:id>/',views.wishlist_user,name="wishlist_user"),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('wishlist_remove<int:id>',views.wishlist_remove,name="wishlist_remove"),
    path('cart_plus<int:id>/',views.cart_plus,name='cart_plus'),
    path('cart_minus<int:id>/',views.cart_minus,name='cart_minus'),
    path('product_page/',views.product_page,name="product_page"),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('forget_password_otp/',views.forget_password_verify_otp,name='forget_password_otp'),
    path('payment_address/',views.payment_address,name="payment_address"),
    path('your_order/',views.your_order_detail,name='your_order'),
    path('order_cancel/',views.order_cancel,name='order_cancel'),
    path('self_picking_way/',views.self_picking_mode,name="self_picking_way"),
    path('new_complain/',views.new_user_complain,name='new_complain'),
    path('complains/',views.chat_complian,name='complains'),

    #
    # ###################### Vendor all Urls #########################
    #
    path('vendor_edit_profile/',views.vendor_edit_profile,name='vendor_edit_profile'),

    # path('product_delete<int:id>/',views.ProductDelete,name='product_delete'),
    path('add_product/',views.Vendor_add_product,name='add_product'),
    path('product_varient/',views.Product_varient,name='product_varient'),
    # path('edit_product<int:id>/',views.EditProduct,name='edit_product'),
    path('vendor_profile/',views.vendor_profile,name='vendor_profile'),
    path('vendor_changepassword/',views.Vendor_changepassword,name='vendor_changepassword'),
    path('vendorregistration/',views.VendorRegister,name='vendorregistration'),
    path('vendorregistrationstoredetail/',views.Vendor_register_store_detail,name="vendor_registration_store_detail"),
    path('vendorregistrationstoredocumentdetail/',views.Vendor_register_store_document_detail,name="vendor_registration_document_deatil"),
    path('vendor_gmail_otp_verify/',views.vendor_otp,name='vendor_gmail_otp'),
    path('vender_resend_otp/',views.vendor_resend_gmail_otp,name='vender_resend_gmail_otp'),
    path('store_view/',views.store_view,name='store_view'),
    path('store_update/',views.store_update,name='store_update'),
    path('pending_order/',views.self_picking_pending_order,name='pending_order'),
    path('cancle_order/',views.self_picking_cancle_order,name='cancel_order'),
    path('deliver_order/',views.self_picking_deliver_order,name='deliver_order'),

    path('delivery_pending/',views.deliver_pending_order,name='delivery_pending_order'),
    path('deliver_cancle/',views.deliver_cancle_order,name='deliver_cancle'),
    path('deliver_confirm/',views.deliver_confirm_order,name='deliver_confirm'),
    path('all_product/',views.all_product_vendor_dashboard,name='all_product_dashboard'),
    path('all_variant/',views.all_variant,name='all_variant'),
    path('remove_variant/',views.remove_variant,name='remove_variant'),
    path('remove_product/',views.remove_product,name='remove_product'),
    path('edit_product/',views.product_edit,name='product_edit'),
    path('variant_edit/',views.variant_edit,name='variant_edit'),
    path('vendor_time_create/',views.vendor_time_create,name='time_slot_create'),
    path('remove_slot/',views.remove_slot,name='remove_slot'),

    # path('product/',views.product,name='product'),
    #
    # ##################### For All User Vendor Admin ####################
    #
    path('login/',views.Login_user,name='login'),
    path('accounts/',include('allauth.urls')),
    path('logout/',views.user_logout,name="logout"),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
