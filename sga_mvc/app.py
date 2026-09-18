# -*- coding: utf-8 -*-
"""
SGA — Sistema de Gestão de Ambientes
Arquitetura MVC:

    Model      -> models/      (dados + regras de negócio puras, sem Streamlit)
    View       -> views/       (apenas apresentação/Streamlit; nunca muta a sessão direto)
    Controller -> controllers/ (única camada que lê/grava st.session_state; orquestra
                                 os casos de uso chamados pelas Views)

Este arquivo é o Front Controller: inicializa o estado, define as rotas
protegidas e despacha cada rota para a View correspondente.
"""

import streamlit as st

from controllers import session_controller
from views import layout_view
from views.components import inject_css

st.set_page_config(page_title="SGA — Sistema de Gestão de Ambientes", page_icon="🏫", layout="wide")

session_controller.init_state()
inject_css()

# Permissão necessária para acessar cada rota protegida (equivalente a ProtectedRoute)
ROUTE_PERMISSION = {
    "dashboard": "canViewDashboard",
    "membros": "canViewMembros",
    "academico": "canManageAcademic",
}

# Mapa de rota -> módulo de View responsável por renderizá-la
VIEW_MODULES = {
    "dashboard": "dashboard_view",
    "reservas": "reservas_view",
    "membros": "membros_view",
    "academico": "academico_view",
    "configuracoes": "configuracoes_view",
}


def main():
    from controllers import auth_controller

    route = session_controller.current_route()

    # Rotas públicas (sem sidebar / sem sessão autenticada)
    if route == "login" or not session_controller.is_logged_in():
        from views import login_view
        login_view.render()
        return

    if route == "suporte":
        from views import suporte_view
        suporte_view.render()
        return

    if route == "menu":
        layout_view.render_sidebar()
        from views import menu_view
        menu_view.render()
        return

    # Rotas protegidas (dentro do layout com sidebar)
    layout_view.render_sidebar()

    required_perm = ROUTE_PERMISSION.get(route)
    if required_perm and not auth_controller.has_perm(required_perm):
        layout_view.render_unauthorized()
        return

    module_name = VIEW_MODULES.get(route)
    if module_name is None:
        session_controller.goto("menu")
        st.rerun()
        return

    module = __import__(f"views.{module_name}", fromlist=[module_name])
    module.render()


if __name__ == "__main__":
    main()
