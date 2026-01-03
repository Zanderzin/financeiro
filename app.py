import streamlit as st
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
    page_title="Dashboard Financeiro | Banco Inter",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhor contraste
st.markdown("""
<style>
    .stMetric {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 1px solid #333;
    }
    .stMetric label {
        color: #b0b0b0 !important;
        font-size: 0.9rem !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
    }
    .stAlert {
        border-radius: 10px;
    }
    div[data-testid="stExpander"] {
        border: 1px solid #333;
        border-radius: 10px;
        background-color: #1e1e1e;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FF6B00;'>💳 Dashboard Financeiro Avançado</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 1.1rem;'>Análise completa e inteligente do seu extrato Banco Inter</p>", unsafe_allow_html=True)
st.markdown("---")

# Upload do arquivo
arquivo = st.file_uploader(
    "📎 Anexe seu extrato do Banco Inter (.csv)",
    type="csv",
    help="Faça o download do extrato em CSV diretamente do app do Banco Inter"
)

if arquivo:
    # Carregamento e processamento
    with st.spinner("🔄 Processando extrato..."):
        df = load_csv(arquivo)
        df = preprocess(df)
        
        # Aplicar categorização automática
        df['categoria'] = df['descricao'].apply(categorizar_transacao)
    
    st.success("✅ Extrato carregado e categorizado com sucesso!")
    
    # Sidebar com filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro de data
    data_min = df['data'].min()
    data_max = df['data'].max()
    
    date_range = st.sidebar.date_input(
        "Período de Análise",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max
    )
    
    if len(date_range) == 2:
        df_filtrado = df[(df['data'] >= pd.Timestamp(date_range[0])) & 
                         (df['data'] <= pd.Timestamp(date_range[1]))]
    else:
        df_filtrado = df
    
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
    st.header("📊 Visão Geral")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💸 Total de Gastos",
            f"R$ {metricas['total_gastos']:,.2f}",
            delta=f"{metricas['variacao_gastos']:.1f}% vs período anterior",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "💰 Total de Entradas",
            f"R$ {metricas['total_entradas']:,.2f}",
            delta=f"{metricas['variacao_entradas']:.1f}% vs período anterior"
        )
    
    with col3:
        saldo_liquido = metricas['total_entradas'] - metricas['total_gastos']
        st.metric(
            "📈 Saldo Líquido",
            f"R$ {saldo_liquido:,.2f}",
            delta="Positivo" if saldo_liquido > 0 else "Negativo",
            delta_color="normal" if saldo_liquido > 0 else "inverse"
        )
    
    with col4:
        st.metric(
            "🔢 Transações",
            f"{len(df_filtrado)}",
            delta=f"Média: R$ {metricas['ticket_medio']:.2f}"
        )
    
    # Segunda linha de KPIs
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            "📅 Gasto Médio Diário",
            f"R$ {metricas['gasto_medio_diario']:.2f}"
        )
    
    with col6:
        st.metric(
            "🏆 Maior Gasto",
            f"R$ {metricas['maior_gasto']:.2f}"
        )
    
    with col7:
        st.metric(
            "📊 Categoria Top",
            metricas['categoria_top']
        )
    
    with col8:
        taxa_poupanca = (saldo_liquido / metricas['total_entradas'] * 100) if metricas['total_entradas'] > 0 else 0
        st.metric(
            "💎 Taxa de Poupança",
            f"{taxa_poupanca:.1f}%",
            delta="Saudável" if taxa_poupanca > 20 else "Atenção",
            delta_color="normal" if taxa_poupanca > 20 else "inverse"
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
        st.subheader("📈 Análise de Tendências Temporais")
        
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
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
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
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
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
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font=dict(color='#ffffff'),
            height=300,
            xaxis=dict(gridcolor='#333'),
            yaxis=dict(gridcolor='#333')
        )
        st.plotly_chart(fig_saldo, use_container_width=True)
    
    with tab2:
        st.subheader("🎯 Análise por Categorias")
        
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
                paper_bgcolor='#1e1e1e',
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
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
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
        st.subheader("🔄 Gastos Recorrentes e Padrões")
        
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
                plot_bgcolor='#1e1e1e',
                paper_bgcolor='#1e1e1e',
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
        st.markdown("**🏆 Top 10 Maiores Gastos Individuais**")
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
        st.subheader("💡 Insights e Recomendações")
        
        insights = analisar_tendencias(df_filtrado)
        
        # Cards de insights
        col_i1, col_i2 = st.columns(2)
        
        with col_i1:
            st.markdown("### 📊 Análise de Comportamento")
            
            if insights['tendencia_gastos'] == 'crescente':
                st.warning(f"⚠️ Seus gastos estão **crescendo** {insights['variacao_percentual']:.1f}% em relação ao período anterior.")
            elif insights['tendencia_gastos'] == 'decrescente':
                st.success(f"✅ Parabéns! Seus gastos estão **diminuindo** {abs(insights['variacao_percentual']):.1f}% em relação ao período anterior.")
            else:
                st.info("📊 Seus gastos estão **estáveis** em relação ao período anterior.")
            
            # Análise de sazonalidade
            dias_semana = df_filtrado[df_filtrado['valor'] < 0].copy()
            dias_semana['dia_semana'] = dias_semana['data'].dt.day_name()
            gastos_por_dia = dias_semana.groupby('dia_semana')['valor'].sum().abs()
            
            if not gastos_por_dia.empty:
                dia_mais_gasto = gastos_por_dia.idxmax()
                st.info(f"📅 Você tende a gastar mais às **{dia_mais_gasto}s**")
        
        with col_i2:
            st.markdown("### 🎯 Recomendações")
            
            # Recomendações baseadas em análise
            if taxa_poupanca < 10:
                st.error("🚨 Sua taxa de poupança está abaixo de 10%. Considere reduzir gastos ou aumentar receitas.")
            elif taxa_poupanca < 20:
                st.warning("⚠️ Tente aumentar sua taxa de poupança para pelo menos 20% da renda.")
            else:
                st.success("✅ Excelente! Você está poupando uma boa parte da renda.")
            
            # Sugestões de economia
            if not categorias.empty:
                cat_top = categorias.nlargest(1, 'valor').iloc[0]
                st.info(f"💡 Considere reduzir gastos em **{cat_top['categoria']}** (R$ {cat_top['valor']:.2f})")
            
            # Alerta de gastos altos
            if metricas['maior_gasto'] > metricas['ticket_medio'] * 5:
                st.warning(f"⚠️ Você teve um gasto muito alto de R$ {metricas['maior_gasto']:.2f}. Revise se foi necessário.")
        
        # Gráfico de evolução da taxa de poupança
        st.markdown("### 📈 Evolução da Taxa de Poupança")
        
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
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font=dict(color='#ffffff'),
            height=300,
            yaxis_title="Taxa de Poupança (%)",
            xaxis_title="Mês",
            xaxis=dict(gridcolor='#333'),
            yaxis=dict(gridcolor='#333')
        )
        st.plotly_chart(fig_poup, use_container_width=True)
    
    with tab5:
        st.subheader("📋 Detalhes das Transações")
        
        # Filtros adicionais
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            ordenar_por = st.selectbox(
                "Ordenar por",
                ["Data (mais recente)", "Data (mais antigo)", "Valor (maior)", "Valor (menor)"]
            )
        
        with col_f2:
            busca = st.text_input("🔍 Buscar na descrição", "")
        
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
            label="📥 Baixar dados filtrados (CSV)",
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

else:
    st.info("⬆️ Faça upload do seu extrato do Banco Inter para começar a análise completa!")
    
    # Instruções
    with st.expander("📖 Como usar este dashboard"):
        st.markdown("""
        ### Passo a passo:
        
        1. **Baixe seu extrato** do app do Banco Inter em formato CSV
        2. **Faça upload** do arquivo usando o botão acima
        3. **Explore** as diferentes abas de análise:
           - **Tendências**: Veja a evolução dos seus gastos ao longo do tempo
           - **Categorias**: Descubra onde você mais gasta
           - **Recorrências**: Identifique gastos que se repetem
           - **Insights**: Receba recomendações personalizadas
           - **Detalhes**: Veja todas as transações com filtros avançados
        
        ### Recursos:
        - 🤖 **Categorização automática** de transações
        - 📊 **Gráficos interativos** com Plotly
        - 🔍 **Filtros avançados** por data, categoria e tipo
        - 💡 **Insights inteligentes** sobre seus hábitos financeiros
        - 📥 **Exportação** de dados filtrados
        """)
    
    with st.expander("🎯 Funcionalidades principais"):
        st.markdown("""
        - ✅ **Análise temporal completa** (mensal, semestral, anual)
        - ✅ **Identificação de gastos recorrentes**
        - ✅ **Cálculo de taxa de poupança**
        - ✅ **Comparação entre períodos**
        - ✅ **Top 10 maiores gastos**
        - ✅ **Análise por categoria com gráficos**
        - ✅ **Alertas e recomendações personalizadas**
        - ✅ **Interface moderna e responsiva**
        """)