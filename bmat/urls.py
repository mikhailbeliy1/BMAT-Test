from django.urls import path
from django.shortcuts import redirect


from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('musical_work/', views.MusicalWorkListView.as_view(), name='musical_work'),
    path('upload_works_csv/', views.upload_works_csv.as_view(), name='upload_works_csv'),
    path('search_iswc/', views.search_iswc.as_view(), name='search_iswc'),
    path('', lambda request: redirect('upload_works_csv/', permanent=False)),
]