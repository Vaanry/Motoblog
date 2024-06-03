"""urls."""
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .views import PostViewSet, MotoViewSet

router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('moto', MotoViewSet)

app_name = 'api'

urlpatterns = [

    path('v1/', include(router.urls)),
    path('users/', views.UsersList.as_view(), name='get_users'),
    path('api-token-auth/', obtain_auth_token),
    path('v1/posts/<int:post_id>/comments/', views.CommentsList.as_view(),
         name='get_comments'),
    path('v1/posts/<int:post_id>/comments/<int:pk>/',
         views.CommentsDetail.as_view(), name='get_comment'),

]
