from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from app_modules.adminapp import views

app_name = "adminapp"

urlpatterns = [
    path('adminindex/',views.AdminIndexView.as_view(),name="adminindex"),
    path('adminprofile/',views.AdminProfileView.as_view(),name="adminprofile"),
    
    # ------------ BASIC_DETAILS_URLS ------------------------
    path('basicdetails_add/',views.BasicDetailsCreateView.as_view(),name="basicdetails_add"),
    path('basicdetails_list/',views.BasicDetailsListView.as_view(),name="basicdetails_list"),
    path('basicdetails_update/<int:pk>/',views.BasicDetailsUpdateView.as_view(),name="basicdetails_update"),
    path('basicdetails_delete/<int:pk>/',views.BasicDetailsDeleteView.as_view(),name="basicdetails_delete"),
    
    # ------------ FAQ-URLS ------------------------
    path('faq_add/',views.FAQCreateView.as_view(),name="faq_add"),
    path('faq_list/',views.FAQListView.as_view(),name="faq_list"),
    path('faq_update/<int:pk>/',views.FAQUpdateView.as_view(),name="faq_update"),
    path('faq_delete/<int:pk>/',views.FAQDeleteView.as_view(),name="faq_delete"),
    path('faq_ajax',views.FAQDatatableView.as_view(),name="faq_ajax"),
    
    # ------------ CATEGORY-URLS ------------------------
    path('category_add/',views.CategoryCreateView.as_view(),name="category_add"),
    path('category_list/',views.CategoryListView.as_view(),name="category_list"),
    path('category_update/<int:pk>/',views.CategoryUpdateView.as_view(),name="category_update"),
    path('category_delete/<int:pk>/',views.CategoryDeleteView.as_view(),name="category_delete"),
    path('category_ajax',views.CategoryDatatableView.as_view(),name="category_ajax"),
    
    # ------------ BLOG-URLS ------------------------
    path('blog_add/',views.BlogCreateView.as_view(),name="blog_add"),
    path('blog_list/',views.BlogListView.as_view(),name="blog_list"),
    path('blog_update/<int:pk>/',views.BlogUpdateView.as_view(),name="blog_update"),
    path('blog_delete/<int:pk>/',views.BlogDeleteView.as_view(),name="blog_delete"),
    path('blog_ajax',views.BlogDatatableView.as_view(),name="blog_ajax"),
    
    # ------------ TESTIMONIAL-URLS ------------------------
    path('testimonial_add/',views.TestimonialCreateView.as_view(),name="testimonial_add"),
    path('testimonial_list/',views.TestimonialListView.as_view(),name="testimonial_list"),
    path('testimonial_update/<int:pk>/',views.TestimonialUpdateView.as_view(),name="testimonial_update"),
    path('testimonial_delete/<int:pk>/',views.TestimonialDeleteView.as_view(),name="testimonial_delete"),
    path('testimonial_ajax',views.TestimonialDatatableView.as_view(),name="testimonial_ajax"),
    
    # ------------ SERVICES-URLS ------------------------
    path('services_add/',views.ServicesCreateView.as_view(),name="services_add"),
    path('services_list/',views.ServicesListView.as_view(),name="services_list"),
    path('services_update/<int:pk>/',views.ServicesUpdateView.as_view(),name="services_update"),
    path('services_delete/<int:pk>/',views.ServicesDeleteView.as_view(),name="services_delete"),
    path('services_ajax',views.ServicesDatatableView.as_view(),name="services_ajax"),
    
    # ------------ ABOUT_PARAMETER-URLS ------------------------
    path('aboutparameter_add/',views.AboutParameterCreateView.as_view(),name="aboutparameter_add"),
    path('aboutparameter_list/',views.AboutParameterListView.as_view(),name="aboutparameter_list"),
    path('aboutparameter_update/<int:pk>/',views.AboutParameterUpdateView.as_view(),name="aboutparameter_update"),
    path('aboutparameter_delete/<int:pk>/',views.AboutParameterDeleteView.as_view(),name="aboutparameter_delete"),
    path('aboutparameter_ajax',views.AboutParameterDatatableView.as_view(),name="aboutparameter_ajax"),
    
]