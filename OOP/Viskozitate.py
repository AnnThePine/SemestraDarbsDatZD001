import time
start = time.time()


import numpy as np
import matplotlib.pyplot as plt
import json


#Fails = "Testa_dati.json"
Fails = "Data_10000.json"

#ielasa datus no json faila
with open(Fails, "r") as file:
    dati = json.load(file)


#nemainīgie mainīgie
Glicerina_blivums = dati["nemainigie_lielumi"]["glicerina_blivums"]
cil_d = np.array(dati["nemainigie_lielumi"]["cilindra_diametrs"])
cels = dati["nemainigie_lielumi"]["cels"]
G = dati["nemainigie_lielumi"]["g"]

#kļūdas
D_kluda = dati["kludas"]["diametrs"]
Glicerina_kluda = dati["kludas"]["glicerins"]
Cild_kluda = dati["kludas"]["cilindra_diametrs"]
Svaru_kluda = dati["kludas"]["svari"]
Laika_kl = dati["kludas"]["laiks"]
G_kl = dati["kludas"]["g"]
cela_kluda = dati["kludas"]["cels"]


#formulas 1
Ievietosanas_metode = lambda a,b: a-b
Vektor_saskait = lambda a,b : np.sqrt(a**2+b**2)
Tilpum  = lambda a : 4/3*np.pi*(a/2)**3
Gad_kl = lambda a : np.std(a)/ np.sqrt(3)*3.182
Vid = lambda a : sum(a)/len(a)
blIv_lod = lambda a,b : a/b
Starpiba = lambda a,b : a-b
taturformula = lambda a,b : 1/(1+2.4*a/b)
Atrumins = lambda ceels, laiks:ceels/laiks
Viskozitate = lambda dia, g, ro, k, v: dia*dia*g*ro*k/(18*v)
Vektor5 = lambda a,b,c,d,e : np.sqrt(a**2+b**2+c**2+d**2+e**2)


def Cil_diametrs(d, dkl):
    dvid = Vid (d)
    gaad_kl = Gad_kl(d)
    delta_d = Vektor_saskait(gaad_kl, dkl)
    return dvid, delta_d

def vids(e, de):
    svertais= e*de
    vid = sum(svertais)/sum(de)
    kluda = sum(de)/len(e)
    return vid, kluda



#izveido objektu lode, kas ietver visas nepieciešamās funkcijas, lai aprēķinātu nepieciešamo
class Lode():
    def __init__(self, diametrs, laiks, masa):
        self.diametrs = np.array(diametrs)
        self.laiks= np.array(laiks)
        self.masa = np.array(masa)

    def Diametra_kl(self):
        dvid = Vid (self.diametrs)
        gaad_kl = Gad_kl(self.diametrs)
        delta_d = Vektor_saskait(gaad_kl, D_kluda)
        return dvid, delta_d
    
    def Videjais_diametrs_lod(self):
        return Vid (self.diametrs)
    
    
    def Tilpums(self):
        dvid, delta_d = self.Diametra_kl()
        tilpums = Tilpum(dvid)
        v_kluda = Ievietosanas_metode(Tilpum(dvid+delta_d),tilpums)
        return tilpums, v_kluda
    
     
    def Masa(self):
        vid_masa = Vid (self.masa)
        gaad_kl = Gad_kl(self.masa)
        kluda = Vektor_saskait(gaad_kl, Svaru_kluda)
        return vid_masa, kluda
        
        
    def Blīvums(self):
        tilpums, v_kluda = self.Tilpums()
        masa, m_kluda = self.Masa()
        blivums = blIv_lod(masa,tilpums)
        masaparc = Ievietosanas_metode(blIv_lod(masa+m_kluda,tilpums),blivums)
        tilpumparc = Ievietosanas_metode(blIv_lod(masa, tilpums+v_kluda),blivums)
        blivkl = Vektor_saskait(masaparc,tilpumparc)
        return blivums, blivkl
    
    def Blivumu_starpiba(self):
        blivums, blivkl = self.Blīvums()
        bliv_starp = Starpiba(blivums, Glicerina_blivums)
        blivparc = Ievietosanas_metode(Starpiba(blivums+blivkl,Glicerina_blivums ),bliv_starp)
        glicparc = Ievietosanas_metode(Starpiba(blivums, Glicerina_blivums+Glicerina_kluda), bliv_starp)
        starpkl = Vektor_saskait(blivparc,glicparc)
        return bliv_starp, starpkl
    
    def Labojums (self):
        d, dkl = self.Diametra_kl()
        dvid, delta_d  = Cil_diametrs(cil_d, Cild_kluda)
        vert = taturformula (d,dvid)
        dparc = Ievietosanas_metode(taturformula(d+dkl,dvid),vert)
        dvidparc = Ievietosanas_metode(taturformula(d,dvid+delta_d),vert)
        kluda = Vektor_saskait(dparc,dvidparc)
        return vert, kluda
    
    
    def Laika_aprekins (self):
        vid_laik = Vid (self.laiks)
        gaad_kl = Gad_kl(self.laiks)
        kluda = Vektor_saskait(gaad_kl, Laika_kl)
        return vid_laik, kluda
    
    def Atrums(self):
        vid_laik, laika_kluda = self.Laika_aprekins()
        vid_atr = Atrumins(cels, vid_laik)
        paccels = Ievietosanas_metode(Atrumins(cels+cela_kluda,vid_laik), vid_atr)
        parclaik = Ievietosanas_metode(Atrumins(cels, vid_laik+laika_kluda), vid_atr)
        atrkl = Vektor_saskait(paccels,parclaik)
        #print(vid_atr, atrkl)
        return vid_atr, atrkl
    
    def Viskozitates_aprekins(self):
        diametrs, diametra_kluda = self.Diametra_kl()
        bliv_starp, starpkl = self.Blivumu_starpiba()
        k, k_kluda = self.Labojums()
        v, v_kluda = self.Atrums()
        viskoz = Viskozitate(diametrs,G,bliv_starp,k,v)
        diapar = Ievietosanas_metode(Viskozitate(diametrs+diametra_kluda,G,bliv_starp,k,v),viskoz)
        gpar = Ievietosanas_metode(Viskozitate(diametrs,G+G_kl,bliv_starp,k,v),viskoz)
        blivpar = Ievietosanas_metode(Viskozitate(diametrs,G,bliv_starp+starpkl,k,v),viskoz)
        kpar = Ievietosanas_metode(Viskozitate(diametrs,G,bliv_starp,k+k_kluda,v),viskoz)
        vpar = Ievietosanas_metode(Viskozitate(diametrs,G,bliv_starp,k,v+v_kluda),viskoz)
        kluda = Vektor5(diapar, gpar, blivpar,kpar, vpar)
        return viskoz, kluda
        
    
    def Viskozitates_vertiba(self):
        viskoz, kluda =self.Viskozitates_aprekins()
        return viskoz
    
    def Viskozitates_kluda (self):
        viskoz, kluda =self.Viskozitates_aprekins()
        return kluda
    
viskkluda = []
viskoz = []
diametrs = []

a = 0   

for lodite in dati["lodites"]:
    lode = Lode(dati["lodites"][lodite]["diametrs"],dati["lodites"][lodite]["laiks"],dati["lodites"][lodite]["masa"])
    viskkluda.append(float(lode.Viskozitates_kluda()))
    viskoz.append(float(lode.Viskozitates_vertiba()))
    diametrs.append(float(lode.Videjais_diametrs_lod()))
    a=1+a
    


vidvisk, vidviskkluda  = vids(np.array(viskoz), np.array(viskkluda))
x=np.linspace(min(diametrs)- 0.0002, max(diametrs) +0.0002)



plt.figure(figsize=(10, 6))
plt.scatter(diametrs, viskoz, color='blue', marker='o', label = "Viskozitātes atkarība no lodītes diametra")
plt.errorbar(diametrs, viskoz, xerr=D_kluda, yerr=viskkluda, fmt='o', color='blue', ecolor='black', capsize=7)
plt.title('Viskozitātes atkarība no lodītes diametra', fontsize=16)
plt.xlabel('Lodītes diametrs (m)', fontsize=14)
plt.ylabel('Viskozitāte ()', fontsize=14)
plt.axhline(y=vidvisk, color='red', linestyle='--', label = "vidējā svērtā viskozitāte")
plt.fill_between(x , y1=vidvisk-vidviskkluda, y2=vidvisk+vidviskkluda,color='red', alpha=.15, linewidth=0, label = "vidējās viskozitātes kļūda")
plt.xlim(left = min(diametrs)- 0.0002, right = max(diametrs)+ 0.0002)
plt.legend()
plt.tight_layout()
#plt.savefig('', dpi=300)

print(f'{time.time() - start:.6f} sekundes, {a} lodites.')

#plt.show()