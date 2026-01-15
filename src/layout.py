def themed_css() -> str:
    return """
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
            background-color: #0E1117;
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
            border-radius: 10px;
            padding: 14px 28px;
            font-weight: 700;
            box-shadow: 0 4px 16px #0E1117;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stDownloadButton > button:hover {
            transform: translateY(-3px);
            border-color: #F5EFEB;
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
    """


def pagina_inicial() -> str:
    return """
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
    """
