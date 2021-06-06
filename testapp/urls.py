
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'testapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('upfile/', views.upfile, name='upfile'),
    path('getdetail/', views.getdetail, name='getdetail'),
    path('gettable/<int:id>', views.gettableback, name='gettableback'),
    path('getdetail/<int:id>', views.getdetailback, name='getdetailback'),
    path('getgraph/', views.getgraph, name='getgraph'),
    path('getgraph/<int:id>', views.getgraphback, name='getgraphback'),
    path('presplitdata/', views.presplitdata, name='presplitdata'),
    path('splitdata/', views.splitdata, name='splitdata'),
    path('presplitdata/<int:id>', views.presplitdataback, name='presplitdataback'),
    path('modelchoose/', views.modelchoose, name='modelchoose'),
    path('splitdataback/<int:tempid>', views.splitdataback, name='splitdataback'),
]

urlpatterns += \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)