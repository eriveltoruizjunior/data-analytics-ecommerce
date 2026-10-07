# ==========================================
# DASHBOARD EXECUTIVO DE VENDAS
# ==========================================
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
plt.ioff()
# ==========================================
# 1. CARREGAMENTO DOS DADOS
# ==========================================
caminho = Path(__file__).resolve().parent / "data" / "vendas.csv"
df = pd.read_csv(caminho)
df["data"] = pd.to_datetime(df["data"])
print("Dados carregados com sucesso!")
print(f"Quantidade de registros: {len(df)}")
print(f"Quantidade de colunas: {len(df.columns)}")
print("\nPrimeiras linhas:")
print(df.head())
# ==========================================
# 2. KPIs PRINCIPAIS
# ==========================================
faturamento_total = df["valor_total"].sum()
ticket_medio = df["valor_total"].mean()
clientes_unicos = df["id_cliente"].nunique()
pedidos_por_cliente = df.groupby("id_cliente")["id_pedido"].count()
media_pedidos_cliente = pedidos_por_cliente.mean()
clientes_recorrentes = (pedidos_por_cliente > 1).sum()
taxa_recorrencia = clientes_recorrentes / clientes_unicos * 100
print("\n==========================================")
print("           KPIs PRINCIPAIS")
print("==========================================")
print(f"Faturamento total: R$ {faturamento_total:,.2f}")
print(f"Ticket médio: R$ {ticket_medio:,.2f}")
print(f"Clientes únicos: {clientes_unicos}")
print(f"Média de pedidos por cliente: {media_pedidos_cliente:.2f}")
print(f"Taxa de recorrência: {taxa_recorrencia:.2f}%")
# ==========================================
# 3. ANÁLISE MENSAL
# ==========================================
resumo_mes = (
    df.assign(mes=df["data"].dt.month)
    .groupby("mes")["valor_total"]
    .sum()
)
meses = [
    "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
    "Jul", "Ago", "Set", "Out", "Nov", "Dez"
]
mes_maior = resumo_mes.idxmax()
faturamento_mes_maior = resumo_mes.max()
nome_mes_maior = meses[mes_maior - 1]
# ==========================================
# 4. ANÁLISE POR PRODUTO
# ==========================================
resumo_produto = (
    df.groupby("produto")["valor_total"]
    .sum()
    .sort_values()
)
produto_lider = resumo_produto.idxmax()
faturamento_produto_lider = resumo_produto.max()
percentual_produto_lider = faturamento_produto_lider / faturamento_total * 100
# ==========================================
# 5. ANÁLISE POR CATEGORIA
# ==========================================
resumo_categoria = (
    df.groupby("categoria")["valor_total"]
    .sum()
    .sort_values()
)
categoria_lider = resumo_categoria.idxmax()
faturamento_categoria_lider = resumo_categoria.max()
percentual_categoria_lider = faturamento_categoria_lider / faturamento_total * 100
# ==========================================
# 6. ANÁLISE RFM
# ==========================================
data_referencia = df["data"].max()
rfm = df.groupby("id_cliente").agg(
    Recencia=("data", lambda x: (data_referencia - x.max()).days),
    Frequencia=("id_pedido", "count"),
    Monetario=("valor_total", "sum")
)
rfm["R"] = pd.qcut(
    rfm["Recencia"],
    4,
    labels=[4, 3, 2, 1]
).astype(int)
rfm["F"] = pd.qcut(
    rfm["Frequencia"],
    4,
    labels=[1, 2, 3, 4]
).astype(int)
rfm["M"] = pd.qcut(
    rfm["Monetario"],
    4,
    labels=[1, 2, 3, 4]
).astype(int)
rfm["Score_RFM"] = rfm["R"] + rfm["F"] + rfm["M"]
def classificar_rfm(score):
    if score <= 5:
        return "RFM Baixo"
    if score <= 7:
        return "RFM Intermediário"
    if score <= 9:
        return "RFM Alto"
    return "RFM Muito Alto"
rfm["Segmento"] = rfm["Score_RFM"].apply(classificar_rfm)
ordem_rfm = [
    "RFM Baixo",
    "RFM Intermediário",
    "RFM Alto",
    "RFM Muito Alto"
]
resumo_rfm = (
    rfm.groupby("Segmento")
    .agg(
        Clientes=("Score_RFM", "count"),
        Faturamento=("Monetario", "sum")
    )
    .reindex(ordem_rfm)
)
segmento_lider = resumo_rfm["Faturamento"].idxmax()
faturamento_segmento_lider = resumo_rfm["Faturamento"].max()
percentual_segmento_lider = (
    faturamento_segmento_lider / faturamento_total
) * 100
# ==========================================
# 7. ANÁLISE POR ESTADO
# ==========================================
resumo_estado = (
    df.groupby("estado")
    .agg(
        Pedidos=("id_pedido", "count"),
        Faturamento=("valor_total", "sum"),
        Ticket_Medio=("valor_total", "mean")
    )
    .sort_values("Faturamento", ascending=False)
)
estado_lider = resumo_estado["Faturamento"].idxmax()
faturamento_estado_lider = resumo_estado.loc[estado_lider, "Faturamento"]
estado_maior_ticket = resumo_estado["Ticket_Medio"].idxmax()
maior_ticket_estado = resumo_estado.loc[estado_maior_ticket, "Ticket_Medio"]
print("\n==========================================")
print("           ANÁLISE POR ESTADO")
print("==========================================")
print(resumo_estado)
print("\nTop 5 estados por faturamento:")
print(resumo_estado.head(5))
# ==========================================
# 8. ANÁLISE POR FORMA DE PAGAMENTO
# ==========================================
resumo_pagamento = (
    df.groupby("forma_pagamento")
    .agg(
        Pedidos=("id_pedido", "count"),
        Faturamento=("valor_total", "sum"),
        Ticket_Medio=("valor_total", "mean")
    )
    .sort_values("Faturamento", ascending=False)
)
pagamento_lider = resumo_pagamento["Faturamento"].idxmax()
faturamento_pagamento_lider = resumo_pagamento.loc[
    pagamento_lider, "Faturamento"
]
print("\n==========================================")
print("      ANÁLISE POR FORMA DE PAGAMENTO")
print("==========================================")
print(resumo_pagamento)
# ==========================================
# 9. INSIGHTS EXECUTIVOS
# ==========================================
print("\n==========================================")
print("           INSIGHTS EXECUTIVOS")
print("==========================================")
print(
    f"Produto líder: {produto_lider} "
    f"({percentual_produto_lider:.2f}% do faturamento)"
)
print(
    f"Categoria líder: {categoria_lider} "
    f"({percentual_categoria_lider:.2f}% do faturamento)"
)
print(
    f"Mês de maior faturamento: {nome_mes_maior} "
    f"(R$ {faturamento_mes_maior:,.2f})"
)
print(
    f"Segmento RFM líder: {segmento_lider} "
    f"({percentual_segmento_lider:.2f}% do faturamento)"
)
print(
    f"Estado líder: {estado_lider} "
    f"(R$ {faturamento_estado_lider:,.2f})"
)
print(
    f"Maior ticket médio: {estado_maior_ticket} "
    f"(R$ {maior_ticket_estado:,.2f})"
)
print(
    f"Forma de pagamento líder: {pagamento_lider} "
    f"(R$ {faturamento_pagamento_lider:,.2f})"
)
# ==========================================
# 10. DASHBOARD
# ==========================================
fig = plt.figure(figsize=(18, 18))
fig.suptitle(
    "Dashboard Executivo de Vendas",
    fontsize=24,
    fontweight="bold",
    y=0.98
)
gs = fig.add_gridspec(
    7,
    4,
    height_ratios=[1.0, 1.8, 1.8, 1.8, 1.6, 1.6, 1.0],
    hspace=0.75,
    wspace=0.25
)
# ==========================================
# 11. KPIs
# ==========================================
kpi_axes = [
    fig.add_subplot(gs[0, 0]),
    fig.add_subplot(gs[0, 1]),
    fig.add_subplot(gs[0, 2]),
    fig.add_subplot(gs[0, 3])
]
kpis = [
    ("Faturamento Total", f"R$ {faturamento_total:,.2f}"),
    ("Ticket Médio", f"R$ {ticket_medio:,.2f}"),
    ("Clientes Únicos", f"{clientes_unicos}"),
    ("Taxa de Recorrência", f"{taxa_recorrencia:.2f}%")
]
for ax, (titulo, valor) in zip(kpi_axes, kpis):
    ax.axis("off")
    ax.text(
        0.5, 0.68, titulo,
        ha="center",
        va="center",
        fontsize=12
    )
    ax.text(
        0.5, 0.30, valor,
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold"
    )
# ==========================================
# 12. FATURAMENTO MENSAL
# ==========================================
ax1 = fig.add_subplot(gs[1, :])
ax1.plot(
    resumo_mes.index,
    resumo_mes.values,
    marker="o",
    linewidth=2
)
ax1.set_title(
    "Evolução do Faturamento Mensal",
    fontsize=14,
    fontweight="bold"
)
ax1.set_xlabel("Mês")
ax1.set_ylabel("Faturamento (R$)")
ax1.set_xticks(resumo_mes.index)
ax1.set_xticklabels(
    [meses[i - 1] for i in resumo_mes.index]
)
ax1.ticklabel_format(
    style="plain",
    axis="y"
)
ax1.grid(
    axis="y",
    alpha=0.3
)
# ==========================================
# 13. FATURAMENTO POR PRODUTO
# ==========================================
ax2 = fig.add_subplot(gs[2, 0:2])
ax2.barh(
    resumo_produto.index,
    resumo_produto.values
)
ax2.set_title(
    "Faturamento por Produto",
    fontsize=14,
    fontweight="bold"
)
ax2.set_xlabel("Faturamento (R$)")
ax2.ticklabel_format(
    style="plain",
    axis="x"
)
ax2.tick_params(
    axis="y",
    labelsize=8
)
ax2.set_xlim(
    0,
    resumo_produto.max() * 1.18
)
for i, valor in enumerate(resumo_produto.values):
    ax2.text(
        valor,
        i,
        f" R$ {valor:,.0f}",
        va="center",
        fontsize=8
    )
ax2.grid(
    axis="x",
    alpha=0.3
)
# ==========================================
# 14. FATURAMENTO POR CATEGORIA
# ==========================================
ax3 = fig.add_subplot(gs[2, 2:4])
ax3.barh(
    resumo_categoria.index,
    resumo_categoria.values
)
ax3.set_title(
    "Faturamento por Categoria",
    fontsize=14,
    fontweight="bold"
)
ax3.set_xlabel("Faturamento (R$)")
ax3.ticklabel_format(
    style="plain",
    axis="x"
)
ax3.set_xlim(
    0,
    resumo_categoria.max() * 1.20
)
for i, valor in enumerate(resumo_categoria.values):
    ax3.text(
        valor,
        i,
        f" R$ {valor:,.0f}",
        va="center",
        fontsize=9
    )
ax3.grid(
    axis="x",
    alpha=0.3
)
# ==========================================
# 15. CLIENTES POR SEGMENTO RFM
# ==========================================
ax4 = fig.add_subplot(gs[3, 0:2])
barras = ax4.bar(
    resumo_rfm.index,
    resumo_rfm["Clientes"]
)
ax4.set_title(
    "Clientes por Segmento RFM",
    fontsize=14,
    fontweight="bold"
)
ax4.set_ylabel("Quantidade de Clientes")
ax4.tick_params(
    axis="x",
    rotation=20,
    labelsize=8
)
for barra in barras:
    altura = barra.get_height()
    ax4.text(
        barra.get_x() + barra.get_width() / 2,
        altura + 0.5,
        f"{int(altura)}",
        ha="center",
        fontweight="bold"
    )
# ==========================================
# 16. FATURAMENTO POR SEGMENTO RFM
# ==========================================
ax5 = fig.add_subplot(gs[3, 2:4])
barras = ax5.bar(
    resumo_rfm.index,
    resumo_rfm["Faturamento"]
)
ax5.set_title(
    "Faturamento por Segmento RFM",
    fontsize=14,
    fontweight="bold"
)
ax5.set_ylabel("Faturamento (R$)")
ax5.ticklabel_format(
    style="plain",
    axis="y"
)
ax5.tick_params(
    axis="x",
    rotation=20,
    labelsize=8
)
for barra in barras:
    altura = barra.get_height()
    ax5.text(
        barra.get_x() + barra.get_width() / 2,
        altura,
        f"R$ {altura:,.0f}",
        ha="center",
        va="bottom",
        fontsize=9,
        fontweight="bold"
    )
# ==========================================
# 17. FATURAMENTO POR ESTADO
# ==========================================
ax6 = fig.add_subplot(gs[4, 0:2])
estado_faturamento = resumo_estado["Faturamento"].sort_values()
ax6.barh(
    estado_faturamento.index,
    estado_faturamento.values
)
ax6.set_title(
    "Faturamento por Estado",
    fontsize=14,
    fontweight="bold"
)
ax6.set_xlabel("Faturamento (R$)")
ax6.ticklabel_format(
    style="plain",
    axis="x"
)
ax6.tick_params(
    axis="y",
    labelsize=8
)
ax6.set_xlim(
    0,
    estado_faturamento.max() * 1.15
)
for i, valor in enumerate(estado_faturamento.values):
    ax6.text(
        valor,
        i,
        f" R$ {valor:,.0f}",
        va="center",
        fontsize=7
    )
ax6.grid(
    axis="x",
    alpha=0.3
)
# ==========================================
# 18. TICKET MÉDIO POR ESTADO
# ==========================================
ax7 = fig.add_subplot(gs[4, 2:4])
estado_ticket = resumo_estado["Ticket_Medio"].sort_values()
ax7.barh(
    estado_ticket.index,
    estado_ticket.values
)
ax7.set_title(
    "Ticket Médio por Estado",
    fontsize=14,
    fontweight="bold"
)
ax7.set_xlabel("Ticket Médio (R$)")
ax7.ticklabel_format(
    style="plain",
    axis="x"
)
ax7.tick_params(
    axis="y",
    labelsize=8
)
ax7.set_xlim(
    0,
    estado_ticket.max() * 1.12
)
for i, valor in enumerate(estado_ticket.values):
    ax7.text(
        valor,
        i,
        f" R$ {valor:,.0f}",
        va="center",
        fontsize=7
    )
ax7.grid(
    axis="x",
    alpha=0.3
)
# ==========================================
# 19. FATURAMENTO POR PAGAMENTO
# ==========================================
ax8 = fig.add_subplot(gs[5, 0:2])
pagamento_faturamento = resumo_pagamento["Faturamento"].sort_values()
ax8.barh(
    pagamento_faturamento.index,
    pagamento_faturamento.values
)
ax8.set_title(
    "Faturamento por Forma de Pagamento",
    fontsize=14,
    fontweight="bold"
)
ax8.set_xlabel("Faturamento (R$)")
ax8.ticklabel_format(
    style="plain",
    axis="x"
)
ax8.tick_params(
    axis="y",
    labelsize=8
)
ax8.set_xlim(
    0,
    pagamento_faturamento.max() * 1.15
)
for i, valor in enumerate(pagamento_faturamento.values):
    ax8.text(
        valor,
        i,
        f" R$ {valor:,.0f}",
        va="center",
        fontsize=8
    )
ax8.grid(
    axis="x",
    alpha=0.3
)
# ==========================================
# 20. PEDIDOS POR PAGAMENTO
# ==========================================
ax9 = fig.add_subplot(gs[5, 2:4])
pagamento_pedidos = resumo_pagamento["Pedidos"].sort_values()
ax9.barh(
    pagamento_pedidos.index,
    pagamento_pedidos.values
)
ax9.set_title(
    "Pedidos por Forma de Pagamento",
    fontsize=14,
    fontweight="bold"
)
ax9.set_xlabel("Quantidade de Pedidos")
ax9.tick_params(
    axis="y",
    labelsize=8
)
ax9.set_xlim(
    0,
    pagamento_pedidos.max() * 1.12
)
for i, valor in enumerate(pagamento_pedidos.values):
    ax9.text(
        valor,
        i,
        f" {int(valor)}",
        va="center",
        fontsize=9
    )
ax9.grid(
    axis="x",
    alpha=0.3
)
# ==========================================
# 21. INSIGHTS EXECUTIVOS
# ==========================================
ax10 = fig.add_subplot(gs[6, :])
ax10.axis("off")
ax10.text(
    0.01,
    0.85,
    "INSIGHTS EXECUTIVOS",
    fontsize=16,
    fontweight="bold"
)
ax10.text(
    0.01,
    0.50,
    f"• Produto líder: {produto_lider} "
    f"({percentual_produto_lider:.2f}% do faturamento)\n"
    f"• Categoria líder: {categoria_lider} "
    f"({percentual_categoria_lider:.2f}% do faturamento)\n"
    f"• Maior faturamento mensal: {nome_mes_maior} "
    f"(R$ {faturamento_mes_maior:,.2f})",
    fontsize=11,
    va="center"
)
ax10.text(
    0.52,
    0.50,
    f"• Segmento RFM líder: {segmento_lider} "
    f"({percentual_segmento_lider:.2f}% do faturamento)\n"
    f"• Estado líder: {estado_lider} "
    f"(R$ {faturamento_estado_lider:,.2f})\n"
    f"• Maior ticket médio: {estado_maior_ticket} "
    f"(R$ {maior_ticket_estado:,.2f})\n"
    f"• Pagamento líder: {pagamento_lider} "
    f"(R$ {faturamento_pagamento_lider:,.2f})",
    fontsize=11,
    va="center"
)
# ==========================================
# 22. EXIBIR DASHBOARD
# ==========================================
# ==========================================
# ANÁLISE DE CLIENTES
# ==========================================
clientes = df.groupby("id_cliente").agg(
    pedidos=("id_pedido", "count"),
    faturamento=("valor_total", "sum"),
    ticket_medio=("valor_total", "mean"),
    ultima_compra=("data", "max")
)
clientes["dias_desde_ultima_compra"] = (
    df["data"].max() - clientes["ultima_compra"]
).dt.days
clientes = clientes.sort_values(
    "faturamento",
    ascending=False
)
print("\n==========================================")
print("           ANÁLISE DE CLIENTES")
print("==========================================")
print(f"Clientes analisados: {len(clientes)}")
print("\nTop 10 clientes por faturamento:")
print(
    clientes[
        ["pedidos", "faturamento", "ticket_medio"]
    ].head(10)
)
# Concentração de faturamento
top_10_faturamento = clientes.head(10)["faturamento"].sum()
top_20_faturamento = clientes.head(20)["faturamento"].sum()

perc_top_10 = (
    top_10_faturamento / faturamento_total
) * 100
perc_top_20 = (
    top_20_faturamento / faturamento_total
) * 100
print("\nConcentração de faturamento:")
print(
    f"Top 10 clientes: "
    f"R$ {top_10_faturamento:,.2f} "
    f"({perc_top_10:.2f}%)"
)
print(
    f"Top 20 clientes: "
    f"R$ {top_20_faturamento:,.2f} "
    f"({perc_top_20:.2f}%)"
)
# Distribuição de frequência
distribuicao_frequencia = (
    clientes["pedidos"]
    .value_counts()
    .sort_index()
)
print("\nDistribuição de pedidos por cliente:")
print(distribuicao_frequencia)
# ==========================================
# PARETO DE CLIENTES
# ==========================================
pareto_clientes = clientes[["faturamento"]].copy()
pareto_clientes["percentual"] = (
    pareto_clientes["faturamento"] / faturamento_total
) * 100
pareto_clientes["percentual_acumulado"] = (
    pareto_clientes["percentual"].cumsum()
)
print("\n==========================================")
print("           PARETO DE CLIENTES")
print("==========================================")
for percentual in [10, 20, 30, 40, 50]:
    quantidade = int(len(clientes) * percentual / 100)
    receita = clientes.head(quantidade)["faturamento"].sum()
    participacao = (
        receita / faturamento_total
    ) * 100
    print(
        f"Top {percentual}% dos clientes "
        f"({quantidade} clientes): "
        f"R$ {receita:,.2f} "
        f"({participacao:.2f}% do faturamento)"
    )
# ==========================================
# PARETO × RFM
# ==========================================
clientes_rfm = clientes.join(
    rfm["Segmento"]
)
top_20_qtd = int(len(clientes_rfm) * 0.20)
top_20_clientes = (
    clientes_rfm
    .head(top_20_qtd)
)
resumo_pareto_rfm = (
    top_20_clientes
    .groupby("Segmento")
    .agg(
        Clientes=("faturamento", "count"),
        Faturamento=("faturamento", "sum"),
        Pedidos=("pedidos", "sum")
    )
    .sort_values(
        "Faturamento",
        ascending=False
    )
)
resumo_pareto_rfm["Participacao"] = (
    resumo_pareto_rfm["Faturamento"]
    / top_20_clientes["faturamento"].sum()
) * 100
print("\n==========================================")
print("           PARETO × RFM")
print("==========================================")
print(
    f"Top 20% da base: "
    f"{top_20_qtd} clientes"
)
print(
    f"Faturamento do Top 20%: "
    f"R$ {top_20_clientes['faturamento'].sum():,.2f}"
)
print("\nDistribuição por segmento RFM:")
print(resumo_pareto_rfm)
# ==========================================
# TOP 20% × PRODUTOS
# ==========================================
ids_top20 = top_20_clientes.index
compras_top20 = df[
    df["id_cliente"].isin(ids_top20)
]
produtos_top20 = (
    compras_top20
    .groupby("produto")
    .agg(
        pedidos=("id_pedido", "count"),
        unidades=("quantidade", "sum"),
        faturamento=("valor_total", "sum")
    )
    .sort_values(
        "faturamento",
        ascending=False
    )
)
produtos_top20["participacao"] = (
    produtos_top20["faturamento"]
    / produtos_top20["faturamento"].sum()
) * 100
print("\n==========================================")
print("        TOP 20% × PRODUTOS")
print("==========================================")
print(
    f"Clientes analisados: {len(ids_top20)}"
)
print(
    f"Faturamento: "
    f"R$ {compras_top20['valor_total'].sum():,.2f}"
)
print("\nProdutos comprados:")
print(produtos_top20)
# ==========================================
# TOP 20% × RESTANTE DA BASE
# ==========================================
ids_top20 = top_20_clientes.index
df["grupo_cliente"] = df["id_cliente"].apply(
    lambda x: "Top 20%" if x in ids_top20 else "Outros 80%"
)
comparacao_clientes = df.groupby(
    "grupo_cliente"
).agg(
    clientes=("id_cliente", "nunique"),
    pedidos=("id_pedido", "count"),
    unidades=("quantidade", "sum"),
    faturamento=("valor_total", "sum")
)
comparacao_clientes["ticket_medio"] = (
    comparacao_clientes["faturamento"]
    / comparacao_clientes["pedidos"]
)
comparacao_clientes["pedidos_por_cliente"] = (
    comparacao_clientes["pedidos"]
    / comparacao_clientes["clientes"]
)
comparacao_clientes["faturamento_por_cliente"] = (
    comparacao_clientes["faturamento"]
    / comparacao_clientes["clientes"]
)
print("\n==========================================")
print("       TOP 20% × OUTROS 80%")
print("==========================================")
print(comparacao_clientes.to_string())
# ==========================================
# TOP 20% × OUTROS 80% — MIX DE PRODUTOS
# ==========================================
comparacao_produtos = (
    df.groupby(["grupo_cliente", "produto"])
    .agg(
        pedidos=("id_pedido", "count"),
        unidades=("quantidade", "sum"),
        faturamento=("valor_total", "sum")
    )
    .reset_index()
)
# Faturamento total de cada grupo
totais_grupo = comparacao_produtos.groupby(
    "grupo_cliente"
)["faturamento"].transform("sum")
# Participação de cada produto dentro do grupo
comparacao_produtos["participacao"] = (
    comparacao_produtos["faturamento"] / totais_grupo
) * 100
print("\n==========================================")
print("     TOP 20% × OUTROS 80% — PRODUTOS")
print("==========================================")
print(
    comparacao_produtos
    .sort_values(
        ["grupo_cliente", "faturamento"],
        ascending=[True, False]
    )
    .to_string(index=False)
)# ==========================================
# DIFERENÇA DE PARTICIPAÇÃO POR PRODUTO
# ==========================================
pivot_produtos = comparacao_produtos.pivot(
    index="produto",
    columns="grupo_cliente",
    values="participacao"
)
pivot_produtos["diferenca_p.p."] = (
    pivot_produtos["Top 20%"] -
    pivot_produtos["Outros 80%"]
)
pivot_produtos = pivot_produtos.sort_values(
    "diferenca_p.p.",
    ascending=False
)
print("\n==========================================")
print("   CONCENTRAÇÃO DE PRODUTOS — TOP 20%")
print("==========================================")
print(pivot_produtos.to_string())
# ==========================================
# TOP 20% × RECÊNCIA
# ==========================================
top20_recencia = top_20_clientes[
    [
        "pedidos",
        "faturamento",
        "ticket_medio",
        "ultima_compra",
        "dias_desde_ultima_compra"
    ]
].copy()
top20_recencia = top20_recencia.sort_values(
    "dias_desde_ultima_compra"
)
print("\n==========================================")
print("        TOP 20% × RECÊNCIA")
print("==========================================")
print(f"Clientes analisados: {len(top20_recencia)}")
print("\nRecência dos clientes Top 20%:")
print(
    top20_recencia[
        [
            "pedidos",
            "faturamento",
            "dias_desde_ultima_compra"
        ]
    ].to_string()
)
print("\nEstatísticas de recência:")
print(
    top20_recencia["dias_desde_ultima_compra"]
    .describe()
)
# ==========================================
# CLASSIFICAÇÃO DE RISCO — TOP 20%
# ==========================================
def classificar_risco(dias):
    if dias <= 30:
        return "Ativo"
    elif dias <= 90:
        return "Atenção"
    else:
        return "Risco"
top20_recencia["risco"] = (
    top20_recencia["dias_desde_ultima_compra"]
    .apply(classificar_risco)
)
resumo_risco = (
    top20_recencia
    .groupby("risco")
    .agg(
        clientes=("faturamento", "count"),
        pedidos=("pedidos", "sum"),
        faturamento=("faturamento", "sum"),
        faturamento_medio=("faturamento", "mean"),
        recencia_media=("dias_desde_ultima_compra", "mean")
    )
)
resumo_risco["participacao_faturamento"] = (
    resumo_risco["faturamento"]
    / top20_recencia["faturamento"].sum()
) * 100
print("\n==========================================")
print("       RISCO — TOP 20%")
print("==========================================")
print(
    resumo_risco
    .sort_values("faturamento", ascending=False)
    .to_string()
)
# ==========================================
# CLIENTES EM RISCO — TOP 20%
# ==========================================
clientes_risco = top20_recencia[
    top20_recencia["risco"] == "Risco"
].copy()
clientes_risco = clientes_risco.sort_values(
    "faturamento",
    ascending=False
)
print("\n==========================================")
print("       CLIENTES EM RISCO — TOP 20%")
print("==========================================")
print(
    clientes_risco[
        [
            "pedidos",
            "faturamento",
            "ticket_medio",
            "dias_desde_ultima_compra"
        ]
    ].to_string()
)
# ==========================================
# PRODUTOS DOS CLIENTES EM RISCO
# ==========================================
ids_risco = clientes_risco.index
compras_risco = df[
    df["id_cliente"].isin(ids_risco)
].copy()
produtos_risco = (
    compras_risco
    .groupby(["id_cliente", "produto"])
    .agg(
        pedidos=("id_pedido", "count"),
        unidades=("quantidade", "sum"),
        faturamento=("valor_total", "sum")
    )
    .reset_index()
    .sort_values(
        ["id_cliente", "faturamento"],
        ascending=[True, False]
    )
)
print("\n==========================================")
print("     PRODUTOS DOS CLIENTES EM RISCO")
print("==========================================")
print(
    produtos_risco.to_string(index=False)
)
# ==========================================
# RISCO × PRODUTO
# ==========================================
resumo_risco_produto = (
    compras_risco
    .groupby("produto")
    .agg(
        clientes=("id_cliente", "nunique"),
        pedidos=("id_pedido", "count"),
        unidades=("quantidade", "sum"),
        faturamento=("valor_total", "sum")
    )
    .sort_values(
        "faturamento",
        ascending=False
    )
)
resumo_risco_produto["participacao"] = (
    resumo_risco_produto["faturamento"]
    / resumo_risco_produto["faturamento"].sum()
) * 100
print("\n==========================================")
print("          RISCO × PRODUTO")
print("==========================================")
print(
    resumo_risco_produto.to_string()
)
# ==========================================
# BASE DE CLIENTES PARA MACHINE LEARNING
# ==========================================
clientes_ml = df.groupby("id_cliente").agg(
    pedidos=("id_pedido", "count"),
    faturamento=("valor_total", "sum"),
    ticket_medio=("valor_total", "mean"),
    unidades=("quantidade", "sum"),
    primeira_compra=("data", "min"),
    ultima_compra=("data", "max"),
    produtos_diferentes=("produto", "nunique")
).reset_index()
clientes_ml["dias_ativo"] = (
    clientes_ml["ultima_compra"] -
    clientes_ml["primeira_compra"]
).dt.days
clientes_ml["frequencia_pedidos"] = (
    clientes_ml["pedidos"] /
    clientes_ml["dias_ativo"]
)
clientes_ml.loc[
    clientes_ml["dias_ativo"] == 0,
    "frequencia_pedidos"
] = 0
clientes_ml["dias_desde_ultima_compra"] = (
    df["data"].max() -
    clientes_ml["ultima_compra"]
).dt.days
print("\n==========================================")
print("      BASE DE CLIENTES — MACHINE LEARNING")
print("==========================================")
print(f"Clientes: {len(clientes_ml)}")
print(f"Variáveis: {len(clientes_ml.columns)}")
print("\nPrimeiras linhas:")
print(
    clientes_ml.head(10).to_string(index=False)
)
print("\nInformações estatísticas:")
print(
    clientes_ml.describe()
)
# ==========================================
# DISTRIBUIÇÃO TEMPORAL — MACHINE LEARNING
# ==========================================
df["mes"] = df["data"].dt.to_period("M")
pedidos_por_mes = (
    df.groupby("mes")
    .agg(
        pedidos=("id_pedido", "count"),
        clientes=("id_cliente", "nunique"),
        faturamento=("valor_total", "sum")
    )
)
print("\n==========================================")
print("   DISTRIBUIÇÃO TEMPORAL — MACHINE LEARNING")
print("==========================================")
print(
    pedidos_por_mes.to_string()
)
print("\nData inicial:", df["data"].min().date())
print("Data final:", df["data"].max().date())
# ==========================================
# BASE TEMPORAL PARA MACHINE LEARNING
# ==========================================
data_corte = pd.Timestamp("2026-07-31")
inicio_previsao = pd.Timestamp("2026-08-01")
fim_previsao = pd.Timestamp("2026-09-24")
# Histórico usado para criar as características
df_historico = df[
    df["data"] <= data_corte
].copy()
# Período usado para definir o comportamento futuro
df_futuro = df[
    (df["data"] >= inicio_previsao) &
    (df["data"] <= fim_previsao)
].copy()
print("\n==========================================")
print("      BASE TEMPORAL — MACHINE LEARNING")
print("==========================================")
print("Data de corte:", data_corte.date())
print("Início da previsão:", inicio_previsao.date())
print("Fim da previsão:", fim_previsao.date())
print("\nHistórico:")
print("Pedidos:", len(df_historico))
print("Clientes:", df_historico["id_cliente"].nunique())
print(
    "Faturamento: R$",
    f"{df_historico['valor_total'].sum():,.2f}"
)
print("\nPeríodo futuro:")
print("Pedidos:", len(df_futuro))
print("Clientes:", df_futuro["id_cliente"].nunique())
print(
    "Faturamento: R$",
    f"{df_futuro['valor_total'].sum():,.2f}"
)
# ==========================================
# CRIAÇÃO DA BASE DE TREINAMENTO
# ==========================================
# 1. Criar características usando SOMENTE o histórico
clientes_hist = df_historico.groupby("id_cliente").agg(
    pedidos=("id_pedido", "count"),
    faturamento=("valor_total", "sum"),
    ticket_medio=("valor_total", "mean"),
    unidades=("quantidade", "sum"),
    primeira_compra=("data", "min"),
    ultima_compra=("data", "max"),
    produtos_diferentes=("produto", "nunique")
).reset_index()
# 2. Tempo de relacionamento do cliente
clientes_hist["dias_ativo"] = (
    clientes_hist["ultima_compra"] -
    clientes_hist["primeira_compra"]
).dt.days
# 3. Frequência de pedidos
clientes_hist["frequencia_pedidos"] = (
    clientes_hist["pedidos"] /
    clientes_hist["dias_ativo"]
)
# Clientes com apenas uma compra
clientes_hist.loc[
    clientes_hist["dias_ativo"] == 0,
    "frequencia_pedidos"
] = 0
# 4. Recência calculada no momento do corte
clientes_hist["dias_desde_corte"] = (
    data_corte -
    clientes_hist["ultima_compra"]
).dt.days
# 5. Identificar clientes que compraram no período futuro
clientes_compraram_futuro = set(
    df_futuro["id_cliente"]
)
# 6. Criar variável-alvo
clientes_hist["target_risco"] = (
    ~clientes_hist["id_cliente"].isin(
        clientes_compraram_futuro
    )
).astype(int)
# ==========================================
# RESULTADO
# ==========================================
print("\n==========================================")
print("       BASE DE TREINAMENTO — ML")
print("==========================================")
print("Clientes:", len(clientes_hist))
print("\nDistribuição do alvo:")
print(
    clientes_hist["target_risco"]
    .value_counts()
    .sort_index()
)
print("\nDistribuição percentual:")
print(
    clientes_hist["target_risco"]
    .value_counts(normalize=True)
    .sort_index()
    .mul(100)
    .round(2)
)
print("\nLegenda:")
print("0 = Cliente comprou no período futuro")
print("1 = Cliente não comprou no período futuro")
print("\nPrimeiras linhas:")
print(
    clientes_hist[
        [
            "id_cliente",
            "pedidos",
            "faturamento",
            "ticket_medio",
            "unidades",
            "produtos_diferentes",
            "dias_ativo",
            "frequencia_pedidos",
            "dias_desde_corte",
            "target_risco"
        ]
    ].head(10)
)
# ==========================================
# SEPARAÇÃO DAS VARIÁVEIS — ML
# ==========================================
features = [
    "pedidos",
    "faturamento",
    "ticket_medio",
    "unidades",
    "produtos_diferentes",
    "dias_ativo",
    "frequencia_pedidos",
    "dias_desde_corte"
]
X = clientes_hist[features]
y = clientes_hist["target_risco"]
print("\n==========================================")
print("       VARIÁVEIS DO MODELO — ML")
print("==========================================")
print("\nVariáveis preditoras:")
for feature in features:
    print("-", feature)
print("\nFormato de X:", X.shape)
print("Formato de y:", y.shape)
print("\nX:")
print(X.head())
print("\ny:")
print(y.head())
print("\nValores ausentes:")
print(X.isnull().sum().sum())
# ==========================================
# DIVISÃO TREINO E TESTE — ML
# ==========================================
from sklearn.model_selection import (
    StratifiedKFold,
    cross_validate,
    train_test_split
)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
print("\n==========================================")
print("       TREINO E TESTE — MACHINE LEARNING")
print("==========================================")
print("\nBase completa:")
print("X:", X.shape)
print("y:", y.shape)
print("\nBase de treinamento:")
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)
print("\nBase de teste:")
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)
print("\nDistribuição do alvo — treino:")
print(
    y_train.value_counts()
    .sort_index()
)
print("\nDistribuição percentual — treino:")
print(
    y_train.value_counts(normalize=True)
    .sort_index()
    .mul(100)
    .round(2)
)
print("\nDistribuição do alvo — teste:")
print(
    y_test.value_counts()
    .sort_index()
)
print("\nDistribuição percentual — teste:")
print(
    y_test.value_counts(normalize=True)
    .sort_index()
    .mul(100)
    .round(2)
)
validacao_cruzada = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)
metricas_validacao = {
    "accuracy": "accuracy",
    "precision": "precision",
    "recall": "recall",
    "f1": "f1"
}

def imprimir_validacao_cruzada(modelo, nome_modelo):
    resultados = cross_validate(
        modelo,
        X_train,
        y_train,
        cv=validacao_cruzada,
        scoring=metricas_validacao
    )
    print(f"\nValidação cruzada — {nome_modelo} (média de 5 folds):")
    for metrica in metricas_validacao:
        media = resultados[f"test_{metrica}"].mean()
        print(f"{metrica.capitalize()}: {media:.2%}")

# ==========================================
# REGRESSÃO LOGÍSTICA COM PADRONIZAÇÃO
# ==========================================
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
modelo_logistico = Pipeline([
    ("scaler", StandardScaler()),
    ("modelo", LogisticRegression(
        max_iter=5000,
        random_state=42
    ))
])
modelo_logistico.fit(
    X_train,
    y_train
)
imprimir_validacao_cruzada(
    modelo_logistico,
    "Regressão Logística"
)
y_pred = modelo_logistico.predict(X_test)
print("\n==========================================")
print("       REGRESSÃO LOGÍSTICA — ML")
print("==========================================")
print("\nModelo treinado com sucesso.")
print("\nPrevisões:")
print(y_pred)
print("\nValores reais:")
print(y_test.to_numpy())
# ==========================================
# AVALIAÇÃO DA REGRESSÃO LOGÍSTICA
# ==========================================
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(
    y_test,
    y_pred,
    pos_label=1
)
recall = recall_score(
    y_test,
    y_pred,
    pos_label=1
)
f1 = f1_score(
    y_test,
    y_pred,
    pos_label=1
)
matriz = confusion_matrix(
    y_test,
    y_pred
)
print("\n==========================================")
print("       AVALIAÇÃO — REGRESSÃO LOGÍSTICA")
print("==========================================")
print(f"\nAccuracy:  {accuracy:.2%}")
print(f"Precision: {precision:.2%}")
print(f"Recall:    {recall:.2%}")
print(f"F1-score:  {f1:.2%}")
print("\nMatriz de Confusão:")
print(matriz)
print("\nRelatório de Classificação:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Comprou novamente",
            "Não comprou novamente"
        ]
    )
)
# ==========================================
# SEGUNDO MODELO — RANDOM FOREST
# ==========================================
from sklearn.ensemble import RandomForestClassifier
modelo_rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=5,
    min_samples_leaf=3,
    random_state=42
)
modelo_rf.fit(
    X_train,
    y_train
)
imprimir_validacao_cruzada(
    modelo_rf,
    "Random Forest"
)
y_pred_rf = modelo_rf.predict(X_test)
print("\n==========================================")
print("          RANDOM FOREST — ML")
print("==========================================")
print("\nModelo treinado com sucesso.")
print("\nPrevisões:")
print(y_pred_rf)
print("\nValores reais:")
print(y_test.to_numpy())
# ==========================================
# AVALIAÇÃO — RANDOM FOREST
# ==========================================
accuracy_rf = accuracy_score(
    y_test,
    y_pred_rf
)
precision_rf = precision_score(
    y_test,
    y_pred_rf,
    pos_label=1
)
recall_rf = recall_score(
    y_test,
    y_pred_rf,
    pos_label=1
)
f1_rf = f1_score(
    y_test,
    y_pred_rf,
    pos_label=1
)
matriz_rf = confusion_matrix(
    y_test,
    y_pred_rf
)
print("\n==========================================")
print("       AVALIAÇÃO — RANDOM FOREST")
print("==========================================")
print(f"\nAccuracy:  {accuracy_rf:.2%}")
print(f"Precision: {precision_rf:.2%}")
print(f"Recall:    {recall_rf:.2%}")
print(f"F1-score:  {f1_rf:.2%}")
print("\nMatriz de Confusão:")
print(matriz_rf)
print("\nRelatório de Classificação:")
print(
    classification_report(
        y_test,
        y_pred_rf,
        target_names=[
            "Comprou novamente",
            "Não comprou novamente"
        ]
    )
)
# ==========================================
# IMPORTÂNCIA DAS VARIÁVEIS — RANDOM FOREST
# ==========================================
importancias = pd.Series(
    modelo_rf.feature_importances_,
    index=features
).sort_values(ascending=False)
print("\n==========================================")
print("     IMPORTÂNCIA DAS VARIÁVEIS — RF")
print("==========================================")
print(
    importancias
)
print("\nPercentual:")
print(
    (importancias * 100).round(2)
)
# ==========================================
# RANKING DE CLIENTES POR RISCO
# ==========================================
prob_risco = modelo_rf.predict_proba(X_test)[:, 1]
resultado_ml = clientes_hist.loc[
    X_test.index,
    [
        "id_cliente",
        "pedidos",
        "faturamento",
        "ticket_medio",
        "dias_desde_corte"
    ]
].copy()
resultado_ml["probabilidade_risco"] = prob_risco
resultado_ml["classe_real"] = y_test.values
resultado_ml["previsao"] = y_pred_rf
resultado_ml = resultado_ml.sort_values(
    "probabilidade_risco",
    ascending=False
)
print("\n==========================================")
print("       RANKING DE RISCO DOS CLIENTES")
print("==========================================")
print(
    resultado_ml[
        [
            "id_cliente",
            "probabilidade_risco",
            "faturamento",
            "pedidos",
            "dias_desde_corte"
        ]
    ].to_string(index=False)
)
# ==========================================
# CLASSIFICAÇÃO OPERACIONAL DO RISCO
# ==========================================
resultado_ml["nivel_risco"] = pd.cut(
    resultado_ml["probabilidade_risco"],
    bins=[-float("inf"), 0.40, 0.60, float("inf")],
    labels=["Baixo", "Médio", "Alto"]
)
resultado_ml["prioridade"] = resultado_ml["nivel_risco"].map({
    "Alto": 1,
    "Médio": 2,
    "Baixo": 3
})
resultado_ml = resultado_ml.sort_values(
    ["prioridade", "probabilidade_risco"],
    ascending=[True, False]
)
print("\n==========================================")
print("       CLASSIFICAÇÃO OPERACIONAL")
print("==========================================")
print(
    resultado_ml[
        [
            "id_cliente",
            "probabilidade_risco",
            "nivel_risco",
            "faturamento",
            "pedidos",
            "dias_desde_corte"
        ]
    ].to_string(index=False)
)
print("\n==========================================")
print("          RESUMO DO RISCO")
print("==========================================")
print(
    resultado_ml["nivel_risco"]
    .value_counts()
    .sort_index()
)
# ==========================================
# RISCO × VALOR FINANCEIRO
# ==========================================
resultado_ml["valor_financeiro"] = pd.cut(
    resultado_ml["faturamento"],
    bins=[-float("inf"), 5000, 15000, float("inf")],
    labels=["Baixo", "Médio", "Alto"]
)
resultado_ml["prioridade_comercial"] = "Baixa"
resultado_ml.loc[
    (resultado_ml["nivel_risco"] == "Alto") &
    (resultado_ml["valor_financeiro"] == "Alto"),
    "prioridade_comercial"
] = "CRÍTICA"
resultado_ml.loc[
    (resultado_ml["nivel_risco"] == "Alto") &
    (resultado_ml["valor_financeiro"] != "Alto"),
    "prioridade_comercial"
] = "Alta"
resultado_ml.loc[
    (resultado_ml["nivel_risco"] == "Médio") &
    (resultado_ml["valor_financeiro"] == "Alto"),
    "prioridade_comercial"
] = "Alta"
resultado_ml.loc[
    (resultado_ml["nivel_risco"] == "Médio") &
    (resultado_ml["valor_financeiro"] == "Médio"),
    "prioridade_comercial"
] = "Média"
print("\n==========================================")
print("       RISCO × VALOR FINANCEIRO")
print("==========================================")
print(
    resultado_ml[
        [
            "id_cliente",
            "probabilidade_risco",
            "nivel_risco",
            "faturamento",
            "valor_financeiro",
            "pedidos",
            "dias_desde_corte",
            "prioridade_comercial"
        ]
    ]
    .sort_values(
        ["prioridade_comercial", "faturamento"],
        ascending=[True, False]
    )
    .to_string(index=False)
)
# ==========================================
# PRODUTOS DOS CLIENTES PRIORITÁRIOS
# ==========================================
clientes_prioritarios = resultado_ml[
    resultado_ml["prioridade_comercial"].isin(["CRÍTICA", "Alta"])
]["id_cliente"]
compras_prioritarias = df[
    df["id_cliente"].isin(clientes_prioritarios)
].copy()
analise_produtos_risco = (
    compras_prioritarias
    .groupby("produto")
    .agg(
        clientes=("id_cliente", "nunique"),
        pedidos=("id_pedido", "count"),
        unidades=("quantidade", "sum"),
        faturamento=("valor_total", "sum")
    )
    .sort_values("faturamento", ascending=False)
)
analise_produtos_risco["participacao"] = (
    analise_produtos_risco["faturamento"]
    / analise_produtos_risco["faturamento"].sum()
    * 100
)
print("\n==========================================")
print("     PRODUTOS — CLIENTES PRIORITÁRIOS")
print("==========================================")
print(analise_produtos_risco)
# ==========================================
# CONSOLIDAÇÃO EXECUTIVA FINAL
# ==========================================
# ------------------------------------------
# PARTICIPAÇÃO DOS 4 PRINCIPAIS PRODUTOS
# ------------------------------------------
top4_produtos = (
    resumo_produto
    .sort_values(ascending=False)
    .head(4)
    .sum()
)
percentual_top4_produtos = (
    top4_produtos / faturamento_total
) * 100
# ------------------------------------------
# TOP 20% DOS CLIENTES
# ------------------------------------------
quantidade_top20 = int(len(clientes) * 0.20)
faturamento_top20 = (
    clientes
    .head(quantidade_top20)["faturamento"]
    .sum()
)
percentual_top20 = (
    faturamento_top20 / faturamento_total
) * 100
# ------------------------------------------
# RFM
# ------------------------------------------
percentual_rfm_lider = (
    faturamento_segmento_lider /
    faturamento_total
) * 100
# ------------------------------------------
# MACHINE LEARNING
# ------------------------------------------
melhor_modelo = "Random Forest"
# Quantidade de clientes por nível de risco
distribuicao_risco = (
    resultado_ml["nivel_risco"]
    .value_counts()
)
# Clientes de alta prioridade
clientes_alta = resultado_ml[
    resultado_ml["prioridade_comercial"].isin(
        ["Alta", "CRÍTICA"]
    )
]
quantidade_clientes_alta = len(clientes_alta)
faturamento_clientes_alta = (
    clientes_alta["faturamento"].sum()
)
# ------------------------------------------
# RESUMO EXECUTIVO
# ------------------------------------------
print("\n")
print("=" * 60)
print("           RESUMO EXECUTIVO DO PROJETO")
print("=" * 60)
print("\n[1] INDICADORES GERAIS")
print(
    f"Faturamento total: "
    f"R$ {faturamento_total:,.2f}"
)
print(
    f"Total de pedidos: "
    f"{len(df)}"
)
print(
    f"Clientes únicos: "
    f"{clientes_unicos}"
)
print(
    f"Ticket médio: "
    f"R$ {ticket_medio:,.2f}"
)
print(
    f"Taxa de recorrência: "
    f"{taxa_recorrencia:.2f}%"
)
print("\n[2] CONCENTRAÇÃO DE PRODUTOS")
print(
    f"Produto líder: "
    f"{produto_lider}"
)
print(
    f"Participação do produto líder: "
    f"{percentual_produto_lider:.2f}%"
)
print(
    f"Top 4 produtos: "
    f"{percentual_top4_produtos:.2f}% "
    f"do faturamento"
)
print("\n[3] CATEGORIAS")
print(
    f"Categoria líder: "
    f"{categoria_lider}"
)
print(
    f"Participação da categoria líder: "
    f"{percentual_categoria_lider:.2f}%"
)
print("\n[4] CLIENTES")
print(
    f"Top 20% dos clientes: "
    f"{quantidade_top20} clientes"
)
print(
    f"Faturamento do Top 20%: "
    f"R$ {faturamento_top20:,.2f}"
)
print(
    f"Participação do Top 20%: "
    f"{percentual_top20:.2f}%"
)
print("\n[5] RFM")
print(
    f"Segmento líder: "
    f"{segmento_lider}"
)
print(
    f"Participação do segmento líder: "
    f"{percentual_rfm_lider:.2f}%"
)
print("\n[6] MACHINE LEARNING")
print(
    f"Modelo selecionado: "
    f"{melhor_modelo}"
)
print(
    f"Accuracy: "
    f"{accuracy_rf:.2%}"
)
print(
    f"Precision — risco: "
    f"{precision_rf:.2%}"
)
print(
    f"Recall — risco: "
    f"{recall_rf:.2%}"
)
print(
    f"F1-score — risco: "
    f"{f1_rf:.2%}"
)
print("\n[7] PRIORIZAÇÃO COMERCIAL")
print(
    f"Clientes de alta prioridade: "
    f"{quantidade_clientes_alta}"
)
print(
    f"Faturamento histórico desses clientes: "
    f"R$ {faturamento_clientes_alta:,.2f}"
)
print(
    f"Clientes Alto risco: "
    f"{distribuicao_risco.get('Alto', 0)}"
)
print(
    f"Clientes Médio risco: "
    f"{distribuicao_risco.get('Médio', 0)}"
)
print(
    f"Clientes Baixo risco: "
    f"{distribuicao_risco.get('Baixo', 0)}"
)
print("\n[8] PRINCIPAIS PRODUTOS DOS CLIENTES PRIORITÁRIOS")
print(
    analise_produtos_risco[
        ["faturamento", "participacao"]
    ]
    .head(3)
)
print("\n" + "=" * 60)
print("             FIM DA ANÁLISE")
print("=" * 60)
diretorio_relatorios = Path(__file__).resolve().parent / "reports"
diretorio_relatorios.mkdir(exist_ok=True)
arquivo_dashboard = diretorio_relatorios / "dashboard_executivo.png"
fig.savefig(arquivo_dashboard, dpi=160, bbox_inches="tight")
print(f"Dashboard salvo em: {arquivo_dashboard}")
plt.show()
plt.show()