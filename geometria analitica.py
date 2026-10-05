"""
📐 Geometria Analítica Visual
==============================
Executar com: streamlit run geometria_analitica.py

9 abas interativas — equações, parâmetros e gráficos em tempo real:
  1. Distância entre dois pontos
  2. Ponto médio
  3. Baricentro do triângulo
  4. Área por determinante
  5. Equação da reta
  6. Cônicas (geral)
  7. Parábola
  8. Elipse
  9. Hipérbole
"""

import math
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ────────────────────────────────────────────────────────────
# PÁGINA
# ────────────────────────────────────────────────────────────
st.set_page_config(page_title="Geometria Analítica Visual", page_icon="📐", layout="wide")
st.markdown("""
<style>
.main-title{font-size:2.2rem;font-weight:800;color:#0f172a;text-align:center;margin-bottom:.3rem}
.subtitle{font-size:1.05rem;color:#64748b;text-align:center;margin-bottom:1.4rem}
.card{background:#f8fafc;border-radius:12px;padding:1.1rem 1.3rem;
      border-left:4px solid #3b82f6;margin-bottom:.9rem;color:#334155;line-height:1.6}
.form{background:#f0fdf4;border-radius:10px;padding:.7rem 1.2rem;
      border-left:4px solid #10b981;margin:.5rem 0;color:#065f46;font-size:1.05rem}
.warn{background:#fffbeb;border-radius:10px;padding:.7rem 1.2rem;
      border-left:4px solid #f59e0b;margin:.5rem 0;color:#78350f}
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────
# UTILITÁRIOS DE LAYOUT
# ────────────────────────────────────────────────────────────
def mostrar(fig, h=460):
    fig.update_layout(height=h, plot_bgcolor="white", paper_bgcolor="white",
                      margin=dict(l=10, r=10, t=50, b=10),
                      font=dict(family="sans-serif", size=13))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def eixos_iguais(fig, xs, ys, pad=1.0, row=1, col=1):
    """Grade limpa com eixos proporcionais."""
    mn = min(min(xs)-pad, min(ys)-pad)
    mx = max(max(xs)+pad, max(ys)+pad)
    fig.update_xaxes(range=[mn, mx], zeroline=True, zerolinecolor="#94a3b8",
                     gridcolor="#e2e8f0", showgrid=True, row=row, col=col)
    fig.update_yaxes(range=[mn, mx], zeroline=True, zerolinecolor="#94a3b8",
                     gridcolor="#e2e8f0", scaleanchor=f"x{'' if (row==1 and col==1) else row}",
                     scaleratio=1, row=row, col=col)

def ponto(fig, x, y, nome, cor="#ef4444", tamanho=12, row=1, col=1):
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text",
        name=nome, text=[nome], textposition="top right",
        textfont=dict(size=13, color=cor),
        marker=dict(size=tamanho, color=cor, line=dict(color="white", width=1.5)),
        hovertemplate=f"{nome} = ({x:.3f}, {y:.3f})<extra></extra>"), row=row, col=col)

def segmento(fig, x0, y0, x1, y1, cor="#3b82f6", dash="solid", nome="", row=1, col=1):
    fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines",
        name=nome, line=dict(color=cor, width=2, dash=dash),
        hoverinfo="skip", showlegend=bool(nome)), row=row, col=col)

def formula(latex_str):
    st.latex(latex_str)

def quiz(chave, enunciado, opcoes, correta, explicacao):
    with st.expander("🎯 Teste sua intuição"):
        r = st.radio(enunciado, opcoes, index=None, key=f"q_{chave}")
        if r is not None:
            if opcoes.index(r) == correta:
                st.success(f"✅ {explicacao}")
            else:
                st.warning("🤔 Não ainda — observe o gráfico e tente de novo.")

# Paleta
COR = dict(A="#ef4444", B="#3b82f6", C="#10b981", M="#f59e0b",
           G="#8b5cf6", seg="#64748b", reta="#06b6d4", area="#fde68a")

# ────────────────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configurações")
    mostrar_formulas = st.checkbox("Mostrar fórmulas e contas", value=True)
    st.markdown("---")
    st.subheader("🧑‍🏫 Como usar")
    st.markdown("Cada aba é **independente**: ajuste os controles e o gráfico atualiza em tempo real.\n\n"
                "Desmarque *Mostrar fórmulas* para focar nos gráficos com alunos do fundamental.")
    st.markdown("---")
    st.caption("Cores: 🔴 A · 🔵 B · 🟢 C · 🟡 M/G")

# ────────────────────────────────────────────────────────────
# TÍTULO
# ────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">📐 Geometria Analítica Visual</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pontos, retas e cônicas — altere os parâmetros e veja a geometria ganhar vida</div>',
    unsafe_allow_html=True)

tabs = st.tabs([
    "1. Distância", "2. Ponto Médio", "3. Baricentro",
    "4. Área (det)", "5. Equação da Reta",
    "6. Cônicas", "7. Parábola", "8. Elipse", "9. Hipérbole",
])

# ══════════════════════════════════════════════════════════════
# ABA 1 — DISTÂNCIA ENTRE DOIS PONTOS
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("""<div class="card">
    A <b>distância</b> entre dois pontos A(x₁,y₁) e B(x₂,y₂) no plano cartesiano vem diretamente
    do Teorema de Pitágoras: os catetos são as diferenças nas coordenadas e a hipotenusa é a distância.
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2.3])
    with c1:
        with st.container(border=True):
            st.markdown("**Ponto A**")
            ax = st.slider("xₐ", -8.0, 8.0, -3.0, 0.5, key="ax_d")
            ay = st.slider("yₐ", -8.0, 8.0, -2.0, 0.5, key="ay_d")
            st.markdown("**Ponto B**")
            bx = st.slider("x_b", -8.0, 8.0, 4.0, 0.5, key="bx_d")
            by = st.slider("y_b", -8.0, 8.0, 3.0, 0.5, key="by_d")
        dx, dy = bx - ax, by - ay
        d = math.hypot(dx, dy)
        st.metric("Distância AB", f"{d:.4f}")
        if mostrar_formulas:
            st.markdown('<div class="form">', unsafe_allow_html=True)
            formula(r"d(A,B)=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}")
            st.markdown(f"Δx = {bx} − ({ax}) = **{dx:.2f}**  \nΔy = {by} − ({ay}) = **{dy:.2f}**")
            formula(rf"d=\sqrt{{{dx:.2f}^2+{dy:.2f}^2}}=\sqrt{{{dx**2+dy**2:.4f}}}={d:.4f}")
            st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        fig = go.Figure()
        # triângulo retângulo auxiliar
        fig.add_trace(go.Scatter(x=[ax, bx, bx, ax], y=[ay, ay, by, ay],
            mode="lines", line=dict(color="#e2e8f0", width=1.5, dash="dot"),
            fill="toself", fillcolor="rgba(226,232,240,.35)", hoverinfo="skip", showlegend=False))
        # catetos
        segmento(fig, ax, ay, bx, ay, cor="#94a3b8", dash="dash", nome="Δx")
        segmento(fig, bx, ay, bx, by, cor="#94a3b8", dash="dash", nome="Δy")
        # hipotenusa
        segmento(fig, ax, ay, bx, by, cor=COR["seg"], nome="d(A,B)")
        # rótulos catetos
        fig.add_trace(go.Scatter(x=[(ax+bx)/2], y=[ay-.5], mode="text",
            text=[f"Δx = {dx:.2f}"], textfont=dict(size=12, color="#64748b"), hoverinfo="skip", showlegend=False))
        fig.add_trace(go.Scatter(x=[bx+.4], y=[(ay+by)/2], mode="text",
            text=[f"Δy = {dy:.2f}"], textfont=dict(size=12, color="#64748b"), hoverinfo="skip", showlegend=False))
        # rótulo distância
        mx, my = (ax+bx)/2, (ay+by)/2
        fig.add_trace(go.Scatter(x=[mx+.3], y=[my+.3], mode="text",
            text=[f"d = {d:.3f}"], textfont=dict(size=13, color="#0f172a", family="monospace"),
            hoverinfo="skip", showlegend=False))
        ponto(fig, ax, ay, f"A({ax},{ay})", COR["A"])
        ponto(fig, bx, by, f"B({bx},{by})", COR["B"])
        eixos_iguais(fig, [ax, bx], [ay, by])
        fig.update_layout(title="Distância entre A e B — Teorema de Pitágoras", showlegend=True,
                          legend=dict(orientation="h", y=-.15))
        mostrar(fig)
    quiz("d1", "Se A=(0,0) e B=(3,4), a distância AB é:",
         ["5","7","12","√7"], 0, "√(9+16)=√25=5. Triângulo 3-4-5 pitagórico!")

# ══════════════════════════════════════════════════════════════
# ABA 2 — PONTO MÉDIO
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("""<div class="card">
    O <b>ponto médio</b> M de um segmento AB é o ponto equidistante dos dois extremos.
    Suas coordenadas são a <b>média aritmética</b> das coordenadas de A e B.
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2.3])
    with c1:
        with st.container(border=True):
            st.markdown("**Ponto A**")
            ax2 = st.slider("xₐ", -8.0, 8.0, -4.0, 0.5, key="ax_m")
            ay2 = st.slider("yₐ", -8.0, 8.0, 2.0, 0.5, key="ay_m")
            st.markdown("**Ponto B**")
            bx2 = st.slider("x_b", -8.0, 8.0, 6.0, 0.5, key="bx_m")
            by2 = st.slider("y_b", -8.0, 8.0, -4.0, 0.5, key="by_m")

        mx2, my2 = (ax2+bx2)/2, (ay2+by2)/2
        dAM = math.hypot(mx2-ax2, my2-ay2)
        dMB = math.hypot(bx2-mx2, by2-my2)
        st.metric("M (xₘ, yₘ)", f"({mx2:.2f}, {my2:.2f})")
        col_a, col_b = st.columns(2)
        col_a.metric("d(A,M)", f"{dAM:.4f}")
        col_b.metric("d(M,B)", f"{dMB:.4f}")
        if mostrar_formulas:
            st.markdown('<div class="form">', unsafe_allow_html=True)
            formula(r"M=\left(\frac{x_1+x_2}{2},\;\frac{y_1+y_2}{2}\right)")
            formula(rf"x_M=\frac{{{ax2}+{bx2}}}{{2}}={mx2:.2f}")
            formula(rf"y_M=\frac{{{ay2}+{by2}}}{{2}}={my2:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        fig2 = go.Figure()
        segmento(fig2, ax2, ay2, bx2, by2, cor=COR["seg"], nome="AB")
        segmento(fig2, ax2, ay2, mx2, my2, cor=COR["A"], dash="dot", nome="AM")
        segmento(fig2, mx2, my2, bx2, by2, cor=COR["B"], dash="dot", nome="MB")
        # marcas iguais no segmento
        for t, cor in [(0.5, COR["M"])]:
            xi, yi = ax2 + t*(bx2-ax2), ay2 + t*(by2-ay2)
            fig2.add_trace(go.Scatter(x=[xi], y=[yi], mode="markers",
                marker=dict(size=8, symbol="x", color=cor), hoverinfo="skip", showlegend=False))
        ponto(fig2, ax2, ay2, f"A({ax2},{ay2})", COR["A"])
        ponto(fig2, bx2, by2, f"B({bx2},{by2})", COR["B"])
        ponto(fig2, mx2, my2, f"M({mx2:.1f},{my2:.1f})", COR["M"], tamanho=14)
        eixos_iguais(fig2, [ax2, bx2, mx2], [ay2, by2, my2])
        fig2.update_layout(title="Ponto médio M equidistante de A e B",
                           legend=dict(orientation="h", y=-.15))
        mostrar(fig2)
    quiz("pm1", "Ponto médio de A(−2,4) e B(6,−2) é:",
         ["(2,1)","(4,2)","(2,−1)","(1,2)"], 0,
         "xₘ=(−2+6)/2=2, yₘ=(4+(−2))/2=1 → M(2,1).")

# ══════════════════════════════════════════════════════════════
# ABA 3 — BARICENTRO DO TRIÂNGULO
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("""<div class="card">
    O <b>baricentro</b> G é o ponto de intersecção das três medianas de um triângulo.
    Suas coordenadas são a média aritmética das coordenadas dos três vértices.
    G divide cada mediana em <b>2:1</b> a partir do vértice.
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2.3])
    with c1:
        with st.container(border=True):
            st.markdown("**Vértice A**")
            ax3 = st.slider("xₐ", -8.0, 8.0, -4.0, 0.5, key="ax_b")
            ay3 = st.slider("yₐ", -8.0, 8.0, -3.0, 0.5, key="ay_b")
            st.markdown("**Vértice B**")
            bx3 = st.slider("x_b", -8.0, 8.0, 4.0, 0.5, key="bx_b")
            by3 = st.slider("y_b", -8.0, 8.0, -3.0, 0.5, key="by_b")
            st.markdown("**Vértice C**")
            cx3 = st.slider("x_c", -8.0, 8.0, 0.0, 0.5, key="cx_b")
            cy3 = st.slider("y_c", -8.0, 8.0, 5.0, 0.5, key="cy_b")

        gx, gy = (ax3+bx3+cx3)/3, (ay3+by3+cy3)/3
        # Verificar se é triângulo degenerado
        area_b = abs((bx3-ax3)*(cy3-ay3) - (cx3-ax3)*(by3-ay3))/2
        st.metric("Baricentro G", f"({gx:.3f}, {gy:.3f})")
        st.metric("Área do triângulo", f"{area_b:.3f} u²")
        if mostrar_formulas:
            st.markdown('<div class="form">', unsafe_allow_html=True)
            formula(r"G=\left(\frac{x_A+x_B+x_C}{3},\;\frac{y_A+y_B+y_C}{3}\right)")
            formula(rf"G=\left(\frac{{{ax3}+{bx3}+{cx3}}}{{3}},\frac{{{ay3}+{by3}+{cy3}}}{{3}}\right)=({gx:.3f},{gy:.3f})")
            st.markdown('</div>', unsafe_allow_html=True)
        if area_b < 0.01:
            st.markdown('<div class="warn">⚠ Vértices colineares — não formam um triângulo.</div>',
                        unsafe_allow_html=True)
    with c2:
        fig3 = go.Figure()
        # triângulo
        fig3.add_trace(go.Scatter(
            x=[ax3,bx3,cx3,ax3], y=[ay3,by3,cy3,ay3],
            mode="lines", fill="toself", fillcolor="rgba(59,130,246,.10)",
            line=dict(color=COR["seg"], width=2), hoverinfo="skip", showlegend=False))
        # medianas: vértice → ponto médio do lado oposto
        medianas = [
            (ax3, ay3, (bx3+cx3)/2, (by3+cy3)/2, "Mediana A"),
            (bx3, by3, (ax3+cx3)/2, (ay3+cy3)/2, "Mediana B"),
            (cx3, cy3, (ax3+bx3)/2, (ay3+by3)/2, "Mediana C"),
        ]
        cores_med = ["#f97316","#a855f7","#06b6d4"]
        for (x0,y0,x1,y1,nm), cor in zip(medianas, cores_med):
            fig3.add_trace(go.Scatter(x=[x0,x1], y=[y0,y1], mode="lines",
                name=nm, line=dict(color=cor, width=1.8, dash="dash"), hoverinfo="skip"))
            ponto(fig3, x1, y1, f"M_{nm[-1]}", cor, tamanho=8)

        ponto(fig3, ax3, ay3, f"A({ax3},{ay3})", COR["A"])
        ponto(fig3, bx3, by3, f"B({bx3},{by3})", COR["B"])
        ponto(fig3, cx3, cy3, f"C({cx3},{cy3})", COR["C"])
        ponto(fig3, gx, gy, f"G({gx:.2f},{gy:.2f})", COR["G"], tamanho=15)
        eixos_iguais(fig3, [ax3,bx3,cx3,gx], [ay3,by3,cy3,gy])
        fig3.update_layout(title="Baricentro G — intersecção das medianas",
                           legend=dict(orientation="h", y=-.18))
        mostrar(fig3, 500)
    quiz("bar1", "O baricentro de A(0,0), B(6,0) e C(0,6) é:",
         ["(3,3)","(2,2)","(6,6)","(1,1)"], 1,
         "G=((0+6+0)/3,(0+0+6)/3)=(2,2).")

# ══════════════════════════════════════════════════════════════
# ABA 4 — ÁREA POR DETERMINANTE
# ══════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("""<div class="card">
    A <b>área de um triângulo</b> cujos vértices são conhecidos pode ser calculada com o valor absoluto
    de um <b>determinante 3×3</b> (regra de Sarrus). Basta ½|det|.
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2.3])
    with c1:
        with st.container(border=True):
            st.markdown("**Vértice A**")
            ax4 = st.slider("xₐ", -8.0, 8.0, -3.0, 0.5, key="ax_ar")
            ay4 = st.slider("yₐ", -8.0, 8.0, -2.0, 0.5, key="ay_ar")
            st.markdown("**Vértice B**")
            bx4 = st.slider("x_b", -8.0, 8.0, 5.0, 0.5, key="bx_ar")
            by4 = st.slider("y_b", -8.0, 8.0, -2.0, 0.5, key="by_ar")
            st.markdown("**Vértice C**")
            cx4 = st.slider("x_c", -8.0, 8.0, 1.0, 0.5, key="cx_ar")
            cy4 = st.slider("y_c", -8.0, 8.0, 5.0, 0.5, key="cy_ar")

        # det = x_A(y_B-y_C) + x_B(y_C-y_A) + x_C(y_A-y_B)
        det = ax4*(by4-cy4) + bx4*(cy4-ay4) + cx4*(ay4-by4)
        area4 = abs(det) / 2
        st.metric("Área do triângulo", f"{area4:.4f} u²")
        if mostrar_formulas:
            st.markdown('<div class="form">', unsafe_allow_html=True)
            formula(r"A=\frac{1}{2}\left|\det\begin{pmatrix}x_A&y_A&1\\x_B&y_B&1\\x_C&y_C&1\end{pmatrix}\right|")
            formula(rf"\det={ax4}({by4}-{cy4})+{bx4}({cy4}-{ay4})+{cx4}({ay4}-{by4})={det:.2f}")
            formula(rf"A=\frac{{1}}{{2}}|{det:.2f}|={area4:.4f}")
            st.markdown('</div>', unsafe_allow_html=True)
            # matriz visual
            st.markdown("**Matriz do determinante:**")
            st.table({
                "x": [ax4, bx4, cx4],
                "y": [ay4, by4, cy4],
                "1": [1, 1, 1],
            })
        if area4 < 0.01:
            st.markdown('<div class="warn">⚠ Pontos colineares — área nula.</div>', unsafe_allow_html=True)
    with c2:
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=[ax4,bx4,cx4,ax4], y=[ay4,by4,cy4,ay4],
            mode="lines", fill="toself", fillcolor="rgba(253,230,138,.5)",
            line=dict(color="#d97706", width=2.5), hoverinfo="skip", showlegend=False))
        # Altura visual (do C até lado AB)
        if abs(bx4-ax4) > 0.01:
            m = (by4-ay4)/(bx4-ax4)
            xh = (cx4 + m*cy4 - m*ay4 + m*m*ax4)/(1+m*m)
            yh = ay4 + m*(xh-ax4)
            segmento(fig4, cx4, cy4, xh, yh, cor="#ef4444", dash="dot", nome="altura")
            fig4.add_trace(go.Scatter(x=[xh], y=[yh], mode="markers",
                marker=dict(size=8, symbol="square", color="#ef4444"),
                hoverinfo="skip", showlegend=False))
        # Rótulo da área no centroide
        gx4, gy4 = (ax4+bx4+cx4)/3, (ay4+by4+cy4)/3
        fig4.add_trace(go.Scatter(x=[gx4], y=[gy4], mode="text",
            text=[f"A = {area4:.3f}"], textfont=dict(size=14, color="#92400e"),
            hoverinfo="skip", showlegend=False))
        ponto(fig4, ax4, ay4, f"A({ax4},{ay4})", COR["A"])
        ponto(fig4, bx4, by4, f"B({bx4},{by4})", COR["B"])
        ponto(fig4, cx4, cy4, f"C({cx4},{cy4})", COR["C"])
        eixos_iguais(fig4, [ax4,bx4,cx4], [ay4,by4,cy4])
        fig4.update_layout(title="Área por determinante (região colorida)", showlegend=True,
                           legend=dict(orientation="h", y=-.15))
        mostrar(fig4)
    quiz("ar1", "A(0,0), B(4,0), C(0,3). Área = ?",
         ["12","6","7","3.5"], 1, "Base 4, altura 3 → A=½×4×3=6. Pelo det: ½|4×3|=6.")

# ══════════════════════════════════════════════════════════════
# ABA 5 — EQUAÇÃO DA RETA
# ══════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("""<div class="card">
    Uma reta no plano pode ser definida de várias formas:
    <b>ponto + inclinação</b>, <b>dois pontos</b>, ou por <b>coeficientes lineares</b>.
    A equação geral é ax + by + c = 0; a reduzida é y = mx + n.
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2.3])
    with c1:
        modo_r = st.radio("Definir por", ["Inclinação + ponto", "Dois pontos", "Forma geral ax+by+c=0"],
                          key="modo_r", horizontal=False)
        if modo_r == "Inclinação + ponto":
            with st.container(border=True):
                m_r = st.slider("Inclinação m", -5.0, 5.0, 1.5, 0.1, key="m_r")
                x0_r = st.slider("x₀ (ponto na reta)", -6.0, 6.0, 0.0, 0.5, key="x0_r")
                y0_r = st.slider("y₀ (ponto na reta)", -6.0, 6.0, 0.0, 0.5, key="y0_r")
            n_r = y0_r - m_r * x0_r
            a_r, b_r, c_r = m_r, -1.0, n_r
            reta_fn = lambda x: m_r * x + n_r
            ang = math.degrees(math.atan(m_r))
        elif modo_r == "Dois pontos":
            with st.container(border=True):
                x0_r = st.slider("x₁", -6.0, 6.0, -3.0, 0.5, key="x1_r2")
                y0_r = st.slider("y₁", -6.0, 6.0, -1.0, 0.5, key="y1_r2")
                x2_r = st.slider("x₂", -6.0, 6.0, 3.0, 0.5, key="x2_r2")
                y2_r = st.slider("y₂", -6.0, 6.0, 4.0, 0.5, key="y2_r2")
            if abs(x2_r - x0_r) < 0.01:
                m_r = None; n_r = None
                a_r, b_r, c_r = 1.0, 0.0, -x0_r
                reta_fn = None
                ang = 90.0
            else:
                m_r = (y2_r - y0_r) / (x2_r - x0_r)
                n_r = y0_r - m_r * x0_r
                a_r, b_r, c_r = m_r, -1.0, n_r
                reta_fn = lambda x: m_r * x + n_r
                ang = math.degrees(math.atan(m_r))
        else:  # forma geral
            with st.container(border=True):
                a_r = st.slider("a", -5.0, 5.0, 2.0, 0.5, key="a_rg")
                b_r = st.slider("b", -5.0, 5.0, -1.0, 0.5, key="b_rg")
                c_r = st.slider("c", -10.0, 10.0, 3.0, 0.5, key="c_rg")
            if abs(b_r) > 0.01:
                m_r = -a_r / b_r
                n_r = -c_r / b_r
                reta_fn = lambda x: m_r * x + n_r
                ang = math.degrees(math.atan(m_r))
            else:
                m_r = None; n_r = None; reta_fn = None; ang = 90.0
            x0_r = 0.0; y0_r = n_r if n_r is not None else 0.0

        if m_r is not None:
            st.metric("Coeficiente angular m", f"{m_r:.4f}")
            st.metric("Coeficiente linear n", f"{n_r:.4f}")
            st.metric("Ângulo de inclinação", f"{ang:.1f}°")
        else:
            st.info(f"Reta vertical: x = {-c_r/a_r:.2f}")

        if mostrar_formulas and m_r is not None:
            st.markdown('<div class="form">', unsafe_allow_html=True)
            formula(r"y = mx + n")
            formula(rf"y = {m_r:.3f}\,x + ({n_r:.3f})")
            formula(rf"{a_r:.2f}x + {b_r:.2f}y + {c_r:.2f} = 0")
            if m_r != 0:
                xi = -n_r/m_r
                formula(rf"\text{{zeros: }} x_0={xi:.3f},\; y_0={n_r:.3f}")
            st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        fig5 = go.Figure()
        xr = np.linspace(-9, 9, 300)
        if reta_fn is not None:
            yr = reta_fn(xr)
            fig5.add_trace(go.Scatter(x=xr, y=yr, mode="lines",
                name=f"y={m_r:.2f}x+{n_r:.2f}",
                line=dict(color=COR["reta"], width=3),
                hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>"))
            # interseções
            if abs(m_r) > 0.001:
                xi = -n_r/m_r
                fig5.add_vline(x=0, line=dict(color="#94a3b8", width=1))
                ponto(fig5, 0, n_r, f"(0,{n_r:.2f})", "#10b981")
                ponto(fig5, xi, 0, f"({xi:.2f},0)", "#f59e0b")
            ponto(fig5, x0_r, y0_r, f"P({x0_r},{y0_r:.1f})", COR["A"])
            if modo_r == "Dois pontos":
                ponto(fig5, x2_r, y2_r, f"Q({x2_r},{y2_r:.1f})", COR["B"])
        else:
            x_vert = -c_r/a_r if modo_r == "Forma geral ax+by+c=0" else x0_r
            fig5.add_vline(x=x_vert, line=dict(color=COR["reta"], width=3))
            ponto(fig5, x0_r, y0_r, f"P({x0_r},{y0_r:.1f})", COR["A"])
            if modo_r == "Dois pontos":
                ponto(fig5, x2_r, y2_r, f"Q({x2_r},{y2_r:.1f})", COR["B"])

        fig5.update_xaxes(range=[-9,9], zeroline=True, zerolinecolor="#94a3b8", gridcolor="#e2e8f0")
        fig5.update_yaxes(range=[-9,9], zeroline=True, zerolinecolor="#94a3b8", gridcolor="#e2e8f0")
        fig5.update_layout(title="Equação da reta no plano cartesiano",
                           showlegend=True, legend=dict(orientation="h", y=-.15))
        mostrar(fig5)

        # Comparar duas retas (paralela / perpendicular)
        with st.expander("🔀 Comparar com segunda reta"):
            m2 = st.slider("m₂ da segunda reta", -5.0, 5.0, -0.67, 0.1, key="m2_r")
            n2 = st.slider("n₂ da segunda reta", -6.0, 6.0, 2.0, 0.5, key="n2_r")
            if m_r is not None:
                paralelas = abs(m2 - m_r) < 0.05
                perp = abs(m2 * m_r + 1) < 0.08
                rel = "PARALELAS ∥" if paralelas else ("PERPENDICULARES ⊥" if perp else "Secantes")
                st.info(f"Relação: **{rel}** (m₁·m₂ = {m_r*m2:.3f})")
                fig5b = go.Figure()
                fig5b.add_trace(go.Scatter(x=xr, y=reta_fn(xr), mode="lines", name="Reta 1",
                    line=dict(color=COR["reta"], width=3)))
                fig5b.add_trace(go.Scatter(x=xr, y=m2*xr+n2, mode="lines", name="Reta 2",
                    line=dict(color="#f97316", width=3)))
                if not paralelas:
                    xi2 = (n2 - n_r) / (m_r - m2)
                    yi2 = m_r*xi2 + n_r
                    ponto(fig5b, xi2, yi2, f"I({xi2:.2f},{yi2:.2f})", "#8b5cf6")
                fig5b.update_xaxes(range=[-9,9], zeroline=True, zerolinecolor="#94a3b8", gridcolor="#e2e8f0")
                fig5b.update_yaxes(range=[-9,9], zeroline=True, zerolinecolor="#94a3b8", gridcolor="#e2e8f0",
                                   scaleanchor="x", scaleratio=1)
                mostrar(fig5b, 340)

    quiz("r1", "Duas retas com m₁=2 e m₂=−0,5 são:",
         ["Paralelas","Perpendiculares","Secantes comuns","Coincidentes"], 1,
         "m₁·m₂ = 2×(−0,5) = −1 → perpendiculares!")

# ══════════════════════════════════════════════════════════════
# ABA 6 — CÔNICAS (GERAL)
# ══════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("""<div class="card">
    As <b>cônicas</b> são curvas obtidas pela intersecção de um cone com um plano.
    A equação geral é <b>Ax² + Bxy + Cy² + Dx + Ey + F = 0</b>.
    O discriminante <b>B² − 4AC</b> classifica o tipo.
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2.3])
    with c1:
        with st.container(border=True):
            st.markdown("**Equação geral: Ax²+Bxy+Cy²+Dx+Ey+F=0**")
            A_c = st.slider("A", -3.0, 3.0, 1.0, 0.1, key="A_con")
            B_c = st.slider("B (rotação)", -3.0, 3.0, 0.0, 0.1, key="B_con")
            C_c = st.slider("C", -3.0, 3.0, 4.0, 0.1, key="C_con")
            D_c = st.slider("D", -5.0, 5.0, 0.0, 0.5, key="D_con")
            E_c = st.slider("E", -5.0, 5.0, 0.0, 0.5, key="E_con")
            F_c = st.slider("F", -20.0, 20.0, -4.0, 0.5, key="F_con")

        disc = B_c**2 - 4*A_c*C_c
        if abs(disc) < 0.01:
            tipo = "⭕ Parábola (B²−4AC = 0)"
        elif disc < 0:
            if abs(A_c-C_c) < 0.01 and abs(B_c) < 0.01:
                tipo = "⭕ Circunferência"
            else:
                tipo = "🥚 Elipse (B²−4AC < 0)"
        else:
            tipo = "🔀 Hipérbole (B²−4AC > 0)"

        st.info(f"**B²−4AC = {disc:.3f}**  →  {tipo}")
        if mostrar_formulas:
            st.markdown('<div class="form">', unsafe_allow_html=True)
            formula(r"Ax^2+Bxy+Cy^2+Dx+Ey+F=0")
            formula(r"\Delta = B^2-4AC \begin{cases} =0 &\text{Parábola}\\ <0 &\text{Elipse/Circ.}\\ >0 &\text{Hipérbole}\end{cases}")
            st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        x_g = np.linspace(-8, 8, 500)
        y_g = np.linspace(-8, 8, 500)
        X, Y = np.meshgrid(x_g, y_g)
        Z = A_c*X**2 + B_c*X*Y + C_c*Y**2 + D_c*X + E_c*Y + F_c

        fig6 = go.Figure()
        fig6.add_trace(go.Contour(x=x_g, y=y_g, z=Z,
            contours=dict(start=0, end=0, size=0.01, coloring="none",
                          showlabels=True, labelfont=dict(size=12)),
            line=dict(color="#3b82f6", width=3),
            colorscale=[[0,"#3b82f6"],[1,"#3b82f6"]],
            showscale=False, name="Cônica"))
        # preenchimento leve
        fig6.add_trace(go.Contour(x=x_g, y=y_g, z=Z,
            contours=dict(start=-0.5, end=0.5, size=1),
            colorscale=[[0,"rgba(59,130,246,.15)"],[1,"rgba(16,185,129,.15)"]],
            showscale=False, hoverinfo="skip", showlegend=False))
        fig6.update_xaxes(range=[-8,8], zeroline=True, zerolinecolor="#94a3b8", gridcolor="#e2e8f0")
        fig6.update_yaxes(range=[-8,8], zeroline=True, zerolinecolor="#94a3b8", gridcolor="#e2e8f0",
                          scaleanchor="x", scaleratio=1)
        fig6.update_layout(title=f"Cônica: {tipo}", showlegend=False)
        mostrar(fig6, 500)
    quiz("con1", "A equação x²+y²=25 representa:",
         ["Uma elipse","Uma circunferência","Uma parábola","Uma hipérbole"], 1,
         "A=C=1, B=0 → B²−4AC=−4<0 e A=C → circunferência de raio 5.")

# ══════════════════════════════════════════════════════════════
# ABA 7 — PARÁBOLA
# ══════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown("""<div class="card">
    A <b>parábola</b> é o lugar geométrico dos pontos equidistantes de um ponto fixo
    (<b>foco</b>) e de uma reta fixa (<b>diretriz</b>). O parâmetro <b>p</b> é a
    distância do vértice ao foco (e do vértice à diretriz).
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2.3])
    with c1:
        with st.container(border=True):
            tipo_p = st.radio("Eixo de simetria", ["Vertical (y=ax²+bx+c)", "Horizontal (x=ay²+by+c)"], key="tp_par")
            hv = st.slider("h (x do vértice)", -5.0, 5.0, 0.0, 0.5, key="h_par")
            kv = st.slider("k (y do vértice)", -5.0, 5.0, 0.0, 0.5, key="k_par")
            p_par = st.slider("p (dist. vértice→foco)", 0.2, 5.0, 1.0, 0.1, key="p_par")
            abre = st.radio("Abre para", ["cima/direita ➡↑", "baixo/esquerda ⬅↓"], key="ab_par")
            sinal_p = 1 if "cima" in abre else -1

        if tipo_p.startswith("Vertical"):
            a_par = 1 / (4 * p_par) * sinal_p
            x_par = np.linspace(hv-7, hv+7, 400)
            y_par = a_par * (x_par - hv)**2 + kv
            fx, fy = hv, kv + sinal_p * p_par
            dir_y = kv - sinal_p * p_par
            st.metric("Foco", f"({fx:.2f}, {fy:.2f})")
            st.metric("Diretriz", f"y = {dir_y:.2f}")
            if mostrar_formulas:
                st.markdown('<div class="form">', unsafe_allow_html=True)
                formula(r"(x-h)^2=4p(y-k)")
                formula(rf"(x-{hv:.1f})^2={4*sinal_p*p_par:.2f}(y-{kv:.1f})")
                formula(rf"a={a_par:.4f},\quad \text{{Foco}}=({fx:.2f},{fy:.2f})")
                formula(rf"\text{{Diretriz}}: y={dir_y:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            a_par = 1 / (4 * p_par) * sinal_p
            y_par = np.linspace(kv-7, kv+7, 400)
            x_par = a_par * (y_par - kv)**2 + hv
            fx, fy = hv + sinal_p * p_par, kv
            dir_x = hv - sinal_p * p_par
            st.metric("Foco", f"({fx:.2f}, {fy:.2f})")
            st.metric("Diretriz", f"x = {dir_x:.2f}")
            if mostrar_formulas:
                st.markdown('<div class="form">', unsafe_allow_html=True)
                formula(r"(y-k)^2=4p(x-h)")
                formula(rf"(y-{kv:.1f})^2={4*sinal_p*p_par:.2f}(x-{hv:.1f})")
                formula(rf"a={a_par:.4f},\quad \text{{Foco}}=({fx:.2f},{fy:.2f})")
                formula(rf"\text{{Diretriz}}: x={dir_x:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        fig7 = go.Figure()
        if tipo_p.startswith("Vertical"):
            fig7.add_trace(go.Scatter(x=x_par, y=y_par, mode="lines",
                name="Parábola", line=dict(color="#3b82f6", width=3)))
            # diretriz
            fig7.add_hline(y=dir_y, line=dict(color="#ef4444", width=2, dash="dash"),
                           annotation_text=f"Diretriz y={dir_y:.2f}",
                           annotation_position="right")
            # eixo de simetria
            fig7.add_vline(x=hv, line=dict(color="#94a3b8", width=1.5, dash="dot"))
            # reta focal (latus rectum)
            lr = 2 * p_par
            fig7.add_trace(go.Scatter(x=[hv-lr, hv+lr], y=[fy, fy], mode="lines",
                name=f"Latus rectum ({2*lr:.2f})", line=dict(color="#10b981", width=2, dash="dot")))
            ponto(fig7, hv, kv, f"V({hv},{kv})", COR["M"])
            ponto(fig7, fx, fy, f"F({fx:.2f},{fy:.2f})", COR["A"])
            eixos_iguais(fig7, [hv-6, hv+6], [kv-6, kv+6])
        else:
            fig7.add_trace(go.Scatter(x=x_par, y=y_par, mode="lines",
                name="Parábola", line=dict(color="#3b82f6", width=3)))
            fig7.add_vline(x=dir_x, line=dict(color="#ef4444", width=2, dash="dash"),
                           annotation_text=f"Diretriz x={dir_x:.2f}",
                           annotation_position="top")
            fig7.add_hline(y=kv, line=dict(color="#94a3b8", width=1.5, dash="dot"))
            lr = 2 * p_par
            fig7.add_trace(go.Scatter(x=[fx, fx], y=[kv-lr, kv+lr], mode="lines",
                name=f"Latus rectum ({2*lr:.2f})", line=dict(color="#10b981", width=2, dash="dot")))
            ponto(fig7, hv, kv, f"V({hv},{kv})", COR["M"])
            ponto(fig7, fx, fy, f"F({fx:.2f},{fy:.2f})", COR["A"])
            eixos_iguais(fig7, [hv-6, hv+6], [kv-6, kv+6])
        fig7.update_layout(title="Parábola: foco, vértice e diretriz",
                           legend=dict(orientation="h", y=-.15))
        mostrar(fig7, 500)
    quiz("par1", "Na parábola x²=8y, qual é a posição do foco?",
         ["(0,2)","(2,0)","(0,4)","(0,−2)"], 0,
         "4p=8 → p=2. Foco em (h,k+p)=(0,0+2)=(0,2).")

# ══════════════════════════════════════════════════════════════
# ABA 8 — ELIPSE
# ══════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown("""<div class="card">
    A <b>elipse</b> é o lugar geométrico dos pontos cuja <b>soma das distâncias a dois focos</b>
    é constante e igual a <b>2a</b>. Relação fundamental: <b>c² = a² − b²</b>, com <b>a > b > 0</b>.
    A <b>excentricidade</b> e = c/a mede o "achatamento" (0 = circunferência, → 1 = muito achatada).
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2.3])
    with c1:
        with st.container(border=True):
            hE = st.slider("h (centro x)", -4.0, 4.0, 0.0, 0.5, key="h_el")
            kE = st.slider("k (centro y)", -4.0, 4.0, 0.0, 0.5, key="k_el")
            aE = st.slider("a (semi-eixo maior)", 1.0, 8.0, 5.0, 0.2, key="a_el")
            
            # Trava para evitar min >= max no slider de b
            max_b = max(0.6, aE - 0.1)
            def_b = min(3.0, max_b)
            bE = st.slider("b (semi-eixo menor)", 0.5, max_b, def_b, 0.1, key="b_el")
            eixo_e = st.radio("Eixo maior ao longo de", ["x","y"], key="eixo_e")

        cE = math.sqrt(max(0.0, aE**2 - bE**2))
        exc = cE / aE
        if eixo_e == "x":
            f1x, f1y = hE - cE, kE
            f2x, f2y = hE + cE, kE
        else:
            f1x, f1y = hE, kE - cE
            f2x, f2y = hE, kE + cE

        st.metric("c (distância centro-foco)", f"{cE:.4f}")
        st.metric("Excentricidade e = c/a", f"{exc:.4f}")
        st.metric("Focos", f"F₁({f1x:.2f},{f1y:.2f})  F₂({f2x:.2f},{f2y:.2f})")
        if mostrar_formulas:
            st.markdown('<div class="form">', unsafe_allow_html=True)
            if eixo_e == "x":
                formula(rf"\frac{{(x-{hE})^2}}{{{aE:.2f}^2}}+\frac{{(y-{kE})^2}}{{{bE:.2f}^2}}=1")
            else:
                formula(rf"\frac{{(x-{hE})^2}}{{{bE:.2f}^2}}+\frac{{(y-{kE})^2}}{{{aE:.2f}^2}}=1")
            formula(r"c^2=a^2-b^2\qquad e=c/a")
            formula(rf"c=\sqrt{{{aE:.2f}^2-{bE:.2f}^2}}={cE:.4f}\qquad e={exc:.4f}")
            formula(r"d(P,F_1)+d(P,F_2)=2a")
            st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        t = np.linspace(0, 2*np.pi, 500)
        if eixo_e == "x":
            xE = hE + aE * np.cos(t)
            yE = kE + bE * np.sin(t)
        else:
            xE = hE + bE * np.cos(t)
            yE = kE + aE * np.sin(t)
        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(x=xE, y=yE, mode="lines", name="Elipse",
            fill="toself", fillcolor="rgba(59,130,246,.08)",
            line=dict(color="#3b82f6", width=3)))
        # semi-eixos
        segmento(fig8, hE, kE, hE+aE if eixo_e=="x" else hE, kE if eixo_e=="x" else kE+aE,
                 cor="#94a3b8", dash="dot", nome=f"a={aE:.1f}")
        segmento(fig8, hE, kE, hE if eixo_e=="x" else hE+bE, kE+bE if eixo_e=="x" else kE,
                 cor="#64748b", dash="dot", nome=f"b={bE:.1f}")
        # corda focal
        fig8.add_trace(go.Scatter(x=[f1x, f2x], y=[f1y, f2y], mode="lines",
            name="Corda focal 2c", line=dict(color="#10b981", width=2, dash="dash")))
        # ponto P sobre a elipse com linhas até focos
        P_ang = st.slider("Ponto P (ângulo °)", 0, 360, 60, 5, key="ang_el")
        P_ang_r = math.radians(P_ang)
        if eixo_e == "x":
            Px = hE + aE*math.cos(P_ang_r); Py = kE + bE*math.sin(P_ang_r)
        else:
            Px = hE + bE*math.cos(P_ang_r); Py = kE + aE*math.sin(P_ang_r)
        d1 = math.hypot(Px-f1x, Py-f1y)
        d2 = math.hypot(Px-f2x, Py-f2y)
        segmento(fig8, Px, Py, f1x, f1y, cor=COR["A"], dash="solid", nome=f"r₁={d1:.3f}")
        segmento(fig8, Px, Py, f2x, f2y, cor=COR["B"], dash="solid", nome=f"r₂={d2:.3f}")
        ponto(fig8, Px, Py, "P", "#f97316", tamanho=12)
        ponto(fig8, hE, kE, "O", "#64748b", tamanho=8)
        ponto(fig8, f1x, f1y, "F₁", COR["A"])
        ponto(fig8, f2x, f2y, "F₂", COR["B"])
        st.info(f"d(P,F₁) + d(P,F₂) = {d1:.4f} + {d2:.4f} = **{d1+d2:.4f}** ≈ 2a = **{2*aE:.4f}**")
        eixos_iguais(fig8, [hE-aE-1, hE+aE+1], [kE-aE-1, kE+aE+1])
        fig8.update_layout(title="Elipse: soma das distâncias aos focos = 2a",
                           legend=dict(orientation="h", y=-.18))
        mostrar(fig8, 520)
    quiz("el1", "Na elipse x²/25+y²/9=1, os focos estão em:",
         ["(±4,0)","(±5,0)","(±3,0)","(0,±4)"], 0,
         "a²=25, b²=9 → c²=16 → c=4. Focos em (±4,0) sobre o eixo x.")

# ══════════════════════════════════════════════════════════════
# ABA 9 — HIPÉRBOLE
# ══════════════════════════════════════════════════════════════
with tabs[8]:
    st.markdown("""<div class="card">
    A <b>hipérbole</b> é o lugar geométrico dos pontos cuja <b>diferença (em módulo) das distâncias
    a dois focos</b> é constante e igual a <b>2a</b>. Relação: <b>c² = a² + b²</b>.
    As <b>assíntotas</b> são retas que a hipérbole se aproxima mas nunca toca.
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2.3])
    with c1:
        with st.container(border=True):
            hH = st.slider("h (centro x)", -4.0, 4.0, 0.0, 0.5, key="h_hip")
            kH = st.slider("k (centro y)", -4.0, 4.0, 0.0, 0.5, key="k_hip")
            aH = st.slider("a", 0.5, 6.0, 3.0, 0.2, key="a_hip")
            bH = st.slider("b", 0.5, 6.0, 2.0, 0.2, key="b_hip")
            eixo_h = st.radio("Eixo real ao longo de", ["x","y"], key="eixo_h")

        cH = math.sqrt(aH**2 + bH**2)
        excH = cH / aH
        if eixo_h == "x":
            f1Hx, f1Hy = hH - cH, kH
            f2Hx, f2Hy = hH + cH, kH
        else:
            f1Hx, f1Hy = hH, kH - cH
            f2Hx, f2Hy = hH, kH + cH

        st.metric("c", f"{cH:.4f}")
        st.metric("Excentricidade e = c/a", f"{excH:.4f}")
        st.metric("Focos", f"F₁({f1Hx:.2f},{f1Hy:.2f})  F₂({f2Hx:.2f},{f2Hy:.2f})")
        if eixo_h == "x":
            st.metric("Assíntotas", f"y−{kH:.1f} = ±{bH/aH:.3f}·(x−{hH:.1f})")
        else:
            st.metric("Assíntotas", f"y−{kH:.1f} = ±{aH/bH:.3f}·(x−{hH:.1f})")

        if mostrar_formulas:
            st.markdown('<div class="form">', unsafe_allow_html=True)
            if eixo_h == "x":
                formula(rf"\frac{{(x-{hH})^2}}{{{aH:.2f}^2}}-\frac{{(y-{kH})^2}}{{{bH:.2f}^2}}=1")
            else:
                formula(rf"\frac{{(y-{kH})^2}}{{{aH:.2f}^2}}-\frac{{(x-{hH})^2}}{{{bH:.2f}^2}}=1")
            formula(r"c^2=a^2+b^2\qquad e=c/a>1")
            formula(rf"c={cH:.4f}\qquad e={excH:.4f}")
            formula(r"|d(P,F_1)-d(P,F_2)|=2a")
            st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        fig9 = go.Figure()
        t_h = np.linspace(-4.5, 4.5, 600)
        # Ramo 1 e Ramo 2
        if eixo_h == "x":
            x_r1 = hH + aH * np.cosh(t_h)
            y_r1 = kH + bH * np.sinh(t_h)
            x_r2 = hH - aH * np.cosh(t_h)
            y_r2 = kH + bH * np.sinh(t_h)
        else:
            y_r1 = kH + aH * np.cosh(t_h)
            x_r1 = hH + bH * np.sinh(t_h)
            y_r2 = kH - aH * np.cosh(t_h)
            x_r2 = hH + bH * np.sinh(t_h)

        fig9.add_trace(go.Scatter(x=x_r1, y=y_r1, mode="lines", name="Ramo 1",
            line=dict(color="#3b82f6", width=3)))
        fig9.add_trace(go.Scatter(x=x_r2, y=y_r2, mode="lines", name="Ramo 2",
            line=dict(color="#06b6d4", width=3)))
        # Assíntotas
        xas = np.linspace(hH-10, hH+10, 200)
        if eixo_h == "x":
            fig9.add_trace(go.Scatter(x=xas, y=kH+(bH/aH)*(xas-hH), mode="lines",
                name="Assíntota +", line=dict(color="#ef4444", width=1.5, dash="dash")))
            fig9.add_trace(go.Scatter(x=xas, y=kH-(bH/aH)*(xas-hH), mode="lines",
                name="Assíntota −", line=dict(color="#ef4444", width=1.5, dash="dash")))
        else:
            fig9.add_trace(go.Scatter(x=xas, y=kH+(aH/bH)*(xas-hH), mode="lines",
                name="Assíntota +", line=dict(color="#ef4444", width=1.5, dash="dash")))
            fig9.add_trace(go.Scatter(x=xas, y=kH-(aH/bH)*(xas-hH), mode="lines",
                name="Assíntota −", line=dict(color="#ef4444", width=1.5, dash="dash")))

        # retângulo central
        fig9.add_shape(type="rect",
            x0=hH-aH, y0=kH-bH, x1=hH+aH, y1=kH+bH,
            line=dict(color="#94a3b8", dash="dot", width=1.5),
            fillcolor="rgba(148,163,184,.08)")

        # Ponto P sobre o ramo 1
        t_P = st.slider("Parâmetro t do ponto P (ramo 1)", -3.0, 3.0, 1.0, 0.1, key="t_hip")
        if eixo_h == "x":
            Px_H = hH + aH * math.cosh(t_P)
            Py_H = kH + bH * math.sinh(t_P)
        else:
            Py_H = kH + aH * math.cosh(t_P)
            Px_H = hH + bH * math.sinh(t_P)

        d1H = math.hypot(Px_H-f1Hx, Py_H-f1Hy)
        d2H = math.hypot(Px_H-f2Hx, Py_H-f2Hy)
        segmento(fig9, Px_H, Py_H, f1Hx, f1Hy, cor=COR["A"], nome=f"r₁={d1H:.3f}")
        segmento(fig9, Px_H, Py_H, f2Hx, f2Hy, cor=COR["B"], nome=f"r₂={d2H:.3f}")
        ponto(fig9, Px_H, Py_H, "P", "#f97316", tamanho=12)
        ponto(fig9, hH, kH, "O", "#64748b", tamanho=8)
        ponto(fig9, f1Hx, f1Hy, "F₁", COR["A"])
        ponto(fig9, f2Hx, f2Hy, "F₂", COR["B"])
        st.info(f"|d(P,F₁) − d(P,F₂)| = |{d1H:.4f} − {d2H:.4f}| = **{abs(d1H-d2H):.4f}** ≈ 2a = **{2*aH:.4f}**")
        limH = max(aH, bH, cH) + 2
        eixos_iguais(fig9, [hH-limH, hH+limH], [kH-limH, kH+limH])
        fig9.update_layout(title="Hipérbole: |d(P,F₁)−d(P,F₂)| = 2a",
                           legend=dict(orientation="h", y=-.18))
        mostrar(fig9, 540)

        # Comparativo elipse vs hipérbole
        with st.expander("⚖️ Elipse × Hipérbole × Parábola"):
            st.markdown("""| Cônica | Definição | Equação padrão | Relação |
|---|---|---|---|
| **Circunferência** | d ao centro = r | x²+y²=r² | c=0, e=0 |
| **Elipse** | d₁+d₂=2a | x²/a²+y²/b²=1 | c²=a²−b², e<1 |
| **Parábola** | d(foco)=d(diretriz) | y²=4px | c=a, e=1 |
| **Hipérbole** | \|d₁−d₂\|=2a | x²/a²−y²/b²=1 | c²=a²+b², e>1 |""")

    quiz("hip1", "Na hipérbole x²/9−y²/16=1, as assíntotas têm inclinação:",
         ["±3/4","±4/3","±9/16","±2"], 1,
         "Assíntotas: y=±(b/a)x=±(4/3)x.")

# RODAPÉ
st.markdown("---")
st.markdown('<div style="text-align:center;color:#94a3b8;font-size:.85rem;padding:1rem;">'
    '📐 <b>Geometria Analítica Visual</b> — distância · ponto médio · baricentro · área · retas · cônicas</div>',
    unsafe_allow_html=True)
