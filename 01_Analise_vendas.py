from pathlib import Path
import pandas as pd
caminho = Path(__file__).resolve().parent / "data" / "vendas.csv"
df = pd.read_csv(caminho)
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())
print(df.describe())
print(df["produto"].value_counts())
print(df["categoria"].value_counts())
print(df["estado"].value_counts())
faturamento_total = df["valor_total"].sum()
ticket_medio = df["valor_total"].mean()
print(f"faturamento total: R$ {faturamento_total:,.2f}")
print(f"ticket médio: R$ {ticket_medio:,.2f}")
faturamento_produto = (
    df.groupby("produto")["valor_total"]
    .sum()
    .sort_values(ascending=False)
)
print(faturamento_produto)
quantidade_produto = df.groupby("produto")["quantidade"].sum()
print(quantidade_produto)
faturamento_categoria = (
    df.groupby("categoria")["valor_total"]
    .sum()
    .sort_values(ascending=False)
)
print(faturamento_categoria)
percentual_categoria = (
    faturamento_categoria / faturamento_total*100
)
print(percentual_categoria)
resumo_categoria = pd.DataFrame({
    "faturamento": faturamento_categoria,
    "percentual": percentual_categoria
})
print(resumo_categoria)
resumo_categoria["percentual"] = resumo_categoria["percentual"].round(2)
print(resumo_categoria)
faturamento_estado = (
    df.groupby("estado")["valor_total"]
    .sum()
    .sort_values(ascending=False)
)
print(faturamento_estado)
percentual_estado = (
    faturamento_estado / faturamento_total * 100
)
percentual_estado = percentual_estado.round(2)
print(percentual_estado)
resumo_estado = pd.DataFrame({
    "faturamento": faturamento_estado,
    "percentual": percentual_estado
})
print(resumo_estado)
pedidos_estado = df.groupby("estado")["id_pedido"].count()
print(pedidos_estado)
ticket_medio_estado = (
    faturamento_estado / pedidos_estado
).round(2)
print(ticket_medio_estado)
resumo_estado = pd.DataFrame({
    "pedidos": pedidos_estado,
    "faturamento": faturamento_estado,
    "ticket_medio": ticket_medio_estado,
    "percentual": percentual_estado
})
print(resumo_estado)
resumo_estado = resumo_estado.sort_values(
    "faturamento",
    ascending=False
)
print(resumo_estado)
pedidos_pagamento = df["forma_pagamento"].value_counts()
print(pedidos_pagamento)
faturamento_pagamento = (
    df.groupby("forma_pagamento")["valor_total"]
    .sum()
    .sort_values(ascending=False)
)
print(faturamento_pagamento)
ticket_medio_pagamento = (
    faturamento_pagamento / pedidos_pagamento
).round(2)
print(ticket_medio_pagamento)
resumo_pagamento = pd.DataFrame({
    "pedidos": pedidos_pagamento,
    "faturamento": faturamento_pagamento,
    "ticket_medio": ticket_medio_pagamento
})
print(resumo_pagamento)
df["data"] = pd.to_datetime(df["data"])
print(df.info())
df["mes"] = df["data"].dt.month
print(df[["data", "mes"]].head(10))
faturamento_mes = (
    df.groupby("mes")["valor_total"]
    .sum()
)
print(faturamento_mes)
pedidos_mes = df.groupby("mes")["id_pedido"].count()
print(pedidos_mes)
ticket_medio_mes = (
    faturamento_mes / pedidos_mes
).round(2)
print(ticket_medio_mes)
resumo_mes = pd.DataFrame({
    "pedidos": pedidos_mes,
    "faturamento": faturamento_mes,
    "ticket_medio": ticket_medio_mes
})
print(resumo_mes)
faturamento_mes_produto =(
    df.groupby(["mes", "produto"])["valor_total"]
    .sum()
)
print(faturamento_mes_produto)
faturamento_mes_produto = (
    df.groupby(["mes", "produto"])["valor_total"]
    .sum()
)
tabela_mes_produto = faturamento_mes_produto.unstack()
print(tabela_mes_produto)
produto_maior_mes = tabela_mes_produto.idxmax(axis=1)
print(produto_maior_mes)
resumo_mes["produto_lider"] = produto_maior_mes
print(resumo_mes)
import matplotlib.pyplot as plt
plt.plot(
    resumo_mes.index,
    resumo_mes["faturamento"],
    marker="o"
)
plt.title("Evolução do faturamento mensal")
plt.xlabel("Mês")
plt.ylabel("Faturamento (R$)")
for mes, valor in zip(resumo_mes.index, resumo_mes["faturamento"]):
    plt.text(mes, valor, f"R$ {valor:,.2f}", ha="center", va="bottom")
plt.show()
plt.figure()
plt.bar(
    faturamento_categoria.index,
    faturamento_categoria.values
)
plt.title("Faturamento por categoria")
plt.xlabel("Categoria")
plt.ylabel("Faturamento (R$)")
plt.show()
plt.figure()
plt.bar(
    faturamento_estado.index,
    faturamento_estado.values
)
plt.title("Faturamento por estado")
plt.xlabel("Estado")
plt.ylabel("Faturamento (R$)")
plt.show()
print("\nResumo por estado:")
print(resumo_estado)
plt.figure()
plt.bar(
    faturamento_produto.index,
    faturamento_produto.values
)
plt.title("Faturamento por produto")
plt.xlabel("Produto")
plt.ylabel("Faturamento (R$)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
faturamento_por_unidade = (
    faturamento_produto / quantidade_produto
).sort_values(ascending=False)
print("\nFaturamento por unidade:")
print(faturamento_por_unidade)
print("\nResumo por estado:")
print(resumo_estado)
faturamento_por_unidade = (
    faturamento_produto / quantidade_produto
).sort_values(ascending=False)
print("\nFaturamento por unidade:")
print(faturamento_por_unidade)
pedidos_produto = df.groupby("produto")["id_pedido"].count()
resumo_produto = pd.DataFrame({
    "pedidos": pedidos_produto,
    "unidades": quantidade_produto,
    "faturamento": faturamento_produto,
    "preco_unitario": faturamento_por_unidade
})
resumo_produto = resumo_produto.sort_values(
    "faturamento",
    ascending=False
)
print("\nResumo por produto:")
print(resumo_produto)
pedidos_produto = df.groupby("produto")["id_pedido"].count()
resumo_produto = pd.DataFrame({
    "pedidos": pedidos_produto,
    "unidades":quantidade_produto,
    "faturamento": faturamento_produto,
    "preco_unitario": faturamento_por_unidade
})
resumo_produto = resumo_produto.sort_values(
    "faturamento",
    ascending=False
)
print("\nResumo por produto:")
print(resumo_produto)
percentual_produto = (
    faturamento_produto / faturamento_total * 100
).round(2)
resumo_produto["percentual_faturamento"] = percentual_produto
print("\nResumo por produto:")
print(resumo_produto)
resumo_produto["percentual_acumulado"] = (
    resumo_produto["percentual_faturamento"].cumsum()
)
print("\nResumo por produto:")
print(resumo_produto)
import matplotlib.pyplot as plt
fig, ax1 = plt.subplots()

ax1.bar(
    resumo_produto.index,
    resumo_produto["percentual_faturamento"]
)
ax1.set_title("Pareto do Faturamento por Produto")
ax1.set_xlabel("Produto")
ax1.set_ylabel("% do faturamento")
ax1.tick_params(axis="x", rotation=45)
ax2 = ax1.twinx()
ax2.plot(
    resumo_produto.index,
    resumo_produto["percentual_acumulado"],
    marker="o"
)
ax2.set_ylabel("% acumulado")
ax2.axhline(80, linestyle="--")
plt.tight_layout()
plt.show()
clientes_unicos = df["id_cliente"].nunique()
print("\nQuantidade de clientes únicos:")
print(clientes_unicos)
pedidos_por_cliente = df.groupby("id_cliente")["id_pedido"].count()
media_pedidos_cliente = pedidos_por_cliente.mean()
print("\nMédia de pedidos por cliente:")
print(round(media_pedidos_cliente, 2))
faturamento_cliente = (
    df.groupby("id_cliente")["valor_total"]
    .sum()
    .sort_values(ascending=False)
)
print("\nFaturamento por cliente:")
print(faturamento_cliente.head(10))
ticket_medio_cliente = (
    faturamento_cliente / pedidos_por_cliente
).sort_values(ascending=False)
print("\nTicket médio por cliente:")
print(ticket_medio_cliente.head(10))
resumo_cliente = pd.DataFrame({
    "pedidos": pedidos_por_cliente,
    "faturamento": faturamento_cliente,
    "ticket_medio": ticket_medio_cliente
})
resumo_cliente = resumo_cliente.sort_values(
    "faturamento",
    ascending=False
)
print("\nResumo por cliente:")
print(resumo_cliente.head(10))
clientes_recorrentes = (pedidos_por_cliente > 1).sum()
clientes_uma_compra = (pedidos_por_cliente == 1).sum()
print("\nClientes recorrentes:")
print(clientes_recorrentes)
print("\nClientes com apenas uma compra:")
print(clientes_uma_compra)
taxa_recorrencia = (
    clientes_recorrentes / clientes_unicos * 100
)
print("\nTaxa de recorrência:")
print(round(taxa_recorrencia, 2), "%")
#Distribuição de clientes por quantidade de pedidos
pedidos_por_cliente = (
    df.groupby("id_cliente")["id_pedido"]
    .count()
)
distribuicao_pedidos = (
    pedidos_por_cliente
    .value_counts()
    .sort_index()
)
distribuicao_pedidos.index.name = "quantidade_pedidos"
print("\nDistribuição de clientes por quantidade de pedidos:")
print(distribuicao_pedidos)
plt.figure()
plt.bar(
    distribuicao_pedidos.index,
    distribuicao_pedidos.values
)
plt.title("Distribuição de clientes por quantidade de pedidos")
plt.xlabel("Quantidade de pedidos")
plt.ylabel("Quantidade de clientes")
plt.xticks(distribuicao_pedidos.index)
plt.show()
percentual_distribuicao = (
    distribuicao_pedidos / clientes_unicos * 100
).round(2)
print("\nPercentual de clientes por quantidade de pedidos")
print(percentual_distribuicao)
# Seguimentação de clientes por frequência de compra
def classificar_cliente(pedidos):
    if pedidos == 1:
        return "Ocasional"
    elif pedidos <= 3:
        return "Recorrente"
    else:
        return "Frequente"
segmentacao_clientes = pedidos_por_cliente.apply(classificar_cliente)
segmentacao_clientes.name = "segmento"
print ("\nSegmentação dos clientes:")
print(segmentacao_clientes.value_counts())
# Faturamento por segmento de clientes
faturamento_por_segmento = (
    df.groupby("id_cliente")["valor_total"]
    .sum()
    .groupby(segmentacao_clientes)
    .sum()
    .sort_values(ascending=False)
)
print("\nFaturamento por segmento:")
print(faturamento_por_segmento)
# Percentual de faturamento por segmento
percentual_faturamento_segmento = (
    faturamento_por_segmento / faturamento_total * 100
).round(2)
print("\nPercentual do faturamento por segmento:")
print(percentual_faturamento_segmento)
# Resumo consolidado por segmento
clientes_por_segmento = segmentacao_clientes.value_counts()
percentual_clientes_segmento = (
    clientes_por_segmento / clientes_unicos * 100
).round(2)
pedidos_por_segmento = (
    pedidos_por_cliente
    .groupby(segmentacao_clientes)
    .sum()
)
ticket_medio_segmento = (
    faturamento_por_segmento / pedidos_por_segmento
).round(2)
resumo_segmento = pd.DataFrame({
    "clientes": clientes_por_segmento,
    "percentual_clientes": percentual_clientes_segmento,
    "pedidos": pedidos_por_segmento,
    "faturamento": faturamento_por_segmento,
    "percentual_faturamento": percentual_faturamento_segmento,
    "ticket_medio": ticket_medio_segmento
})
print("\nResumo consolidado por segmento:")
print(resumo_segmento)
# Gráfico: participação de clientes x participação do faturamento
plt.figure()
x = range(len(resumo_segmento))
plt.bar(
    [i - 0.2 for i in x],
    resumo_segmento["percentual_clientes"],
    width=0.4,
    label="% Clientes"
)
plt.bar(
    [i + 0.2 for i in x],
    resumo_segmento["percentual_faturamento"],
    width=0.4,
    label="% Faturamento"
)
plt.xticks(x, resumo_segmento.index)
plt.ylabel("Percentual (%)")
plt.title("Participação de Clientes x Faturamento por Segmento")
plt.legend()
plt.tight_layout()
plt.show()
# Análise de recência dos clientes
ultima_compra_cliente = (
    df.groupby("id_cliente")["data"]
    .max()
)
data_referencia = df["data"].max()
recencia_cliente = (
    data_referencia - ultima_compra_cliente
).dt.days
resumo_recencia = pd.DataFrame({
    "ultima_compra": ultima_compra_cliente,
    "dias_sem_comprar": recencia_cliente
})
print("\nData de referência:")
print(data_referencia)
print("\nRecência dos clientes:")
print(resumo_recencia.head(10))
# Estatísticas da recência dos clientes
print("\nEstatísticas de recência:")
print(recencia_cliente.describe())
print("\nMediana da recência:")
print(recencia_cliente.median())
print("\nQuantis da recência:")
print(recencia_cliente.quantile([0.25, 0.50, 0.75, 0.90]))
# Pontuação de recência para RFM
recencia_score = pd.qcut(
    recencia_cliente,
    q=4,
    labels=[4, 3, 2, 1]
)
print("\nPontuação de recência:")
print(recencia_score.value_counts().sort_index())
# Resumo da pontuação de recência
resumo_recencia = pd.DataFrame({
    "dias_sem_comprar": recencia_cliente,
    "score_recencia": recencia_score
})
print("\nResumo da recência:")
print(resumo_recencia.head(10))
# Pontuação de frequência para RFM
frequencia_score = pd.qcut(
    pedidos_por_cliente,
    q=4,
    labels=[1, 2, 3, 4]
)
print("\nPontuação de frequência:")
print(frequencia_score.value_counts().sort_index())
# Resumo da frequência
resumo_frequencia = pd.DataFrame({
    "pedidos": pedidos_por_cliente,
    "score_frequencia": frequencia_score
})
print("\nResumo da frequência:")
print(resumo_frequencia.head(10))
# Pontuação monetária para RFM
monetario_score = pd.qcut(
    faturamento_cliente,
    q=4,
    labels=[1, 2, 3, 4]
)
print("\nPontuação monetária:")
print(monetario_score.value_counts().sort_index())
# Resumo do valor monetário
resumo_monetario = pd.DataFrame({
    "faturamento": faturamento_cliente,
    "score_monetario": monetario_score
})
print("\nResumo monetário:")
print(resumo_monetario.head(10))
# Consolidando a análise RFM
resumo_rfm = pd.DataFrame({
    "recencia_dias": recencia_cliente,
    "frequencia_pedidos": pedidos_por_cliente,
    "faturamento": faturamento_cliente,
    "score_recencia": recencia_score.astype(int),
    "score_frequencia": frequencia_score.astype(int),
    "score_monetario": monetario_score.astype(int)
})
# Criando o código RFM
resumo_rfm["score_rfm"] = (
    resumo_rfm["score_recencia"].astype(str)
    + resumo_rfm["score_frequencia"].astype(str)
    + resumo_rfm["score_monetario"].astype(str)
)
# Criando uma pontuação numérica total
resumo_rfm["score_total"] = (
    resumo_rfm["score_recencia"]
    + resumo_rfm["score_frequencia"]
    + resumo_rfm["score_monetario"]
)
print("\nResumo RFM:")
print(resumo_rfm.head(10))
# Distribuição da pontuação RFM
distribuicao_rfm = (
    resumo_rfm["score_total"]
    .value_counts()
    .sort_index()
)
print("\nDistribuição do score total RFM:")
print(distribuicao_rfm)
print("\nEstatísticas do score total RFM:")
print(resumo_rfm["score_total"].describe())
print("\nMediana do score total RFM:")
print(resumo_rfm["score_total"].median())
# Segmentação final do score RFM
def classificar_rfm(score):
    if score <= 5:
        return "RFM Baixo"
    elif score <= 7:
        return "RFM Intermediário"
    elif score <= 9:
        return "RFM Alto"
    else:
        return "RFM Muito Alto"
resumo_rfm["segmento_rfm"] = (
    resumo_rfm["score_total"].apply(classificar_rfm)
)
print("\nSegmentação RFM:")
print(resumo_rfm["segmento_rfm"].value_counts())
# Resumo financeiro por segmento RFM
resumo_segmento_rfm = (
    resumo_rfm
    .groupby("segmento_rfm")
    .agg(
        clientes=("score_total", "count"),
        pedidos=("frequencia_pedidos", "sum"),
        faturamento=("faturamento", "sum"),
        ticket_medio=("faturamento", "mean")
    )
)
resumo_segmento_rfm["percentual_clientes"] = (
    resumo_segmento_rfm["clientes"] / clientes_unicos * 100
).round(2)
resumo_segmento_rfm["percentual_faturamento"] = (
    resumo_segmento_rfm["faturamento"] / faturamento_total * 100
).round(2)
print("\nResumo dos segmentos RFM:")
print(resumo_segmento_rfm)
# Produtos mais comprados por segmento RFM
dados_rfm_produto = df.merge(
    resumo_rfm[["segmento_rfm"]],
    left_on="id_cliente",
    right_index=True
)
produtos_por_segmento = (
    dados_rfm_produto
    .groupby(["segmento_rfm", "produto"])["quantidade"]
    .sum()
    .sort_values(ascending=False)
)
print("\nQuantidade de produtos vendidos por segmento RFM:")
print(produtos_por_segmento)
# Produto mais comprado em cada segmento RFM
produto_lider_segmento = (
    dados_rfm_produto
    .groupby(["segmento_rfm", "produto"])["quantidade"]
    .sum()
    .reset_index()
    .sort_values(
        ["segmento_rfm", "quantidade"],
        ascending=[True, False]
    )
    .groupby("segmento_rfm")
    .head(1)
)
print("\nProduto líder por segmento RFM:")
print(produto_lider_segmento)
# Categorias mais compradas por segmento RFM
categorias_por_segmento = (
    dados_rfm_produto
    .groupby(["segmento_rfm", "categoria"])["quantidade"]
    .sum()
    .sort_values(ascending=False)
)
print("\nQuantidade de produtos vendidos por categoria e segmento RFM:")
print(categorias_por_segmento)
# Categoria líder por segmento RFM
categoria_lider_segmento = (
    dados_rfm_produto
    .groupby(["segmento_rfm", "categoria"])["quantidade"]
    .sum()
    .reset_index()
    .sort_values(
        ["segmento_rfm", "quantidade"],
        ascending=[True, False]
    )
    .groupby("segmento_rfm")
    .head(1)
)
print("\nCategoria líder por segmento RFM:")
print(categoria_lider_segmento)
# Participação percentual das categorias dentro de cada segmento RFM
quantidade_categoria_segmento = (
    dados_rfm_produto
    .groupby(["segmento_rfm", "categoria"])["quantidade"]
    .sum()
)
percentual_categoria_segmento = (
    quantidade_categoria_segmento
    .groupby(level=0)
    .transform(lambda x: x / x.sum() * 100)
    .round(2)
)
print("\nPercentual de categorias dentro de cada segmento RFM:")
print(percentual_categoria_segmento)
# Tabela de participação por categoria e segmento
tabela_categoria_rfm = (
    percentual_categoria_segmento
    .unstack()
)
print("\nTabela de participação das categorias por segmento RFM:")
print(tabela_categoria_rfm)
# Faturamento por categoria dentro de cada segmento RFM
faturamento_categoria_segmento = (
    dados_rfm_produto
    .groupby(["segmento_rfm", "categoria"])["valor_total"]
    .sum()
)
percentual_faturamento_categoria = (
    faturamento_categoria_segmento
    .groupby(level=0)
    .transform(lambda x: x / x.sum() * 100)
    .round(2)
)
print("\nPercentual de faturamento por categoria dentro de cada segmento RFM:")
print(percentual_faturamento_categoria)
# Tabela de faturamento por categoria e segmento RFM
tabela_faturamento_categoria_rfm = (
    percentual_faturamento_categoria
    .unstack()
)
print("\nTabela de faturamento por categoria e segmento RFM:")
print(tabela_faturamento_categoria_rfm)
# Faturamento absoluto por categoria e segmento RFM
tabela_valor_categoria_rfm = (
    dados_rfm_produto
    .groupby(["segmento_rfm", "categoria"])["valor_total"]
    .sum()
    .unstack(fill_value=0)
)
print("\nFaturamento por categoria e segmento RFM (R$):")
print(tabela_valor_categoria_rfm.round(2))
# Categoria com maior faturamento em cada segmento RFM
categoria_maior_faturamento = (
    tabela_valor_categoria_rfm.idxmax(axis=1)
)
valor_maior_faturamento = (
    tabela_valor_categoria_rfm.max(axis=1)
)
resultado_categoria_rfm = pd.DataFrame({
    "categoria": categoria_maior_faturamento,
    "faturamento": valor_maior_faturamento
})
print("\nCategoria com maior faturamento por segmento RFM:")
print(resultado_categoria_rfm.round(2))
# Faturamento por produto dentro de cada segmento RFM
faturamento_produto_rfm = (
    dados_rfm_produto
    .groupby(["segmento_rfm", "produto"])["valor_total"]
    .sum()
    .sort_values(ascending=False)
)
print("\nFaturamento por produto e segmento RFM:")
print(faturamento_produto_rfm)
# Top 3 produtos por faturamento em cada segmento RFM
top3_produtos_rfm = (
    dados_rfm_produto
    .groupby(["segmento_rfm", "produto"])["valor_total"]
    .sum()
    .reset_index()
    .sort_values(
        ["segmento_rfm", "valor_total"],
        ascending=[True, False]
    )
    .groupby("segmento_rfm")
    .head(3)
)
print("\nTop 3 produtos por faturamento em cada segmento RFM:")
print(top3_produtos_rfm)
# Participação do Top 3 produtos no faturamento de cada segmento RFM
faturamento_top3 = (
    top3_produtos_rfm
    .groupby("segmento_rfm")["valor_total"]
    .sum()
)
faturamento_segmento = (
    resumo_rfm
    .groupby("segmento_rfm")["faturamento"]
    .sum()
)
percentual_top3 = (
    faturamento_top3 / faturamento_segmento * 100
).round(2)
print("\nParticipação do Top 3 no faturamento de cada segmento:")
print(percentual_top3)
# Resumo da concentração de faturamento
resumo_concentracao = pd.DataFrame({
    "faturamento_segmento": faturamento_segmento,
    "faturamento_top3": faturamento_top3,
    "percentual_top3": percentual_top3
})
print("\nResumo da concentração por segmento:")
print(resumo_concentracao)
# Participação do RFM Muito Alto no faturamento total
faturamento_rfm_muito_alto = (
    resumo_segmento_rfm.loc["RFM Muito Alto", "faturamento"]
)
percentual_rfm_muito_alto = (
    faturamento_rfm_muito_alto / faturamento_total * 100
)
print("\nParticipação do RFM Muito Alto no faturamento total:")
print(round(percentual_rfm_muito_alto, 2), "%")
# ==========================================
# KPIs PRINCIPAIS DO PROJETO
# ==========================================
kpis = {
    "Faturamento total": faturamento_total,
    "Ticket médio": ticket_medio,
    "Clientes únicos": clientes_unicos,
    "Média de pedidos por cliente": media_pedidos_cliente,
    "Taxa de recorrência (%)": taxa_recorrencia,
    "Faturamento RFM Muito Alto": faturamento_rfm_muito_alto,
    "Participação RFM Muito Alto (%)": percentual_rfm_muito_alto,
}
painel_kpis = pd.Series(kpis)
print("\n==========================================")
print("           PAINEL DE KPIs")
print("==========================================")
print(painel_kpis)
print("\nKPIs formatados:")
print(f"Faturamento total: R$ {faturamento_total:,.2f}")
print(f"Ticket médio: R$ {ticket_medio:,.2f}")
print(f"Clientes únicos: {clientes_unicos}")
print(f"Média de pedidos por cliente: {media_pedidos_cliente:.2f}")
print(f"Taxa de recorrência: {taxa_recorrencia:.2f}%")
print(f"Faturamento RFM Muito Alto: R$ {faturamento_rfm_muito_alto:,.2f}")
print(f"Participação RFM Muito Alto: {percentual_rfm_muito_alto:.2f}%")
# ==========================================
# GRÁFICO - FATURAMENTO POR SEGMENTO RFM
# ==========================================
plt.figure()
plt.bar(
    resumo_segmento_rfm.index,
    resumo_segmento_rfm["faturamento"]
)
plt.title("Faturamento por Segmento RFM")
plt.xlabel("Segmento RFM")
plt.ylabel("Faturamento (R$)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()
# ==========================================
# GRÁFICO - FATURAMENTO POR SEGMENTO RFM
# ==========================================
plt.figure()
plt.bar(
    resumo_segmento_rfm.index,
    resumo_segmento_rfm["faturamento"]
)
plt.title("Faturamento por Segmento RFM")
plt.xlabel("Segmento RFM")
plt.ylabel("Faturamento (R$)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()
# ==========================================
# GRÁFICO - CLIENTES X FATURAMENTO POR RFM
# ==========================================
plt.figure()
x = range(len(resumo_segmento_rfm))
plt.bar(
    [i - 0.2 for i in x],
    resumo_segmento_rfm["percentual_clientes"],
    width=0.4,
    label="% Clientes"
)
plt.bar(
    [i + 0.2 for i in x],
    resumo_segmento_rfm["percentual_faturamento"],
    width=0.4,
    label="% Faturamento"
)
plt.xticks(x, resumo_segmento_rfm.index, rotation=20)
plt.xlabel("Segmento RFM")
plt.ylabel("Percentual (%)")
plt.title("Participação de Clientes x Faturamento por Segmento RFM")
plt.legend()
plt.tight_layout()
plt.show()
# ==========================================
# CLIENTES X FATURAMENTO POR SEGMENTO RFM
# ==========================================
plt.figure()
x = range(len(resumo_segmento_rfm))
plt.bar(
    [i - 0.2 for i in x],
    resumo_segmento_rfm["percentual_clientes"],
    width=0.4,
    label="% Clientes"
)
plt.bar(
    [i + 0.2 for i in x],
    resumo_segmento_rfm["percentual_faturamento"],
    width=0.4,
    label="% Faturamento"
)
plt.xticks(
    x,
    resumo_segmento_rfm.index,
    rotation=20
)
plt.xlabel("Segmento RFM")
plt.ylabel("Percentual (%)")
plt.title("Participação de Clientes x Faturamento por Segmento RFM")
plt.legend()
plt.tight_layout()
plt.show()
# ==========================================
# GRÁFICO - FATURAMENTO POR SEGMENTO RFM
# ==========================================
plt.figure()

plt.bar(
    resumo_segmento_rfm.index,
    resumo_segmento_rfm["faturamento"]
)
plt.title("Faturamento por Segmento RFM")
plt.xlabel("Segmento RFM")
plt.ylabel("Faturamento (R$)")
plt.xticks(rotation=20)
plt.tight_layout()
plt.show()
# ==========================================
# GRÁFICO - CLIENTES X FATURAMENTO POR RFM
# ==========================================
ordem_rfm = [
    "RFM Baixo",
    "RFM Intermediário",
    "RFM Alto",
    "RFM Muito Alto"
]
dados_grafico_rfm = resumo_segmento_rfm.reindex(ordem_rfm)
plt.figure()
x = range(len(dados_grafico_rfm))
plt.bar(
    [i - 0.2 for i in x],
    dados_grafico_rfm["percentual_clientes"],
    width=0.4,
    label="% Clientes"
)
plt.bar(
    [i + 0.2 for i in x],
    dados_grafico_rfm["percentual_faturamento"],
    width=0.4,
    label="% Faturamento"
)
plt.xticks(
    x,
    dados_grafico_rfm.index,
    rotation=20
)
plt.xlabel("Segmento RFM")
plt.ylabel("Percentual (%)")
plt.title("Participação de Clientes x Faturamento por Segmento RFM")
plt.legend()
plt.tight_layout()
plt.show()
# ==========================================
# GRÁFICO - FATURAMENTO POR CATEGORIA E RFM
# ==========================================
ordem_rfm = [
    "RFM Baixo",
    "RFM Intermediário",
    "RFM Alto",
    "RFM Muito Alto"
]
dados_categoria_rfm = (
    tabela_valor_categoria_rfm
    .reindex(ordem_rfm)
)
ax = dados_categoria_rfm.plot(
    kind="bar",
    figsize=(10, 6)
)
plt.title("Faturamento por Categoria e Segmento RFM")
plt.xlabel("Segmento RFM")
plt.ylabel("Faturamento (R$)")
plt.xticks(rotation=20)
plt.legend(title="Categoria")
plt.tight_layout()
plt.show()
# ==========================================
# DASHBOARD - FATURAMENTO MENSAL
# ==========================================
plt.figure(figsize=(10, 6))
meses = resumo_mes.index
faturamento = resumo_mes["faturamento"]
plt.plot(
    meses,
    faturamento,
    marker="o"
)
plt.title("Evolução do Faturamento Mensal")
plt.xlabel("Mês")
plt.ylabel("Faturamento (R$)")
plt.xticks(meses)
# Valores sobre os pontos
for mes, valor in zip(meses, faturamento):
    plt.text(
        mes,
        valor,
        f"R$ {valor:,.0f}",
        ha="center",
        va="bottom"
    )
plt.grid(axis="y")
plt.tight_layout()
plt.show()
# ==========================================
# GRÁFICO - CLIENTES X FATURAMENTO POR RFM
# ==========================================
ordem_rfm = [
    "RFM Baixo",
    "RFM Intermediário",
    "RFM Alto",
    "RFM Muito Alto"
]
dados_grafico_rfm = resumo_segmento_rfm.reindex(ordem_rfm)
plt.figure(figsize=(10, 6))
x = range(len(dados_grafico_rfm))
barras_clientes = plt.bar(
    [i - 0.2 for i in x],
    dados_grafico_rfm["percentual_clientes"],
    width=0.4,
    label="% Clientes"
)
barras_faturamento = plt.bar(
    [i + 0.2 for i in x],
    dados_grafico_rfm["percentual_faturamento"],
    width=0.4,
    label="% Faturamento"
)
plt.xticks(
    x,
    dados_grafico_rfm.index,
    rotation=20
)
plt.xlabel("Segmento RFM")
plt.ylabel("Percentual (%)")
plt.title("Participação de Clientes x Faturamento por Segmento RFM")
for barra in barras_clientes:
    altura = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura,
        f"{altura:.2f}%",
        ha="center",
        va="bottom"
    )
for barra in barras_faturamento:
    altura = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura,
        f"{altura:.2f}%",
        ha="center",
        va="bottom"
    )
plt.legend()
plt.tight_layout()
plt.show()
# ==========================================
# GRÁFICO - FATURAMENTO POR PRODUTO
# ==========================================
faturamento_produto_grafico = (
    df.groupby("produto")["valor_total"]
    .sum()
    .sort_values(ascending=True)
)
plt.figure(figsize=(10, 6))
plt.barh(
    faturamento_produto_grafico.index,
    faturamento_produto_grafico.values
)
plt.title("Faturamento por Produto")
plt.xlabel("Faturamento (R$)")
plt.ylabel("Produto")
plt.tight_layout()
plt.show()
# ==========================================
# GRÁFICO - EVOLUÇÃO DO FATURAMENTO MENSAL
# ==========================================
plt.figure(figsize=(10, 6))
plt.plot(
    resumo_mes.index,
    resumo_mes["faturamento"],
    marker="o"
)
plt.title("Evolução do Faturamento Mensal")
plt.xlabel("Mês")
plt.ylabel("Faturamento (R$)")
nomes_meses = [
    "Jan", "Fev", "Mar", "Abr", "Mai",
    "Jun", "Jul", "Ago", "Set"
]
plt.xticks(
    resumo_mes.index,
    nomes_meses
)
for mes, valor in zip(
    resumo_mes.index,
    resumo_mes["faturamento"]
):
    plt.text(
        mes,
        valor,
        f"{valor:,.0f}",
        ha="center",
        va="bottom"
    )
plt.grid(axis="y")
plt.tight_layout()
plt.show()
# ==========================================
# GRÁFICO - FATURAMENTO POR CATEGORIA
# ==========================================
faturamento_categoria_grafico = (
    df.groupby("categoria")["valor_total"]
    .sum()
    .sort_values(ascending=True)
)
plt.figure(figsize=(10, 6))
barras = plt.barh(
    faturamento_categoria_grafico.index,
    faturamento_categoria_grafico.values
)
plt.title("Faturamento por Categoria")
plt.xlabel("Faturamento (R$)")
plt.ylabel("Categoria")
# Valores nas barras
for barra in barras:
    valor = barra.get_width()
    plt.text(
        valor,
        barra.get_y() + barra.get_height() / 2,
        f"R$ {valor:,.2f}",
        va="center",
        ha="left"
    )
# Remove a notação científica do eixo
plt.ticklabel_format(
    style="plain",
    axis="x"
)
plt.tight_layout()
plt.show()