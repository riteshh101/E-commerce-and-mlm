from django.urls import path
from app import api_views
urlpatterns = [
    path('user_list/',api_views.UserRegister.as_view({'get':'list'})),
    path('user_register/',api_views.UserRegister.as_view({'post':'create'})),
    path('user_register_delete/<int:id>/',api_views.UserRegister.as_view({'delete':'destroy'})),
    path('user_resend_mail_otp/',api_views.UserResendMailOtp.as_view({'post':'create'})),
    path('user_otp_verify/',api_views.UserOtpVerify.as_view({'post':'create'})),
    path('user_change_pwd/',api_views.UserChangePwd.as_view({'post':'create'})),
    path('user_update/<int:id>/',api_views.UserRegister.as_view({'put':'update'})),


    path('contact_create/',api_views.Contactall.as_view({'post':'create'})),
    path('contact_list/',api_views.Contactall.as_view({'get':'list'})),
    path('contact_delete/<int:id>/',api_views.Contactall.as_view({'delete':'destory'})),

    path('vendor_register/',api_views.VendorRegister.as_view({'post':'create'})),
    path('vendor_list/',api_views.VendorRegister.as_view({'get':'list'})),
    path('vendor_resend_mail_Otp/',api_views.VendorResendMailOtp.as_view({'post':'create'})),
    path('vendor_otp_verify/',api_views.VendorOtpVerify.as_view({'post':'create'})),
    path('vendor_change_pwd/',api_views.VendorChangePwd.as_view({'post':'create'})),
    path('vendor_update/<int:id>/',api_views.VendorRegister.as_view({'put':'update'})),
    path('vendor_register_store_details/',api_views.VendorRegisterStoreDetails.as_view({'post':'create'})),
    path('vendor_register_store_details_list/',api_views.VendorRegisterStoreDetails.as_view({'get':'list'})),
    path('vendor_store_update/<int:id>/',api_views.VendorRegisterStoreDetails.as_view({'put':'update'})),
    path('vendor_register_store_dcument_detail/',api_views.VendorRegisterStoredcumentDetail.as_view({'post':'create'})),
    path('vendor_register_store_dcument_detail_list/',api_views.VendorRegisterStoredcumentDetail.as_view({'get':'list'})),

    path('category_list/',api_views.CategoryALL.as_view({'get':'list'})),
    path('category_create/',api_views.CategoryALL.as_view({'post':'create'})),
    path('category_update/<int:id>/',api_views.CategoryALL.as_view({'put':'update'})),
    path('category_delete/<int:id>/',api_views.CategoryALL.as_view({'delete':'destory'})),

    path('subcategory_list/',api_views.SubcategoryALL.as_view({'get':'list'})),
    path('subcategory_list_by-category/',api_views.SubcategoryALL.as_view({'post':'create'})),

    path('brands_list/',api_views.SubSubcategoryAll.as_view({'get':'list'})),
    path('brands_list_by_subcategory/',api_views.SubSubcategoryAll.as_view({'post':'create'})),


    path('login/',api_views.Login_check.as_view({'post':'create'})),
    path('logout/',api_views.Logout_check.as_view({'get':'list'})),

    path('banner_list/',api_views.BannerALL.as_view({'get':'list'})),
    path('forget_password/',api_views.Forget_password.as_view({'post':'create'})),
    path('forget_password_verify_otp/',api_views.Forget_Password_Verify_Otp.as_view({'post':'create'})),
    path('forget_password_resend_otp/',api_views.Forget_Password_Resend_Otp.as_view({'post':'create'})),
    path('product_list/',api_views.ProductALL.as_view({'get':'list'})),
    path('product_list_by_stor/',api_views.ProductALL.as_view({'post':'create'})),
    path('image_list/',api_views.ImageAll.as_view({'get':'list'})),
    path('color_size_brand_list/',api_views.ColorSizeBrandAll.as_view({'get':'list'})),
    path('Variants_brand_color_size_list/',api_views.VariantsAll.as_view({'post':'create'})),
    path('addres_search_for_shop/',api_views.Addres_Search_For_Shop.as_view({'post':'create'})),
    path('addres_search_for_shop_after_login/',api_views.Addres_Search_For_Shop_after_Login.as_view({'post':'create'})),
    path('bottom_banner_list/',api_views.Bottom_BannerAll.as_view({'get':'list'})),
    path('variant_subcategry_stor_list/',api_views.VariantbySubcategryStor.as_view({'post':'create'})),
    path('variantby_subcategry_list/',api_views.VariantbySubcategry.as_view({'post':'create'})),
]
