from django.shortcuts import render
from .models import Funcionario, Atendimento, Atividade
from .serializers import (
    Employee_serializers,
    CheckInSerializer,
    CheckOutSerializer,
    AtendimentoSerializer,
    EmployeeAttendanceSerializer,
    MonthlyAttendanceSerializer,
    AtividadeSerializer,
    FuncionarioAtividadesHojeSerializer
)
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
from rest_framework.generics import ListAPIView
from rest_framework import generics
from datetime import date,timedelta


class Employee_view(APIView):

    def get(self, request):
        funcionarios = Funcionario.objects.all()
        serializers = Employee_serializers(funcionarios, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = Employee_serializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckInView(APIView):
    def post(self, request):
        serializer = CheckInSerializer(data=request.data)

        if serializer.is_valid():
            atendimento = serializer.save()

            response_serializer = AtendimentoSerializer(atendimento)

            response_data = {
                "status": "Check-in registrado com sucesso",
                "data": response_serializer.data,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckOutView(APIView):
    def post(self, request):
        serializer = CheckOutSerializer(data=request.data)
        if serializer.is_valid():
            atendimento = serializer.validated_data["atendimento"]
            atendimento.checkout = serializer.validated_data["checkout"]
            atendimento.save()

            funcionario = atendimento.funcionario

            return Response(
                {
                    "status": "Check-out registrado",
                    "atendimento_id": atendimento.id,
                    "funcionario_id": funcionario.id,
                    "funcionario_nome": funcionario.nome,
                    "checkin": (
                        atendimento.checkin.strftime("%d-%m-%Y %H:%M")
                        if atendimento.checkin
                        else None
                    ),
                    "checkout": atendimento.checkout.strftime("%d-%m-%Y %H:%M"),
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckInListView(ListAPIView):
    serializer_class = AtendimentoSerializer

    def get_queryset(self):
        return Atendimento.objects.filter(checkin__isnull=False)


class CheckOutListView(ListAPIView):
    serializer_class = AtendimentoSerializer

    def get_queryset(self):
        return Atendimento.objects.filter(checkout__isnull=False)


class AtendimentosPorDataView(APIView):
    def get(self, request):
        data_str = request.query_params.get("data")
        if not data_str:
            return Response(
                {"erro": "Parâmetro 'data' é obrigatório. Exemplo: ?data=05-06-2025"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            data_formatada = datetime.strptime(data_str, "%d-%m-%Y").date()
        except ValueError:
            return Response(
                {"erro": "Formato de data inválido. Use DD-MM-YYYY."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        atendimentos = Atendimento.objects.filter(data=data_formatada)
        serializer = AtendimentoSerializer(atendimentos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeAttendanceListView(generics.ListAPIView):
    serializer_class = EmployeeAttendanceSerializer
    queryset = Funcionario.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = {"date": date.today().strftime("%d-%m-%Y"), "employees": serializer.data}

        return Response(data)

class MonthlyAttendanceView(generics.RetrieveAPIView):
    serializer_class = MonthlyAttendanceSerializer

    def get_object(self):
        employee_id = self.kwargs.get('employee_id')
        return get_object_or_404(Funcionario, id=employee_id)
    

class AtividadeCreateView(generics.CreateAPIView):
    queryset = Atividade.objects.all()
    serializer_class = AtividadeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class FuncionariosAtividadesHojeView(ListAPIView):
    serializer_class = FuncionarioAtividadesHojeSerializer

    def get_queryset(self):
        hoje = date.today()

        funcionarios_com_atendimento = Atendimento.objects.filter(data=hoje) \
            .values_list('funcionario_id', flat=True)

        funcionarios_com_atividade = Atividade.objects.filter(data=hoje) \
            .values_list('funcionario_id', flat=True)

        funcionarios_ids = set(funcionarios_com_atendimento) | set(funcionarios_com_atividade)

        return Funcionario.objects.filter(id__in=funcionarios_ids)
