from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<user_id>\d+)$', views.index, name='index'),
    url(r'^edit_profile/(?P<user_id>\d+)$', views.edit_profile, name='edit_profile'),
    url(r'^edit_profile/edit_times$', views.view_times, name="view_times"),
    url(r'^edit_profile/update_times$', views.update_times, name='update_times'),
    url(r'^edit_profile/update_image$', views.image, name='update_image')
]
