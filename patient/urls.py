from django.urls import path
from django.urls.resolvers import URLPattern
from .import views

urlpatterns = [
    path('', views.PersonListView.as_view(), name='patient_changelist'),
    # path('add/', views.PersonCreateView.as_view(), name='patient_add'),
    
    path('<int:pk>/', views.PersonUpdateView.as_view(), name='patient_change'),
    path('add/', views.createAppointment, name="patient_add"),
    path('ajax/load-specialists/', views.load_specialists, name='ajax_load_cities'),
    path('success/', views.success, name='success')
    
]
