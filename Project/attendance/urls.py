from django.urls import path
from . import views
from .views import CheckInListView, CheckOutListView, AtendimentosPorDataView,EmployeeAttendanceListView,MonthlyAttendanceView,AtividadeCreateView,FuncionariosAtividadesHojeView

urlpatterns = [
    path("employee", views.Employee_view.as_view(), name="attendance"),
    path("employee", views.Employee_view.as_view(), name="funcionario-list"),
    path("attendance/Check-in", views.CheckInView.as_view(), name="funcionario-list"),
    path("attendance/Check-out", views.CheckOutView.as_view(), name="funcionario-list"),
    path('attendance/checkins/', CheckInListView.as_view(), name='listar-checkins'),
    path('attendance/checkouts/', CheckOutListView.as_view(), name='listar-checkouts'),
    path('attendance/bay-day/', AtendimentosPorDataView.as_view(), name='atendimentos-por-data'),
    path('employee-attendance', EmployeeAttendanceListView.as_view(), name='employee-attendance'),
    path('attendance/employees/<int:employee_id>', MonthlyAttendanceView.as_view(), name='monthly-attendance'),
    path('atividades', AtividadeCreateView.as_view(), name='criar-atividade'),
    path('activities', FuncionariosAtividadesHojeView.as_view(), name='funcionarios-atividades-hoje'),
]
