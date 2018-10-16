from django.conf.urls import url
from symptom_checker import views
from django.contrib import admin
from django.urls import path
app_name='symptom_checker'
urlpatterns=[
    path('',views.SymptomsListview.as_view(),name='list'),
    path('search_result/',views.SymptomDetailView.as_view(),name='search_result'),
    path('<int:pk>/',views.SymptomDetailView.as_view(),name='detail'),
]
