import streamlit as st
import pandas as pd
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

st.set_page_config(page_title="Controle de Obras", layout="centered")

st.title("📋 Formulário de Acompanhamento de Obras")

nome_obra = st.text_input("Nome da obra")
responsavel = st.text_input("Responsável")
no_prazo = st.selectbox("Está no prazo?", ["Sim", "Não"])
data_termino = st.date_input("Data prevista de término")
observacoes = st.text_area("Observações")

if st.button("Enviar"):
    if not nome_obra or not responsavel:
        st.warning("Preencha pelo menos o nome da obra e o responsável.")
    else:
        novo_dado = {
            "nome_obra": nome_obra,
            "responsavel": responsavel,
            "no_prazo": no_prazo,
            "data_termino": str(data_termino),
            "observacoes": observacoes
        }

        arquivo = "obras.xlsx"

        if os.path.exists(arquivo):
            df = pd.read_excel(arquivo)
            df = pd.concat([df, pd.DataFrame([novo_dado])], ignore_index=True)
        else:
            df = pd.DataFrame([novo_dado])

        df.to_excel(arquivo, index=False)

        st.success("Dados salvos com sucesso!")

# ----- DASHBOARD -----

st.markdown("---")
st.header("📊 Dashboard de Obras")

if os.path.exists("obras.xlsx"):
    df = pd.read_excel("obras.xlsx")

    total = len(df)
    no_prazo = (df["no_prazo"] == "Sim").sum()
    atrasadas = (df["no_prazo"] == "Não").sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("🏗️ Total de Obras", total)
    col2.metric("✅ No Prazo", no_prazo)
    col3.metric("⛔ Atrasadas", atrasadas)

    st.markdown("### Status das Obras")

    fig, ax = plt.subplots()
    df["no_prazo"].value_counts().plot(kind="bar", ax=ax)
    ax.set_xlabel("Status")
    ax.set_ylabel("Quantidade")
    ax.set_title("")

    st.pyplot(fig)

    st.markdown("### 📋 Lista Completa")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Nenhuma obra cadastrada ainda.")
