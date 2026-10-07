import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
random.seed(42)
#====================================================
#CONFIGURAÇÕES
#====================================================
QUANTIDADE_CLIENTES = 150
PERCENTUAL_CLIENTES_RECORRENTES = 0.70
PROBABILIDADE_RECOMPRA_REGULAR = 0.85
PROBABILIDADE_RECOMPRA_OCASIONAL = 0.10
DATA_INICIAL = datetime(2026, 1, 1)
DATA_CORTE = datetime(2026, 7, 31)
DATA_INICIO_FUTURO = datetime(2026, 8, 1)
DATA_FIM_FUTURO = datetime(2026, 9, 24)
PRODUTOS = [
    {"nome": "Smartphone", "categoria": "Eletronicos", "preco": 1899.90},
    {"nome": "Notebook", "categoria": "Eletronicos", "preco": 3499.90},
    {"nome": "Fone Bluetooth", "categoria": "Eletronicos", "preco": 199.90},
    {"nome": "Smart TV", "categoria": "Eletronicos", "preco": 2499.90},
    {"nome": "Tênis Esportivo", "categoria": "Esporte", "preco": 299.90},
    {"nome": "Camiseta", "categoria": "Esporte", "preco": 79.90},
    {"nome": "Mochila", "categoria": "Esporte", "preco": 149.90},
    {"nome": "Relógio Smart", "categoria": "Eletronicos", "preco": 399.90},
    {"nome": "Cadeira Gamer", "categoria": "Móveis", "preco": 899.90},
    {"nome": "Teclado Mecânico", "categoria": "Eletronicos", "preco": 299.90},
]
FORMAS_PAGAMENTO=[
    "PIX",
    "Cartão de Crédito",
    "Cartão de Débito",
    "Boleto"
]
ESTADOS =[
    "SP",
    "PR",
    "MG",
    "RJ",
    "SC",
    "RS",
    "GO",
    "BA",
    "PE",
    "ES"
]
#====================================================
#FUNÇÃO PARA GERAR UMA DATA ALEATÓRIA
#====================================================
def gerar_data(data_inicial, data_final):
    dias = (data_final - data_inicial).days
    return data_inicial + timedelta(days=random.randint(0, dias))
#====================================================
# FUNÇÃO PARA GERAR UMA VENDA
#====================================================
def gerar_venda(numero_pedido, id_cliente, data):
    produto = random.choice(PRODUTOS)
    quantidade = random.randint(1, 5)
    preco_unitario = produto["preco"]
    valor_total = quantidade * preco_unitario
    venda = {

        "id_pedido": numero_pedido,
        "data": data.strftime("%Y-%m-%d"),
        "id_cliente": id_cliente,
        "produto": produto["nome"],
        "categoria": produto["categoria"],
        "quantidade": quantidade,
        "preco_unitario": preco_unitario,
        "valor_total": round(valor_total, 2),
        "forma_pagamento": random.choice(FORMAS_PAGAMENTO),
        "estado": random.choice(ESTADOS)
    }

    return venda
# ==========================================
# GERAR DATASET
# ==========================================
def gerar_dataset():
    vendas = []
    clientes = list(range(1, QUANTIDADE_CLIENTES + 1))
    random.shuffle(clientes)
    quantidade_recorrentes = int(
        QUANTIDADE_CLIENTES * PERCENTUAL_CLIENTES_RECORRENTES
    )
    clientes_recorrentes = set(clientes[:quantidade_recorrentes])
    numero_pedido = 1

    for id_cliente in range(1, QUANTIDADE_CLIENTES + 1):
        recorrente = id_cliente in clientes_recorrentes
        quantidade_historica = (
            random.randint(4, 9) if recorrente else random.randint(1, 3)
        )

        for _ in range(quantidade_historica):
            data = gerar_data(DATA_INICIAL, DATA_CORTE)
            vendas.append(gerar_venda(numero_pedido, id_cliente, data))
            numero_pedido += 1

        probabilidade_recompra = (
            PROBABILIDADE_RECOMPRA_REGULAR
            if recorrente
            else PROBABILIDADE_RECOMPRA_OCASIONAL
        )
        if random.random() < probabilidade_recompra:
            quantidade_futura = random.randint(1, 2) if recorrente else 1
            for _ in range(quantidade_futura):
                data = gerar_data(DATA_INICIO_FUTURO, DATA_FIM_FUTURO)
                vendas.append(gerar_venda(numero_pedido, id_cliente, data))
                numero_pedido += 1

    vendas.sort(key=lambda venda: (venda["data"], venda["id_pedido"]))
    for numero_pedido, venda in enumerate(vendas, start=1):
        venda["id_pedido"] = numero_pedido

    return vendas
# ==========================================
# SALVAR CSV
# ==========================================
def salvar_csv(vendas):
    pasta_data = Path(__file__).resolve().parent / "data"
    pasta_data.mkdir(exist_ok=True)
    arquivo = pasta_data / "vendas.csv"
    campos = [
        "id_pedido",
        "data",
        "id_cliente",
        "produto",
        "categoria",
        "quantidade",
        "preco_unitario",
        "valor_total",
        "forma_pagamento",
        "estado"
    ]
    with open(
        arquivo,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as arquivo_csv:
        escritor = csv.DictWriter(
            arquivo_csv,
            fieldnames=campos
        )
        escritor.writeheader()
        escritor.writerows(vendas)
    print("Dataset criado com sucesso!")
    print(f"Arquivo: {arquivo}")
    print(f"Quantidade de vendas: {len(vendas)}")
# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================
if __name__ == "__main__":

    vendas = gerar_dataset()

    salvar_csv(vendas)