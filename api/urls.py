from rest_framework.routers import DefaultRouter

from api.views import FileViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('files', FileViewSet)

urlpatterns = router.urls
