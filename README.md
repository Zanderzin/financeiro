# 💳 Dashboard Financeiro Banco Inter

Dashboard avançado para análise de extratos bancários do Banco Inter com categorização automática, insights inteligentes e visualizações interativas.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Funcionalidades

### 📊 Análises Completas
- **Visão Geral**: KPIs principais com comparação entre períodos
- **Análise Temporal**: Evolução mensal, semestral e anual dos gastos
- **Categorização Automática**: Identifica automaticamente 11 categorias de gastos
- **Gastos Recorrentes**: Detecta gastos que se repetem frequentemente
- **Top 10**: Maiores gastos individuais do período
- **Taxa de Poupança**: Acompanhe quanto você está conseguindo poupar

### 📈 Visualizações Interativas
- Gráficos de linha para tendências temporais
- Gráficos de pizza para distribuição por categorias
- Gráficos de barras comparativas
- Evolução do saldo ao longo do tempo
- Comparação entradas vs gastos

### 🎯 Insights Inteligentes
- Análise de comportamento de gastos
- Recomendações personalizadas
- Alertas de gastos altos
- Identificação de padrões de consumo
- Sugestões de economia

### 🔍 Filtros Avançados
- Filtro por período (data range)
- Filtro por categoria
- Filtro por tipo de transação (gastos/entradas)
- Busca na descrição
- Múltiplas opções de ordenação

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a passo

1. **Clone o repositório**
```bash
git clone https://github.com/Zanderzin/financeiro.git
cd financeiro
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute o dashboard**
```bash
streamlit run app.py
```

5. **Acesse no navegador**
```
http://localhost:8501
```

## 📋 Como Usar

### 1. Obtenha seu extrato do Banco Inter

1. Abra o app do Banco Inter
2. Vá em **Extrato**
3. Selecione o período desejado
4. Clique em **Exportar** ou **Compartilhar**
5. Escolha o formato **CSV**
6. Salve o arquivo no seu computador

### 2. Faça o upload no dashboard

1. Abra o dashboard no navegador
2. Clique em **"Anexe seu extrato do Banco Inter (.csv)"**
3. Selecione o arquivo CSV baixado
4. Aguarde o processamento automático

### 3. Explore as análises

Navegue pelas 5 abas principais:

- **📈 Tendências**: Veja como seus gastos evoluem ao longo do tempo
- **🎯 Categorias**: Descubra onde você mais gasta seu dinheiro
- **🔄 Recorrências**: Identifique gastos recorrentes e padrões
- **💡 Insights**: Receba recomendações personalizadas
- **📋 Detalhes**: Veja todas as transações com filtros avançados

## 🏗️ Estrutura do Projeto

```
dashboard-financeiro-inter/
│
├── app.py                 # Aplicação principal do Streamlit
├── requirements.txt       # Dependências do projeto
├── README.md             # Documentação
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py    # Funções para carregar CSV
│   ├── preprocessing.py  # Limpeza e preparação dos dados
│   └── analytics.py      # Funções de análise e categorização
│
└── assets/               # Recursos estáticos (opcional)
```

## 🎨 Categorias Automáticas

O sistema identifica automaticamente 11 categorias principais:

| Categoria | Exemplos |
|-----------|----------|
| 🍔 Alimentação | iFood, Rappi, Restaurantes, Supermercados |
| 🚗 Transporte | Uber, 99, Postos de combustível, Estacionamento |
| 🏠 Moradia | Aluguel, Condomínio, Luz, Água, Internet |
| 💊 Saúde | Farmácias, Hospitais, Clínicas, Plano de Saúde |
| 📚 Educação | Escolas, Cursos, Livros, Material escolar |
| 🎬 Lazer | Netflix, Spotify, Cinema, Shows, Jogos |
| 👕 Vestuário | Lojas de roupa, Calçados, Acessórios |
| 💇 Serviços | Salão, Academia, Barbearia, Lavanderia |
| 💸 Transferências | PIX, TED, DOC |
| 📊 Investimentos | Aplicações, Poupança, Fundos, Ações |
| ❓ Outros | Transações não categorizadas |

## 📊 Métricas Calculadas

### KPIs Principais
- **Total de Gastos**: Soma de todas as despesas
- **Total de Entradas**: Soma de todas as receitas
- **Saldo Líquido**: Diferença entre entradas e gastos
- **Número de Transações**: Total de movimentações

### Métricas Avançadas
- **Gasto Médio Diário**: Quanto você gasta por dia
- **Maior Gasto**: Maior transação do período
- **Categoria Top**: Categoria com mais gastos
- **Taxa de Poupança**: Percentual da renda que você economiza
- **Ticket Médio**: Valor médio por transação

### Análises Temporais
- Evolução mensal de gastos
- Comparação semestral
- Tendências anuais
- Variação percentual entre períodos

## 🛠️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)**: Framework para criação de aplicações web
- **[Pandas](https://pandas.pydata.org/)**: Manipulação e análise de dados
- **[Plotly](https://plotly.com/)**: Visualizações interativas
- **[NumPy](https://numpy.org/)**: Computação numérica

## 🤝 Contribuindo

Contribuições são sempre bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📝 Melhorias Futuras

- [ ] Exportação de relatórios em PDF
- [ ] Previsão de gastos futuros com ML
- [ ] Comparação com médias nacionais
- [ ] Metas de gastos por categoria
- [ ] Alertas de gastos incomuns
- [ ] Integração com API do Banco Inter
- [ ] Análise de gastos compartilhados
- [ ] Dashboard mobile otimizado
- [ ] Modo escuro
- [ ] Suporte a múltiplas contas

## ⚠️ Avisos Importantes

- Este projeto **NÃO** coleta ou armazena dados bancários
- Todos os dados são processados localmente no seu navegador
- Nunca compartilhe seus extratos com terceiros não confiáveis
- Este é um projeto independente, não oficial do Banco Inter

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ para ajudar pessoas a terem melhor controle financeiro

## 🙏 Agradecimentos

- Banco Inter pelo formato de extrato estruturado
- Comunidade Streamlit pelos excelentes recursos
- Todos que contribuíram com feedback e sugestões

---

**Dica**: Para melhores resultados, use extratos de pelo menos 3 meses para análises mais precisas!

Se este projeto te ajudou, considere dar uma ⭐ no repositório!
