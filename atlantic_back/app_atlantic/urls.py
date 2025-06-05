from django.urls import path
from . import views

urlpatterns = [
    path("attendance", views.Attendance_View.as_view(), name="attendance"),
    path("funcionarios", views.Attendance_View.as_view(), name="funcionario-list"),
    path("atendimentos", views.Atendimento_View.as_view(), name="criar-atendimento"),
    path("atendimentos/<int:funcionario_id>",views.Atendimento_View.as_view(),name="func-atendimentos",),
    path('checkin', views.CheckInView.as_view(), name='checkin'),
    path('checkout', views.CheckOutView.as_view(), name='checkout'),
    path('status/<int:funcionario_id>/', views.AtendimentoStatusView.as_view(), name='status'),
]
