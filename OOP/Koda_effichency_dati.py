import matplotlib.pyplot as plt
import numpy as np

laiki = {
    "lod1": np.array([1.076963, 1.009974 , 0.997254, 1.031266, 1.032557]),
    "lod5": np.array([1.123743, 1.009090, 1.025543, 1.098922, 1.035158]),
    "lod10": np.array([1.040404, 1.050332, 0.981162, 1.026704, 1.000967]),
    "lod50": np.array([1.042068, 1.060019, 1.013903, 1.052787, 1.037045]),
    "lod100": np.array([1.076536, 1.059948, 1.046332, 1.072513, 1.058344]),
    "lod1000": np.array([2.770935, 2.639781, 2.727597, 2.626006, 2.604084]),
    "lod5000": np.array([6.480999, 6.488184, 6.570326, 6.628771, 6.669182]),
    "lod10000": np.array([10.861531, 11.061050, 11.261991, 10.953151, 11.103859]),
}

laiks = []

for i in laiki.keys():
    avg = np.average(laiki[i])
    laiks.append(avg)

Skaits = [1,5,10,50,100,1000,5000,10000]




plt.figure(figsize=(6, 4))
plt.scatter(Skaits, np.array(laiks), color='blue', marker='o', label = "Laika atkarība no lodīšu skaita datos")
plt.title('Izpildes laika atkarība no lodīšu skaita datos', fontsize=16) 
#plt.xscale("log")
plt.xlabel('Lodīšu skaits', fontsize=14)
plt.ylabel('Laiks (s)', fontsize=14)
plt.legend()
plt.tight_layout()
plt.show()