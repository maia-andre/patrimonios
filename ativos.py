import flet as ft
import pandas as pd
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

# Função para importar dados de um arquivo CSV
def importar_csv_para_banco(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path, encoding='ISO-8859-1', delimiter=';')
        registros_importados = 0
        for index, row in df.iterrows():
            try:
                # Verifica se a placa patrimonial é válida (1 a 6 dígitos)
                placa = str(row['placa_patrimonial'])
                if not placa.isdigit() or not (1 <= len(placa) <= 6):
                    print(f"Registro {index} tem placa patrimonial inválida: {row['placa_patrimonial']}")
                    continue  # Pula para o próximo registro

                # Verifica se o código_unidade é válido (1 a 6 dígitos)
                codigo_unidade = str(row['codigo_unidade'])
                if not codigo_unidade.isdigit() or not (1 <= len(codigo_unidade) <= 6):
                    print(f"Registro {index} tem código_unidade inválido: {row['codigo_unidade']}")
                    continue  # Pula para o próximo registro

                # Cria o objeto BemPatrimonial com os dados válidos
                bem = BemPatrimonial(
                    placa_patrimonial=placa,
                    descricao=row['descricao'],
                    codigo_unidade=codigo_unidade,
                    unidade_orcamentaria=row['unidade_orcamentaria']
                )
                session.add(bem)
                registros_importados += 1
            except Exception as e:
                print(f"Erro ao importar registro {index}: {e}")
        session.commit()
        print(f"{registros_importados} registros importados com sucesso!")
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")

# Importar dados do CSV (chame essa função com o caminho do arquivo CSV)
importar_csv_para_banco("ativos_outubro.csv")

def main(page: ft.Page):
    # Função para garantir que apenas um checkbox seja selecionado
    def checkbox_changed(e):
        if e.control == checkbox_placa and checkbox_placa.value:
            checkbox_unidade.value = False
        elif e.control == checkbox_unidade and checkbox_unidade.value:
            checkbox_placa.value = False
        checkbox_placa.update()
        checkbox_unidade.update()

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
        for item in resultados:
            tabela_dados.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item.placa_patrimonial)),
                        ft.DataCell(ft.Text(item.descricao)),
                        ft.DataCell(ft.Text(item.codigo_unidade)),
                        ft.DataCell(ft.Text(item.unidade_orcamentaria)),
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

    # Layout da página
    page.add(
        ft.Text("Consulta de bens patrimoniais", size=30, weight="bold"),
        checkbox_placa,
        checkbox_unidade,
        input_codigo,
        botao_busca,
        tabela_dados,
    )

# Executar o app
ft.app(target=main)
