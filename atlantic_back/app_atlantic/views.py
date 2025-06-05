from django.shortcuts import render

from .models import Funcionario, Atendimento, Atividade
from .serializers import (
    FuncSerializers,
    AtendSerializers,
    AtiviSerializers,
    CheckInSerializer,
    CheckOutSerializer,
)

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime


class Attendance_View(APIView):

    def get(self, request):
        funcionarios = Funcionario.objects.all()
        serializers = FuncSerializers(funcionarios, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = FuncSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class Atendimento_View(APIView):

    def post(self, request):
        funcionario_id = request.data.get("funcionario")

        if not funcionario_id:
            return Response(
                {"error": "O campo 'funcionario' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not Funcionario.objects.filter(id=funcionario_id).exists():
            return Response(
                {"error": f"Funcionário com ID {funcionario_id} não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializers = AtendSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, funcionario_id):
        try:
            funcionario = Funcionario.objects.get(id=funcionario_id)
        except Funcionario.DoesNotExist:
            return Response(
                {"detail": "Funcionário não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        atendimentos = Atendimento.objects.filter(funcionario=funcionario)
        serializer = AtendSerializers(atendimentos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CheckInView(APIView):
    def post(self, request):
        serializer = CheckInSerializer(data=request.data)
        if serializer.is_valid():
            atendimento = Atendimento.objects.create(
                funcionario=serializer.validated_data["funcionario"],
                checkin=serializer.validated_data["checkin"],
                data=datetime.now().date(),
                checkout=None,
            )
            return Response(
                {"status": "Check-in registrado", "id": atendimento.id},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckOutView(APIView):
    def post(self, request):
        serializer = CheckOutSerializer(data=request.data)
        if serializer.is_valid():
            funcionario = serializer.validated_data["funcionario"]
            checkout_time = serializer.validated_data["checkout"]

            try:
                atendimento = Atendimento.objects.get(
                    funcionario=funcionario,
                    data=datetime.now().date(),
                    checkout__isnull=True  
                )
                
                atendimento.checkout = checkout_time
                atendimento.save()
                
                
                return Response(
                    CheckInSerializer(atendimento).data,
                    status=status.HTTP_201_CREATED
                )
                
            except Atendimento.DoesNotExist:
                return Response(
                    {"error": "Check-in não encontrado para hoje ou check-out já registrado."},
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AtendimentoStatusView(APIView):
    def get(self, request, funcionario_id):
        atendimento = Atendimento.objects.filter(funcionario_id=funcionario_id).last()

        if atendimento:
            serializer = AtendimentoStatusSerializer(atendimento)
            return Response(serializer.data)
        return Response(
            {"status": "Nenhum registro encontrado"}, status=status.HTTP_404_NOT_FOUND
        )
