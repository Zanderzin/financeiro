import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def gasto_mensal(df):
    """Calcula gastos mensais"""
    return (
        df[df['valor'] < 0]
        .groupby('mes_ano', as_index=False)['valor']
        .sum()
        .assign(valor=lambda x: x['valor'].abs())
    )


def gasto_semestral(df):
    """Calcula gastos semestrais"""
    return (
        df[df['valor'] < 0]
        .groupby(['ano', 'semestre'])['valor']
        .sum()
        .reset_index()
        .assign(valor=lambda x: x['valor'].abs())
    )


def gasto_anual(df):
    """Calcula gastos anuais"""
    return (
        df[df['valor'] < 0]
        .groupby('ano')['valor']
        .sum()
        .reset_index()
        .assign(valor=lambda x: x['valor'].abs())
    )


def gasto_por_categoria(df):
    """Calcula gastos por categoria"""
    return (
        df[df['valor'] < 0]
        .groupby('categoria')['valor']
        .sum()
        .reset_index()
        .sort_values('valor')
        .assign(valor=lambda x: x['valor'].abs())
    )


def eh_nome_pessoa(texto):
    """
    Detecta se o texto parece ser um nome de pessoa (para PIX/transferências)
    """
    if pd.isna(texto):
        return False
    
    texto = texto.lower().strip()
    
    # Remove números e caracteres especiais comuns em CNPJs
    tem_muitos_numeros = sum(c.isdigit() for c in texto) > len(texto) * 0.3
    if tem_muitos_numeros:
        return False
    
    # Palavras que indicam que NÃO é pessoa (empresas, estabelecimentos)
    palavras_empresa = [
        'ltda', 'eireli', 'sa', 's.a', 's/a', 'me', 'epp', 'comercio', 
        'agencia', 'restaurante', 'loja', 'bar', 'padaria', 'mercado',
        'posto', 'shopping', 'center', 'magazine', 'supermercado',
        'delivery', 'express', 'online', 'store', 'shop', 'company',
        'distribuidora', 'ifood', 'uber', 'rappi', 'ticket', 'estacio',
        'cinema', 'teatro', 'hospital', 'clinica', 'farmacia', 'drogaria',
        'petronorte', 'taguatinga', 'mc donald', 'mcdonald', 'creperia',
        'pica-pau', 'magalupay', 'gmcm', 'combustivel', 'brasilia'
    ]
    
    for palavra in palavras_empresa:
        if palavra in texto:
            return False
    
    # Padrões comuns de nomes brasileiros
    palavras = texto.split()
    
    # Se tem 2+ palavras e nenhuma é empresa, provavelmente é nome
    if len(palavras) >= 2:
        # Lista de nomes comuns brasileiros (primeiros nomes e sobrenomes)
        nomes_comuns = [
            # Primeiros nomes comuns
            'jose', 'maria', 'joao', 'ana', 'antonio', 'francisco', 'carlos',
            'paulo', 'pedro', 'lucas', 'marcos', 'gabriel', 'rafael', 'bruno',
            'fernando', 'rodrigo', 'patricia', 'sandra', 'juliana', 'fernanda',
            'camila', 'beatriz', 'luciana', 'mariana', 'amanda', 'julia',
            'bruna', 'larissa', 'natalia', 'vanessa', 'marcelo', 'eduardo',
            'gustavo', 'felipe', 'diego', 'vitor', 'matheus', 'thiago',
            'ricardo', 'roberto', 'sergio', 'luis', 'luciene', 'bernardo',
            'alexander', 'alessandra', 'giovanna', 'paula', 'jonatas',
            'alex', 'teixeira', 'macedo', 'francisca',
            # Sobrenomes comuns
            'silva', 'santos', 'oliveira', 'souza', 'costa', 'ferreira', 
            'rodrigues', 'almeida', 'nascimento', 'lima', 'araujo', 'ribeiro', 
            'carvalho', 'martins', 'dias', 'lopes', 'gomes', 'mendes', 'barros', 
            'cardoso', 'rocha', 'miranda', 'duarte', 'monteiro', 'freitas', 
            'barbosa', 'campos', 'aquino', 'morais', 'brandao', 'macena'
        ]
        
        # Verifica se alguma palavra do texto está na lista de nomes
        for palavra in palavras:
            if len(palavra) > 2 and palavra in nomes_comuns:
                return True
        
        # Se tem 2-4 palavras de tamanho razoável, provavelmente é nome
        if 2 <= len(palavras) <= 4:
            palavras_validas = [p for p in palavras if len(p) > 2]
            if len(palavras_validas) >= 2:
                # Verifica se não tem palavras muito comerciais
                palavras_comerciais = ['delivery', 'express', 'online', 'store', 'shop']
                tem_comercial = any(pc in texto for pc in palavras_comerciais)
                if not tem_comercial:
                    return True
    
    return False


def categorizar_transacao(descricao):
    """
    Categoriza automaticamente uma transação com base na descrição
    usando palavras-chave inteligentes + detecção automática de nomes
    """
    if pd.isna(descricao):
        return 'Outros'
    
    descricao_lower = descricao.lower()
    
    # Dicionário de categorias com palavras-chave
    categorias = {
        'Alimentação': [
            'ifood', 'quentinhas', 'sabor', 'macarons', 'nino', 'loucos por burger', 
            'biscoitos', 'rappi', 'bolos', 'uber eats', 'restaurante', 'lanchonete',
            'padaria', 'dog', 'mcdonalds', 'mc donald', 'sucoetal', 'bacio', 'bauducco', 
            'lancheteria', 'benedito', 'veloce', 'creperia', 'pica-pau', 'marmitexleo', 
            'mercado', 'taguatinga', 'supermercado', 'açougue', 'hortifruti',
            'pizza', 'burger', 'distribuidora', 'fini', 'casa do pao', 'pao', 
            'big box', 'burguer', 'imperio dos paes', 'bobs', 
            'subway', 'giraffas', 'outback', 'dominos', 'torta', 'dona', 
            'abbraccio', 'coco bambu', 'spoleto', 'habibs', 'leonardobianoda',
            'american cookies', 'sorbe', 'cafe', 'bakery', 'pao de acucar', 
            'carrefour', 'extra', 'walmart', 'assai', 'luzia de fatima miranda', 
            'atacadao'
        ],
        'Transporte': [
            'uber', 'iguatemi', 'car', 'combustiveis', 'estacionament', 'lyft', 
            'cabify', '99', 'taxi', 'combustivel', 'gasolina', 'posto', 'park', 
            'parkshopping', 'petronorte', 'shell', 'boulevard', 'ipiranga', 
            'br petroleo', 'petrobras', 'gmcm', 'estacionamento', 'valet', 'onibus', 
            'metro', 'metrô', 'transporte', 'pedágio', 'pedagio', 'viacard', 
            'carlos ieje de sena', 'sem parar'
        ],
        'Moradia': [
            'aluguel', 'condominio', 'condomínio', 'iptu', 'luz', 'agua',
            'água', 'gas', 'gás', 'internet', 'telefone', 'neoenergia',
            'caesb', 'correios', 'celpe', 'cemig', 'copel', 'light'
        ],
        'Online': [
            'amazon', 'mercado livre', 'magalu', 'magalupay', 'americanas', 'submarino',
            'shoptime', 'casas bahia', 'netshoes', 'centauro', 'aliexpress',
            'ebay', 'etsy', 'wish', 'shein', 'pagseguro international', 'zaful'
        ],
        'Mensalidades': [
            'netflix', 'spotify', 'disney plus', 'hbo max', 'amazon prime',
            'globoplay', 'fatura', 'youtube premium', 'tim', 'claro', 'vivo', 
            'oi', 'laricell', 'apple music', 'deezer', 'google drive', 'dropbox', 
            'icloud', 'one drive', 'adobe', 'canva', 'notion', 'evernote', 
            'slack', 'zoom', 'microsoft 365'
        ],
        'Saúde': [
            'farmacia', 'farmácia', 'drogaria', 'drogasil', 'pacheco',
            'pague menos', 'hospital', 'clinica', 'clínica', 'laboratorio',
            'laboratório', 'médico', 'medico', 'dentista', 'fisioterapia',
            'plano de saude', 'unimed', 'amil', 'sulamerica', 'bradesco saude',
            'advance fisioterapia'  # Específico do seu extrato
        ],
        'Educação': [
            'escola', 'faculdade', 'universidade', 'curso', 'livro', 'livraria',
            'material escolar', 'estacio', 'ceub', 'unieuro', 'edx', 'alura', 
            'iesb', 'projecao', 'udf', 'papelaria', 'udemy', 'coursera',
            'kaplan', 'wizard', 'ccaa', 'cna', 'fisk'
        ],
        'Lazer': [
            'cinema', 'ciatoy', 'teatro', 'ri happy', 'ingresso', 'netflix', 
            'spotify', 'amazon prime', 'ticket', 'disney', 'hbo', 'apple music', 
            'deezer', 'youtube premium', 'entretenimento', 'globoplay', 
            'crunchyroll', 'paramount', 'steam', 'playstation', 'xbox', 
            'nintendo', 'game'
        ],
        'Vestuário': [
            'renner', 'riachuelo', 'c&a', 'zara', 'hering', 'marisa',
            'pernambucanas', 'magazine luiza', 'nike', 'adidas', 'centauro',
            'netshoes', 'decathlon', 'roupa', 'calcado', 'calçado', 'sapato'
        ],
        'Serviços': [
            'salao', 'salão', 'barbearia', 'cabeleireiro', 'manicure',
            'academia', 'smartfit', 'bluefit', 'bio ritmo', 'lavanderia',
            'costureira', 'chaveiro', 'encanador', 'eletricista'
        ],
        'Investimentos': [
            'investimento', 'aplicacao', 'aplicação', 'poupanca', 'poupança',
            'tesouro', 'cdb', 'lci', 'lca', 'acao', 'ações', 'lig liquidez', 'fundo'
        ]
    }
    
    # PRIMEIRO: Verificar categorias específicas (antes de transferências)
    # Isso garante que "Mc Donalds", "Taguatinga", etc vão para categorias certas
    for categoria, palavras_chave in categorias.items():
        for palavra in palavras_chave:
            if palavra in descricao_lower:
                return categoria
    
    # SEGUNDO: Verificar se é transferência/PIX
    palavras_transferencia = ['pix', 'ted', 'doc', 'transferencia', 'transferência', 'recebido', 'enviado']
    for palavra in palavras_transferencia:
        if palavra in descricao_lower:
            return 'Transferências'
    
    # TERCEIRO: Verificar se parece ser nome de pessoa (PIX para pessoa física)
    # Só chega aqui se não matchou nenhuma categoria específica
    if eh_nome_pessoa(descricao):
        return 'Transferências'
    
    return 'Outros'


def calcular_metricas_avancadas(df):
    """
    Calcula métricas avançadas do extrato
    """
    # Separar gastos e entradas
    gastos = df[df['valor'] < 0]['valor'].abs()
    entradas = df[df['valor'] > 0]['valor']
    
    # Calcular variações (comparando com período anterior)
    dias_periodo = (df['data'].max() - df['data'].min()).days
    if dias_periodo > 0:
        metade_periodo = dias_periodo // 2
        data_meio = df['data'].min() + timedelta(days=metade_periodo)
        
        gastos_periodo1 = df[(df['data'] < data_meio) & (df['valor'] < 0)]['valor'].abs().sum()
        gastos_periodo2 = df[(df['data'] >= data_meio) & (df['valor'] < 0)]['valor'].abs().sum()
        
        entradas_periodo1 = df[(df['data'] < data_meio) & (df['valor'] > 0)]['valor'].sum()
        entradas_periodo2 = df[(df['data'] >= data_meio) & (df['valor'] > 0)]['valor'].sum()
        
        variacao_gastos = ((gastos_periodo2 - gastos_periodo1) / gastos_periodo1 * 100) if gastos_periodo1 > 0 else 0
        variacao_entradas = ((entradas_periodo2 - entradas_periodo1) / entradas_periodo1 * 100) if entradas_periodo1 > 0 else 0
    else:
        variacao_gastos = 0
        variacao_entradas = 0
    
    # Categoria que mais gastou
    if 'categoria' in df.columns:
        categoria_top = (
            df[df['valor'] < 0]
            .groupby('categoria')['valor']
            .sum()
            .abs()
            .idxmax()
        )
    else:
        categoria_top = 'N/A'
    
    metricas = {
        'total_gastos': gastos.sum(),
        'total_entradas': entradas.sum(),
        'ticket_medio': gastos.mean() if len(gastos) > 0 else 0,
        'maior_gasto': gastos.max() if len(gastos) > 0 else 0,
        'gasto_medio_diario': gastos.sum() / max(dias_periodo, 1),
        'categoria_top': categoria_top,
        'variacao_gastos': variacao_gastos,
        'variacao_entradas': variacao_entradas
    }
    
    return metricas


def identificar_gastos_recorrentes(df, min_frequencia=2):
    """
    Identifica gastos que aparecem múltiplas vezes
    """
    gastos = df[df['valor'] < 0].copy()
    
    if gastos.empty:
        return pd.DataFrame()
    
    # Normalizar descrições para melhor agrupamento
    gastos['descricao_norm'] = (
        gastos['descricao']
        .str.lower()
        .str.strip()
        .str[:30]  # Primeiros 30 caracteres
    )
    
    # Agrupar por descrição normalizada
    recorrentes = (
        gastos.groupby('descricao_norm')
        .agg({
            'descricao': 'first',
            'valor': ['count', 'mean', 'sum']
        })
        .reset_index(drop=True)
    )
    
    recorrentes.columns = ['descricao', 'frequencia', 'valor_medio', 'total_gasto']
    recorrentes['valor_medio'] = recorrentes['valor_medio'].abs()
    recorrentes['total_gasto'] = recorrentes['total_gasto'].abs()
    
    # Filtrar apenas os que aparecem mais de min_frequencia vezes
    recorrentes = recorrentes[recorrentes['frequencia'] >= min_frequencia]
    
    return recorrentes.sort_values('total_gasto', ascending=False)


def analisar_tendencias(df):
    """
    Analisa tendências de gastos e comportamento
    """
    dias_periodo = (df['data'].max() - df['data'].min()).days
    
    if dias_periodo < 30:
        return {
            'tendencia_gastos': 'insuficiente',
            'variacao_percentual': 0,
            'dias_analisados': dias_periodo
        }
    
    # Dividir em dois períodos
    metade_periodo = dias_periodo // 2
    data_meio = df['data'].min() + timedelta(days=metade_periodo)
    
    gastos_periodo1 = df[(df['data'] < data_meio) & (df['valor'] < 0)]['valor'].abs().sum()
    gastos_periodo2 = df[(df['data'] >= data_meio) & (df['valor'] < 0)]['valor'].abs().sum()
    
    if gastos_periodo1 > 0:
        variacao = ((gastos_periodo2 - gastos_periodo1) / gastos_periodo1) * 100
    else:
        variacao = 0
    
    if variacao > 5:
        tendencia = 'crescente'
    elif variacao < -5:
        tendencia = 'decrescente'
    else:
        tendencia = 'estável'
    
    return {
        'tendencia_gastos': tendencia,
        'variacao_percentual': variacao,
        'dias_analisados': dias_periodo,
        'periodo1_gastos': gastos_periodo1,
        'periodo2_gastos': gastos_periodo2
    }


def calcular_saude_financeira(df):
    """
    Calcula um score de saúde financeira de 0 a 100
    """
    total_entradas = df[df['valor'] > 0]['valor'].sum()
    total_gastos = df[df['valor'] < 0]['valor'].abs().sum()
    
    if total_entradas == 0:
        return 0
    
    # Taxa de poupança (quanto sobra)
    taxa_poupanca = ((total_entradas - total_gastos) / total_entradas) * 100
    
    # Score baseado em múltiplos fatores
    score = 0
    
    # 1. Taxa de poupança (50 pontos)
    if taxa_poupanca >= 30:
        score += 50
    elif taxa_poupanca >= 20:
        score += 40
    elif taxa_poupanca >= 10:
        score += 25
    elif taxa_poupanca >= 0:
        score += 10
    
    # 2. Diversificação de gastos (25 pontos)
    if 'categoria' in df.columns:
        categorias_usadas = df[df['valor'] < 0]['categoria'].nunique()
        if categorias_usadas >= 5:
            score += 25
        elif categorias_usadas >= 3:
            score += 15
        else:
            score += 5
    
    # 3. Consistência de gastos (25 pontos)
    gastos_mensais = gasto_mensal(df)
    if len(gastos_mensais) > 1:
        cv = gastos_mensais['valor'].std() / gastos_mensais['valor'].mean()
        if cv < 0.2:  # Gastos muito consistentes
            score += 25
        elif cv < 0.4:
            score += 15
        else:
            score += 5
    
    return min(score, 100)