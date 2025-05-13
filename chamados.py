import streamlit as st
import pandas as pd
import datetime
from pathlib import Path
import os

st.set_page_config(
    page_title="Abertura de Chamado",
    page_icon="🛠️",
    layout="centered"
)

menu = st.sidebar.selectbox("📋 Menu", ["Cadastro de Chamado", "Registros"])

if menu == "Cadastro de Chamado":
    st.header("📨 Abertura de Chamado SalesOps (Dados) - **MADM Consultoria**")

    st.markdown("""
    Preencha o formulário abaixo para registrar um chamado junto à equipe de suporte técnico.
    """)

    
    if "colaboradores" not in st.session_state:
        st.session_state.colaboradores = [""]
    if "novos_colaboradores" not in st.session_state:
        st.session_state.novos_colaboradores = []

    nome = st.text_input("Seu nome completo", max_chars=50)
    email = st.text_input("Seu e-mail corporativo", placeholder="exemplo@empresa.com.br")
    titulo = st.text_input("Título do chamado", max_chars=100)
    descricao = st.text_area("Descrição detalhada do problema", height=150)

    tipo = st.selectbox("Tipo de Solicitação", [
        "Novo colaborador(a)",
        "Erro de sistema",
        "Acesso negado a kommo",
        "Alteração de equipe",
        "Chamada muda - 3c",
        "Tela em branco campanha - 3c"
    ])

    
    if tipo == "Novo colaborador(a)":
        st.markdown("### 👤 Cadastro de Novo Colaborador")
        if st.button("➕ Adicionar novo colaborador"):
            st.session_state.novos_colaboradores.append({
                "nome": "",
                "email": "",
                "equipe": "",
                "acesso": "3c"
            })

        for idx, colaborador in enumerate(st.session_state.novos_colaboradores):
            st.markdown(f"**Colaborador {idx + 1}**")
            colaborador["nome"] = st.text_input(f"Nome {idx + 1}", key=f"nome_{idx}")
            colaborador["email"] = st.text_input(f"E-mail {idx + 1}", key=f"email_{idx}")
            colaborador["equipe"] = st.selectbox(
                f"Equipe Responsável {idx + 1}",
                [
                    "Equipe Ariana", "Equipe Julia", "Equipe Maiana", "Equipe Mariana Paranhos",
                    "Equipe Vinicius", "Equipe Irene", "Equipe Jennifer", "Equipe Hugo",
                    "Quinquênio", "PRO - Leticia", "AS - Francieli", "GANHO - Lucilene"
                ],
                key=f"equipe_{idx}"
            )
            colaborador["acesso"] = st.selectbox(
                f"Acesso {idx + 1}",
                ["3c", "Kommo", "Ambas"],
                key=f"acesso_{idx}"
            )
            st.markdown("---")

    nova_equipe = None
    if tipo == "Alteração de equipe":
        nova_equipe = st.selectbox("Selecione a nova equipe", [
            "Equipe Ariana", "Equipe Julia", "Equipe Maiana", "Equipe Mariana Paranhos",
            "Equipe Vinicius", "Equipe Irene", "Equipe Jennifer", "Equipe Hugo",
            "Quinquênio", "PRO - Leticia", "AS - Francieli", "GANHO - Lucilene"
        ])

        st.markdown("**Colaboradores(as) a serem alterados(as):**")
        for i in range(len(st.session_state.colaboradores)):
            st.session_state.colaboradores[i] = st.text_input(
                f"Nome do colaborador(a) {i+1}",
                value=st.session_state.colaboradores[i],
                key=f"colaborador_{i}"
            )

        if st.button("➕ Adicionar outro colaborador(a)"):
            st.session_state.colaboradores.append("")

    prioridade = st.radio("Prioridade do chamado", ["Baixa", "Média", "Alta", "Crítica"])
    data_abertura = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    botao = st.button("Enviar chamado")

    if botao:
        erros = False

        if not nome.strip():
            st.error("Por favor, preencha seu nome.")
            erros = True

        if "@" not in email or "." not in email:
            st.error("Por favor, insira um e-mail válido.")
            erros = True

        if not titulo.strip():
            st.error("O título do chamado é obrigatório.")
            erros = True

        if not descricao.strip():
            st.error("A descrição é obrigatória.")
            erros = True

        if tipo == "Alteração de equipe":
            if not nova_equipe:
                st.error("Por favor, selecione a nova equipe.")
                erros = True
            if not any(nome.strip() for nome in st.session_state.colaboradores):
                st.error("Você precisa informar pelo menos um nome de colaborador(a).")
                erros = True

        if tipo == "Novo colaborador(a)" and not st.session_state.novos_colaboradores:
            st.error("Adicione pelo menos um novo colaborador.")
            erros = True

        if not erros:
            st.success("✅ Chamado registrado com sucesso!")
            st.write(f"**Data de Criação:** {data_abertura}")
            st.write(f"**Data:** {data_abertura}")
            st.write(f"**Nome:** {nome}")
            st.write(f"**E-mail:** {email}")
            st.write(f"**Título:** {titulo}")
            st.write(f"**Descrição:** {descricao}")
            st.write(f"**Tipo:** {tipo}")
            st.write(f"**Prioridade:** {prioridade}")

            dados = {
                "Data de Criação": [data_abertura],
                "Data": [data_abertura],
                "Nome": [nome],
                "Email": [email],
                "Título": [titulo],
                "Descrição": [descricao],
                "Tipo": [tipo],
                "Prioridade": [prioridade],
                "Nova Equipe": [nova_equipe if tipo == "Alteração de equipe" else ""],
                "Colaboradores(as)": [", ".join(c for c in st.session_state.colaboradores if c.strip()) if tipo == "Alteração de equipe" else ""],
                "Novos Nomes": [", ".join([colaborador['nome'] for colaborador in st.session_state.novos_colaboradores]) if tipo == "Novo colaborador(a)" else ""],
                "Novos Emails": [", ".join([colaborador['email'] for colaborador in st.session_state.novos_colaboradores]) if tipo == "Novo colaborador(a)" else ""],
                "Equipes": [", ".join([colaborador['equipe'] for colaborador in st.session_state.novos_colaboradores]) if tipo == "Novo colaborador(a)" else ""],
                "Acessos": [", ".join([colaborador['acesso'] for colaborador in st.session_state.novos_colaboradores]) if tipo == "Novo colaborador(a)" else ""],
            }

            pasta_tipo = tipo.replace(" ", "_").lower()
            caminho_pasta = Path(f"registros/{pasta_tipo}")
            os.makedirs(caminho_pasta, exist_ok=True)

            csv_path = caminho_pasta / "registros.csv"
            df = pd.DataFrame(dados)

            if csv_path.exists():
                df.to_csv(csv_path, mode='a', header=False, index=False)
            else:
                df.to_csv(csv_path, index=False)

elif menu == "Registros":
    st.header("📄 Registros de Chamados")
    csv_path = Path("registros")

    if csv_path.exists():
        subpastas = [f for f in csv_path.iterdir() if f.is_dir()]
        for subpasta in subpastas:
            st.subheader(subpasta.name)
            sub_csv_path = subpasta / "registros.csv"
            if sub_csv_path.exists():
                df = pd.read_csv(sub_csv_path)

                
                df["Data de Criação"] = pd.to_datetime(df["Data de Criação"], format="%d/%m/%Y %H:%M")

                # Filtra os registros dos últimos 10 dias
                data_atual = datetime.datetime.now()
                dez_dias_atras = data_atual - datetime.timedelta(days=10)
                df_filtrado = df[df["Data de Criação"] >= dez_dias_atras]

                
                if not df_filtrado.empty:
                    st.dataframe(df_filtrado, use_container_width=True)
                    st.download_button("📥 Baixar CSV", data=df_filtrado.to_csv(index=False), file_name=f"{subpasta.name}_registros.csv", mime="text/csv")
                else:
                    st.info("Nenhum registro encontrado nos últimos 10 dias.")
            else:
                st.info("Nenhum registro encontrado ainda.")
    else:
        st.info("Nenhuma subpasta de registros encontrada.")
