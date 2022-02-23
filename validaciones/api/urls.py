from rest_framework import routers
from . import views


router = routers.DefaultRouter()

router.register(r'validations', views.ValidationViewSet)
router.register(r'costs', views.CostViewSet)

urlpatterns = []
urlpatterns += router.urls