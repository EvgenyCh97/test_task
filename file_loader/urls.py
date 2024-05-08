from rest_framework.routers import DefaultRouter

from file_loader.views import FileViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('files', FileViewSet)

urlpatterns = router.urls
