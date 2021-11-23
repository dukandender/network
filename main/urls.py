from django.urls import include,path
from django.conf.urls import url
from . import views

app_name='main'

urlpatterns = [
    path('',views.index,name='index'),
    path('logout/',views.logout_view,name='logout'),
    path('login/', views.login_view, name='login'),
    path('signup/',views.signup,name='signup'),
    path('newpost/',views.newpost_view,name='newpost'),
    path('postcomment/',views.newcomment_view,name='postcomment'),
    path('deletecomment/',views.deletecomment_view,name='deletecomment'),
    path('deletepost/',views.deletepost_view,name='deletepost'),
    path('follow/',views.follow_view,name='follow'),
    path('<str:name>/',views.userpage,name='userpage')
]