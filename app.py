import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta

from src.data_loader import load_csv
from src.preprocessing import preprocess
from src.analytics import (
    gasto_mensal,
    gasto_semestral,
    gasto_anual,
    gasto_por_categoria,
    categorizar_transacao,
    calcular_metricas_avancadas,
    identificar_gastos_recorrentes,
    analisar_tendencias
)

# Configuração da página
st.set_page_config(
    page_title="Lumen - Dashboard Financeiro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado - Paleta Navy, Teal & Sky Blue
st.markdown("""
<style>
    /* ==================== PALETA DE CORES ====================
    Navy: #2F4156
    Teal: #597C9D
    Sky Blue: #ACD9E6
    Beige: #F5EFEB
    White: #FFFFFF
    =========================================================== */
    /* =======CORES ORIGINAIS DO STREAMLIT PARA REFERÊNCIA======= */
    /* Fundo padrão: #F0F2F6 */
    /* Texto padrão: #262730 */
    
    /* ==================== CONFIGURAÇÕES GERAIS ==================== */
    
    /* Fundo principal do app */
    .stApp {
        background-image: #2F4156;
    }
    /* ==================== SIDEBAR (BARRA LATERAL) ==================== */
    
    /* Fundo da sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2F4156 100%, #2F4156 100%);
        box-shadow: 4px 0 20px rgba(0,0,0,0.1);
    }
    
    /* Texto da sidebar */
    section[data-testid="stSidebar"] * {
        color: #F5EFEB !important;
    }
    
    /* Título/Header da sidebar */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #F5EFEB !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Divisores na sidebar */
    section[data-testid="stSidebar"] hr {
        border-color: #F5EFEB;
        opacity: 0.4;
    }
    
    /* Labels da sidebar */
    section[data-testid="stSidebar"] label {
        color: #F5EFEB !important;
        font-weight: 600 !important;
    }
    
    /* ==================== CARDS DE MÉTRICAS ==================== */
    
    .stMetric {
        background: linear-gradient(135deg, #2F4156 100%, #F5EFEB 100%);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(47,65,86,0.15);
        border: 2px solid #0E1117;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Efeito hover nos cards */
    .stMetric:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 32px rgba(89,124,157,0.25);
        border-color: #F5EFEB;
    }
    
    /* Label das métricas */
    .stMetric label {
        color: #597C9D !important;
        font-size: 0.9rem !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    
    /* Valor das métricas */
    .stMetric [data-testid="stMetricValue"] {
        color: #2F4156 !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 4px rgba(47,65,86,0.1);
    }
    
    /* Delta das métricas */
    .stMetric [data-testid="stMetricDelta"] {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    /* ==================== ABAS ==================== */
    
    /* Container das abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: linear-gradient(135deg, #2F4156 0%, #3d5670 100%);
        padding: 12px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Abas individuais */
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(172,217,230,0.15);
        border-radius: 10px;
        padding: 14px 28px;
        color: #F5EFEB;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    /* Aba ativa */
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0E1117 100%, #0E1117 100%);
        color: #FFFFFF;
        border-color: #F5EFEB;
        box-shadow: 0 6px 16px rgba(89,124,157,0.3);
        transform: scale(1.05);
    }
    
    /* Aba hover */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(172,217,230,0.25);
        border-color: #F5EFEB;
        transform: translateY(-2px);
    }
    
    /* ==================== BOTÕES ==================== */
    
    /* Botão principal */
    .stButton > button {
        background: linear-gradient(135deg, #0E1117 0%, #0E1117 100%);
        color: white;
        border-radius: 10px;
        padding: 14px 28px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(89,124,157,0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(89,124,157,0.4);
        border-color: #F5EFEB;
        background: linear-gradient(135deg, #0E1117 0%, #0E1117 100%);
    }
    
    /* Botão de download */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #2F4156 65%, #2F4156 100%);
        color: #2F4156;
        border: none;
        border-radius: 10px;
        padding: 14px 28px;
        font-weight: 700;
        box-shadow: 0 4px 16px #0E1117;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(172,217,230,0.4);
    }
    
    /* ==================== INPUTS ==================== */
    
    /* Text input, select, etc */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div {
        background: linear-gradient(135deg, rgba(245,239,235,0.1) 0%, rgba(245,239,235,0.05) 100%);
        color: #2F4156;
        border: 2px solid #2F4156;
        border-radius: 10px;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: #597C9D;
        box-shadow: 0 0 0 3px rgba(89,124,157,0.2);
        background-color: #2F4156;
    }
    
    /* ==================== ALERTAS CUSTOMIZÁVEIS ==================== */
    
    .stAlert {
        border-radius: 12px;
        border-left: 5px solid #597C9D;
        color: #2F4156;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Classes customizadas para alertas */
    .custom-alert-success {
        background: linear-gradient(135deg, rgba(76,175,80,0.15) 0%, rgba(76,175,80,0.08) 100%) !important;
        border-left-color: #4CAF50 !important;
    }
    
    .custom-alert-warning {
        background: linear-gradient(135deg, rgba(255,193,7,0.15) 0%, rgba(255,193,7,0.08) 100%) !important;
        border-left-color: #FFC107 !important;
    }
    
    .custom-alert-error {
        background: linear-gradient(135deg, rgba(244,67,54,0.15) 0%, rgba(244,67,54,0.08) 100%) !important;
        border-left-color: #F44336 !important;
    }
    
    .custom-alert-info {
        background: linear-gradient(135deg, rgba(172,217,230,0.2) 0%, rgba(172,217,230,0.1) 100%) !important;
        border-left-color: #ACD9E6 !important;
    }
    
    /* ==================== EXPANDERS ==================== */
    
    div[data-testid="stExpander"] {
        border: 2px solid #F5EFEB;
        border-radius: 12px;
        background: linear-gradient(135deg, #F5EFEB 0%, #FFFFFF 100%);
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    div[data-testid="stExpander"]:hover {
        border-color: #597C9D;
        box-shadow: 0 6px 20px rgba(89,124,157,0.15);
    }
    
    /* Header do expander */
    div[data-testid="stExpander"] summary {
        color: #2F4156;
        font-weight: 700;
        padding: 18px;
    }
    
    /* ==================== DATAFRAMES/TABELAS ==================== */
    
    /* Container da tabela */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.1);
    }
    
    /* Header da tabela */
    .stDataFrame thead tr th {
        background: linear-gradient(135deg, #597C9D 0%, #6b8eaf 100%);
        color: white !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        border: none;
        padding: 16px;
    }
    
    /* Linhas da tabela */
    .stDataFrame tbody tr {
        background-color: #F5EFEB;
        border-bottom: 1px solid #ACD9E6;
        transition: background-color 0.2s ease;
    }
    
    .stDataFrame tbody tr:nth-child(even) {
        background-color: #FFFFFF;
    }
    
    .stDataFrame tbody tr:hover {
        background-color: rgba(172,217,230,0.2);
    }
    
    /* ==================== SLIDER ==================== */
    
    .stSlider > div > div > div > div {
        background-color: #597C9D;
    }
    
    .stSlider > div > div > div > div > div {
        background-color: #F5EFEB;
    }
    
    /* ==================== FILE UPLOADER ==================== */
    
    .stFileUploader {
        background: linear-gradient(135deg, #2F4156 0%, #2F4156 100%);
        border: 3px dashed #F5EFEB;
        border-radius: 16px;
        padding: 28px;
        transition: all 0.3s ease;
    }
    
    /* ==================== SCROLLBAR ==================== */
    
    /* Scrollbar no geral */
    ::-webkit-scrollbar {
        width: 14px;
        height: 14px;
    }
    
    ::-webkit-scrollbar-track {
        background: #2F4156;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #597C9D 0%, #ACD9E6 100%);
        border-radius: 8px;
        border: 2px solid #2F4156;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #ACD9E6 0%, #597C9D 100%);
    }
    
    /* ==================== TÍTULOS E TEXTO ==================== */
    
    h1 {
        color: #F5EFEB;
        font-weight: 800;
        text-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    h2, h3 {
        color: #ACD9E6;
        font-weight: 700;
    }
    
    p, span, div {
        color: #F5EFEB;
    }
    
    /* ==================== RADIO BUTTONS ==================== */
    
    .stRadio > div {
        background: linear-gradient(135deg, rgba(245,239,235,0.1) 0%, rgba(245,239,235,0.05) 100%);
        padding: 14px;
        border-radius: 10px;
    }
    
    .stRadio label {
        color: #F5EFEB !important;
        font-weight: 500;
    }
    
    /* ==================== CHECKBOX ==================== */
    
    .stCheckbox label {
        color: #F5EFEB !important;
        font-weight: 500;
    }
    
    /* ==================== DIVISORES ==================== */
    
    hr {
        border-color: #F5EFEB;
        opacity: 0.4;
        margin: 2.5rem 0;
    }
    
    /* ==================== MULTISELECT ==================== */
    
    .stMultiSelect span {
        background-color: #0E1117 !important;
        color: white !important;
        border-radius: 6px;
        padding: 4px 8px;
    }
    
    /* ==================== DATE INPUT ==================== */
    
    .stDateInput > div > div > input {
        background-color: rgba(245,239,235,0.9);
        color: #2F4156;
        border: 2px solid #1d2835;
        border-radius: 10px;
        font-weight: 500;
    }
    
    .stDateInput > div > div > input:focus {
        border-color: #F5EFEB;
        box-shadow: 0 0 0 3px rgba(89,124,157,0.2);
    }
    
    /* ==================== SPINNER ==================== */
    
    .stSpinner > div {
        border-top-color: #F5EFEB !important;
    }
    
    /* ==================== ANIMAÇÕES ==================== */
    
    @keyframes fadeInUp {
        from { 
            opacity: 0; 
            transform: translateY(30px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    .stMetric {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* ==================== SOMBRAS SUAVES ==================== */
    
    .element-container {
        animation: fadeInUp 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'dados_carregados' not in st.session_state:
    st.session_state.dados_carregados = False

# Mostrar logo e upload apenas se dados não foram carregados
if not st.session_state.dados_carregados:
    st.markdown("<h1 style='text-align: center; color: #F5EFEB;'>Lumen</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ACD9E6; font-size: 1.1rem;'>Iluminando suas finanças com inteligência</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Upload do arquivo com estilo melhorado
    st.markdown(
        """
        <style>
        /* Seleciona o botão do file_uploader */
        [data-testid="stFileUploader"] button {
            /* tamanho do botão */
            min-width: 200px;        /* aumente conforme necessário (ex.: 240, 280) */
            height: 64px;            /* altura do botão */
            padding: 0 16px;         /* espaçamento horizontal interno */
            border-radius: 10px;     /* cantos arredondados */
            font-size: 16px;         /* tamanho da fonte (mesmo se o texto estiver transparente) */
            line-height: 44px;       /* ajuda a centralizar verticalmente quando não usamos flex */
        }

        /* Como usamos ::after para o texto customizado, precisamos garantir o alinhamento */
        [data-testid="stFileUploader"] button::after {
            font-size: 16px;         /* mantenha consistente com o botão */
        }

        /* Opcional: se quiser “esticar” o botão para ocupar a largura toda do container */
        .btn-upload-full [data-testid="stFileUploader"] button {
            width: 100%;
            justify-content: center;  /* caso o texto original apareça em algum tema */
        }

        /* (Se notar o texto do ::after um pouco “deslocado” no vertical em alguns temas) */
        [data-testid="stFileUploader"] button {
            position: relative;
            display: inline-flex;     /* garante centralização nota 10 */
            align-items: center;
            justify-content: center;
        }
        [data-testid="stFileUploader"] button::after {
            position: absolute;
            inset: 0;                 /* ocupa toda a área do botão */
            display: flex;
            align-items: center;
            justify-content: center;
            pointer-events: none;
        }

        /* 1) Esconde instruções internas do dropzone */
        [data-testid="stFileUploaderDropzoneInstructions"] {
            display: none !important;
        }

        /* 2) (Opcional) Esconde o aviso de limite/tipo de arquivo, caso não queira exibir */
        [data-testid="stFileUploaderFileSizeLimit"],
        [data-testid="stFileUploaderType"] {
            display: none !important;
        }

        /* 3) Estiliza a área do dropzone para combinar com tema escuro */
        [data-testid="stFileUploaderDropzone"] {
            background: #597C9D !important;  /* cinza escuro */
            height: 100px;
            border-radius: 12px !important;
        }

        /* 4) Troca o texto do botão "Browse files" por "Selecionar arquivo" */
        [data-testid="stFileUploader"] button {
            position: relative !important;
            color: transparent !important;        /* esconde o texto original */
        }
        [data-testid="stFileUploader"] button::after {
            content: "Selecionar arquivo";        /* seu texto aqui */
            position: absolute;
            inset: 0;                             /* top/right/bottom/left = 0 */
            display: flex;
            align-items: center;
            justify-content: center;
            color: #e2e8f0;                       /* texto claro */
            font-weight: 600;
            pointer-events: none;                 /* não bloquear clique */
        }

        /* 5) (Opcional) Ajustes de visual do botão */
        [data-testid="stFileUploader"] button {
            background-color: #0E1117 !important; /* azul */
            border-color: #0E1117 !important;
        }

        /* 6) (Opcional) Tira o label duplicado dentro do dropzone para ficar limpinho */
        [data-testid="stFileUploader"] label > div:first-child {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    st.subheader("Anexe seu extrato do Banco Inter")
    st.caption("Arraste e solte o arquivo aqui ou clique no botão para selecionar o CSV.")

    arquivo = st.file_uploader(
        "Anexe seu extrato do Banco Inter (.csv)",
        type="csv",
        help="Faça o download do extrato em CSV diretamente do app do Banco Inter",
        label_visibility="collapsed"
    )

    st.markdown("</div>", unsafe_allow_html=True)
else:
    arquivo = st.session_state.arquivo

if arquivo and not st.session_state.dados_carregados:
    # Carregamento e processamento
    with st.spinner("🔄 Processando extrato..."):
        df = load_csv(arquivo)
        df = preprocess(df)
        
        # Aplicar categorização automática
        df['categoria'] = df['descricao'].apply(categorizar_transacao)
        
        # Salvar no session state
        st.session_state.df = df
        st.session_state.arquivo = arquivo
        st.session_state.dados_carregados = True
        st.rerun()

if st.session_state.dados_carregados:
    df = st.session_state.df
    
    st.success("Extrato carregado e categorizado com sucesso!")
    
    # Sidebar com filtros
    st.sidebar.header("Filtros")
    
    # Botão de Novo Upload na sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("Novo Upload", use_container_width=True):
        st.session_state.dados_carregados = False
        st.session_state.df = None
        st.session_state.arquivo = None
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Filtro de data no formato brasileiro
    data_min = df['data'].min().date()
    data_max = df['data'].max().date()
    
    st.sidebar.markdown("**Período de Análise**")
    
    col_data1, col_data2 = st.sidebar.columns(2)
    
    with col_data1:
        data_inicio = st.date_input(
            "De:",
            value=data_min,
            min_value=data_min,
            max_value=data_max,
            format="DD/MM/YYYY"
        )
    
    with col_data2:
        data_fim = st.date_input(
            "Até:",
            value=data_max,
            min_value=data_min,
            max_value=data_max,
            format="DD/MM/YYYY"
        )
    
    # Filtrar dados pelo período
    df_filtrado = df[(df['data'] >= pd.Timestamp(data_inicio)) & 
                     (df['data'] <= pd.Timestamp(data_fim))]
    
    st.sidebar.markdown("---")
    
    # Filtro de categoria
    categorias_unicas = sorted(df_filtrado['categoria'].unique())
    categorias_selecionadas = st.sidebar.multiselect(
        "Categorias",
        options=categorias_unicas,
        default=categorias_unicas
    )
    
    if categorias_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['categoria'].isin(categorias_selecionadas)]
    
    # Filtro de tipo de transação
    tipo_transacao = st.sidebar.radio(
        "Tipo de Transação",
        options=["Todas", "Apenas Gastos", "Apenas Entradas"],
        index=0
    )
    
    if tipo_transacao == "Apenas Gastos":
        df_filtrado = df_filtrado[df_filtrado['valor'] < 0]
    elif tipo_transacao == "Apenas Entradas":
        df_filtrado = df_filtrado[df_filtrado['valor'] > 0]
    
    # Métricas avançadas
    metricas = calcular_metricas_avancadas(df_filtrado)
    
    # KPIs Principais
    st.header("Visão Geral")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total de Gastos",
            f"R$ {metricas['total_gastos']:,.2f}",
            delta=f"{metricas['variacao_gastos']:.1f}% vs período anterior",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Total de Entradas",
            f"R$ {metricas['total_entradas']:,.2f}",
            delta=f"{metricas['variacao_entradas']:.1f}% vs período anterior"
        )
    
    with col3:
        saldo_liquido = metricas['total_entradas'] - metricas['total_gastos']
        st.metric(
            "Saldo Líquido",
            f"R$ {saldo_liquido:,.2f}",
            delta="Positivo" if saldo_liquido > 0 else "Negativo",
            delta_color="normal" if saldo_liquido > 0 else "inverse"
        )
    
    with col4:
        st.metric(
            "Transações",
            f"{len(df_filtrado)}",
            delta=f"Média: R$ {metricas['ticket_medio']:.2f}"
        )
    
    # Segunda linha de KPIs
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            "Gasto Médio Diário",
            f"R$ {metricas['gasto_medio_diario']:.2f}"
        )
    
    with col6:
        st.metric(
            "Maior Gasto",
            f"R$ {metricas['maior_gasto']:.2f}"
        )
    
    with col7:
        st.metric(
            "Categoria Top",
            metricas['categoria_top']
        )
    
    with col8:
        taxa_poupanca = (saldo_liquido / metricas['total_entradas'] * 100) if metricas['total_entradas'] > 0 else 0
        st.metric(
            "Taxa de Poupança",
            f"{taxa_poupanca:.1f}%"
        )
    
    st.divider()
    
    # Abas de análise
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Tendências", 
        "🎯 Categorias", 
        "🔄 Recorrências", 
        "💡 Insights",
        "📋 Detalhes"
    ])
    
    with tab1:
        st.subheader("Análise de Tendências Temporais")
        
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            # Gasto mensal
            st.markdown("**Evolução Mensal de Gastos**")
            mensal = gasto_mensal(df_filtrado)
            
            fig_mensal = px.line(
                mensal,
                x="mes_ano",
                y="valor",
                markers=True,
                labels={
                    "mes_ano": "Mês",
                    "valor": "R$ Gasto"
                }
            )
            fig_mensal.update_traces(
                line_color='#FF6B6B',
                line_width=3,
                marker=dict(size=10)
            )
            fig_mensal.update_layout(
                hovermode='x unified',
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='#ffffff'),
                height=350,
                xaxis=dict(gridcolor='#333'),
                yaxis=dict(gridcolor='#333')
            )
            st.plotly_chart(fig_mensal, use_container_width=True)
        
        with col_t2:
            # Comparação Entradas vs Gastos
            st.markdown("**Entradas vs Gastos Mensais**")
            
            entradas_mensais = (
                df_filtrado[df_filtrado['valor'] > 0]
                .groupby('mes_ano')['valor']
                .sum()
                .reset_index()
                .rename(columns={'valor': 'Entradas'})
            )
            
            gastos_mensais = mensal.rename(columns={'valor': 'Gastos'})
            
            comparacao = pd.merge(entradas_mensais, gastos_mensais, on='mes_ano', how='outer').fillna(0)
            
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(
                x=comparacao['mes_ano'],
                y=comparacao['Entradas'],
                name='Entradas',
                marker_color='#51CF66'
            ))
            fig_comp.add_trace(go.Bar(
                x=comparacao['mes_ano'],
                y=comparacao['Gastos'],
                name='Gastos',
                marker_color='#FF6B6B'
            ))
            
            fig_comp.update_layout(
                barmode='group',
                hovermode='x unified',
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='#ffffff'),
                height=350,
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                xaxis=dict(gridcolor='#333'),
                yaxis=dict(gridcolor='#333')
            )
            st.plotly_chart(fig_comp, use_container_width=True)
        
        # Gráfico de linha do tempo com saldo
        st.markdown("**Evolução do Saldo ao Longo do Tempo**")
        df_timeline = df_filtrado.sort_values('data').copy()
        
        fig_saldo = px.line(
            df_timeline,
            x='data',
            y='saldo',
            labels={'data': 'Data', 'saldo': 'Saldo (R$)'}
        )
        fig_saldo.update_traces(line_color='#4DABF7', line_width=2)
        fig_saldo.add_hline(y=0, line_dash="dash", line_color="red", opacity=0.5)
        fig_saldo.update_layout(
            hovermode='x unified',
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            font=dict(color='#ffffff'),
            height=300,
            xaxis=dict(gridcolor='#333'),
            yaxis=dict(gridcolor='#333')
        )
        st.plotly_chart(fig_saldo, use_container_width=True)
    
    with tab2:
        st.subheader("Análise por Categorias")
        
        col_c1, col_c2 = st.columns([1, 1])
        
        with col_c1:
            # Gráfico de pizza
            st.markdown("**Distribuição de Gastos**")
            categorias = gasto_por_categoria(df_filtrado)
            categorias['valor'] = categorias['valor'].abs()
            
            fig_pizza = px.pie(
                categorias,
                values='valor',
                names='categoria',
                hole=0.4
            )
            fig_pizza.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}'
            )
            fig_pizza.update_layout(
                height=400,
                paper_bgcolor='#0E1117',
                font=dict(color='#ffffff'),
                showlegend=True,
                legend=dict(font=dict(color='#ffffff'))
            )
            st.plotly_chart(fig_pizza, use_container_width=True)
        
        with col_c2:
            # Gráfico de barras horizontal
            st.markdown("**Ranking de Gastos por Categoria**")
            
            fig_cat = px.bar(
                categorias.sort_values('valor', ascending=True),
                x="valor",
                y="categoria",
                orientation="h",
                text='valor'
            )
            fig_cat.update_traces(
                texttemplate='R$ %{text:,.2f}',
                textposition='outside',
                marker_color='#4DABF7'
            )
            fig_cat.update_layout(
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='#ffffff'),
                height=400,
                xaxis_title="Valor Gasto (R$)",
                yaxis_title="",
                xaxis=dict(gridcolor='#333'),
                yaxis=dict(gridcolor='#333')
                )
            st.plotly_chart(fig_cat, use_container_width=True)

            # Tabela detalhada por categoria
        st.markdown("**Detalhamento por Categoria**")
        
        df_cat_detalhado = (
            df_filtrado[df_filtrado['valor'] < 0]
            .groupby('categoria')
            .agg({
                'valor': ['sum', 'count', 'mean'],
            })
            .round(2)
        )
        df_cat_detalhado.columns = ['Total Gasto', 'Nº Transações', 'Ticket Médio']
        df_cat_detalhado['Total Gasto'] = df_cat_detalhado['Total Gasto'].abs()
        df_cat_detalhado['Ticket Médio'] = df_cat_detalhado['Ticket Médio'].abs()
        df_cat_detalhado['% do Total'] = (df_cat_detalhado['Total Gasto'] / df_cat_detalhado['Total Gasto'].sum() * 100).round(1)
        df_cat_detalhado = df_cat_detalhado.sort_values('Total Gasto', ascending=False)
        
        st.dataframe(
            df_cat_detalhado.style.format({
                'Total Gasto': 'R$ {:,.2f}',
                'Nº Transações': '{:.0f}',
                'Ticket Médio': 'R$ {:,.2f}',
                '% do Total': '{:.1f}%'
            }),
            use_container_width=True
        )

    with tab3:
        st.subheader("Gastos Recorrentes e Padrões")
        
        recorrentes = identificar_gastos_recorrentes(df_filtrado)
        
        if not recorrentes.empty:
            st.markdown(f"**Identificamos {len(recorrentes)} gastos recorrentes:**")
            
            # Visualização de gastos recorrentes
            fig_rec = px.bar(
                recorrentes.head(10),
                x='total_gasto',
                y='descricao',
                orientation='h',
                text='frequencia',
                color='total_gasto',
                color_continuous_scale='Reds'
            )
            fig_rec.update_traces(
                texttemplate='%{text}x - R$ %{x:,.2f}',
                textposition='outside'
            )
            fig_rec.update_layout(
                plot_bgcolor='#0E1117',
                paper_bgcolor='#0E1117',
                font=dict(color='#ffffff'),
                height=400,
                xaxis_title="Total Gasto (R$)",
                yaxis_title="",
                showlegend=False,
                xaxis=dict(gridcolor='#333'),
                yaxis=dict(gridcolor='#333')
            )
            st.plotly_chart(fig_rec, use_container_width=True)
            
            # Tabela detalhada
            st.markdown("**Detalhes dos Gastos Recorrentes**")
            recorrentes_display = recorrentes.copy()
            recorrentes_display['categoria'] = recorrentes_display['descricao'].apply(categorizar_transacao)
            
            st.dataframe(
                recorrentes_display[['descricao', 'categoria', 'frequencia', 'valor_medio', 'total_gasto']]
                .style.format({
                    'frequencia': '{:.0f}x',
                    'valor_medio': 'R$ {:,.2f}',
                    'total_gasto': 'R$ {:,.2f}'
                }),
                use_container_width=True
            )
        else:
            st.info("Nenhum gasto recorrente identificado no período selecionado.")
        
        # Top 10 maiores gastos individuais
        st.markdown("**Top 10 Maiores Gastos Individuais**")
        top_gastos = (
            df_filtrado[df_filtrado['valor'] < 0]
            .nlargest(10, 'valor', keep='first')[['data', 'descricao', 'categoria', 'valor']]
            .copy()
        )
        top_gastos['valor'] = top_gastos['valor'].abs()
        
        st.dataframe(
            top_gastos.style.format({
                'data': lambda x: x.strftime('%d/%m/%Y'),
                'valor': 'R$ {:,.2f}'
            }),
            use_container_width=True
        )

    with tab4:
        st.subheader("Insights e Recomendações")
        
        insights = analisar_tendencias(df_filtrado)
        
        # Cards de insights com cores customizáveis
        col_i1, col_i2 = st.columns(2)
        
        with col_i1:
            st.markdown("### Análise de Comportamento")
            
            if insights['tendencia_gastos'] == 'crescente':
                st.markdown(f"""<div class="custom-alert-warning" style="padding: 20px; border-radius: 12px; border-left: 5px solid #FFC107; margin-bottom: 15px;">
                    Seus gastos estão <strong>crescendo</strong> {insights['variacao_percentual']:.1f}% em relação ao período anterior.
                </div>""", unsafe_allow_html=True)
            elif insights['tendencia_gastos'] == 'decrescente':
                st.markdown(f"""<div class="custom-alert-success" style="padding: 20px; border-radius: 12px; border-left: 5px solid #4CAF50; margin-bottom: 15px;">
                    Parabéns! Seus gastos estão <strong>diminuindo</strong> {abs(insights['variacao_percentual']):.1f}% em relação ao período anterior.
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="custom-alert-info" style="padding: 20px; border-radius: 12px; border-left: 5px solid #ACD9E6; margin-bottom: 15px;">
                    Seus gastos estão <strong>estáveis</strong> em relação ao período anterior.
                </div>""", unsafe_allow_html=True)
            
            # Análise de sazonalidade
            dias_semana = df_filtrado[df_filtrado['valor'] < 0].copy()
            dias_semana['dia_semana'] = dias_semana['data'].dt.day_name()

            # Dicionário para tradução dos dias da semana
            traducao_dias = {
                'Monday': 'Segunda-feira',
                'Tuesday': 'Terça-feira',
                'Wednesday': 'Quarta-feira',
                'Thursday': 'Quinta-feira',
                'Friday': 'Sexta-feira',
                'Saturday': 'Sábado',
                'Sunday': 'Domingo'
            }

            # Traduzir os dias para português
            dias_semana['dia_semana'] = dias_semana['dia_semana'].map(traducao_dias)

            gastos_por_dia = dias_semana.groupby('dia_semana')['valor'].sum().abs()

            if not gastos_por_dia.empty:
                dia_mais_gasto = gastos_por_dia.idxmax()
                st.markdown(f"""<div class="custom-alert-info" style="padding: 20px; border-radius: 12px; border-left: 5px solid #ACD9E6; margin-bottom: 15px;">
                    Você tende a gastar mais às <strong>{dia_mais_gasto}s</strong>
                </div>""", unsafe_allow_html=True)
        
        with col_i2:
            st.markdown("### Recomendações")
            
            # Recomendações baseadas em análise
            if taxa_poupanca < 10:
                st.markdown(f"""<div class="custom-alert-error" style="padding: 20px; border-radius: 12px; border-left: 5px solid #F44336; margin-bottom: 15px;">
                    Sua taxa de poupança está abaixo de 10%. Considere reduzir gastos ou aumentar receitas.
                </div>""", unsafe_allow_html=True)
            elif taxa_poupanca < 20:
                st.markdown(f"""<div class="custom-alert-warning" style="padding: 20px; border-radius: 12px; border-left: 5px solid #FFC107; margin-bottom: 15px;">
                    Tente aumentar sua taxa de poupança para pelo menos 20% da renda.
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""<div class="custom-alert-success" style="padding: 20px; border-radius: 12px; border-left: 5px solid #4CAF50; margin-bottom: 15px;">
                    Excelente! Você está poupando uma boa parte da renda.
                </div>""", unsafe_allow_html=True)
            
            # Sugestões de economia
            if not categorias.empty:
                cat_top = categorias.nlargest(1, 'valor').iloc[0]
                st.markdown(f"""<div class="custom-alert-info" style="padding: 20px; border-radius: 12px; border-left: 5px solid #ACD9E6; margin-bottom: 15px;">
                    Considere reduzir gastos em <strong>{cat_top['categoria']}</strong> (R$ {cat_top['valor']:.2f})
                </div>""", unsafe_allow_html=True)
            
            # Alerta de gastos altos
            if metricas['maior_gasto'] > metricas['ticket_medio'] * 5:
                st.markdown(f"""<div class="custom-alert-warning" style="padding: 20px; border-radius: 12px; border-left: 5px solid #FFC107; margin-bottom: 15px;">
                    Você teve um gasto muito alto de R$ {metricas['maior_gasto']:.2f}. Revise se foi necessário.
                </div>""", unsafe_allow_html=True)
        
        # Gráfico de evolução da taxa de poupança
        st.markdown("### Evolução da Taxa de Poupança")
        
        df_mensal_completo = df_filtrado.groupby('mes_ano').agg({
            'valor': lambda x: x[x < 0].sum()
        }).reset_index()
        df_mensal_completo.columns = ['mes_ano', 'gastos']
        
        entradas_mes = df_filtrado[df_filtrado['valor'] > 0].groupby('mes_ano')['valor'].sum().reset_index()
        entradas_mes.columns = ['mes_ano', 'entradas']
        
        df_poupanca = pd.merge(df_mensal_completo, entradas_mes, on='mes_ano', how='left').fillna(0)
        df_poupanca['gastos'] = df_poupanca['gastos'].abs()
        df_poupanca['saldo'] = df_poupanca['entradas'] - df_poupanca['gastos']
        df_poupanca['taxa_poupanca'] = (df_poupanca['saldo'] / df_poupanca['entradas'] * 100).fillna(0)
        
        fig_poup = go.Figure()
        fig_poup.add_trace(go.Scatter(
            x=df_poupanca['mes_ano'],
            y=df_poupanca['taxa_poupanca'],
            mode='lines+markers',
            name='Taxa de Poupança',
            line=dict(color='#51CF66', width=3),
            marker=dict(size=10),
            fill='tozeroy',
            fillcolor='rgba(81, 207, 102, 0.2)'
        ))
        fig_poup.add_hline(y=20, line_dash="dash", line_color="green", 
                        annotation_text="Meta: 20%", annotation_position="right")
        fig_poup.update_layout(
            hovermode='x unified',
            plot_bgcolor='#0E1117',
            paper_bgcolor='#0E1117',
            font=dict(color='#ffffff'),
            height=300,
            yaxis_title="Taxa de Poupança (%)",
            xaxis_title="Mês",
            xaxis=dict(gridcolor='#333'),
            yaxis=dict(gridcolor='#333')
        )
        st.plotly_chart(fig_poup, use_container_width=True)

    with tab5:
        st.subheader("Detalhes das Transações")
        
        # Filtros adicionais
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            ordenar_por = st.selectbox(
                "Ordenar por",
                ["Data (mais recente)", "Data (mais antigo)", "Valor (maior)", "Valor (menor)"]
            )
        
        with col_f2:
            busca = st.text_input("Buscar na descrição", "")
        
        with col_f3:
            linhas = st.slider("Linhas a exibir", 10, 100, 50)
        
        # Aplicar filtros
        df_display = df_filtrado.copy()
        
        if busca:
            df_display = df_display[
                df_display['descricao'].str.contains(busca, case=False, na=False)
            ]
        
        # Ordenação
        if ordenar_por == "Data (mais recente)":
            df_display = df_display.sort_values('data', ascending=False)
        elif ordenar_por == "Data (mais antigo)":
            df_display = df_display.sort_values('data', ascending=True)
        elif ordenar_por == "Valor (maior)":
            df_display = df_display.sort_values('valor', ascending=False)
        else:
            df_display = df_display.sort_values('valor', ascending=True)
        
        # Exibir tabela
        df_display_formatted = df_display[['data', 'descricao', 'categoria', 'valor', 'saldo']].head(linhas)
        
        st.dataframe(
            df_display_formatted.style.format({
                'data': lambda x: x.strftime('%d/%m/%Y'),
                'valor': lambda x: f"R$ {x:,.2f}",
                'saldo': lambda x: f"R$ {x:,.2f}"
            }).applymap(
                lambda x: 'color: red' if isinstance(x, (int, float)) and x < 0 else 'color: green',
                subset=['valor']
            ),
            use_container_width=True,
            height=600
        )
        
        # Botão de download
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Baixar dados filtrados (CSV)",
            data=csv,
            file_name=f"extrato_filtrado_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    st.divider()

    # Rodapé com informações
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        st.info(f"📅 **Período analisado:** {(df_filtrado['data'].max() - df_filtrado['data'].min()).days} dias")

    with col_f2:
        st.info(f"🔢 **Total de transações:** {len(df_filtrado)}")

    with col_f3:
        st.info(f"📊 **Categorias identificadas:** {df_filtrado['categoria'].nunique()}")
