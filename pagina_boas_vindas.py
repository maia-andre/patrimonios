import flet as ft

def pagina_boas_vindas(page: ft.Page):
    page.title = "Bem-vindo"
    
    def ir_para_ativos(e):
        page.go("/ativos")

    def ir_para_listar(e):
        page.go("/listar")

    page.add(
        ft.Text("Bem-vindo à aplicação de bens patrimoniais!", size=30, weight="bold"),
        ft.ElevatedButton("Consulta de bens patrimoniais", on_click=ir_para_ativos),
        ft.ElevatedButton("Listar bens patrimoniais", on_click=ir_para_listar)
    )
