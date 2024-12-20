import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime

#sāk laika skaitīšanu
sākums = datetime.datetime.now()

def viskozitāte(d, g, rhoL, rhoS, x, t, D, g_sist, rhoL_sist, rhoS_sist):
    v = x / t
    k = 1 / (1 + 2.4 * (d / D))
    mu = (d**2 * g * (rhoL - rhoS) * k / (18 * v))

    D_v_x = v - (x + x_sist) / t
    D_v_t = v - x / (t + t_sist)
    D_v = np.sqrt(D_v_x**2 + D_v_t**2)

    D_k_d = k - 1 / (1 + 2.4 * ((d + d_sist) / D))
    D_k_D = k - 1 / (1 + 2.4 * (d / (D + D_sist)))
    D_k = np.sqrt(D_k_d**2 + D_k_D**2)

    D_mu_d = mu - ((d + d_sist)**2 * g * (rhoL - rhoS) * k / (18 * v))
    D_mu_g = mu - (d**2 * (g + g_sist) * (rhoL - rhoS) * k / (18 * v))
    D_mu_rhoL = mu - (d**2 * g * ((rhoL + rhoL_sist) - rhoS) * k / (18 * v))
    D_mu_rhoS = mu - (d**2 * g * (rhoL - (rhoS + rhoS_sist)) * k / (18 * v))
    D_mu_k = mu - (d**2 * g * (rhoL - rhoS) * (k + D_k) / (18 * v))
    D_mu_v = mu - (d**2 * g * (rhoL - rhoS) * k / (18 * (v + D_v)))
    D_mu = np.sqrt(D_mu_d**2 + D_mu_g**2 + D_mu_rhoL**2 + D_mu_rhoS**2 + D_mu_k**2 + D_mu_v**2)

    return mu, D_mu

df = pd.read_csv('5_1Viskozitâte.txt', delimiter='\t')
df.columns = df.columns.str.strip()

mērījumi = df[['Diamtrs', 'Laiks1', 'Laiks2', 'Laiks3']].iloc[1:].astype(float)

g = 9.81
x_values = {'Laiks1': 0.093, 'Laiks2': 0.098, 'Laiks3': 0.1}
rhoS = 1260
rhoL = 7500
D = 0.062

x_sist = 0.01
t_sist = 0.16
d_sist = 0.00003
D_sist = 0.00003
g_sist = 0.01
rhoL_sist = 10
rhoS_sist = 10

laiks_kolonnas = ['Laiks1', 'Laiks2', 'Laiks3']
rezultāti = []

for _, rinda in mērījumi.iterrows():
    d = rinda['Diamtrs'] / 1000
    for laiks_kolonna in laiks_kolonnas:
        t = rinda[laiks_kolonna]
        x = x_values[laiks_kolonna]
        mu, D_mu = viskozitāte(d, g, rhoL, rhoS, x, t, D, g_sist, rhoL_sist, rhoS_sist)
        rezultāti.append([d, mu, D_mu])

rezultāti_df = pd.DataFrame(rezultāti, columns=['Diametrs [m]', 'Viskozitāte [Pa·s]', 'Viskozitātes kļūda [Pa·s]'])

vidējais_mu = rezultāti_df['Viskozitāte [Pa·s]'].mean()
vidējais_kļūda = rezultāti_df['Viskozitātes kļūda [Pa·s]'].mean()

fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
measurement_titles = ['1. mērījuma punkts', '2. mērījuma punkts', '3. mērījuma punkts']

for i, (laiks_kolonna, title) in enumerate(zip(laiks_kolonnas, measurement_titles)):
    kolonnas_df = rezultāti_df.iloc[i::3].reset_index(drop=True)
    ax = axes[i]
    ax.errorbar(
        kolonnas_df['Diametrs [m]'], 
        kolonnas_df['Viskozitāte [Pa·s]'], 
        yerr=kolonnas_df['Viskozitātes kļūda [Pa·s]'], 
        fmt='o', ecolor='black', capsize=5, 
        label=f'Glicerīna viskozitāte ar pilno kļūdu'
    )
    ax.axhline(vidējais_mu, color='red', linestyle='--', label='Vidējā viskozitāte')
    x_min, x_max = ax.get_xlim()
    ax.fill_between(
        [x_min, x_max],
        [vidējais_mu - vidējais_kļūda] * 2,
        [vidējais_mu + vidējais_kļūda] * 2,
        color='red', alpha=0.3, label='Viskozitātes vidējā kļūda'
    )

    ax.set_xlabel('Diametrs [m]', fontsize=12)
    if i == 0:
        ax.set_ylabel('Viskozitāte [Pa·s]', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, linestyle='--')

fig.suptitle('Glicerīna viskozitāte', fontsize=16)

plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

#beidz laika skaitīšanu un saliek datus failā "laiki.csv"
Izpildes_laiks = (datetime.datetime.now() - sākums).total_seconds()
formatēšana = f"{Izpildes_laiks:.6f}"
rindu_skaits = len(df) - 1
jaunie_dati = pd.DataFrame([[rindu_skaits, formatēšana]], columns=['Row Count', 'Processing Time'])

datu_fails = 'laiki.csv'

if not pd.io.common.file_exists(datu_fails):
    jaunie_dati.to_csv(datu_fails, index=False)
else:
    jaunie_dati.to_csv(datu_fails, mode='a', header=False, index=False)