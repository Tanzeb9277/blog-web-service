from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'blogapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='view'),
    path(route='', view=views.PostListView.as_view(), name='index'),
    path('login/', views.login_request, name='login'),
    path('registration/', views.registration_request, name='registration'),
    path('logout/', views.logout_request, name='logout'),
    path('create-post/', views.create_post, name='create_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('post-list', view=views.AppPostList),
    path('post-page/<int:pk>/', view=views.PostDetail),
    path('new-comment/<int:post_id>/', views.NewComment.as_view()),
    path('comments/<int:post_id>/',  views.GetComments)


 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)