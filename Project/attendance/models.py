from django.db import models


class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    codigo = models.CharField(max_length=20, unique=True)
    cargo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome} ({self.codigo}) - {self.cargo}"


class Atendimento(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE, related_name='atendimentos')
    data = models.DateField()
    checkin = models.DateTimeField(null=True, blank=True)
    checkout = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Atendimento de {self.funcionario.nome} em {self.data}"


class Atividade(Atendimento):
    descricao = models.TextField()

    def __str__(self):
        return f"Atividade: {self.descricao} ({self.funcionario.nome} - {self.data})"
