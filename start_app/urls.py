from django.urls import path
from start_app import views
app_name = "start_app"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('acticles/', views.ArticleView.as_view()),
    path('articles/<int:pk>', views.ArticleView.as_view()),
    path('files/', views.FileUploadView.as_view()),
    path('files/<int:pk>', views.FileUploadView.as_view()),
]

