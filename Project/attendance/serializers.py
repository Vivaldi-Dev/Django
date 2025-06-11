from rest_framework import serializers
from .models import Funcionario, Atendimento, Atividade
from datetime import date, timedelta


class Employee_serializers(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = "__all__"

    def create(self, validated_data):
        return Funcionario.objects.create(**validated_data)


class CheckInSerializer(serializers.Serializer):
    codigo = serializers.CharField(write_only=True)
    checkin = serializers.DateTimeField(input_formats=["%d-%m-%Y %H:%M"])
    funcionario_nome = serializers.CharField(source="funcionario.nome", read_only=True)
    funcionario_codigo = serializers.CharField(
        source="funcionario.codigo", read_only=True
    )

    def validate(self, data):
        codigo = data.get("codigo")
        checkin_time = data.get("checkin")

        try:
            funcionario = Funcionario.objects.get(codigo=codigo)
        except Funcionario.DoesNotExist:
            raise serializers.ValidationError("Código de funcionário inválido.")

        data_checkin = checkin_time.date()
        if Atendimento.objects.filter(
            funcionario=funcionario, data=data_checkin
        ).exists():
            raise serializers.ValidationError("Este funcionário já fez check-in hoje.")

        data["funcionario"] = funcionario
        return data

    def create(self, validated_data):
        return Atendimento.objects.create(
            funcionario=validated_data["funcionario"],
            data=validated_data["checkin"].date(),
            checkin=validated_data["checkin"],
        )


class CheckOutSerializer(serializers.Serializer):
    codigo = serializers.CharField()
    checkout = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M", input_formats=["%d-%m-%Y %H:%M"]
    )

    def validate(self, data):
        codigo = data.get("codigo")
        checkout_time = data.get("checkout")

        try:
            funcionario = Funcionario.objects.get(codigo=codigo)
        except Funcionario.DoesNotExist:
            raise serializers.ValidationError("Código de funcionário inválido.")

        data_checkout = checkout_time.date()

        try:
            atendimento = Atendimento.objects.get(
                funcionario=funcionario, data=data_checkout
            )
        except Atendimento.DoesNotExist:
            raise serializers.ValidationError(
                "Nenhum check-in encontrado para esse funcionário hoje."
            )

        if atendimento.checkout:
            raise serializers.ValidationError("Este funcionário já fez check-out hoje.")

        data["atendimento"] = atendimento
        return data

    def update(self, instance, validated_data):
        instance.checkout = validated_data["checkout"]
        instance.save()
        return instance


class AtendimentoSerializer(serializers.ModelSerializer):
    funcionario_nome = serializers.CharField(source="funcionario.nome", read_only=True)
    funcionario_id = serializers.IntegerField(source="funcionario.id", read_only=True)
    checkin = serializers.DateTimeField(format="%d-%m-%Y %H:%M", required=False)
    checkout = serializers.DateTimeField(format="%d-%m-%Y %H:%M", required=False)

    class Meta:
        model = Atendimento
        fields = [
            "id",
            "funcionario_id",
            "funcionario_nome",
            "data",
            "checkin",
            "checkout",
        ]


class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    checkin_time = serializers.SerializerMethodField()
    checkout_time = serializers.SerializerMethodField()

    class Meta:
        model = Funcionario
        fields = [
            "id",
            "nome",
            "codigo",
            "status",
            "checkin_time",
            "checkout_time",
            "cargo",
        ]

    def get_status(self, obj):
        hoje = date.today()
        try:
            atendimento = Atendimento.objects.get(funcionario=obj, data=hoje)
            if atendimento.checkout:
                return "Checked Out"
            return "Checked In"
        except Atendimento.DoesNotExist:
            return "Not Checked In"

    def get_checkin_time(self, obj):
        hoje = date.today()
        try:
            atendimento = Atendimento.objects.get(funcionario=obj, data=hoje)
            return (
                atendimento.checkin.strftime("%d-%m-%Y %H:%M")
                if atendimento.checkin
                else None
            )
        except Atendimento.DoesNotExist:
            return None

    def get_checkout_time(self, obj):
        hoje = date.today()
        try:
            atendimento = Atendimento.objects.get(funcionario=obj, data=hoje)
            return (
                atendimento.checkout.strftime("%d-%m-%Y %H:%M")
                if atendimento.checkout
                else None
            )
        except Atendimento.DoesNotExist:
            return None


class MonthlyAttendanceSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField()
    total_present_days = serializers.SerializerMethodField()
    total_absent_days = serializers.SerializerMethodField()
    current_month = serializers.SerializerMethodField()

    class Meta:
        model = Funcionario
        fields = [
            "id",
            "nome",
            "codigo",
            "current_month",
            "days",
            "total_present_days",
            "total_absent_days",
        ]

    def get_current_month(self, obj):
        return date.today().strftime("%B %Y")

    def get_days(self, obj):
        today = date.today()
        first_day = today.replace(day=1)
        last_day = today

        atendimentos = Atendimento.objects.filter(
            funcionario=obj, data__range=[first_day, last_day]
        ).order_by("data")

        days_data = []
        current_day = first_day

        while current_day <= last_day:
            atendimento = atendimentos.filter(data=current_day).first()

            day_status = {
                "date": current_day.strftime("%d-%m-%Y"),
                "weekday": current_day.strftime("%A"),
                "status": "Ausente",
                "checkin": None,
                "checkout": None,
            }

            if atendimento:
                if atendimento.checkout:
                    day_status["status"] = "Presente"
                else:
                    day_status["status"] = "Check-in apenas"

                day_status["checkin"] = (
                    atendimento.checkin.strftime("%H:%M")
                    if atendimento.checkin
                    else None
                )
                day_status["checkout"] = (
                    atendimento.checkout.strftime("%H:%M")
                    if atendimento.checkout
                    else None
                )

            days_data.append(day_status)
            current_day += timedelta(days=1)

        return days_data

    def get_total_present_days(self, obj):
        today = date.today()
        first_day = today.replace(day=1)

        return Atendimento.objects.filter(
            funcionario=obj, data__range=[first_day, today], checkin__isnull=False
        ).count()

    def get_total_absent_days(self, obj):
        today = date.today()
        first_day = today.replace(day=1)

        total_days = (today - first_day).days + 1
        present_days = self.get_total_present_days(obj)

        return total_days - present_days


class AtividadeSerializer(serializers.ModelSerializer):
    codigo = serializers.CharField(write_only=True)
    checkin = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M", 
        input_formats=["%d-%m-%Y %H:%M"], 
        required=False
    )
    checkout = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M", 
        input_formats=["%d-%m-%Y %H:%M"], 
        required=False
    )
    funcionario_nome = serializers.CharField(source="funcionario.nome", read_only=True)

    class Meta:
        model = Atividade
        fields = [
            "id",
            "codigo",
            "funcionario_nome",
            "data",
            "checkin",
            "checkout",
            "descricao",
        ]
        read_only_fields = ["data"]

    def validate(self, data):
        codigo = data.get("codigo")
        checkin = data.get("checkin")
        checkout = data.get("checkout")
        descricao = data.get("descricao")

        try:
            funcionario = Funcionario.objects.get(codigo=codigo)
        except Funcionario.DoesNotExist:
            raise serializers.ValidationError({"codigo": "Código de funcionário inválido."})

        data["funcionario"] = funcionario

        if checkin:
            data["data"] = checkin.date()
            if not descricao:
                raise serializers.ValidationError(
                    {"descricao": "Este campo é obrigatório quando faz check-in."}
                )
        elif checkout:
            data["data"] = checkout.date()
            # Não requer descrição para checkout
        else:
            raise serializers.ValidationError(
                {"checkin": "Informe pelo menos check-in ou check-out."}
            )

        return data

    def create(self, validated_data):
        codigo = validated_data.pop("codigo", None)
        funcionario = validated_data.get("funcionario")
        checkin = validated_data.get("checkin")
        checkout = validated_data.get("checkout")
        data = validated_data.get("data")

        # Caso seja apenas CHECKOUT
        if checkout and not checkin:
            try:
                atividade = Atividade.objects.filter(
                    funcionario=funcionario,
                    data=data,
                    checkout__isnull=True
                ).latest('checkin')  # Pega o registro mais recente sem checkout
                
                atividade.checkout = checkout
                atividade.save()
                return atividade

            except Atividade.DoesNotExist:
                raise serializers.ValidationError(
                    {"checkout": "Nenhum check-in encontrado para realizar o check-out."}
                )

        return Atividade.objects.create(**validated_data)



class FuncionarioAtividadesHojeSerializer(serializers.ModelSerializer):
    atividades = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Funcionario
        fields = ["id", "nome", "codigo", "cargo", "status", "atividades"]

    def get_atividades(self, obj):
        hoje = date.today()
        atividades = Atividade.objects.filter(funcionario=obj, data=hoje)
        return AtividadeSerializer(atividades, many=True).data

    def get_status(self, obj):
        hoje = date.today()
        try:
            atendimento = Atendimento.objects.get(funcionario=obj, data=hoje)
            if atendimento.checkout:
                return "Finalizado"
            if atendimento.checkin:
                return "Em andamento"
        except Atendimento.DoesNotExist:
            pass
        return "Não iniciado"
