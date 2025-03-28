from ninja import Router
from .schemas import FinSchema
from .models import Lancamentos
from typing import List

financeiro_router = Router()

@financeiro_router.post('inserir_gastos/', response={200: str})
def inserir_gastos(request, fin_schema: FinSchema):

    Mes = fin_schema.dict().get('Mes')
    Data = fin_schema.dict().get('Data')    
    Estabelecimento = fin_schema.dict().get('Estabelecimento')
    Tipo_Conta = fin_schema.dict().get('Tipo_Conta')
    Parcelas = fin_schema.dict().get('Parcelas')
    Valor = fin_schema.dict().get('Valor')
    Total = fin_schema.dict().get('Total')
    Centro_Custo = fin_schema.dict().get('Centro_Custo')
    Despesa_fv = fin_schema.dict().get('Despesa_fv')
    Tipo_Lancamento = fin_schema.dict().get('Tipo_Lancamento')

    financeiro = Lancamentos(
        Mes = Mes,
        Data = Data,
        Estabelecimento = Estabelecimento,
        Tipo_Conta = Tipo_Conta,
        Parcelas = Parcelas,
        Valor = Valor,
        Total = Total,
        Centro_Custo = Centro_Custo,
        Despesa_fv = Despesa_fv,
        Tipo_Lancamento = Tipo_Lancamento
    )

    financeiro.save()

    return 'Dados inseridos com sucesso!'

@financeiro_router.get('buscar_gastos/', response=List[FinSchema])
def buscar_gastos(request):

    itens = Lancamentos.objects.all()

    return itens