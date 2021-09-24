from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from product.views import CategoryListView, PostsViewSet, PostImageView

router = DefaultRouter()
router.register('posts', PostsViewSet)


schema_view = get_schema_view(
   openapi.Info(
      title="Test API",
      default_version='v1',
      description="Test description",
    ),
   public=True,
)

urlpatterns = [
    path('', schema_view.with_ui()),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/review/', include('review.urls')),
    path('api/categories/', CategoryListView.as_view()),
    path('api/account/', include('account.urls')),
    path('api/product/', include('product.urls')),
    path('api/image/', PostImageView.as_view()),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
