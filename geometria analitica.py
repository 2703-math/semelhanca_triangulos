"""
📐 Geometria Analítica Visual
==============================
Executar com: streamlit run "geometria analitica.py"

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

def eixos_iguais(fig, xs, ys, pad=1.0, row=None, col=None):
    """Grade limpa com eixos proporcionais."""
    mn = min(min(xs)-pad, min(ys)-pad)
    mx = max(max(xs)+pad, max(ys)+pad)
    kw = {}
    if row is not None: kw["row"] = row
    if col is not None: kw["col"] = col
    
    fig.update_xaxes(range=[mn, mx], zeroline=True, zerolinecolor="#94a3b8",
                     gridcolor="#e2e8f0", showgrid=True, **kw)
    fig.update_yaxes(range=[mn, mx], zeroline=True, zerolinecolor="#94a3b8",
                     gridcolor="#e2e8f0", scaleanchor=f"x{'' if (row in (None, 1) and col in (None, 1)) else row}",
                     scaleratio=1, **kw)

def ponto(fig, x, y, nome, cor="#ef4444", tamanho=12, row=None, col=None):
    kw = {}
    if row is not None: kw["row"] = row
    if col is not None: kw["col"] = col
    
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text",
        name=nome, text=[nome], textposition="top right",
        textfont=dict(size=13, color=cor),
        marker=dict(size=tamanho, color=cor, line=dict(color="white", width=1.5)),
        hovertemplate=f"{nome} = ({x:.3f}, {y:.3f})<extra></extra>"), **kw)

def segmento(fig, x0, y0, x1, y1, cor="#3b82f6", dash="solid", nome="", row=None, col=None):
    kw = {}
    if row is not None: kw["row"] = row
    if col is not None: kw["col"] = col
    
    fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines",
        name=nome, line=dict(color=cor, width=2, dash=dash),
        hoverinfo="skip", showlegend=bool(nome)), **kw)

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
