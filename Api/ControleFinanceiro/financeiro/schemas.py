from ninja import ModelSchema
from .models import Lancamentos

class FinSchema(ModelSchema):
    class Meta:
        model = Lancamentos
        fields = ['Mes', 'Data', 'Estabelecimento', 'Tipo_Conta', 'Parcelas', 'Valor', 'Vlr_Parcela', 'Centro_Custo', 'Despesa_fv', 'Tipo_Lancamento', 'Id', 'Hora']