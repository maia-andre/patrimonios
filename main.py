import flet as ft
from ativos import pagina_ativos
from pagina_listar import pagina_listar

def main(page: ft.Page):
    # Função para navegar para a página de ativos
    def navegar_ativos(e):
        page.go("/ativos")

    # Função para navegar para a página de boas-vindas
    def navegar_boas_vindas(e):
        page.go("/")

    # Definindo a página de boas-vindas
    def pagina_boas_vindas():
        page.title = "Bem-vindo"
        page.clean()  # Limpa a página atual
        page.add(
            ft.Text("Bem-vindo ao Sistema de Bens Patrimoniais", size=30, weight="bold"),
            ft.ElevatedButton("Consultar Bens Patrimoniais", on_click=navegar_ativos),
            ft.ElevatedButton("Listar Bens Patrimoniais", on_click=lambda e: page.go("/listar"))  # Navegar para Listar
        )

    # Inicia com a página de boas-vindas
    pagina_boas_vindas()

    # Define a navegação das páginas
    page.on_route_change = lambda e: {
        "/": pagina_boas_vindas,
        "/ativos": lambda: pagina_ativos(page),
        "/listar": lambda: pagina_listar(page),
    }.get(e.route, lambda: page.add(ft.Text("Página não encontrada.")))()

# Executar o app
ft.app(target=main)
