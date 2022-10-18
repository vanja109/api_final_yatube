from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'groups', GroupViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
