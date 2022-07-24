from django.urls import path
from . import views
app_name = 'racing'
urlpatterns = [
    path('', views.main, name = 'main'),
    path('<int:race_id>/', views.detail, name = 'detail'),
    path('date=<str:race_date>/', views.index, name = 'index'),
]