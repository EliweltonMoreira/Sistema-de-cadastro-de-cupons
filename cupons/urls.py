from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='cupom.index'),
    path('detalhe/<str:codigo>', views.detalhe, name='cupom.detalhe'),
    path('adicionar/', views.adicionar, name='cupom.adicionar'),
    path('editar/<str:codigo>', views.editar, name='cupom.editar'),
    path('usar/<str:codigo>', views.usar, name='cupom.usar'),
    path('expirar/<str:codigo>', views.expirar, name='cupom.expirar'),
    path('deletar/<str:codigo>', views.deletar, name='cupom.deletar'),
]
