"""
PHENOMENOLOGICAL BASELINE & LORENTZ SUPPRESSION SCALE
Objetivo: Extrapolar o coeficiente de arrasto a partir de dados ópticos (SDSS).

[!] NOTE: This calculation is for supplementary and diagnostic purposes; 
the precise M_LV numerical derivation is not explicitly used in the main 
methodological manuscript.
"""

import numpy as np

def run_extrapolation():
    print("="*80)
    print(" CROSS-MESSENGER BASELINE & M_LV BOUNDS (SUPPLEMENTARY)")
    print("="*80)

    # 1. Dados Ópticos Macroscópicos (SDSS Quasars)
    z_ref_quasar = 1.5
    dipole_amplitude_opt = 0.27

    # 2. Ambiente Local de Ondas Gravitacionais (GWTC-3)
    z_target_gw = 0.19

    # Extrapolação linear assumindo acoplamento a geodésicas nulas
    beta_predicted = dipole_amplitude_opt * (z_target_gw / z_ref_quasar)

    print("[+] Extrapolating Macroscopic Dipole to GW Local Environment...")
    print(f"    - Quasar Reference Redshift : {z_ref_quasar}")
    print(f"    - Optical Dipole Amplitude  : {dipole_amplitude_opt}")
    print(f"    - GW Target Redshift        : {z_target_gw}")
    print(f"    => Predicted Beta_disp      : {beta_predicted:.4f}")

    # 3. Cálculo da Escala de Supressão de Lorentz (M_LV) - USO SUPLEMENTAR
    # Fórmula: M_LV = (E * D) / delta_Psi
    
    f_gw = 100.0 # Frequência típica do ringdown (Hz)
    
    # Energia do graviton em GeV (E = h*f)
    E_gw_GeV = f_gw * 4.1357e-15 * 1e-9 
    
    distance_Mpc = 800.0 # Distância comóvel típica
    
    # CONVERSÃO CORRETA: Mpc para GeV^-1
    distance_GeV_inv = distance_Mpc * 1.564e38 
    
    delta_psi = beta_predicted # O atraso de fase na ordem do beta
    
    # Calculando a escala de energia (M_LV)
    M_LV = (E_gw_GeV * distance_GeV_inv) / delta_psi

    print("\n[+] Bounding Lorentz-Violating Suppression Scale (M_LV)...")
    print(f"    - Graviton Energy (100 Hz)  : {E_gw_GeV:.2e} GeV")
    print(f"    - Comoving Distance         : {distance_Mpc} Mpc")
    print(f"    - Required M_LV Scale       : {M_LV:.2e} GeV")
    
    planck_scale = 1.22e19
    print(f"\n[!] Planck Scale Reference      : {planck_scale:.2e} GeV")
    if M_LV > planck_scale:
        print("    [ASSESSMENT] The required suppression scale exceeds the Planck scale.")
        print("    [ASSESSMENT] Phenomenological phase-drag remains compatible with local Lorentz constraints.")
    print("="*80)

if __name__ == "__main__":
    run_extrapolation()