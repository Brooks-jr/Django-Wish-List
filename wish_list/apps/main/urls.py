from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.home_page),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<id>\d+)$', views.remove,  name="remove_item"),    
    url(r'^add_item$', views.add),
    url(r'^item_form$', views.new_item),
    url(r'^view_item/(?P<item_id>\d+)$', views.view_item, name='view_item'),
    url(r'^join/(?P<item_id>\d+)$', views.join),
    url(r'^unjoin/(?P<item_id>\d+)$', views.unjoin),
    
]
