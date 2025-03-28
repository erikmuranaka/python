import sys
from os import getcwd
import pyodbc
from ninja import Router
from .schemas import FinSchema
from .models import Lancamentos
from typing import List

financeiro_router = Router()

@financeiro_router.post('inserir_gastos/', response={200: str})
def inserir_gastos(request, fin_schema: FinSchema):

    conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=G:\Meu Drive\Planilha_Gastos\MuranakaSistemas\Api\ControleFinanceiro\Financeiro.accdb;')

    cursor = conn.cursor()

    Mes = fin_schema.dict().get('Mes')
    Data = fin_schema.dict().get('Data')    
    Estabelecimento = fin_schema.dict().get('Estabelecimento')
    Tipo_Conta = fin_schema.dict().get('Tipo_Conta')
    Parcelas = fin_schema.dict().get('Parcelas')
    Valor = fin_schema.dict().get('Valor')
    Vlr_Parcela = fin_schema.dict().get('Vlr_Parcela')
    Centro_Custo = fin_schema.dict().get('Centro_Custo')
    Despesa_fv = fin_schema.dict().get('Despesa_fv')
    Tipo_Lancamento = fin_schema.dict().get('Tipo_Lancamento')
    Hora = fin_schema.dict().get('Hora')

    sql = f'''
           insert into Lancamentos (Mes, Data, Estabelecimento, Tipo_Conta, Parcelas, Valor, Vlr_Parcela, Centro_Custo, Despesa_fv, Tipo_Lancamento, Hora)
                   values
                   ({Mes}, '{Data}', '{Estabelecimento}', '{Tipo_Conta}', {Parcelas}, {Valor}, {Vlr_Parcela}, '{Centro_Custo}', '{Despesa_fv}', '{Tipo_Lancamento}', '{Hora}')
    '''
    
    cursor.execute(sql)
    
    conn.commit()
    conn.close()

    return 'Dados inseridos com sucesso!'

@financeiro_router.get('buscar_ultimo_gasto/', response=List[FinSchema])
def buscar_ultimo_gasto(request):

    conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=G:\Meu Drive\Planilha_Gastos\MuranakaSistemas\Api\ControleFinanceiro\Financeiro.accdb;')

    cursor = conn.cursor()

    list = []

    cursor.execute('SELECT top 1 * FROM Lancamentos order by Id desc')

    for row in cursor.fetchall():
        dados = {
            "Mes": row[0],
            "Data": row[1],
            "Estabelecimento": row[2],
            "Valor": row[3],
            "Tipo_Conta": row[4],
            "Parcelas": row[5],
            "Vlr_Parcela": row[6],
            "Centro_Custo": row[7],
            "Despesa_fv": row[8],
            "Tipo_Lancamento": row[9],
            "Id": row[10],
            "Hora": row[11]
        }

        list.append(dados)

    cursor.close()
    conn.close()

    return list

@financeiro_router.post('buscar_gasto/', response=List[FinSchema])
def buscar_gasto(request, fin_schema: FinSchema):

    conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; DBQ=G:\Meu Drive\Planilha_Gastos\MuranakaSistemas\Api\ControleFinanceiro\Financeiro.accdb;')

    cursor = conn.cursor()

    Data = fin_schema.dict().get('Data')    
    Estabelecimento = fin_schema.dict().get('Estabelecimento')
    Hora = fin_schema.dict().get('Hora')

    list = []

    cursor.execute("SELECT top 1 * FROM Lancamentos where estabelecimento = ? and Data = ? and hora = ?", Estabelecimento, Data, Hora)

    for row in cursor.fetchall():
        dados = {
            "Mes": row[0],
            "Data": row[1],
            "Estabelecimento": row[2],
            "Valor": row[3],
            "Tipo_Conta": row[4],
            "Parcelas": row[5],
            "Vlr_Parcela": row[6],
            "Centro_Custo": row[7],
            "Despesa_fv": row[8],
            "Tipo_Lancamento": row[9],
            "Id": row[10],
            "Hora": row[11]
        }

        list.append(dados)

    cursor.close()
    conn.close()

    return list