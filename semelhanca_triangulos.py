import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Geometria Visual",
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
    
    fig.add_trace(go.Scatter(
        x=[B[0], C_vert[0], A[0], B[0]], 
        y=[B[1], C_vert[1], A[1], B[1]],
        fill="toself", fillcolor="rgba(46, 204, 113, 0.2)", 
        line=dict(color="#27ae60", width=3), hoverinfo="skip"
    ))
    
    fig.add_trace(go.Scatter(
        x=[A[0], H_proj[0]], y=[A[1], H_proj[1]],
        mode="lines", line=dict(color="#e74c3c", width=2, dash="dash"), hoverinfo="skip"
    ))
    
    t_size = 0.4
    ang_x = [A[0] - t_size*(c/a), A[0] - t_size*(c/a) + t_size*(b/a), A[0] + t_size*(b/a)]
    ang_y = [A[1] - t_size*(h/c), A[1] - t_size*(h/c) - t_size*(h/b), A[1] - t_size*(h/b)]
    fig.add_trace(go.Scatter(x=ang_x, y=ang_y, mode="lines", line=dict(color="#333", width=1.5)))

    fig.add_trace(go.Scatter(
        x=[H_proj[0], H_proj[0]+0.3, H_proj[0]+0.3, H_proj[0]], 
        y=[H_proj[1]+0.3, H_proj[1]+0.3, H_proj[1], H_proj[1]],
        mode="lines", line=dict(color="#333", width=1.5)
    ))
    
    fig.add_annotation(x=a/2, y=-0.8, text=f"a = {a:.2f}", showarrow=False, font=dict(size=14, color="#333"))
    fig.add_annotation(x=m/2, y=-0.3, text=f"m = {m:.2f}", showarrow=False, font=dict(size=13, color="#2980b9"))
    fig.add_annotation(x=m + n/2, y=-0.3, text=f"n = {n:.2f}", showarrow=False, font=dict(size=13, color="#8e44ad"))
    fig.add_annotation(x=m + 0.3, y=h/2, text=f"h = {h:.2f}", showarrow=False, font=dict(size=14, color="#e74c3c"))
    fig.add_annotation(x=m/2 - 0.4, y=h/2 + 0.4, text=f"c = {c:.2f}", showarrow=False, font=dict(size=14, color="#27ae60"))
    fig.add_annotation(x=m + n/2 + 0.4, y=h/2 + 0.4, text=f"b = {b:.2f}", showarrow=False, font=dict(size=14, color="#27ae60"))

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='white', margin=dict(l=0, r=0, t=10, b=10), height=400, showlegend=False
    )
    return fig

def plot_terno_pitagorico(cateto1, cateto2, hipotenusa):
    """Desenha um triângulo retângulo clássico focado em valores inteiros"""
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
# TÍTULO E MENU LATERAL
# ============================================
st.markdown('<div class="main-title">📐 Geometria Visual</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Explorando as proporções e relações dos triângulos de forma interativa</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configurações")
    st.markdown("---")
    topico = st.radio(
        "📚 Escolha o cenário:",
        [
            "Semelhança de Triângulos", 
            "Relações Métricas (Triângulo Retângulo)",
            "Ternos Pitagóricos (Lados Inteiros)"
        ],
        index=0
    )
    st.markdown("---")

# ============================================
# 1. SEMELHANÇA DE TRIÂNGULOS
# ============================================
if topico == "Semelhança de Triângulos":
    st.header("🔍 Semelhança de Triângulos")
    
    st.markdown("""
    <div class="concept-card" style="border-left-color: #3498db;">
        <b>Definição:</b> Dois triângulos são semelhantes se seus ângulos correspondentes forem congruentes e seus lados homólogos forem proporcionais. 
        O número que representa essa proporção é chamado de <b>razão de semelhança (k)</b>.
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.subheader("Triângulo Original (T1)")
        base = st.slider("Base (b)", 2.0, 10.0, 6.0, step=0.5)
        altura = st.slider("Altura (h)", 2.0, 10.0, 5.0, step=0.5)
        desloc = st.slider("Inclinação (Topo)", 0.0, base, base/2, step=0.5)
        
        st.markdown("---")
        st.subheader("Ampliação / Redução")
        k = st.slider("Razão de Semelhança (k)", 0.5, 3.0, 1.5, step=0.1)
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
        
        st.markdown("""
        <div class="step-box">
            <b>💡 O que isso significa?</b><br>
            Não importa a forma do triângulo, ao aplicar a razão <b>k</b>, as medidas dos lados são multiplicadas pelo mesmo fator.
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 2. RELAÇÕES MÉTRICAS NO TRIÂNGULO RETÂNGULO
# ============================================
elif topico == "Relações Métricas (Triângulo Retângulo)":
    st.header("📐 Relações Métricas no Triângulo Retângulo")
    
    st.markdown("""
    <div class="concept-card" style="border-left-color: #27ae60;">
        <b>Definição:</b> Ao traçar a altura relativa à hipotenusa, dividimos o triângulo retângulo em dois menores. 
        Surgem as famosas relações métricas, incluindo o <b>Teorema de Pitágoras</b>!
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.subheader("Medidas dos Catetos")
        c = st.slider("Cateto Esquerdo (c)", 1.0, 15.0, 3.0, step=0.5)
        b = st.slider("Cateto Direito (b)", 1.0, 15.0, 4.0, step=0.5)
    
    a = math.sqrt(b**2 + c**2)
    m = (c**2) / a
    n = (b**2) / a
    h = (b * c) / a
    
    st.markdown(r"$$ a^2 = b^2 + c^2 \quad | \quad h^2 = m \cdot n \quad | \quad c^2 = a \cdot m \quad | \quad b^2 = a \cdot n $$")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(plot_relacoes_metricas(c, b), use_container_width=True)
    
    with col2:
        st.subheader("🧮 Passo a Passo")
        
        st.markdown(f"""
        <div style="font-size:1.05rem;line-height:1.9;">
        <b>1. Teorema de Pitágoras:</b><br>
        a<sup>2</sup> = b<sup>2</sup> + c<sup>2</sup> &rarr; a = &radic;({b:.1f}<sup>2</sup> + {c:.1f}<sup>2</sup>) = <b>{a:.2f}</b>
        <hr>
        <b>2. Projeções (m e n):</b><br>
        m = c<sup>2</sup> / a = ({c:.1f}<sup>2</sup>) / {a:.2f} = <b>{m:.2f}</b><br>
        n = b<sup>2</sup> / a = ({b:.1f}<sup>2</sup>) / {a:.2f} = <b>{n:.2f}</b><br>
        <span style="color:#777; font-size:0.9rem;"><i>Verificação: {m:.2f} + {n:.2f} = {m+n:.2f}</i></span>
        <hr>
        <b>3. Altura relativa (h):</b><br>
        h = (b &times; c) / a = ({b:.1f} &times; {c:.1f}) / {a:.2f} = <b>{h:.2f}</b>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="step-box">
            <b>💡 Dica Pedagógica:</b><br>
            Configure <b>c = 3</b> e <b>b = 4</b>. Você verá o famoso triângulo pitagórico aparecer de forma exata!
        </div>
        """, unsafe_allow_html=True)

# ============================================
# 3. TERNOS PITAGÓRICOS
# ============================================
elif topico == "Ternos Pitagóricos (Lados Inteiros)":
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
    
    with st.sidebar:
        st.subheader("Escolha o Terno Base")
        selecao = st.selectbox("Família Pitagórica", list(familias.keys()))
        
        st.markdown("---")
        st.subheader("Multiplicador (k)")
        k_int = st.slider("Multiplicar lados por:", 1, 5, 1, step=1)
        st.info("Multiplicar um terno pitagórico por um número inteiro sempre gera um novo terno pitagórico!")

    base_c1, base_c2, base_h = familias[selecao]
    
    # Aplica o multiplicador
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
        <div style="font-size:1.1rem;line-height:2;">
        <b>Terno Base:</b> ({base_c1}, {base_c2}, {base_h})<br>
        <b>Multiplicador (k):</b> {k_int}<br>
        <hr>
        <b>Novas Medidas:</b><br>
        Cateto 1 = {base_c1} &times; {k_int} = <b>{c1}</b><br>
        Cateto 2 = {base_c2} &times; {k_int} = <b>{c2}</b><br>
        Hipotenusa = {base_h} &times; {k_int} = <b>{h}</b>
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
    📐 <b>Geometria Visual</b> — Ferramenta educacional para o ensino de Matemática<br>
    Altere as configurações na barra lateral para interagir com o sistema.
</div>
""", unsafe_allow_html=True)