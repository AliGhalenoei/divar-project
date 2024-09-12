from django.urls import path 
from .import views


urlpatterns = [
    path('save/advertisement/<int:advertisement_id>/',views.SaveAdvertisementView.as_view(),name='save_advertisement'),
    path('view/advertisement/<int:advertisement_id>/',views.ViewAdvertisementView.as_view(),name='view_advertisement'),
    path('delete/note/<int:note_id>/',views.DeleteAdvertisementNoteView.as_view(),name='delete_note'),
    # create advertisement
    path('create/advertisement/',views.CreateAdvertisementView.as_view(),name='create_advertisement'),
    path('delete/advertisement/<int:advertisement_id>/',views.DeleteAdvertisementView.as_view(),name='delete_advertisement'),

    path('contact/us/',views.ContactUsView.as_view(),name='contact')
]