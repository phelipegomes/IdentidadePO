# grafico_termometro.py
# Código para construção do gráfico termômetro no Power BI
# Este script deve ser inserido no visual Python do Power BI

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Pré-processamento dos dados
# dataset = pandas.DataFrame(Final_Score, Nome)
# dataset = dataset.drop_duplicates()

# Preparação dos dados
df = dataset  # Power BI fornece automaticamente
df_grouped = df.groupby("Nome")["Final_Score"].mean().reset_index()
df_grouped["Score"] = df_grouped["Final_Score"].round(2)

# Organização das faixas e rótulos
unique_scores = sorted(df_grouped["Score"].unique())
labels_por_score = {score: [] for score in unique_scores}
for idx, row in df_grouped.iterrows():
    labels_por_score[row["Score"]].append((idx, row["Nome"]))

# Ajustes para posicionamento
ajuste_vertical = 0.05
y_centro = 1.14
y_acima_base = 1.22
y_abaixo_base = 1.06
faixa_alternada = {}

# Definição do gradiente de cores
cmap = LinearSegmentedColormap.from_list("termo", ["#F8C8DC", "#800020"])
fig, ax = plt.subplots(figsize=(24, 10))
gradient = np.linspace(0, 1, 1800).reshape(1, -1)
ax.imshow(gradient, aspect='auto', cmap=cmap, extent=[0, 1, y_centro-0.02, y_centro+0.02], zorder=1)

# Construção da base do termômetro
tick_scores = [i / 100 for i in range(0, 101, 10)]
tick_y = y_centro - 0.05
for score in tick_scores:
    ax.plot([score, score], [tick_y+0.018, y_centro-0.02], ls=':', lw=2.0, color='lightgray', zorder=1)
    ax.text(score, tick_y, f"{int(score*100)}%", ha='center', va='bottom', fontsize=23, fontweight='bold', color='#444', zorder=12)

# Posicionamento das competências
for score, labels in labels_por_score.items():
    if not labels:
        continue

    if score not in faixa_alternada:
        faixa_alternada[score] = 'acima' if (int(score * 100) // 10) % 2 == 0 else 'abaixo'

    direcao = 1 if faixa_alternada[score] == 'acima' else -1
    y_base = y_acima_base if direcao == 1 else y_abaixo_base
    va = 'bottom' if direcao == 1 else 'top'
    seta_yini = y_centro + 0.01 if direcao == 1 else y_centro - 0.01
    seta_yfinal_base = y_base - 0.003 if direcao == 1 else y_base + 0.003

    ax.annotate('', xy=(score, seta_yfinal_base), xytext=(score, seta_yini),
                arrowprops=dict(arrowstyle='->', lw=1.4, color='gray', linestyle='-'), zorder=2)

    for pos, (idx, nome) in enumerate(labels):
        y = y_base + direcao * pos * ajuste_vertical
        fonte = 15 if len(nome) <= 30 else 13
        ax.text(score, y, nome, ha='center', va=va, fontsize=fonte, fontweight='bold', zorder=10)

# Ajustes finais
ax.set_xlim(-0.03, 1.03)
ax.set_ylim(1.0, 1.4)
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
plt.tight_layout()
plt.show()
