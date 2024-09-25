from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import DefaultRouter

from api import views

urlpatterns = [
    path('wallets/<uuid:wallet_uuid>/operation/', views.OperationViewSet.as_view({'post': 'operation'}),
         name='operation'),
]

router = DefaultRouter()
router.register("wallets", views.WalletViewSet)

urlpatterns += router.urls

urlpatterns += [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
