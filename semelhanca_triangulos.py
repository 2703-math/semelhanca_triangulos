import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Geometria Visual: Triângulos",
    page_icon="📐",
    layout="wide"
)

# ============================================
# CSS PERSONALIZADO
# ============================================
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .concept-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 4px solid;
        margin-bottom: 1rem;
    }
    .step-box {
        background: #fff8e1;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÕES DE PLOTAGEM (PLOTLY)
# ============================================
def plot_semelhanca(base, altura, deslocamento, k):
    fig = go.Figure()
    
    x1 = [0, base, deslocamento, 0]
    y1 = [0, 0, altura, 0]
    
    offset_x = base + 2
    x2 = [offset_x, offset_x + (base * k), offset_x + (deslocamento * k), offset_x]
    y2 = [0, 0, altura * k, 0]
    
    fig.add_trace(go.Scatter(
        x=x1, y=y1, fill="toself", fillcolor="rgba(52, 152, 219, 0.4)", 
        line=dict(color="#2980b9", width=2), name="T1", hoverinfo="skip"
    ))
    
    fig.add_trace(go.Scatter(
        x=x2, y=y2, fill="toself", fillcolor="rgba(231, 76, 60, 0.4)", 
        line=dict(color="#c0392b", width=2), name="T2", hoverinfo="skip"
    ))
    
    fig.add_annotation(x=base/2, y=-0.5, text="Base", showarrow=False, font=dict(color="#2980b9"))
    fig.add_annotation(x=offset_x + (base*k)/2, y=-0.5, text="Base '", showarrow=False, font=dict(color="#c0392b"))

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='white', margin=dict(l=0, r=0, t=20, b=20), height=350, showlegend=False
    )
    return fig

def plot_relacoes_metricas(c, b):
    fig = go.Figure()
    
    a = math.sqrt(b**2 + c**2)
    m = (c**2) / a
    n = (b**2) / a
    h = (b * c) / a
    
    B = (0, 0)
    C_vert = (a, 0)
    A = (m, h)
    H_proj = (m, 0)
    
    # Triângulo Principal
    fig.add_trace(go.Scatter(
        x=[B[0], C_vert[0], A[0], B[0]], 
        y=[B[1], C_vert[1], A[1], B[1]],
        mode="lines", line=dict(color="#2c3e50", width=4), name="Maior", hoverinfo="skip"
    ))
    
    # Altura interna tracejada
    fig.add_trace(go.Scatter(
        x=[A[0], H_proj[0]], y=[A[1], H_proj[1]],
        mode="lines", line=dict(color="#e74c3c", width=2, dash="dash"), hoverinfo="skip"
    ))
    
    fig.add_annotation(x=m/2, y=-0.3, text=f"m = {m:.2f}", showarrow=False, font=dict(size=13, color="#2980b9"))
    fig.add_annotation(x=m + n/2, y=-0.3, text=f"n = {n:.2f}", showarrow=False, font=dict(size=13, color="#c0392b"))
    fig.add_annotation(x=m - 0.4, y=h/2, text=f"h = {h:.2f}", showarrow=False, font=dict(size=13, color="#e74c3c"))
    fig.add_annotation(x=m/2 - 0.4, y=h/2 + 0.3, text=f"c = {c:.2f}", showarrow=False, font=dict(size=13, color="#2980b9"))
    fig.add_annotation(x=m + n/2 + 0.4, y=h/2 + 0.3, text=f"b = {b:.2f}", showarrow=False, font=dict(size=13, color="#c0392b"))
    fig.add_annotation(x=a/2, y=-0.8, text=f"Hipotenusa a = {a:.2f}", showarrow=False, font=dict(size=14, color="#2c3e50", weight="bold"))

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-1, a + 1]),
        yaxis=dict(scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False, visible=False, range=[-1.2, h + 1]),
        plot_bgcolor='white', margin=dict(l=0, r=0, t=10, b=10), height=380, showlegend=False
    )
    return fig

def transform_pt(pt, passos_rot, espelho):
    x, y = pt
    if espelho:
        x = -x
    for _ in range(passos_rot % 4):
        x, y = -y, x
    return (x, y)

def plot_triangulo_isolado(v0, v1, v2, ang_v0, ang_v1, ang_v2, cor, nome, passos_rot, espelhar):
    tv0 = transform_pt(v0, passos_rot, espelhar)
    tv1 = transform_pt(v1, passos_rot, espelhar)
    tv2 = transform_pt(v2, passos_rot, espelhar)
    
    cx = (tv0[0] + tv1[0] + tv2[0]) / 3.0
    cy = (tv0[1] + tv1[1] + tv2[1]) / 3.0
    
    def label_pos(v):
        return (v[0] + 0.32 * (cx - v[0]), v[1] + 0.32 * (cy - v[1]))
    
    p0 = label_pos(tv0)
    p1 = label_pos(tv1)
    p2 = label_pos(tv2)
    
    x_vals = [tv0[0], tv1[0], tv2[0], tv0[0]]
    y_vals = [tv0[1], tv1[1], tv2[1], tv0[1]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_vals, y=y_vals, fill="toself", fillcolor=cor.replace("1)", "0.15)"),
        line=dict(color=cor, width=3), hoverinfo="skip"
    ))
    
    # Marcas/Rótulos dos ângulos internos
    fig.add_annotation(x=p0[0], y=p0[1], text=ang_v0, showarrow=False, font=dict(size=13, color="#333", family="sans-serif"))
    fig.add_annotation(x=p1[0], y=p1[1], text=ang_v1, showarrow=False, font=dict(size=13, color="#333", family="sans-serif"))
    fig.add_annotation(x=p2[0], y=p2[1], text=ang_v2, showarrow=False, font=dict(size=13, color="#333", family="sans-serif"))
    
    all_x = [tv0[0], tv1[0], tv2[0]]
    all_y = [tv0[1], tv1[1], tv2[1]]
    max_range = max(max(map(abs, all_x)), max(map(abs, all_y)), 2.0) + 1.2
    
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, visible=False, range=[-max_range, max_range]),
        yaxis=dict(scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False, visible=False, range=[-max_range, max_range]),
        plot_bgcolor='white', margin=dict(l=0, r=0, t=25, b=0), height=280, showlegend=False,
        title=dict(text=nome, font=dict(size=14, color=cor), x=0.5, xanchor='center')
    )
    return fig

def plot_terno_pitagorico(cateto1, cateto2, hipotenusa):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[0, cateto1, 0, 0],
        y=[0, 0, cateto2, 0],
        fill="toself", fillcolor="rgba(155, 89, 182, 0.3)",
        line=dict(color="#8e44ad", width=3),
        hoverinfo="skip"
    ))
    
    t = min(cateto1, cateto2) * 0.1
    fig.add_trace(go.Scatter(
        x=[t, t, 0], y=[0, t, t],
        mode="lines", line=dict(color="#333", width=1.5), hoverinfo="skip"
    ))
    
    fig.add_annotation(x=cateto1/2, y=-cateto2*0.08, text=f"{cateto1}", showarrow=False, font=dict(size=16, color="#8e44ad"))
    fig.add_annotation(x=-cateto1*0.05, y=cateto2/2, text=f"{cateto2}", showarrow=False, font=dict(size=16, color="#8e44ad"))
    fig.add_annotation(x=cateto1/2 + cateto1*0.05, y=cateto2/2 + cateto2*0.05, text=f"{hipotenusa}", showarrow=False, font=dict(size=18, color="#c0392b"))

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='white', margin=dict(l=20, r=20, t=20, b=20), height=350, showlegend=False
    )
    return fig

# ============================================
# TÍTULO E ABAS DE NAVEGAÇÃO SUPERIORES
# ============================================
st.markdown('<div class="main-title">📐 Geometria Visual</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Explorando as proporções e relações dos triângulos de forma interativa</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "Semelhança de Triângulos", 
    "Relações Métricas (Triângulo Retângulo)",
    "Ternos Pitagóricos (Lados Inteiros)"
])

# ============================================
# 1. SEMELHANÇA DE TRIÂNGULOS
# ============================================
with tab1:
    st.header("🔍 Semelhança de Triângulos")
    
    st.markdown("""
    <div class="concept-card" style="border-left-color: #3498db;">
        <b>Definição:</b> Dois triângulos são semelhantes se seus ângulos correspondentes forem congruentes e seus lados homólogos forem proporcionais. 
        O número que representa essa proporção é chamado de <b>razão de semelhança (k)</b>.
    </div>
    """, unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns([1, 2])
    with col_c1:
        st.subheader("Parâmetros")
        base = st.slider("Base (b)", 2.0, 10.0, 6.0, step=0.5, key="sem_b")
        altura = st.slider("Altura (h)", 2.0, 10.0, 5.0, step=0.5, key="sem_h")
        desloc = st.slider("Inclinação (Topo)", 0.0, base, base/2, step=0.5, key="sem_d")
        k = st.slider("Razão de Semelhança (k)", 0.5, 3.0, 1.5, step=0.1, key="sem_k")
        st.info("Se k > 1: Ampliação\n\nSe k < 1: Redução")

    lado_esquerdo1 = math.sqrt(desloc**2 + altura**2)
    lado_direito1 = math.sqrt((base - desloc)**2 + altura**2)
    lado_esquerdo2 = lado_esquerdo1 * k
    lado_direito2 = lado_direito1 * k
    base2 = base * k
    
    st.markdown(r"$$ \frac{\text{Lado T}_2}{\text{Lado T}_1} = k $$")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(plot_semelhanca(base, altura, desloc, k), use_container_width=True)
    
    with col2:
        st.subheader("🧮 Comparando os Lados")
        st.markdown(f"""
        <div style="font-size:1.1rem;line-height:1.8;">
        <b>Triângulo 1 (Original)</b><br>
        Base = {base:.2f}<br>
        Lado Esquerdo = {lado_esquerdo1:.2f}<br>
        Lado Direito = {lado_direito1:.2f}
        <hr>
        <b>Triângulo 2 (Proporcional)</b><br>
        Base' = {base:.2f} &times; {k} = <b>{base2:.2f}</b><br>
        Lado Esq.' = {lado_esquerdo1:.2f} &times; {k} = <b>{lado_esquerdo2:.2f}</b><br>
        Lado Dir.' = {lado_direito1:.2f} &times; {k} = <b>{lado_direito2:.2f}</b>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 2. RELAÇÕES MÉTRICAS NO TRIÂNGULO RETÂNGULO
# ============================================
with tab2:
    st.header("📐 Relações Métricas no Triângulo Retângulo")
    
    st.markdown("""
    <div class="concept-card" style="border-left-color: #27ae60;">
        <b>Definição:</b> Ao traçar a altura relativa à hipotenusa, dividimos o triângulo retângulo em dois menores. 
        Todos os três triângulos formados são semelhantes entre si e possuem exatamente os mesmos ângulos internos ($\text{90°}, \alpha, \beta$)!
    </div>
    """, unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns([1, 2])
    with col_c1:
        st.subheader("Medidas dos Catetos")
        c = st.slider("Cateto Esquerdo (c)", 1.0, 15.0, 3.0, step=0.5, key="rel_c")
        b = st.slider("Cateto Direito (b)", 1.0, 15.0, 4.0, step=0.5, key="rel_b")
    
    a = math.sqrt(b**2 + c**2)
    m = (c**2) / a
    n = (b**2) / a
    h = (b * c) / a
    
    st.markdown(r"$$ a^2 = b^2 + c^2 \quad | \quad h^2 = m \cdot n \quad | \quad c^2 = a \cdot m \quad | \quad b^2 = a \cdot n $$")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(plot_relacoes_metricas(c, b), use_container_width=True)
    
    with col2:
        st.subheader("🧮 Fórmulas e Cálculos")
        st.markdown(f"""
        <div style="font-size:1.0rem;line-height:1.7;">
        <b>1. Pitágoras (Hipotenusa a):</b> a = &radic;({b:.1f}<sup>2</sup> + {c:.1f}<sup>2</sup>) = <b>{a:.2f}</b><br>
        <b>2. Projeção (m):</b> m = c<sup>2</sup> / a = <b>{m:.2f}</b><br>
        <b>3. Projeção (n):</b> n = b<sup>2</sup> / a = <b>{n:.2f}</b><br>
        <b>4. Altura (h):</b> h = (b &times; c) / a = <b>{h:.2f}</b>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🧩 Os 3 Triângulos Semelhantes Separados com Marcação de Ângulos")
    st.markdown("Use o seletor de rotação sucessiva e o espelhamento para girar os triângulos. Note como os ângulos internos **(90°, α e β)** correspondem perfeitamente em todos eles!")

    tcol1, tcol2, tcol3 = st.columns(3)
    
    with tcol1:
        st.markdown("<b>1. Triângulo Maior (Geral)</b>", unsafe_allow_html=True)
        rot_1 = st.selectbox("Rotação", ["0°", "90°", "180°", "270°"], key="rot1")
        esp_1 = st.checkbox("Espelhar", key="esp1")
        passos_1 = {"0°":0, "90°":1, "180°":2, "270°":3}[rot_1]
        fig_t1 = plot_triangulo_isolado((0,0), (c,0), (0,b), "90°", "α", "β", "#2c3e50", "Triângulo Maior", passos_1, esp_1)
        st.plotly_chart(fig_t1, use_container_width=True)

    with tcol2:
        st.markdown("<b>2. Triângulo Intermediário</b>", unsafe_allow_html=True)
        rot_2 = st.selectbox("Rotação", ["0°", "90°", "180°", "270°"], key="rot2")
        esp_2 = st.checkbox("Espelhar", key="esp2")
        passos_2 = {"0°":0, "90°":1, "180°":2, "270°":3}[rot_2]
        fig_t2 = plot_triangulo_isolado((0,0), (m,0), (0,h), "90°", "α", "β", "#2980b9", "Triângulo Intermediário", passos_2, esp_2)
        st.plotly_chart(fig_t2, use_container_width=True)

    with tcol3:
        st.markdown("<b>3. Triângulo Menor</b>", unsafe_allow_html=True)
        rot_3 = st.selectbox("Rotação", ["0°", "90°", "180°", "270°"], key="rot3")
        esp_3 = st.checkbox("Espelhar", key="esp3")
        passos_3 = {"0°":0, "90°":1, "180°":2, "270°":3}[rot_3]
        fig_t3 = plot_triangulo_isolado((0,0), (n,0), (0,h), "90°", "β", "α", "#c0392b", "Triângulo Menor", passos_3, esp_3)
        st.plotly_chart(fig_t3, use_container_width=True)

# ============================================
# 3. TERNOS PITAGÓRICOS
# ============================================
with tab3:
    st.header("✨ Ternos Pitagóricos")
    
    st.markdown("""
    <div class="concept-card" style="border-left-color: #8e44ad;">
        <b>Definição:</b> Um terno pitagórico é formado por três números <b>inteiros</b> que satisfazem o Teorema de Pitágoras. 
        Eles são perfeitos para criar exercícios e provas sem resultados com decimais!
    </div>
    """, unsafe_allow_html=True)

    familias = {
        "Família 3-4-5": (4, 3, 5),
        "Família 5-12-13": (12, 5, 13),
        "Família 8-15-17": (15, 8, 17),
        "Família 7-24-25": (24, 7, 25)
    }
    
    col_c1, col_c2 = st.columns([1, 2])
    with col_c1:
        st.subheader("Configuração")
        selecao = st.selectbox("Família Pitagórica", list(familias.keys()), key="ter_fam")
        k_int = st.slider("Multiplicar lados por (k):", 1, 5, 1, step=1, key="ter_k")
        st.info("Multiplicar um terno pitagórico por um número inteiro sempre gera um novo terno pitagórico!")

    base_c1, base_c2, base_h = familias[selecao]
    c1 = base_c1 * k_int
    c2 = base_c2 * k_int
    h = base_h * k_int
    
    st.markdown(r"$$ (\text{Cateto}_1)^2 + (\text{Cateto}_2)^2 = (\text{Hipotenusa})^2 $$")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(plot_terno_pitagorico(c1, c2, h), use_container_width=True)
    
    with col2:
        st.subheader("🧮 Prova Real")
        st.markdown(f"""
        <div style="font-size:1.1rem;line-height:1.8;">
        <b>Terno Base:</b> ({base_c1}, {base_c2}, {base_h})<br>
        <b>Multiplicador (k):</b> {k_int}<br>
        <hr>
        <b>Novas Medidas:</b><br>
        Cateto 1 = <b>{c1}</b><br>
        Cateto 2 = <b>{c2}</b><br>
        Hipotenusa = <b>{h}</b>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background:#f8f9fa; border-radius:10px; padding:1rem; margin-top:1rem; text-align:center;">
            <b>Testando no Teorema de Pitágoras:</b><br>
            {c1}<sup>2</sup> + {c2}<sup>2</sup> = {h}<sup>2</sup><br>
            {c1**2} + {c2**2} = {h**2}<br>
            <span style="color:#27ae60; font-weight:bold; font-size:1.2rem;">{c1**2 + c2**2} = {h**2} ✅</span>
        </div>
        """, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    📐 <b>Geometria Visual</b> — Ferramenta educacional para o ensino de Matemática
</div>
""", unsafe_allow_html=True)
