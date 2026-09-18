# -*- coding: utf-8 -*-
"""[VIEW] Login — equivalente a src/pages/Login.tsx. Apenas apresentação;
toda regra de negócio/estado é delegada aos Controllers."""

import streamlit as st

from controllers import academico_controller, auth_controller, session_controller
from models import seed_data as data
from views.components import PRIMARY, TEXT_DARK, TEXT_MUTED, badge_html


@st.dialog("Criar nova conta", width="large")
def register_modal():
    ss = st.session_state
    if "_reg_step" not in ss:
        ss._reg_step = 1
        ss._reg_form = {
            "nome": "", "email": "", "cpf": "", "funcao": "Aluno",
            "nucleo": "", "curso": "", "turno": "", "turma": "",
            "senha": "", "confirmar": "",
        }
        ss._reg_disciplinas = []

    form = ss._reg_form

    if ss._reg_step == 1:
        st.caption("Etapa 1 de 2 — Dados pessoais e de acesso")
        form["nome"] = st.text_input("Nome completo *", value=form["nome"])
        form["email"] = st.text_input("E-mail *", value=form["email"])
        form["cpf"] = st.text_input("CPF *", value=form["cpf"], placeholder="000.000.000-00")
        form["funcao"] = st.selectbox(
            "Função", data.FUNCOES, index=data.FUNCOES.index(form["funcao"]) if form["funcao"] in data.FUNCOES else 3
        )
        c1, c2 = st.columns(2)
        form["senha"] = c1.text_input("Senha *", value=form["senha"], type="password")
        form["confirmar"] = c2.text_input("Confirmar senha *", value=form["confirmar"], type="password")

        if st.button("Continuar →", type="primary", use_container_width=True):
            err = auth_controller.validate_step1(form["nome"], form["email"], form["cpf"],
                                                  form["senha"], form["confirmar"])
            if err:
                st.error(err)
            else:
                ss._reg_step = 2
                st.rerun()

    else:
        st.caption("Etapa 2 de 2 — Vínculo acadêmico")
        nucleos_ativos = auth_controller.nucleos_ativos_nomes()
        form["nucleo"] = st.selectbox("Núcleo *", [""] + nucleos_ativos,
                                       index=([""] + nucleos_ativos).index(form["nucleo"]) if form["nucleo"] in nucleos_ativos else 0)
        nucleo_obj = academico_controller.get_nucleo_by_name(form["nucleo"]) if form["nucleo"] else None
        cursos_list = academico_controller.cursos_by_nucleo(nucleo_obj["id"]) if nucleo_obj else []
        curso_names = [c["nome"] for c in cursos_list]
        form["curso"] = st.selectbox("Curso *", [""] + curso_names,
                                      index=([""] + curso_names).index(form["curso"]) if form["curso"] in curso_names else 0)
        form["turno"] = st.selectbox("Turno *", [""] + data.TURNOS,
                                      index=([""] + data.TURNOS).index(form["turno"]) if form["turno"] in data.TURNOS else 0)

        curso_obj = next((c for c in cursos_list if c["nome"] == form["curso"]), None)
        all_turmas = academico_controller.turmas_by_curso(curso_obj["id"]) if curso_obj else []
        turma_list = [t for t in all_turmas if not form["turno"] or t["turno"] == form["turno"]]
        turma_names = [t["nome"] for t in turma_list]
        form["turma"] = st.selectbox("Turma *", [""] + turma_names,
                                      index=([""] + turma_names).index(form["turma"]) if form["turma"] in turma_names else 0)

        turma_obj = next((t for t in turma_list if t["nome"] == form["turma"]), None)
        disc_list = academico_controller.disciplinas_by_turma(turma_obj["id"]) if turma_obj else []
        if disc_list:
            disc_names = [d["nome"] for d in disc_list]
            ss._reg_disciplinas = st.multiselect("Disciplinas", disc_names, default=ss._reg_disciplinas)

        c1, c2 = st.columns(2)
        if c1.button("← Voltar", use_container_width=True):
            ss._reg_step = 1
            st.rerun()
        if c2.button("Enviar cadastro", type="primary", use_container_width=True):
            if not form["nucleo"] or not nucleo_obj:
                st.error("Selecione o Núcleo.")
            elif not form["curso"] or not curso_obj:
                st.error("Selecione o Curso.")
            elif not form["turno"]:
                st.error("Selecione o Turno.")
            elif not form["turma"] or not turma_obj:
                st.error("Selecione a Turma.")
            else:
                auth_controller.submit_registration(form, ss._reg_disciplinas)
                del ss._reg_step
                del ss._reg_form
                del ss._reg_disciplinas
                st.success("Cadastro enviado! Aguarde a aprovação de um administrador.")
                st.balloons()
                if st.button("Fechar"):
                    st.rerun()


def render():
    st.markdown(
        f"""
        <div style="text-align:center; padding: 2rem 0 1rem;">
            <div style="display:inline-flex; align-items:center; justify-content:center;
                        width:64px; height:64px; border-radius:16px; background:{PRIMARY};
                        color:white; font-weight:800; font-size:1.1rem; margin-bottom: 1rem;">
                SGA
            </div>
            <h1 style="color:{TEXT_DARK}; font-weight:800; margin-bottom:0.2rem;">
                Sistema de Gestão de Ambientes
            </h1>
            <p style="color:{TEXT_MUTED}; font-size:0.9rem;">
                Plataforma integrada para gerenciamento de reservas, controle de ambientes
                e organização de membros da instituição.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1.1], gap="large")

    with left:
        st.markdown("#### Bem-vindo")
        st.caption("Acesse sua conta para continuar")
        with st.form("login_form"):
            st.text_input("E-mail", placeholder="seu@email.com")
            st.text_input("Senha", type="password", placeholder="••••••••")
            st.checkbox("Lembrar de mim")
            submitted = st.form_submit_button("Entrar", type="primary", use_container_width=True)
            if submitted:
                st.info("Use uma das contas de demonstração à direita para entrar no sistema.")

        st.write("")
        if st.button("Criar nova conta", use_container_width=True):
            register_modal()

        st.write("")
        st.markdown(
            f'<p style="text-align:center; font-size:0.8rem; color:{TEXT_MUTED};">'
            f'Problemas de acesso? <a href="#" style="color:{PRIMARY}; font-weight:600;">'
            f'Contate o suporte</a></p>',
            unsafe_allow_html=True,
        )
        if st.button("→ Central de Ajuda", use_container_width=True):
            session_controller.goto("suporte")
            st.rerun()

    with right:
        st.markdown("###### Entrar como — Demonstração")
        cols = st.columns(2)
        for i, u in enumerate(auth_controller.demo_users()):
            rc = data.ROLE_COLORS[u["role"]]
            with cols[i % 2]:
                with st.container(border=True):
                    st.markdown(badge_html(u["role"], rc["bg"], rc["text"], rc["dot"]), unsafe_allow_html=True)
                    st.markdown(f"**{u['nome']}**")
                    if u.get("nucleo"):
                        st.caption(f"Núcleo {u['nucleo']}")
                    st.caption(auth_controller.role_description(u["role"]))
                    if st.button("Entrar", key=f"demo_{i}", use_container_width=True):
                        auth_controller.login_as(u)
                        st.rerun()

    st.write("")
    st.markdown("<hr/>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Ambientes", "200+")
    c2.metric("Reservas/mês", "1.4k")
    c3.metric("Satisfação", "98%")
