from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('go/', views.redirect_to_task, name='redirect_to_task'),
    path('task/all', views.all_tasks),
    path('task/<int:id>', views.get_task),
    path('task/add', views.add_task),
    path('task/update', views.update_task),
    path('task/delete/<int:id>', views.delete_task),
]