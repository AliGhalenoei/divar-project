from django.urls import path
from .import views

urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('filter/by/category/<slug:slug_category>/',views.HomeView.as_view(),name='filter_by_category'),
    path('filter/by/city/<slug:slug_city>/',views.HomeView.as_view(),name='filter_by_city'),

    path('detail/advertisement/<slug:slug_advertisement>/',views.DetailAdvertisementsView.as_view(),name='detail_advertisement'),
    path('advertisement/saves/',views.AdvertisementsSaveView.as_view(),name='advertisement_saves'),
    path('advertisement/notes/',views.AdvertisementsNoteView.as_view(),name='advertisement_notes'),
    path('recent/visit/',views.RecentVisitsView.as_view(),name='recent_visits'),

    path('user/profile/<int:user_id>/',views.UserProfileView.as_view(),name='user_profile'),
    path('update/profile/<int:user_id>/',views.UpdateProfileView.as_view(),name='update_profile'),

    path('404/',views.Page404View.as_view(),name='404'),
]
