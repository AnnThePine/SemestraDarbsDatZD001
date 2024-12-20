import pandas as pd
import matplotlib.pyplot as plt

#Nolasa datus no faila laiki.csv
df = pd.read_csv('laiki.csv')
df.columns = ['Datu_skaits', 'Laiks']

#Sagrupē ik 3 datu_skaits rindiņas un izrēķina tām vidējo vērtību.
grouped = df.groupby('Datu_skaits').apply(
    lambda g: pd.DataFrame({
        'Vidējais_laiks': [g['Laiks'].iloc[i:i+3].mean() for i in range(0, len(g), 3)]
    })
).reset_index(level=1, drop=True).reset_index()

# Saglabā datus jaunā csv failā ("vidējie_laiki.csv")
output_file = 'vidējie_laiki.csv'
grouped.to_csv(output_file, index=False)
print(f"Results saved to {output_file}")

#Uztaisa grafiku
plt.figure(figsize=(10, 6))
plt.plot(
    grouped['Vidējais_laiks'], grouped['Datu_skaits'], marker='o', 
    label="Vidējais Laiks", color='blue', linestyle = 'none'
)

#Saliek grafikam asu, leģendas un paša grafika nosaukumu
plt.xlabel('Vidējais laiks [s]', fontsize=12)
plt.ylabel('Datu skaits', fontsize=12)
plt.title('Vidējais laiks (pandas)', fontsize=14)
plt.legend(fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()