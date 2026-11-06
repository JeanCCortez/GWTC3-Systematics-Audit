"""
JACOBIAN DESTACKING DIAGNOSTIC (EMPIRICAL PROJECTION)
Objetivo: Ler os dados reais do GWTC-3 e aplicar a projeção analítica 
do destacking espacial. O código encontra o pico empiricamente para 
anotação, sem forçar gaussianas artificiais.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# Configuração de estética acadêmica (PRD Standard)
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 12,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'figure.dpi': 300
})

def run_empirical_diagnostic():
    print("="*80)
    print(" METHODOLOGICAL DIAGNOSTIC: JACOBIAN DESTACKING ON REAL DATA")
    print("="*80)
    
    file_path = r"E:\Documentos\rrt\art1\new\GWTC-3-confident.csv"
    
    if not os.path.exists(file_path):
        print(f"[!] ERRO: O ficheiro {file_path} não foi encontrado.")
        return

    # Leitura do ficheiro ignorando possíveis linhas de metadados
    df = pd.read_csv(file_path, comment='#')
    
    col_m1 = next((c for c in df.columns if 'mass_1_source' in c.lower() 
                   and 'lower' not in c.lower() and 'upper' not in c.lower()), None)
    col_m2 = next((c for c in df.columns if 'mass_2_source' in c.lower() 
                   and 'lower' not in c.lower() and 'upper' not in c.lower()), None)
    
    if not col_m1 or not col_m2:
        print("[!] ERRO: Colunas de massa fonte ausentes.")
        return
        
    df_clean = df.dropna(subset=[col_m1, col_m2])
    m1 = df_clean[col_m1].values
    m2 = df_clean[col_m2].values
    
    # Cálculo empírico da Massa de Chirp
    chirp_mass_obs = ((m1 * m2)**0.6) / ((m1 + m2)**0.2)
    print(f"[*] Sucesso: Extraídos {len(chirp_mass_obs)} eventos reais do GWTC-3.")
    
    # Aplicação do Destacking (Fator empírico baseado em beta=0.034)
    inflation_factor = 1.0352
    chirp_mass_corr = chirp_mass_obs / inflation_factor
    print(f"[*] Transformação Jacobiana aplicada (Fator de Deflação: {inflation_factor})")
    
    # KDEs Empíricas
    kde_obs = gaussian_kde(chirp_mass_obs, bw_method=0.25)
    kde_corr = gaussian_kde(chirp_mass_corr, bw_method=0.25)
    
    mass_grid = np.linspace(5, 60, 500)
    pdf_obs = kde_obs(mass_grid)
    pdf_corr = kde_corr(mass_grid)
    
    # --- ENCONTRAR O PICO ANÔMALO EMPIRICAMENTE (30 a 40 M_sun) ---
    mask_anomaly = (mass_grid >= 30) & (mass_grid <= 40)
    peak_idx = np.argmax(pdf_obs[mask_anomaly])
    peak_x = mass_grid[mask_anomaly][peak_idx]
    peak_y = pdf_obs[mask_anomaly][peak_idx]
    
    # Plotagem
    fig, ax = plt.subplots(figsize=(7, 5))
    
    ax.plot(mass_grid, pdf_obs, color='firebrick', linewidth=2.5, label='Reported Demography (Raw GWTC-3)')
    ax.fill_between(mass_grid, 0, pdf_obs, color='firebrick', alpha=0.15)
    
    ax.plot(mass_grid, pdf_corr, color='navy', linestyle='-', linewidth=2.5, label='Jacobian Diagnostic (Phase-Drag Destacked)')
    ax.fill_between(mass_grid, 0, pdf_corr, color='navy', alpha=0.15)
    
    # Seta dinâmica apontando para o pico real nos dados
    ax.annotate(r'Anomalous $\sim 35 M_\odot$ Excess', xy=(peak_x, peak_y), 
                xytext=(peak_x + 5, peak_y + (max(pdf_obs)*0.15)),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6),
                fontsize=10)
    
    ax.set_xlabel(r'Inferred Chirp Mass ($\mathcal{M}$) [$M_\odot$]')
    ax.set_ylabel('Probability Density (Arbitrary Units)')
    ax.set_xlim(5, 60)
    ax.set_ylim(0, max(max(pdf_obs), max(pdf_corr)) * 1.15)
    
    ax.set_yticks([]) 
    plt.title("Empirical Mass Distribution Shift (Diagnostic Projection)", pad=15)
    plt.legend(loc='upper right')
    plt.tight_layout()
    
    plt.savefig('fig1_mass_destacking.pdf')
    print(f"[*] Anotação posicionada precisamente na massa: {peak_x:.2f} M_sun")
    print("    -> Gráfico final gravado como 'fig1_mass_destacking.pdf'")
    print("="*80)

if __name__ == "__main__":
    run_empirical_diagnostic()