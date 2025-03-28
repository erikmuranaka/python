#encoding: utf-8

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import datetime
import json
import re
import requests

base_dados = 'G:/Meu Drive/Planilha_Gastos/base_dados.csv'

# Add the phone number of the group and code to scan
target = 'WhatsApp da Riqueza'

diasSemana = ('Monday'.upper(), 'Tuesday'.upper(), 'Wednesday'.upper(), 'Thursday'.upper(), 'Friday'.upper(), 'Saturday'.upper(), 'Sunday'.upper(),
              'Segunda-Feira'.upper(), 'Terça-Feira'.upper(), 'Quarta-Feira'.upper(), 'Quinta-Feira'.upper(), 'Sexta-Feira'.upper(), 'Sábado'.upper(), 'Domingo'.upper())

objtipo_lancamento = {
    "Entrada": ["Salário", "Reembolso", "Recebimento"]
}

def busca_centroCusto(estabelecimento):

    v_centroCusto = ''

    try:
        file = open("centro_custo.json", encoding='utf-8')

        data = json.load(file)

        for cc in data:
            for texto in data[cc]:
                if texto.upper() == str.upper(estabelecimento):
                    v_centroCusto = cc
        
        file.close()

        objcentroC = v_centroCusto.split(' ')

        CentroCusco = objcentroC[0] if len(objcentroC) > 0 else ''
        Despesa_fv = objcentroC[1] if len(objcentroC) > 1 else 'V'

        return CentroCusco, Despesa_fv
    except:
        return ''
    
def config_Estabelecimento(estabelecimento):

    objEstab = estabelecimento.split(' ')

    if len(objEstab) > 2:
        EstabC = objEstab[0]
        NomeEstab = f"{objEstab[1]} {objEstab[2]}"

        CentroCusco, Despesa_fv = busca_centroCusto(EstabC)

        return CentroCusco, Despesa_fv, NomeEstab
    elif len(objEstab) > 1:
        EstabC = objEstab[0]
        NomeEstab = objEstab[1]

        CentroCusco, Despesa_fv = busca_centroCusto(EstabC)

        if len(CentroCusco) > 0:
            return CentroCusco, Despesa_fv, NomeEstab
        else:
            CentroCusco, Despesa_fv = busca_centroCusto(f"{EstabC} {NomeEstab}")

            return CentroCusco, Despesa_fv, f"{EstabC} {NomeEstab}"
    else:
        NomeEstab = objEstab[0]

        CentroCusco, Despesa_fv = busca_centroCusto(NomeEstab)

        return CentroCusco, Despesa_fv, NomeEstab
        
def busca_tipo_lanc(centroCusto):

    v_tipo = 'S'

    data = objtipo_lancamento['Entrada']

    for cc in data:
        if cc.upper() == str.upper(centroCusto):
            v_tipo = 'E'

    return v_tipo

def save_data(dados):

    df = pd.read_csv(base_dados, delimiter=';')

    new_base = [
        {"Mes": item[0],
         "Data": item[1],
         "Estabelecimento": item[2],
         "Valor": item[3],
         "Tipo_Conta": item[4],
         "Parcela": item[5],
         "Vlr_parcela": item[6],
         "Centro_Custo": item[7],
         "Despesa_fv": item[8],
         "Tipo_Lancamento": item[9]
        }
        for item in df.values
    ]

    new_base.append(dados)

    df_new = pd.DataFrame(new_base)

    df_new.to_csv(base_dados, sep=';', index=False, encoding='utf-8')

def Busca_Ultimo_Registro():
    response = requests.get("http://127.0.0.1:8000/api/buscar_ultimo_gasto/")
    
    try:
        data = response.json()

        data = data[0]
    except:
        data = []

    return data

def Busca_Registro(dados):

    response = requests.post("http://127.0.0.1:8000/api/buscar_gasto/", json=dados)
    
    try:
        data = response.json()

        data = data[0]
    except:
        data = []

    return data
    
def read_messages(mensagem, horalida):
    msg = mensagem.split('\n')

    hora = msg[len(msg)-1].strip()

    if (hora != horalida):

        msg = msg[len(msg)-2].strip()

        vTexto = re.findall("\d", msg)[0]

        vDigito = msg.find(vTexto)

        DescrEstab = msg[0:vDigito-1]

        vRestoTexto = msg[vDigito:]

        gastos = vRestoTexto.split(' ')

        try:
            valor = gastos[0].replace(",",".")
        except:
            valor = '0'

        try:
            Tipo_Conta = gastos[1]
        except:
            Tipo_Conta = ''
        
        try:
            parcela = int(gastos[2])
        except:
            parcela = int(1)

        if float(valor) > 0:
            vlr_Parcela = str(float(valor) / parcela)
        else:
            vlr_Parcela = '0'

        CentroCusco, Despesa_fv, NomeEstab = config_Estabelecimento(DescrEstab)

        tipo_lancamento = busca_tipo_lanc(CentroCusco)

        data = datetime.date.today()

        dataStr = data + datetime.timedelta()

        v_dados = {
            "Mes": data.month,
            "Data": dataStr,
            "Estabelecimento": NomeEstab,
            "Valor": valor,
            "Tipo_Conta": Tipo_Conta,
            "Parcela": parcela,
            "Vlr_Parcela": vlr_Parcela,
            "Centro_Custo": CentroCusco,
            "Despesa_fv": Despesa_fv,
            "Tipo_Lancamento": tipo_lancamento,
            "Hora": hora,
            "Id": 0
        }

        ultimoReg = Busca_Ultimo_Registro()

        HoraUltimoReg = ultimoReg['Hora']
        EstabUltimoReg = ultimoReg['Estabelecimento']

        if float(valor.replace(",",".")) > 0:
            if (NomeEstab != EstabUltimoReg) or (hora != HoraUltimoReg):
                response = requests.post("http://127.0.0.1:8000/api/inserir_gastos/", json=v_dados)

                data = response.json()

                print('==============================')
                print(data)
                print('==============================')

    return hora

def valida_ultimo_reg_salva(dados):

    ultimoReg = Busca_Ultimo_Registro()

    HoraUltimoReg = ultimoReg['Hora']
    EstabUltimoReg = ultimoReg['Estabelecimento']

    if float(dados['valor'].replace(",",".")) > 0:
        if (dados['NomeEstab'] != EstabUltimoReg) or (dados['hora'] != HoraUltimoReg):
            response = requests.post("http://127.0.0.1:8000/api/inserir_gastos/", json=dados)

            data = response.json()

            print('==============================')
            print(data)
            print('==============================')

def valida_reg_salva(dados):

    Reg = Busca_Registro(dados)

    if len(Reg) <= 0:
        if float(dados['Valor'].replace(",",".")) > 0:
            response = requests.post("http://127.0.0.1:8000/api/inserir_gastos/", json=dados)

            data = response.json()

            print('==============================')
            print(data)
            print('==============================')

def read_config_messages(mensagem, diasPassados):

    msg = mensagem.split('\n')

    hora = msg[len(msg)-1].strip()

    msg = msg[len(msg)-2].strip()

    vTexto = re.findall("\d", msg)[0]

    vDigito = msg.find(vTexto)

    DescrEstab = msg[0:vDigito-1]

    vRestoTexto = msg[vDigito:]

    gastos = vRestoTexto.split(' ')

    try:
        valor = gastos[0].replace(",",".")
    except:
        valor = '0'

    try:
        Tipo_Conta = gastos[1]
    except:
        Tipo_Conta = ''
    
    try:
        parcela = int(gastos[2])
    except:
        parcela = int(1)

    if float(valor) > 0:
        vlr_Parcela = str(float(valor) / parcela)
    else:
        vlr_Parcela = '0'

    CentroCusco, Despesa_fv, NomeEstab = config_Estabelecimento(DescrEstab)

    tipo_lancamento = busca_tipo_lanc(CentroCusco)

    data = datetime.date.today()

    dataStr = data + datetime.timedelta(days=-diasPassados)

    dataStr = dataStr.strftime("%Y-%m-%d")

    v_dados = {
        "Mes": data.month,
        "Data": dataStr,
        "Estabelecimento": NomeEstab,
        "Valor": valor,
        "Tipo_Conta": Tipo_Conta,
        "Parcela": parcela,
        "Vlr_Parcela": vlr_Parcela,
        "Centro_Custo": CentroCusco,
        "Despesa_fv": Despesa_fv,
        "Tipo_Lancamento": tipo_lancamento,
        "Hora": hora,
        "Id": 0
    }

    return v_dados

def read_messages_antigas(mensagem):
    msgs = mensagem.split('\n')

    mensagemAtual = ''
    diasPassados = 0
    hora = ''

    for msg in msgs:
        print(msg)
        
        if msg.upper() in ('Sincronizando mensagens mais antigas. Clique para ver o progresso.'.upper(), diasSemana):
            if msg.upper() in (diasSemana):
                diasPassados = 2
            elif msg == 'ONTEM':
                diasPassados = 1
            else:
                diasPassados = 0
            
            continue
        elif msg.find(':') < 0:
            mensagemAtual = msg

            continue
        else:
            hora = msg

            mensagemAtual = f"{mensagemAtual}\n{hora}"

            dados = read_config_messages(mensagemAtual, diasPassados)

            valida_reg_salva(dados)

    return hora

def main():

    #Set up ChromeDriver path
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-data-dir=chrome-data")

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 30)

    count = 0

    # Abrir WhatsApp Web
    driver.get("https://web.whatsapp.com/")

    horalida = ''

    while True:

        try:
            while len(driver.find_elements(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div/div/div[2]/div/canvas')) < 1:

                target_group = wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[contains(@title,'{target}')]")))
                target_group.click()

                messages = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main"]/div[3]/div/div[2]')))

                horalida = read_messages(messages[0].text, horalida)

                # if count == 0:
                #     horalida = read_messages_antigas(messages[0].text)

                #     #count += 1
                # else:
                #     horalida = read_messages(messages[0].text, horalida)
                    

        except Exception as err :
            print(err.args)

main()