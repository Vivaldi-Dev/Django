from rest_framework import serializers
from .models import Funcionario, Atendimento, Atividade
from datetime import date


class FuncSerializers(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = "__all__"

    def create(self, validated_data):
        return Funcionario.objects.create(**validated_data)


class AtendSerializers(serializers.ModelSerializer):
    data = serializers.DateField(default=date.today)  

    class Meta:
        model = Atendimento
        fields = "__all__"

    def create(self, validated_data):
        return Atendimento.objects.create(**validated_data)

    
class CheckInSerializer(serializers.ModelSerializer):

    class Meta:
        model = Atendimento
        fields = ['funcionario', 'checkin']  
          
class CheckOutSerializer(serializers.ModelSerializer):
    checkout = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Atendimento
        fields = ['funcionario' , 'checkout']  
     

class AtiviSerializers(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = "__all__"

    def create(self, validated_data):
        return Atividade.objects.create(**validated_data)
