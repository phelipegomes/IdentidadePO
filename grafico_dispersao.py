# O código a seguir para criar um dataframe e remover as linhas duplicadas sempre é executado e age como um preâmbulo para o script: 

# dataset = pandas.DataFrame(Nome, Id_Tribo, Score_Profissional_Auto, Score_Profissional_Comite, Media_Empresa_Auto, Media_Tribo_Auto, Media_Empresa_Comite, Media_Tribo_Comite)
# dataset = dataset.drop_duplicates()

# Cole ou digite aqui seu código de script:

import matplotlib.pyplot as plt
import numpy as np

df = dataset.copy()

X_MIN, X_MAX = 10, 39
Y_MIN, Y_MAX = 10, 39

LABEL_BOX_W = 1.2
LABEL_BOX_H = 0.45
LABEL_ADJUST_MAX_ITER = 50

OFFSET_X = 0.6
OFFSET_Y = 0.4

def jitter_coords(coords, pontos_fixos=None, threshold=0.01, jitter_amount=0.15):
    coords = coords.copy()
    n = coords.shape[0]
    for i in range(n):
        for j in range(i+1, n):
            dist = np.linalg.norm(coords[i] - coords[j])
            if dist < threshold:
                angle = np.random.uniform(0, 2*np.pi)
                coords[j,0] += jitter_amount * np.cos(angle)
                coords[j,1] += jitter_amount * np.sin(angle)
        if pontos_fixos is not None:
            for pf in pontos_fixos:
                while np.linalg.norm(coords[i] - pf) < 0.15:
                    angle = np.random.uniform(0, 2*np.pi)
                    coords[i,0] += 0.15*np.cos(angle)
                    coords[i,1] += 0.15*np.sin(angle)
    return coords

def checa_colisao_box(x1, y1, w1, h1, x2, y2, w2, h2):
    return (abs(x1 - x2) * 2 < (w1 + w2)) and (abs(y1 - y2) * 2 < (h1 + h2))

def posicoes_candidatas(bolinha):
    return [
        (OFFSET_X, 0, 'left', 'center'),     
        (-OFFSET_X, 0, 'right', 'center'),   
        (0, OFFSET_Y, 'center', 'bottom'),  
        (0, -OFFSET_Y, 'center', 'top'),    
        (OFFSET_X, OFFSET_Y, 'left', 'bottom'),   
        (-OFFSET_X, OFFSET_Y, 'right', 'bottom'), 
        (OFFSET_X, -OFFSET_Y, 'left', 'top'),     
        (-OFFSET_X, -OFFSET_Y, 'right', 'top')    
    ]

def posiciona_labels(bolinhas):
    n = len(bolinhas)
    labels = [None]*n
    for i in range(n):
        dx, dy, ha, va = posicoes_candidatas(bolinhas[i])[0]
        labels[i] = [bolinhas[i][0] + dx, bolinhas[i][1] + dy, ha, va, 0]

    for _ in range(LABEL_ADJUST_MAX_ITER):
        mudou = False
        for i in range(n):
            x_lab_i, y_lab_i, ha_i, va_i, idx_i = labels[i]
            bol_x_i, bol_y_i = bolinhas[i]
            w_i, h_i = LABEL_BOX_W, LABEL_BOX_H

            colidiu_bolinha = any(
                checa_colisao_box(x_lab_i, y_lab_i, w_i, h_i, bolinhas[j][0], bolinhas[j][1], 0.15, 0.15)
                for j in range(n) if j != i
            )

            colidiu_label = any(
                checa_colisao_box(x_lab_i, y_lab_i, w_i, h_i, labels[k][0], labels[k][1], w_i, h_i)
                for k in range(n) if k != i and labels[k] is not None
            )

            if colidiu_bolinha or colidiu_label:
                idx_novo = (idx_i + 1) % len(posicoes_candidatas(bolinhas[i]))
                dx, dy, ha, va = posicoes_candidatas(bolinhas[i])[idx_novo]
                labels[i] = [bolinhas[i][0] + dx, bolinhas[i][1] + dy, ha, va, idx_novo]
                mudou = True

        if not mudou:
            break

    # Ajuste final para colisões
    for i in range(n):
        x_lab, y_lab, ha, va, idx = labels[i]
        bol_x, bol_y = bolinhas[i]
        dx, dy, _, _ = posicoes_candidatas(bolinhas[i])[idx]
        distancia_extra = 0.0
        while True:
            colidiu = False
            for j in range(n):
                if i == j:
                    continue
                if checa_colisao_box(x_lab, y_lab, LABEL_BOX_W, LABEL_BOX_H, bolinhas[j][0], bolinhas[j][1], 0.15, 0.15):
                    colidiu = True
                    break
                if labels[j] is not None:
                    x_lab_j, y_lab_j, _, _, _ = labels[j]
                    if checa_colisao_box(x_lab, y_lab, LABEL_BOX_W, LABEL_BOX_H, x_lab_j, y_lab_j, LABEL_BOX_W, LABEL_BOX_H):
                        colidiu = True
                        break
            if not colidiu:
                break
            distancia_extra += 0.2
            x_lab = bol_x + dx*(1 + distancia_extra)
            y_lab = bol_y + dy*(1 + distancia_extra)
            labels[i][0] = x_lab
            labels[i][1] = y_lab

    return [(x, y, ha, va) for x, y, ha, va, _ in labels]

def desenha_linha_curva(ax, start, end, color='gray', lw=0.8, alpha=0.7, zorder=2):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    dist = np.hypot(dx, dy)
    if dist == 0:
        dist = 0.1
    perp_x = -dy / dist
    perp_y = dx / dist
    ctrl_dist = dist * 0.3
    sinal = 1 if (start[0] + start[1]) % 2 == 0 else -1
    ctrl_x = start[0] + dx/2 + sinal * perp_x * ctrl_dist
    ctrl_y = start[1] + dy/2 + sinal * perp_y * ctrl_dist

    t = np.linspace(0,1,20)
    xs = (1-t)**2 * start[0] + 2*(1-t)*t*ctrl_x + t**2*end[0]
    ys = (1-t)**2 * start[1] + 2*(1-t)*t*ctrl_y + t**2*end[1]
    ax.plot(xs, ys, color=color, lw=lw, alpha=alpha, linestyle='--', zorder=zorder)

# ---------- Preparar dados ---------- #
df_profs = df[['Nome', 'Score_Profissional_Auto', 'Score_Profissional_Comite']].copy().reset_index(drop=True)

# Calcular médias da tribo e da empresa no filtro atual
if 'Media_Empresa_Auto' in df.columns and not df['Media_Empresa_Auto'].isna().all():
    media_empresa = np.array([df['Media_Empresa_Auto'].mean(), df['Media_Empresa_Comite'].mean()])
else:
    media_empresa = None

if 'Media_Tribo_Auto' in df.columns and not df['Media_Tribo_Auto'].isna().all():
    media_tribo = np.array([df['Media_Tribo_Auto'].mean(), df['Media_Tribo_Comite'].mean()])
else:
    media_tribo = None

# Jitter profissionais para não sobrepor médias
pontos_fixos = []
if media_empresa is not None: pontos_fixos.append(media_empresa)
if media_tribo is not None: pontos_fixos.append(media_tribo)

coords = df_profs[['Score_Profissional_Auto','Score_Profissional_Comite']].to_numpy(dtype=float)
coords_jittered = jitter_coords(coords, pontos_fixos=pontos_fixos)
bolinhas = [(x,y) for x,y in coords_jittered]

# ---------- Plot ---------- #
fig, ax = plt.subplots(figsize=(10, 8))

# Bolinhas profissionais
for x, y in bolinhas:
    ax.scatter(x, y, color='#ec4f94', s=60, edgecolors='black', zorder=4)

# Labels profissionais
labels_pos = posiciona_labels(bolinhas)
for i, (lx, ly, ha, va) in enumerate(labels_pos):
    desenha_linha_curva(ax, bolinhas[i], (lx, ly))
    ax.text(lx, ly, df_profs.iloc[i]['Nome'], fontsize=7, color='white',
            ha=ha, va=va,
            bbox=dict(facecolor='black', alpha=0.75, boxstyle='round,pad=0.3'), zorder=10)

# Média Empresa
if media_empresa is not None:
    ax.scatter(media_empresa[0], media_empresa[1],
               color='red', s=100, edgecolors='black', label='Média Empresa', zorder=5)

# Média Tribo
if media_tribo is not None:
    ax.scatter(media_tribo[0], media_tribo[1],
               color='#59b16a', s=100, edgecolors='black', label='Média Tribo', zorder=5)

# Linha de referência
ax.plot([X_MIN, X_MAX], [X_MIN, X_MAX], linestyle='--', color='gray', label='Auto = Comitê', zorder=1)

ax.set_xlabel('Soma das Notas - Autoavaliação')
ax.set_ylabel('Soma das Notas - Avaliação do Comitê')
ax.set_title('Mapa de Dispersão: Empresa vs Tribo', fontsize=16)
ax.set_xlim(X_MIN, X_MAX)
ax.set_ylim(Y_MIN, Y_MAX)
ax.grid(True, linestyle=':', linewidth=0.7, alpha=0.6)
ax.legend(loc='lower right')

plt.tight_layout()
plt.show()






