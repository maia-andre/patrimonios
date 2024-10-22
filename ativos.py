import flet as ft
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

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

# Estado para controle de linhas expandidas
linhas_expandidas = {}

def pagina_ativos(page: ft.Page):
    # Função para garantir que apenas um checkbox seja selecionado
    def checkbox_changed(e):
        if e.control == checkbox_placa and checkbox_placa.value:
            checkbox_unidade.value = False
        elif e.control == checkbox_unidade and checkbox_unidade.value:
            checkbox_placa.value = False
        checkbox_placa.update()
        checkbox_unidade.update()

    # Função para alternar a expansão e contração da linha
    def alternar_linha_expandida(index):
        linhas_expandidas[index] = not linhas_expandidas.get(index, False)
        buscar_dados(None)  # Recarrega os dados para refletir a mudança de estado

    # Função de busca no banco de dados
    def buscar_dados(e):
        input_value = input_codigo.value

        # Validação do input (1 a 6 dígitos)
        if not input_value.isdigit() or not (1 <= len(input_value) <= 6):
            page.snack_bar = ft.SnackBar(ft.Text("Código inválido! Digite de 1 a 6 dígitos."), open=True)
            page.update()
            return
        
        # Limpar resultados da tabela
        tabela_dados.rows.clear()

        # Lógica de busca
        if checkbox_placa.value:  # Buscar por Placa Patrimonial
            resultados = session.query(BemPatrimonial).filter(BemPatrimonial.placa_patrimonial == input_value).all()
        elif checkbox_unidade.value:  # Buscar por Código da Unidade
            resultados = session.query(BemPatrimonial).filter(BemPatrimonial.codigo_unidade == input_value).all()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Selecione uma opção de busca!"), open=True)
            page.update()
            return

        # Populando a tabela com os resultados
        for index, item in enumerate(resultados):
            expandido = linhas_expandidas.get(index, False)  # Verifica se a linha está expandida
            altura_celula = 60 if not expandido else None  # Altura compacta ou expansível (None permite altura automática)

            # Adiciona a linha principal
            tabela_dados.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.GestureDetector(
                            content=ft.Container(ft.Text(item.placa_patrimonial, no_wrap=False), width=100, height=altura_celula),
                            on_tap=lambda e, index=index: alternar_linha_expandida(index)
                        )),
                        ft.DataCell(ft.GestureDetector(
                            content=ft.Container(ft.Text(item.descricao, no_wrap=False), width=300, height=altura_celula),
                            on_tap=lambda e, index=index: alternar_linha_expandida(index)
                        )),
                        ft.DataCell(ft.GestureDetector(
                            content=ft.Container(ft.Text(item.codigo_unidade, no_wrap=False), width=150, height=altura_celula),
                            on_tap=lambda e, index=index: alternar_linha_expandida(index)
                        )),
                        ft.DataCell(ft.GestureDetector(
                            content=ft.Container(ft.Text(item.unidade_orcamentaria, no_wrap=False), width=200, height=altura_celula),
                            on_tap=lambda e, index=index: alternar_linha_expandida(index)
                        )),
                    ]
                )
            )

        tabela_dados.update()

    # Título do aplicativo
    page.title = "Consulta de bens patrimoniais"

    # Checkboxes para seleção exclusiva
    checkbox_placa = ft.Checkbox(label="Placa Patrimonial", value=False, on_change=checkbox_changed)
    checkbox_unidade = ft.Checkbox(label="Unidade Orçamentária", value=False, on_change=checkbox_changed)

    # Campo de entrada para código
    input_codigo = ft.TextField(label="Digite o código (1-6 dígitos)", width=300)

    # Botão de busca
    botao_busca = ft.ElevatedButton("Buscar", on_click=buscar_dados)

    # Tabela de dados
    tabela_dados = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Placa patrimonial")),
            ft.DataColumn(ft.Text("Descrição do item")),
            ft.DataColumn(ft.Text("Código da unidade")),
            ft.DataColumn(ft.Text("Unidade orçamentária")),
        ],
        rows=[],
    )

    # Botão de voltar
    botao_voltar = ft.ElevatedButton("Voltar", on_click=lambda e: page.go("/"))

    # Layout da página
    page.add(
        ft.Text("Consulta de bens patrimoniais", size=30, weight="bold"),
        checkbox_placa,
        checkbox_unidade,
        input_codigo,
        botao_busca,
        tabela_dados,
        botao_voltar
    )
