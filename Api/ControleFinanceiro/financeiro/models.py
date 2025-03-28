from django.db import models

lancamento_choices = (
    ('C', 'Credito'),
    ('D', 'Debito'),
    ('P', 'Pix'),
    ('R', 'Reembolso'),
    ('S', 'Salario'),
)

despesa_fv_choices = (
    ('F', 'Fixo'),
    ('V', 'Variavel')
)

# Create your models here.
class Lancamentos(models.Model):
    Data = models.DateField()
    Mes = models.IntegerField()
    Estabelecimento = models.CharField(max_length=255)
    Tipo_Conta = models.CharField(max_length=1, choices=lancamento_choices, default='C')
    Parcelas = models.IntegerField(default=1)
    Valor = models.FloatField(default=0)
    Vlr_Parcela = models.FloatField(default=0)
    Centro_Custo = models.CharField(max_length=255)
    Despesa_fv = models.CharField(max_length=1, choices=despesa_fv_choices, default='V')
    Tipo_Lancamento = models.CharField(max_length=1, default='S')
    Id = models.IntegerField()
    Hora = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao
    
class Centro_Custo(models.Model):
    nome_id = models.CharField(max_length=255)
    Estabelecimento = models.CharField(max_length=255)
    fixo_variavel = models.CharField(max_length=1, choices=despesa_fv_choices, default='V')
    Tipo_Lancamento = models.CharField(max_length=1, default='S')

    def __str__(self):
        return self.nome_id