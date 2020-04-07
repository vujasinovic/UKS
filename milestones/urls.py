from django.urls import path

from . import views

urlpatterns = [
    path('', views.MilestoneList.as_view(), name='milestone_list'),
    path('view/<int:pk>', views.MilestoneView.as_view(), name='milestone_view'),
    path('new', views.MilestoneCreate.as_view(), name='milestone_new'),
    path('view/<int:pk>', views.MilestoneView.as_view(), name='milestone_view'),
    path('edit/<int:pk>', views.MilestoneUpdate.as_view(), name='milestone_edit'),
    path('delete/<int:pk>', views.MilestoneDelete.as_view(), name='milestone_delete'),
]
