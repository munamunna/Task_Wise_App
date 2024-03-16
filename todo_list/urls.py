from django.urls import path
from rest_framework.routers import DefaultRouter
from todo_list.views import TodoItemViewSet
from rest_framework.authtoken.views import ObtainAuthToken

router=DefaultRouter()


urlpatterns =[
   path('todos/', TodoItemViewSet.as_view({'get': 'list', 'post': 'create'})),
   path('todos/<int:pk>/', TodoItemViewSet.as_view({'delete': 'destroy', 'put': 'update','get':'list'})),
   path('todos/overdue/', TodoItemViewSet.as_view({'get': 'get_overdue_items'})),
    path('todos/<int:pk>/update_due_date/', TodoItemViewSet.as_view({'put': 'update_due_date'}), name='update_due_date'),
    path('todos/overdue/<int:pk>/', TodoItemViewSet.as_view({'get': 'get_overdue_item'}), name='overdue-todo-detail'),
    
]+router.urls