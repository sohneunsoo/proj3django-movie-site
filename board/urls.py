from django.urls import path
from . import views

app_name= "board"

urlpatterns=[
    path('',views.index, name='index'),
    path('<int:moviecode>', views.detail, name='detail'),
    path('comment/', views.comment, name='comment'),
    path('open', views.open, name='open'),
    path('heart/<int:moviecode>', views.heart, name='heart'),
    path('words/<int:moviecode>', views.wcm, name='wordsm'),
    path('wordsall', views.wc, name='words'),
    path('commentlike', views.commentlike, name='commentlike'),
]