import flet as ft
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from fpdf import FPDF

# Configuração do banco de dados
DATABASE_URL = "sqlite:///bens_patrimoniais.db"  # Exemplo usando SQLite
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Definindo a tabela no banco de dados
class BemPatrimonial(Base):
    __tablename__ = 'bens_patrimoniais'
    id = Column(Integer, primary_key=True)
    placa_patrimonial = Column(String(6), nullable=False)
    descricao = Column(String, nullable=False)
    codigo_unidade = Column(String(6), nullable=False)
    unidade_orcamentaria = Column(String, nullable=False)

# Criar a tabela (se não existir)
Base.metadata.create_all(engine)

def pagina_listar(page: ft.Page):
    # Tabela para armazenar dados temporariamente
    tabela_dados = []

    # Função para adicionar placa patrimonial
    def adicionar_placa(e):
        placa = input_placa.value
        # Lógica para buscar os dados do banco de dados
        resultado = session.query(BemPatrimonial).filter(BemPatrimonial.placa_patrimonial == placa).first()
        if resultado:
            tabela_dados.append(resultado)
            atualizar_tabela()
            input_placa.value = ""  # Limpa o campo após adição
            page.snack_bar = ft.SnackBar(ft.Text("Placa adicionada!"), open=True)
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Placa não encontrada!"), open=True)
            page.update()

    # Função para atualizar a tabela exibida
    def atualizar_tabela():
        tabela.rows.clear()
        for item in tabela_dados:
            tabela.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item.placa_patrimonial)),
                        ft.DataCell(ft.Text(item.descricao)),
                        ft.DataCell(ft.Text(item.codigo_unidade)),
                        ft.DataCell(ft.Text(item.unidade_orcamentaria)),
                    ]
                )
            )
        tabela.update()

    # Função para limpar a tabela
    def limpar_tabela(e):
        tabela_dados.clear()
        atualizar_tabela()
        page.snack_bar = ft.SnackBar(ft.Text("Tabela limpa!"), open=True)
        page.update()

    # Função para exportar PDF
    def exportar_pdf(e):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Cabeçalho
        pdf.cell(200, 10, txt="Lista de Bens Patrimoniais", ln=True, align='C')
        pdf.cell(50, 10, "Placa", 1)
        pdf.cell(80, 10, "Descrição", 1)
        pdf.cell(40, 10, "Código Unidade", 1)
        pdf.cell(40, 10, "Unidade Orçamentária", 1)
        pdf.ln()

        # Dados da tabela
        for item in tabela_dados:
            pdf.cell(50, 10, item.placa_patrimonial, 1)
            pdf.cell(80, 10, item.descricao, 1)
            pdf.cell(40, 10, item.codigo_unidade, 1)
            pdf.cell(40, 10, item.unidade_orcamentaria, 1)
            pdf.ln()

        pdf.output("lista_bens_patrimoniais.pdf")
        page.snack_bar = ft.SnackBar(ft.Text("PDF exportado com sucesso!"), open=True)
        page.update()

    # Layout da página
    page.title = "Listar Bens Patrimoniais"
    page.clean()
    
    input_placa = ft.TextField(label="Digite a Placa Patrimonial", width=300)
    botao_adicionar = ft.ElevatedButton("Adicionar Placa", on_click=adicionar_placa)
    botao_limpar = ft.ElevatedButton("Limpar Tabela", on_click=limpar_tabela)
    botao_exportar_pdf = ft.ElevatedButton("Exportar PDF", on_click=exportar_pdf)
    botao_voltar = ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/"))

    # Tabela de dados
    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Placa")),
            ft.DataColumn(ft.Text("Descrição")),
            ft.DataColumn(ft.Text("Código Unidade")),
            ft.DataColumn(ft.Text("Unidade Orçamentária")),
        ],
        rows=[]
    )

    # Adiciona componentes ao layout
    page.add(
        ft.Text("Listar Bens Patrimoniais", size=30, weight="bold"),
        input_placa,
        ft.Row([botao_adicionar, botao_limpar, botao_exportar_pdf, botao_voltar]),
        tabela
    )
