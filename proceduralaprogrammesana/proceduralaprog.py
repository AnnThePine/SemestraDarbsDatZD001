#visi dati tiek pierakstīti ar SI sistēmas mērvienībām
#importē bibliotēkas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#funkcija kas aprēķina vidējo viskozitāti lodītei, kā arī pilno kļūdu
def viskozitāte(d, g, rhoL, rhoS, x, t, D, g_sist, rhoL_sist, rhoS_sist):
    v = x / t
    #aprēķina korelācijas koeficientu k
    k = 1 / (1 + 2.4 * (d / D))
    #aprēķina viskozitāti - viskozitātes koeficients mu
    mu = (d**2 * g * (rhoL - rhoS) * k / (18 * v))

    #rēķina kļūdas
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

    #atgriež viskozitātes koeficientu mu un pilno kļūdu D_mu
    return mu, D_mu

#ar pandas bibliotēku lasa datu failu
df = pd.read_csv('5_1Viskozitâte.txt', delimiter='\t')
df.columns = df.columns.str.strip()

#pārdefinē skaitļus no string us float
mērījumi = df[['Diamtrs', 'Laiks1', 'Laiks2', 'Laiks3']].iloc[1:].astype(float)

#konstantes
g = 9.81
x_vērtības = {'Laiks1': 0.093, 'Laiks2': 0.098, 'Laiks3': 0.1}
rhoS = 1260
rhoL = 7500
D = 0.062

#sistemātiskās kļūdas
x_sist = 0.01
t_sist = 0.16
d_sist = 0.00003
D_sist = 0.00003
g_sist = 0.01
rhoL_sist = 10
rhoS_sist = 10

#piešķir katrai vērtībai tukšu sarakstu
laiks_kolonnas = ['Laiks1', 'Laiks2', 'Laiks3']
rezultāti = []

#aprēķina viskozitāti un kļūdas katrai kolonnai
for _, rinda in mērījumi.iterrows():
    d = rinda['Diamtrs'] / 1000  
    for laiks_kolonna in laiks_kolonnas:
        t = rinda[laiks_kolonna]
        x = x_vērtības[laiks_kolonna]   
        mu, D_mu = viskozitāte(d, g, rhoL, rhoS, x, t, D, g_sist, rhoL_sist, rhoS_sist)
        rezultāti.append([d, mu, D_mu])

#pārveido sarakstu par DataFrame
rezultāti_df = pd.DataFrame(rezultāti, columns=['Diametrs [m]', 'Viskozitāte [Pa·s]', 'Viskozitātes kļūda [Pa·s]'])

#aprēķina vidējo viskozitāti un kļūdu
vidējais_mu = rezultāti_df['Viskozitāte [Pa·s]'].mean()
vidējais_kļūda = rezultāti_df['Viskozitātes kļūda [Pa·s]'].mean()

#uztaisa 3 grafikus, kuriem ir 1 y ass
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

#katram grafikam pielikts savs virsraksts
measurement_titles = ['1. mērījuma punkts', '2. mērījuma punkts', '3. mērījuma punkts']

#katram mērījumam grafikā piemēro vienu punktu, kā arī kļūdu līnijas
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
    #uztaisa vidējās vērtības līniju, ar vīdējo kļūdu laukumu ap to
    ax.axhline(vidējais_mu, color='red', linestyle='--', label='Vidējā viskozitāte')
    x_min, x_max = ax.get_xlim()
    ax.fill_between(
        [x_min, x_max],
        [vidējais_mu - vidējais_kļūda] * 2,
        [vidējais_mu + vidējais_kļūda] * 2,
        color='red', alpha=0.3, label='Viskozitātes vidējā kļūda'
    )
    #uztaisa virstrakstus asīm un nosaka leģendas novietojumu
    ax.set_xlabel('Diametrs [m]', fontsize=12)
    if i == 0:
        ax.set_ylabel('Viskozitāte [Pa·s]', fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(loc='lower right', fontsize=10)
    ax.grid(True, linestyle='--')

#uztaisa virsrakstu visam grafikam
fig.suptitle('Glicerīna viskozitāte', fontsize=16)

#grafikus sašaurina un parāda gala grafiku
plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.show()

'''
Mainīgo nosaukumu atšifrējums viskozitātes funkcijai
d - lodītes diametrs
g -Zemes gravitācijas paātrinājums
rhoL - lodītes blīvums
rhoS - šķīduma (glicerīna) blīvums
x - pārvietojums starp mērījuma vietām
t - laiks
D - mērcilindra diametrs
g_sist - sistemātiskā kļūda Zemes gravitācijas paātrinājumam
rhoL_sist - sistemātiskā kļūda lodītes blīvumam
rhoS_sist - sistemātiskā kļūda šķīduma (glicerīna) blīvumam
k - korelācijas koeficients
mu - viskozitātes koeficients
D_v_x - ātruma pilnās kļūdas aprēķināšana ar ievietošanas metodi pēc pārvietojuma
D_v_t - ātruma pilnās kļūdas aprēķināšana ar ievietošanas metodi pēc laika
D_v - ātruma pilnā kļūda
D_k_d - korelācijas koeficienta pilnās kļūdas aprēķināšana ar ievietošanas metodi pēc lodītes diametra
D_k_D - korelācijas koeficienta pilnās kļūdas aprēķināšana ar ievietošanas metodi pēc mērcilindra diametra
D_k -korelācijas koeficienta pilnā kļūda
D_mu_d - viskozitātes koeficienta pilnās kļūdas aprēķināšana ar ievietošanas metodi pēc pārvietojuma
D_mu_g - viskozitātes koeficienta pilnās kļūdas aprēķināšana ar ievietošanas metodi pēc gravitācoijas paātrinājuma
D_mu_rhoL - viskozitātes koeficienta pilnās kļūdas aprēķināšana ar ievietošanas metodi pēc lodītes blīvuma
D_mu_rhoS - viskozitātes koeficienta pilnās kļūdas aprēķināšana ar ievietošanas metodi pēc šķīduma (glicerīna) blīvuma
D_mu_k - viskozitātes koeficienta pilnās kļūdas aprēķināšana ar ievietošanas metodi pēc korelācijas koeficienta
D_mu_v - viskozitātes koeficienta pilnās kļūdas aprēķināšana ar ievietošanas metodi pēc lodītes ātruma
D_mu - viskozitātes koeficienta pilnā kļūda
x_vērtības - pārvietojuma vērtības katram posmam
x_sist - pārvietojuma sistemātiskā kļūda
t_sist - laika sistemātiskā kļūda
d_sist lodītes diametra sistemātiskā kļūda
D_sist - mērcilindra diametra sistemātiskā kļūda
'''