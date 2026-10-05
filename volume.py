import streamlit as st
import math
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Relação de Volumes Geométricos",
    page_icon="📐",
    layout="wide"
)

# Funções de cálculo
def volume_cubo(aresta):
    return aresta ** 3

def volume_paralelepipedo(c, l, h):
    return c * l * h

def volume_esfera(raio):
    return (4/3) * math.pi * raio ** 3

def volume_cilindro(raio, altura):
    return math.pi * raio ** 2 * altura

def volume_cone(raio, altura):
    return (1/3) * math.pi * raio ** 2 * altura

def volume_piramide(base, altura):
    return (1/3) * base ** 2 * altura

# Título
st.title("📐 Relação entre Volumes dos Sólidos Geométricos")
st.markdown("---")

# Sidebar com controles
st.sidebar.header("⚙️ Parâmetros")

raio = st.sidebar.slider("Raio (r)", 1.0, 10.0, 3.0, 0.5)
aresta = st.sidebar.slider("Aresta do Cubo (a)", 1.0, 20.0, 6.0, 0.5)
altura = st.sidebar.slider("Altura (h)", 1.0, 20.0, 6.0, 0.5)

# Cálculos
v_cubo = volume_cubo(aresta)
v_paralelepipedo = volume_paralelepipedo(aresta, aresta, altura)
v_esfera = volume_esfera(raio)
v_cilindro = volume_cilindro(raio, altura)
v_cone = volume_cone(raio, altura)
v_piramide = volume_piramide(aresta, altura)

# Dados organizados
dados = {
    'Sólido': ['Cubo', 'Paralelepípedo', 'Esfera', 'Cilindro', 'Cone', 'Pirâmide'],
    'Fórmula': ['a³', 'c×l×h', '(4/3)πr³', 'πr²h', '(1/3)πr²h', '(1/3)a²h'],
    'Volume': [v_cubo, v_paralelepipedo, v_esfera, v_cilindro, v_cone, v_piramide]
}

df = pd.DataFrame(dados)

# Layout em colunas
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Tabela de Volumes")
    df['Volume'] = df['Volume'].apply(lambda x: f"{x:.2f}")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Métricas das relações importantes
    st.subheader("🔍 Relações Fundamentais")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Cone/Cilindro", f"{v_cone/v_cilindro:.2%}", "1/3 esperado")
        st.metric("Pirâmide/Cubo", f"{v_piramide/v_cubo:.2%}", "1/3 esperado")
    with col_b:
        st.metric("Esfera/Cilindro", f"{v_esfera/v_cilindro:.2%}", "2/3 esperado")
        st.metric("Esfera/Cubo", f"{v_esfera/v_cubo:.2%}", "π/6 ≈ 52.36%")

with col2:
    # Gráfico de barras
    st.subheader("📈 Comparação Visual")
    
    fig_barras = go.Figure(data=[
        go.Bar(
            x=dados['Sólido'],
            y=dados['Volume'],
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3'],
            text=[f"{v:.2f}" for v in dados['Volume']],
            textposition='auto',
        )
    ])
    
    fig_barras.update_layout(
        yaxis_title="Volume (unidades cúbicas)",
        xaxis_title="Sólido Geométrico",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_barras, use_container_width=True)
    
    # Gráfico de pizza
    fig_pizza = px.pie(
        values=dados['Volume'],
        names=dados['Sólido'],
        hole=0.3,
        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3']
    )
    fig_pizza.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pizza, use_container_width=True)

# Verificações matemáticas
st.markdown("---")
st.subheader("✅ Verificação das Relações Matemáticas")

col_ver1, col_ver2, col_ver3 = st.columns(3)

with col_ver1:
    diferenca1 = abs(v_cone - v_cilindro/3)
    st.success(f"**Cone = 1/3 Cilindro**\\n\\n{v_cone:.2f} ≈ {v_cilindro/3:.2f}\\n\\nDiferença: {diferenca1:.10f}")

with col_ver2:
    diferenca2 = abs(v_piramide - v_cubo/3)
    st.success(f"**Pirâmide = 1/3 Cubo**\\n\\n{v_piramide:.2f} ≈ {v_cubo/3:.2f}\\n\\nDiferença: {diferenca2:.10f}")

with col_ver3:
    diferenca3 = abs(v_esfera - (2/3)*v_cilindro)
    st.info(f"**Esfera = 2/3 Cilindro**\\n\\n{v_esfera:.2f} ≈ {(2/3)*v_cilindro:.2f}\\n\\nDiferença: {diferenca3:.10f}")

# Fórmulas
with st.expander("📚 Ver todas as fórmulas"):
    st.markdown("""
    | Sólido | Fórmula | Descrição |
    |--------|---------|-----------|
    | **Cubo** | V = a³ | Aresta ao cubo |
    | **Paralelepípedo** | V = c × l × h | Comprimento × Largura × Altura |
    | **Esfera** | V = (4/3)πr³ | Quatro terços de pi vezes raio cúbico |
    | **Cilindro** | V = πr²h | Pi vezes raio ao quadrado vezes altura |
    | **Cone** | V = (1/3)πr²h | Um terço do cilindro equivalente |
    | **Pirâmide** | V = (1/3)a²h | Um terço da base quadrada vezes altura |
    """)

st.caption("💡 Dica: Ajuste os sliders na barra lateral para ver como as relações se mantêm independentemente dos valores!")
