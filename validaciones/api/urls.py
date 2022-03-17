from rest_framework import routers
from . import views
from django.urls import path

router = routers.DefaultRouter()

router.register(r'validations', views.ValidationViewSet)
router.register(r'costs', views.CostViewSet)

router.register(r'profitability', views.ProfitabilityViewSet)

urlpatterns = [
	path('update/', views.updateValidation.as_view()),
]
urlpatterns += router.urls
