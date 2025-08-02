from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import pandas as pd
import io
import base64
import os
import tempfile
from datetime import datetime
from typing import Dict, Any

def create_pdf_styles():
    """
    Crea gli stili per il documento PDF
    """
    styles = getSampleStyleSheet()
    
    # Stile per il titolo principale
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    ))
    
    # Stile per i sottotitoli
    styles.add(ParagraphStyle(
        name='CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    ))
    
    # Stile per il testo normale
    styles.add(ParagraphStyle(
        name='CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_JUSTIFY
    ))
    
    return styles

def base64_to_image(base64_string: str, width: float = 4*inch) -> Image:
    """
    Converte una stringa base64 in un oggetto Image per ReportLab
    """
    if not base64_string:
        return None
        
    # Decodifica base64
    image_data = base64.b64decode(base64_string)
    
    # Crea un file temporaneo
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        tmp_file.write(image_data)
        tmp_path = tmp_file.name
    
    # Crea l'oggetto Image con dimensioni più piccole
    img = Image(tmp_path, width=width, height=3*inch)
    
    return img, tmp_path

def create_statistics_table(stats: Dict[str, Any]) -> Table:
    """
    Crea una tabella con le statistiche descrittive
    """
    data = [['Metrica', 'Valore']]
    
    # Informazioni dataset
    dataset_info = stats['basic_statistics']['dataset_info']
    data.append(['Numero di righe', str(dataset_info['total_rows'])])
    data.append(['Numero di colonne', str(dataset_info['total_columns'])])
    data.append(['Memoria utilizzata', dataset_info['memory_usage']])
    
    # Valori mancanti
    missing_values = dataset_info['missing_values']
    total_missing = sum(missing_values.values())
    data.append(['Valori mancanti totali', str(total_missing)])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    return table

def create_numeric_summary_table(numeric_summary: Dict[str, Any]) -> Table:
    """
    Crea una tabella con il riassunto delle variabili numeriche
    """
    if not numeric_summary:
        return None
    
    # Header
    columns = list(numeric_summary.keys())
    stats = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
    
    data = [['Statistica'] + columns]
    
    for stat in stats:
        row = [stat.upper()]
        for col in columns:
            value = numeric_summary[col].get(stat, 0)
            if isinstance(value, float):
                row.append(f"{value:.2f}")
            else:
                row.append(str(value))
        data.append(row)
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    return table

def generate_pdf_report(df: pd.DataFrame, analysis_results: Dict[str, Any], filename: str) -> str:
    """
    Genera il report PDF completo
    """
    # Crea il file PDF temporaneo
    pdf_path = f"temp_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    # Inizializza il documento
    doc = SimpleDocTemplate(pdf_path, pagesize=A4, topMargin=1*inch)
    story = []
    styles = create_pdf_styles()
    
    # TITOLO PRINCIPALE
    title = Paragraph(f"📊 Report Statistico - {filename}", styles['CustomTitle'])
    story.append(title)
    story.append(Spacer(1, 20))
    
    # INFORMAZIONI GENERALI
    story.append(Paragraph("📋 Informazioni Dataset", styles['CustomHeading']))
    
    # Tabella con statistiche generali
    stats_table = create_statistics_table(analysis_results)
    story.append(stats_table)
    story.append(Spacer(1, 20))
    
    # TIPI DI COLONNE
    column_types = analysis_results['column_types']
    story.append(Paragraph("🔢 Tipi di Colonne", styles['CustomHeading']))
    
    types_text = f"""
    <b>Colonne Numeriche ({len(column_types['numeric'])}):</b> {', '.join(column_types['numeric']) if column_types['numeric'] else 'Nessuna'}<br/>
    <b>Colonne Categoriche ({len(column_types['categorical'])}):</b> {', '.join(column_types['categorical']) if column_types['categorical'] else 'Nessuna'}<br/>
    <b>Colonne Temporali ({len(column_types['datetime'])}):</b> {', '.join(column_types['datetime']) if column_types['datetime'] else 'Nessuna'}
    """
    story.append(Paragraph(types_text, styles['CustomNormal']))
    story.append(Spacer(1, 20))
    
    # STATISTICHE NUMERICHE
    if 'numeric_summary' in analysis_results['basic_statistics']:
        story.append(PageBreak())
        story.append(Paragraph("📊 Statistiche Descrittive - Variabili Numeriche", styles['CustomHeading']))
        
        numeric_table = create_numeric_summary_table(analysis_results['basic_statistics']['numeric_summary'])
        if numeric_table:
            story.append(numeric_table)
            story.append(Spacer(1, 20))
    
    # GRAFICI DI DISTRIBUZIONE
    story.append(PageBreak())
    story.append(Paragraph("📈 Grafici di Distribuzione", styles['CustomHeading']))
    
    temp_files = []  # Per tenere traccia dei file temporanei da eliminare
    
    for i, plot_b64 in enumerate(analysis_results['plots']['distributions']):
        if plot_b64:
            img, temp_path = base64_to_image(plot_b64, width=4*inch)  # Ridotto da 6 a 4 inch
            temp_files.append(temp_path)
            story.append(img)
            story.append(Spacer(1, 10))  # Ridotto spazio da 15 a 10
    
    # MATRICE DI CORRELAZIONE
    if analysis_results['plots']['correlation_heatmap']:
        story.append(PageBreak())
        story.append(Paragraph("🔗 Matrice di Correlazione", styles['CustomHeading']))
        
        corr_img, temp_path = base64_to_image(analysis_results['plots']['correlation_heatmap'], width=4*inch)
        temp_files.append(temp_path)
        story.append(corr_img)
        story.append(Spacer(1, 10))
    
    # GRAFICI TEMPORALI
    if analysis_results['plots']['time_series']:
        story.append(PageBreak())
        story.append(Paragraph("⏰ Andamenti Temporali", styles['CustomHeading']))
        
        for plot_b64 in analysis_results['plots']['time_series']:
            if plot_b64:
                img, temp_path = base64_to_image(plot_b64, width=4*inch)
                temp_files.append(temp_path)
                story.append(img)
                story.append(Spacer(1, 10))
    
    # GRAFICI CATEGORICI
    if analysis_results['plots']['categorical']:
        story.append(PageBreak())
        story.append(Paragraph("📋 Distribuzioni Categoriche", styles['CustomHeading']))
        
        for plot_b64 in analysis_results['plots']['categorical']:
            if plot_b64:
                img, temp_path = base64_to_image(plot_b64, width=4*inch)
                temp_files.append(temp_path)
                story.append(img)
                story.append(Spacer(1, 10))
    
    # FOOTER
    story.append(PageBreak())
    footer_text = f"""
    <br/><br/>
    <i>Report generato da Statly il {datetime.now().strftime('%d/%m/%Y alle %H:%M')}</i><br/>
    <i>Statly - Analisi Statistica Semplificata</i>
    """
    story.append(Paragraph(footer_text, styles['CustomNormal']))
    
    # Costruisci il PDF
    doc.build(story)
    
    # Pulizia file temporanei
    for temp_file in temp_files:
        try:
            os.unlink(temp_file)
        except:
            pass
    
    return pdf_path
