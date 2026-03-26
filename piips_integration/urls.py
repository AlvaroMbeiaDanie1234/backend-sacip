from django.urls import path
from . import views

urlpatterns = [
    path('delituosos_procurados/public/todas', views.get_delituosos_procurados, name='delituosos_procurados'),
    path('dinfop_delitouso/public/todas', views.get_dinfop_delituoso, name='dinfop_delitouso'),
    path('detido/public/todas', views.get_detido, name='get_detido'),
    path('ocorrencias/public/todas', views.get_ocorrencias, name='get_ocorrencias'),
    path('minio/file/', views.get_minio_file, name='minio_file'),
]
