import pandas as pd
import numpy as np

def preprocess(df):
    """
    Processa e limpa o DataFrame do extrato bancário
    Corrige problema de conversão de valores monetários mistos
    """
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
    )

    df = df.rename(columns={
        'data_lançamento': 'data',
        'histórico': 'historico',
        'descrição': 'descricao',
        'valor': 'valor',
        'saldo': 'saldo'
    })

    df['data'] = pd.to_datetime(df['data'], dayfirst=True)

    # 🔥 CONVERSÃO ROBUSTA DE VALORES MONETÁRIOS
    # Problema: O Banco Inter pode exportar em formato BR (vírgula) ou US (ponto)
    # Precisamos detectar automaticamente o formato
    for col in ['valor', 'saldo']:
        def converter_valor_monetario(valor_str):
            """
            Converte strings monetárias nos formatos:
            - Brasileiro: 1.234,56 ou 40,00
            - Americano: 1,234.56 ou 40.00 ou 545.76
            """
            if pd.isna(valor_str):
                return np.nan
            
            valor_str = str(valor_str).strip()
            
            # Remove espaços
            valor_str = valor_str.replace(' ', '')
            
            # Conta quantas vírgulas e pontos existem
            num_virgulas = valor_str.count(',')
            num_pontos = valor_str.count('.')
            
            # Formato brasileiro: vírgula é decimal
            if num_virgulas == 1 and num_pontos <= 1:
                if num_pontos == 1:
                    # Ex: 1.234,56 - remove ponto (milhar) e troca vírgula por ponto
                    valor_str = valor_str.replace('.', '').replace(',', '.')
                else:
                    # Ex: 40,00 ou -40,00 - apenas troca vírgula por ponto
                    valor_str = valor_str.replace(',', '.')
            
            # Formato americano: ponto é decimal
            elif num_pontos == 1 and num_virgulas == 0:
                # Ex: 545.76 ou 40.00 ou -40.00 - já está correto
                pass
            
            # Tem vírgula como separador de milhar
            elif num_pontos == 1 and num_virgulas >= 1:
                # Ex: 1,234.56 - remove vírgula (milhar)
                valor_str = valor_str.replace(',', '')
            
            # Apenas pontos (milhares)
            elif num_pontos > 1 and num_virgulas == 0:
                # Ex: 1.234.567 - remove pontos (milhares)
                valor_str = valor_str.replace('.', '')
            
            # Apenas vírgulas
            elif num_virgulas > 1 and num_pontos == 0:
                # Ex: 1,234,567 - remove vírgulas (milhares)
                valor_str = valor_str.replace(',', '')
            
            # Misto complexo
            elif num_pontos > 0 and num_virgulas > 0:
                # Descobre qual é o separador decimal (último caractere especial)
                ultima_virgula = valor_str.rfind(',')
                ultimo_ponto = valor_str.rfind('.')
                
                if ultima_virgula > ultimo_ponto:
                    # Vírgula é decimal: Ex: 1.234.567,89
                    valor_str = valor_str.replace('.', '').replace(',', '.')
                else:
                    # Ponto é decimal: Ex: 1,234,567.89
                    valor_str = valor_str.replace(',', '')
            
            try:
                return float(valor_str)
            except ValueError:
                print(f"Erro ao converter: {valor_str}")
                return np.nan
        
        df[col] = df[col].apply(converter_valor_monetario)

    df = df.dropna(subset=['data', 'valor'])

    df['ano'] = df['data'].dt.year
    df['mes'] = df['data'].dt.month
    df['mes_ano'] = df['data'].dt.to_period('M').astype(str)
    df['semestre'] = df['data'].dt.month.apply(lambda x: 1 if x <= 6 else 2)

    return df