from django.contrib import admin
from .models import Funcionario, Atendimento, Atividade

admin.site.register(Funcionario)
admin.site.register(Atendimento)
admin.site.register(Atividade)