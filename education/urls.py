from django.urls import path, include
from rest_framework import routers
from courses.apps import CoursesConfig
from .views import CourseViewSet
from . import views

app_name = CoursesConfig.name

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', views.LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lesson/', views.LessonListAPIView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', views.LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lesson/update/<int:pk>/', views.LessonUpdateAPIView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', views.LessonDestroyPIView.as_view(), name='lesson-delete'),

]
urlpatterns += router.urls