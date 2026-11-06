"""
PARAMETRIC DEGENERACY ENGINE
Objetivo: Demonstrar analiticamente o mecanismo de degenerescência em templates IMR.
A atenuação viscosa (arrasto) corta o espectro de frequências (ringdown) prematuramente. 
Para maximizar a verossimilhança (Likelihood) num template de vácuo sem perdas, 
o algoritmo é matematicamente forçado a inflar a massa inferida.
"""

def run_mechanism_proof():
    print("="*80)
    print(" METHODOLOGICAL AUDIT: DEGENERACY MECHANISM (DISPERSIVE PHASE-DRAG)")
    print("="*80)

    # 1. A Fonte Física (Massa real injetada)
    true_mass = 30.0 # Massa total em massas solares
    # A frequência de corte (ISCO) no vácuo perfeito (f ~ 1/M)
    f_isco_true = 4400.0 / true_mass 
    
    print(f"[*] True Source Mass (Injected)      : {true_mass:.2f} M_sun")
    print(f"[*] True Cutoff Frequency (ISCO)     : {f_isco_true:.1f} Hz")

    # 2. O Arrasto Fenomenológico (Phase Impedance Baseline)
    beta_dispersive = 0.034 
    
    # A onda atinge o detector truncada prematuramente
    f_isco_observed = f_isco_true * (1 - beta_dispersive)
    
    print(f"[*] Dispersive Drag Baseline (Beta)  : {beta_dispersive}")
    print(f"[*] Observed Truncated Frequency     : {f_isco_observed:.1f} Hz")

    # 3. Recuperação Bayesiana (Template Lossless)
    # O pipeline busca o melhor fit assumindo propagação em vácuo perfeito
    recovered_mass = 4400.0 / f_isco_observed
    
    inflation_pct = ((recovered_mass - true_mass) / true_mass) * 100

    print("\n" + "="*80)
    print(" BAYESIAN RECOVERY VERDICT (ALGORITHMIC BIAS)")
    print("="*80)
    print(f"Inferred Mass (Lossless Template) : {recovered_mass:.4f} M_sun")
    print(f"Systematic Algorithmic Inflation  : +{inflation_pct:.2f}%")
    print("="*80)

if __name__ == "__main__":
    run_mechanism_proof()