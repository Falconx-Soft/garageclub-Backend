from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register(r'validations', views.ValidationViewSet)
router.register(r'costs', views.CostViewSet)

router.register(r'profitability', views.ProfitabilityViewSet)

urlpatterns = []
urlpatterns += router.urls