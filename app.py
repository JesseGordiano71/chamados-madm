import streamlit as st
import datetime

st.set_page_config(
    page_title="Contrato de trabalho",
    page_icon="🖊️",
    layout="centered"
)

st.header("Contrato de trabalho")

st.markdown("""
## Bem-vindo ao seu contrato de trabalho

Este é o seu **contrato individual de trabalho**, que estabelece as condições básicas para sua atuação na empresa.

Ao aceitar os termos abaixo, você concorda com as cláusulas previstas, tais como jornada de trabalho, responsabilidades, política interna, sigilo de informações e demais obrigações legais.

### Instruções:
- Leia atentamente o conteúdo do contrato;
- Caso esteja de acordo, marque a opção *"Aceite o termo"*;
- Em seguida, preencha seus dados pessoais para que possamos registrar formalmente seu aceite.

**Importante:** seus dados serão armazenados com segurança e utilizados exclusivamente para fins contratuais e administrativos internos.
""")

checkbox = st.checkbox("Aceite o termo")


def formatar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf

if checkbox:
    nome = st.text_input("Digite seu nome", max_chars=50)

    cpf_raw = st.text_input("Digite seu CPF (apenas números)", max_chars=11, placeholder="Ex: 00000000000")
    cpf = formatar_cpf(cpf_raw)

    idade = st.number_input("Digite sua idade", step=1, format="%d", min_value=1)

    data = st.date_input(
        "Data de nascimento",
        value=datetime.date(2000, 1, 1),
        min_value=datetime.date(1900, 1, 1),
        format="DD/MM/YYYY"
    )

    genero = st.radio("Selecione seu gênero", ("Masculino", "Feminino", "Prefiro não informar"))
    opcao = st.selectbox("Qual sua cor", ["Branca", "Negra", "Parda", "Amarela", "Indígena"])


    botao = st.button("Cadastrar")

    if botao:
        erros = False

        if nome.strip() == "":
            st.error("Por favor, preencha seu nome.", icon="❌")
            erros = True

        if len(cpf_raw.strip()) != 11:
            st.error("Por favor, preencha um CPF válido com 11 dígitos.", icon="❌")
            erros = True

        if not erros:
            st.success("Parabéns! Você realizou o cadastro.", icon="✅")
            st.write(f"Nome: {nome}" )
            st.write("CPF:", cpf)
            st.write(f"idade: {idade}")
            st.write(f"Genero: {genero}")
            st.write(f"Cor: {opcao}")
                     

else:
    st.info("Você precisa aceitar os termos para preencher seus dados.", icon="⚠️")
