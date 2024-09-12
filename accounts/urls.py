from django.urls import path 
from .import views



urlpatterns = [
    path('authentications/',views.UserAuthenticationView.as_view(),name='authentications'),
    path('veryfy/',views.UserVeryfyAccountView.as_view(),name='veryfy'),
    path('logout/',views.UserLogoutView.as_view(),name='logout'),
]