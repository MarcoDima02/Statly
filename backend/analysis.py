import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from datetime import datetime
from typing import Dict, List, Any
import json

# Configurazione stile matplotlib
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def convert_numpy_types(obj):
    """
    Converte tipi NumPy in tipi Python standard per la serializzazione JSON
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    return obj

def detect_column_types(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Classifica le colonne del DataFrame per tipo di dato
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = []
    
    # Prova a identificare colonne temporali
    for col in categorical_cols.copy():
        if 'data' in col.lower() or 'date' in col.lower() or 'time' in col.lower():
            try:
                pd.to_datetime(df[col])
                datetime_cols.append(col)
                categorical_cols.remove(col)
            except:
                pass
    
    return {
        'numeric': numeric_cols,
        'categorical': categorical_cols,
        'datetime': datetime_cols
    }

def basic_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calcola statistiche descrittive di base
    """
    stats = {
        'dataset_info': {
            'total_rows': int(len(df)),
            'total_columns': int(len(df.columns)),
            'missing_values': {col: int(df[col].isnull().sum()) for col in df.columns},
            'memory_usage': f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"
        }
    }
    
    # Statistiche per colonne numeriche
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        numeric_describe = df[numeric_cols].describe()
        stats['numeric_summary'] = {}
        for col in numeric_cols:
            stats['numeric_summary'][col] = {
                'count': int(numeric_describe.loc['count', col]),
                'mean': float(numeric_describe.loc['mean', col]),
                'std': float(numeric_describe.loc['std', col]),
                'min': float(numeric_describe.loc['min', col]),
                '25%': float(numeric_describe.loc['25%', col]),
                '50%': float(numeric_describe.loc['50%', col]),
                '75%': float(numeric_describe.loc['75%', col]),
                'max': float(numeric_describe.loc['max', col])
            }
        
        # Correlazioni se ci sono almeno 2 colonne numeriche
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr()
            stats['correlations'] = {}
            for col1 in numeric_cols:
                stats['correlations'][col1] = {}
                for col2 in numeric_cols:
                    corr_val = corr_matrix.loc[col1, col2]
                    if pd.notna(corr_val):
                        stats['correlations'][col1][col2] = float(corr_val)
                    else:
                        stats['correlations'][col1][col2] = None
    
    # Statistiche per colonne categoriche
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        stats['categorical_summary'] = {}
        for col in categorical_cols:
            mode_val = df[col].mode()
            stats['categorical_summary'][col] = {
                'unique_values': int(df[col].nunique()),
                'most_frequent': mode_val.iloc[0] if not mode_val.empty else None,
                'value_counts': {str(k): int(v) for k, v in df[col].value_counts().head(5).items()}
            }
    
    return stats

def create_distribution_plots(df: pd.DataFrame) -> List[str]:
    """
    Crea grafici di distribuzione per le colonne numeriche
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    plot_images = []
    
    for col in numeric_cols[:4]:  # Limita a 4 grafici per evitare overload
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))  # Ridotto da 12,5 a 10,4
        
        # Istogramma
        ax1.hist(df[col].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax1.set_title(f'Distribuzione di {col}')
        ax1.set_xlabel(col)
        ax1.set_ylabel('Frequenza')
        ax1.grid(True, alpha=0.3)
        
        # Box plot
        ax2.boxplot(df[col].dropna())
        ax2.set_title(f'Box Plot di {col}')
        ax2.set_ylabel(col)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Converti in base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')  # Ridotto DPI da 300 a 150
        img_buffer.seek(0)
        img_b64 = base64.b64encode(img_buffer.read()).decode()
        plot_images.append(img_b64)
        
        plt.close()
    
    return plot_images

def create_correlation_heatmap(df: pd.DataFrame) -> str:
    """
    Crea una heatmap delle correlazioni tra variabili numeriche
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        return None
    
    plt.figure(figsize=(8, 6))  # Ridotto da 10,8 a 8,6
    correlation_matrix = df[numeric_cols].corr()
    
    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=0.5
    )
    
    plt.title('Matrice di Correlazione', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    # Converti in base64
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')  # Ridotto DPI
    img_buffer.seek(0)
    img_b64 = base64.b64encode(img_buffer.read()).decode()
    
    plt.close()
    
    return img_b64

def create_time_series_plots(df: pd.DataFrame, column_types: Dict[str, List[str]]) -> List[str]:
    """
    Crea grafici temporali se sono presenti colonne di data/tempo
    """
    datetime_cols = column_types['datetime']
    numeric_cols = column_types['numeric']
    plot_images = []
    
    for date_col in datetime_cols:
        # Converti la colonna in datetime
        df_temp = df.copy()
        df_temp[date_col] = pd.to_datetime(df_temp[date_col])
        df_temp = df_temp.sort_values(date_col)
        
        for num_col in numeric_cols[:2]:  # Max 2 grafici per colonna temporale
            plt.figure(figsize=(10, 4))  # Ridotto da 12,6 a 10,4
            
            plt.plot(df_temp[date_col], df_temp[num_col], marker='o', linewidth=2, markersize=4)
            plt.title(f'Andamento di {num_col} nel Tempo', fontsize=12, fontweight='bold')  # Ridotto font
            plt.xlabel(date_col)
            plt.ylabel(num_col)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Converti in base64
            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')  # Ridotto DPI
            img_buffer.seek(0)
            img_b64 = base64.b64encode(img_buffer.read()).decode()
            plot_images.append(img_b64)
            
            plt.close()
    
    return plot_images

def create_categorical_plots(df: pd.DataFrame) -> List[str]:
    """
    Crea grafici per variabili categoriche
    """
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    plot_images = []
    
    for col in categorical_cols[:3]:  # Limita a 3 grafici
        if df[col].nunique() > 20:  # Skip colonne con troppe categorie
            continue
            
        plt.figure(figsize=(8, 4))  # Ridotto da 10,6 a 8,4
        
        value_counts = df[col].value_counts().head(10)  # Top 10 valori
        
        plt.bar(range(len(value_counts)), value_counts.values, color='lightcoral', alpha=0.8)
        plt.title(f'Distribuzione di {col}', fontsize=12, fontweight='bold')  # Ridotto font
        plt.xlabel(col)
        plt.ylabel('Frequenza')
        plt.xticks(range(len(value_counts)), value_counts.index, rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        # Converti in base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')  # Ridotto DPI
        img_buffer.seek(0)
        img_b64 = base64.b64encode(img_buffer.read()).decode()
        plot_images.append(img_b64)
        
        plt.close()
    
    return plot_images

def perform_statistical_analysis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Funzione principale che coordina tutta l'analisi statistica
    """
    # Identifica i tipi di colonne
    column_types = detect_column_types(df)
    
    # Statistiche di base
    basic_stats = basic_statistics(df)
    
    # Crea tutti i grafici
    distribution_plots = create_distribution_plots(df)
    correlation_heatmap = create_correlation_heatmap(df)
    time_series_plots = create_time_series_plots(df, column_types)
    categorical_plots = create_categorical_plots(df)
    
    # Componi il risultato finale
    results = {
        'column_types': column_types,
        'basic_statistics': basic_stats,
        'plots': {
            'distributions': distribution_plots,
            'correlation_heatmap': correlation_heatmap,
            'time_series': time_series_plots,
            'categorical': categorical_plots
        },
        'analysis_timestamp': datetime.now().isoformat()
    }
    
    # Converti tutti i tipi NumPy in tipi Python standard
    results = convert_numpy_types(results)
    
    return results
