from rest_framework import serializers
from .models import Funcionario, Atendimento, Atividade
from datetime import date


class Employee_serializers(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = "__all__"

    def create(self, validated_data):
        return Funcionario.objects.create(**validated_data)


class CheckInSerializer(serializers.Serializer):
    codigo = serializers.CharField()
    checkin = serializers.DateTimeField(input_formats=["%d-%m-%Y %H:%M"])

    def validate(self, data):
        codigo = data.get('codigo')
        checkin_time = data.get('checkin')

        try:
            funcionario = Funcionario.objects.get(codigo=codigo)
        except Funcionario.DoesNotExist:
            raise serializers.ValidationError("Código de funcionário inválido.")

        data_checkin = checkin_time.date()
        if Atendimento.objects.filter(funcionario=funcionario, data=data_checkin).exists():
            raise serializers.ValidationError("Este funcionário já fez check-in hoje.")

        data['funcionario'] = funcionario
        return data

    def create(self, validated_data):
        return Atendimento.objects.create(
            funcionario=validated_data['funcionario'],
            data=validated_data['checkin'].date(),
            checkin=validated_data['checkin']
        )


class CheckOutSerializer(serializers.Serializer):
    codigo = serializers.CharField()
    checkout = serializers.DateTimeField(format="%d-%m-%Y %H:%M", input_formats=["%d-%m-%Y %H:%M"])

    def validate(self, data):
        codigo = data.get('codigo')
        checkout_time = data.get('checkout')

        try:
            funcionario = Funcionario.objects.get(codigo=codigo)
        except Funcionario.DoesNotExist:
            raise serializers.ValidationError("Código de funcionário inválido.")

        data_checkout = checkout_time.date()

        try:
            atendimento = Atendimento.objects.get(funcionario=funcionario, data=data_checkout)
        except Atendimento.DoesNotExist:
            raise serializers.ValidationError("Nenhum check-in encontrado para esse funcionário hoje.")

        if atendimento.checkout:
            raise serializers.ValidationError("Este funcionário já fez check-out hoje.")

        data['atendimento'] = atendimento
        return data

    def update(self, instance, validated_data):
        instance.checkout = validated_data['checkout']
        instance.save()
        return instance


class AtendimentoSerializer(serializers.ModelSerializer):
    funcionario_nome = serializers.CharField(source='funcionario.nome', read_only=True)
    funcionario_id = serializers.IntegerField(source='funcionario.id', read_only=True)
    checkin = serializers.DateTimeField(format="%d-%m-%Y %H:%M", required=False)
    checkout = serializers.DateTimeField(format="%d-%m-%Y %H:%M", required=False)

    class Meta:
        model = Atendimento
        fields = ['id', 'funcionario_id', 'funcionario_nome', 'data', 'checkin', 'checkout']
