import pandas as pd
import yagmail
import os

EMAIL = "guilherme.cm220@gmail.com" 
SENHA_APP = "celular123" 
DESTINO = "seba.moreira85@gmail.com" 

arquivo = "obras.xlsx"

if not os.path.exists(arquivo):
    print("Nenhum dado ainda para enviar.")
    exit()

df = pd.read_excel(arquivo)

total = len(df)
no_prazo = (df["no_prazo"] == "Sim").sum()
atrasadas = (df["no_prazo"] == "Não").sum()

mensagem = f"""
Olá!

Segue o resumo diário das obras:

Total de obras: {total}
No prazo: {no_prazo}
Atrasadas: {atrasadas}

Lista completa em anexo.

Att,
Sistema de Controle de Obras
"""

yag = yagmail.SMTP(EMAIL, SENHA_APP)
yag.send(
    to=DESTINO,
    subject="📊 Relatório Diário de Obras",
    contents=mensagem,
    attachments=arquivo
)

print("Relatório enviado com sucesso!")