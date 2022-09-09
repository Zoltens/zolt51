from django.urls import path

from .views import index, NameView, save_data

urlpatterns = [
    path('', index, name='index'),
    path('save/', save_data, name='save'),
    path('api/', NameView.as_view()),
]
