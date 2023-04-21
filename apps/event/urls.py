from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('create/', views.EventCreateView.as_view(), name='event_create'),
    path('update/<int:pk>/', views.EventUpdateView.as_view(), name='event_update'),
    path('delete/<int:pk>/', views.EventDeleteView.as_view(), name='event_delete'),
]
