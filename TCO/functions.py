# Importer les données 
import pandas as pd
df_ve = pd.read_csv('Csv après traitement/df_ve_clean.csv')
df_region = pd.read_csv('Csv après traitement/df_region_clean.csv')
df_entretien = pd.read_csv('Csv après traitement/df_entretien_clean.csv')
df_vt = pd.read_csv('Csv après traitement/df_vt_clean.csv')

## Calcul des indicateurs pour la voiture Thermique ## 

# Definir la fonction cost_vt
# return price_vt = le prix d'achat moyen pour la categorie de VT selectionnée
def cost_vt (categorie):
  mod = df_vt['categorie_vt'].str.contains(categorie)
  price_vt = df_vt['prix_moyen_categorie'][list(df_vt['categorie_vt']).index(categorie)]
  return price_vt

# Pas d'aides allouées pour les véhicules thermiques #


# Définir la fonction cartegrise_cost_vt 
# return total_cartegrise_cost_vt == le prix de la CG pour la categorie de VT concernée
def cartegrise_cost_vt(statut,region_name, categorie):
  taxe_regionale = df_region['montant_taxe_region_vt'][list(df_region['region']).index(region_name)] * (df_vt['CV_categorie'][list(df_vt['categorie_vt']).index(categorie)])
  taxe_fixe = df_region['taxe_fixe'][list(df_region['region']).index(region_name)]
  frais_supp = df_region['frais_supp'][list(df_region['region']).index(region_name)]
  taxe_pro = df_region['taxe_pro'][list(df_region['region']).index(region_name)]
  if statut =="particulier":
    total_cartegrise_cost_vt = taxe_regionale + taxe_fixe + frais_supp
  elif statut =="professionnel":
    total_cartegrise_cost_vt = taxe_regionale + taxe_fixe + frais_supp + taxe_pro
  return total_cartegrise_cost_vt

# Definir la fonction calcul_tvs_vt 
# return tvs_vt == prix estimé pour la tvs / an 
def calcul_tvs_vt(statut, categorie):
  if statut == 'professionnel' :
    premiere_composante = df_vt['tvs_moyenne_un'][list(df_vt['categorie_vt']).index(categorie)]
    deuxieme_composante = df_vt['tvs_seconde_composante'][list(df_vt['categorie_vt']).index(categorie)]
    tvs_vt = int(premiere_composante + deuxieme_composante)
  else :
    tvs_vt = 0
  return tvs_vt 

# Definir la fonction carburant_cost
# return total_carburant_cost == prix estimé du carburant / 1 an pour un VT 
def carburant_cost_vt (categorie, profil):
  cout = df_vt['conso_100km_categorie'][list(df_vt['categorie_vt']).index(categorie)]
  if profil == 30000:
    total_carburant_cost = round((cout/100) * 30000,2)
  elif profil == 20000:
    total_carburant_cost = round((cout/100) * 20000,2)
  else:
    total_carburant_cost = round((cout/100) * 15000,2)
  return total_carburant_cost

# Definir la fonction prix_stationnement_vt
# return : prix_vt = prix du stationnement / vt / 1 an / region
def prix_stationnement_vt(region_name):
   prix_vt = df_region['prix_stationnement_vt'][list(df_region['region']).index(region_name)]
   return prix_vt

# Definir la fonction entretien_cost_vt
# total_entretien_vt == cout de l'entretien / 5 ans / vt
def entretien_cost_vt (profil):
  if profil == 30000:
    total_entretien_vt = df_entretien.loc[1,['R1','R2','R3','R4','R5','CT']].sum()
  elif profil == 20000:
    total_entretien_vt= df_entretien.loc[1,['R1','R2','R3','CT']].sum()
  elif profil == 15000:
    total_entretien_vt = df_entretien.loc[1,['R1','R2','CT']].sum()
  return total_entretien_vt

# Definir la fonction impact_co2_vt 
# return total_co2 == emission de co2 moyennes pour la categorie de vt exprimé en tonnes / an
# paris_ny == equivalent A/R paris-NY en avion (round à l'entier supérieur) 

def impact_co2_vt (categorie,profil):
  cat = df_vt['categorie_vt'].str.contains(categorie)
  conso_co2 = df_vt['co2_categorie'][list(df_vt['categorie_vt']).index(categorie)]
  if profil == 30000:
    total_co2_vt = conso_co2 * 30000
    paris_ny = round(total_co2_vt/1000000)
  elif profil == 20000:
    total_co2_vt = conso_co2 * 20000
    paris_ny = round(total_co2_vt/1000000)
  elif profil == 15000:
    total_co2_vt = conso_co2 * 15000
    paris_ny = round(total_co2_vt/1000000)
  return total_co2_vt/1000000, paris_ny

## Calcul du TCO pour la voiture Thermique 
# tco_vt == Total Cost of Ownership / 5 ans moyen (pour la categorie de voiture Thermique)
def calcul_tco_vt(categorie, region_name, statut,profil):
  price = cost_vt(categorie)
  aides_vt = 0 # jamais d'aides pour les Véhicules Thermiques
  cg_cost = cartegrise_cost_vt(statut,region_name, categorie)
  carburant = carburant_cost_vt(categorie,profil)
  stationnement = prix_stationnement_vt(region_name)
  entretien = entretien_cost_vt(profil)
  tvs = calcul_tvs_vt(statut, categorie)
  tco_vt = round((price - aides_vt) + cg_cost + (carburant*5) + (stationnement*5) + (entretien) + (tvs*5),2)
  return tco_vt

# Définir la fonction impact_co2_vt 
# return total_co2_vt == emission de co2 moyennes pour la categorie de vt exprimé en tonnes / an
# paris_ny == equivalent A/R paris-NY en avion (round à l'entier supérieur) 

def impact_co2_vt (categorie,profil):
  cat = df_vt['categorie_vt'].str.contains(categorie)
  conso_co2 = df_vt['co2_categorie'][list(df_vt['categorie_vt']).index(categorie)]
  if profil == 30000:
    total_co2_vt = conso_co2 * 30000
    paris_ny = round(total_co2_vt/1000000)
  elif profil == 20000:
    total_co2_vt = conso_co2 * 20000
    paris_ny = round(total_co2_vt/1000000)
  elif profil == 15000:
    total_co2_vt = conso_co2 * 15000
    paris_ny = round(total_co2_vt/1000000)
  return total_co2_vt/1000000, paris_ny

## Calcul des indicateurs pour la voiture Electrique ## 

# Definir la fonction cost_ve
# return price_ve = le prix d'achat pour 1 modèle de VE
def cost_ve (modele):
  mod = df_ve['modele_ve'].str.contains(modele)
  price_ve = df_ve['cout_achat'][list(df_ve['modele_ve']).index(modele)]
  return price_ve

# Definir la fonction calcul_aides
# return bonus_eco == valeur nationale
# region_aides = montant variable en fonction de la région et/ou du statut 
def calcul_aides(region_name,statut):
   region_aides = 0
   bonus_eco = df_region['bonus_eco'][0]
   if statut == 'professionnel' and df_region['aides_region_profesionnel'][list(df_region['region']).index(region_name)] == True :
      region_aides = df_region['montant_aides_pro'][list(df_region['region']).index(region_name)]
   else : 
      region_aides = 0
   if statut == 'particulier' and df_region['aides_region_particulier'][list(df_region['region']).index(region_name)] == True :
      region_aides = df_region['montant_aides_part'][list(df_region['region']).index(region_name)]
   else : 
      region_aides = 0
   return bonus_eco, region_aides

# definir la fonction cartegrise_cost_ve
# return total_cartegrise_cost_ve == total des frais a payer pour la carte grise d'un VE  
def cartegrise_cost_ve(statut,region_name):
  taxe_regionale = df_region['montant_taxe_region_vt'][list(df_region['region']).index(region_name)] * 0
  taxe_fixe = df_region['taxe_fixe'][list(df_region['region']).index(region_name)]
  frais_supp = df_region['frais_supp'][list(df_region['region']).index(region_name)]
  taxe_pro = df_region['taxe_pro'][list(df_region['region']).index(region_name)]
  if statut =="particulier":
    total_cartegrise_cost_ve = taxe_regionale + taxe_fixe + frais_supp
  elif statut =="professionnel":
    total_cartegrise_cost_ve = taxe_regionale + taxe_fixe + frais_supp + taxe_pro
  return total_cartegrise_cost_ve

# Pas de TVS à payer pour les véhicules électriques
########

# Pour le coût de la recharge
# return total_cost == prix estimé de la recharge / 1 an pour un VE 
def recharge_cost (modele, profil):
  mod = df_ve['modele_ve'].str.contains(modele)
  cout = df_ve['cout_de_la_recharge_100km'][list(df_ve['modele_ve']).index(modele)]
  if profil == 30000:
    total_cost = round((cout/100) * 30000,2)
  elif profil == 20000:
    total_cost = round((cout/100) * 20000,2)
  else:
    total_cost = round((cout/100) * 15000,2)
  return total_cost

# Definir la fonction prix_stationnement_ve 
# return :
        # prix_ve == prix du stationnement / ve / 1 an / region
        # free_cities == Liste de villes avec stationenement gratuit pour les VE
        # pref_cities == Liste de villes avec stationnement a tarif préférentiel pour les VE
# Si free_cities et/ou pref_cities ne contient pas de villes, 
# Valeur définie dans le df == Aucune ville dans votre région
def prix_stationnement_ve(region_name):
   prix_ve = df_region['prix_stationnement_ve'][list(df_region['region']).index(region_name)]
   free_cities = ""
   if free_cities != 'Aucune ville dans votre région':
      free_cities = df_region['ville_avec_gratuite_ve'][list(df_region['region']).index(region_name)]
   pref_cities = ""
   if pref_cities != 'Aucune ville dans votre région':
      pref_cities = df_region['ville_avec_tp_ve'][list(df_region['region']).index(region_name)]
   return prix_ve, free_cities, pref_cities

# Definir entretien_cost_ve 
# total_entretien_ve == cout de l'entretien / 5 ans / ve
def entretien_cost_ve (profil):
  total_entretien_ve = 0
  if profil == 30000:
    total_entretien_ve = df_entretien.loc[0,['R1','R2','R3','R4','R5','CT']].sum()
  elif profil == 20000:
    total_entretien_ve = df_entretien.loc[0,['R1','R2','R3','CT']].sum()
  elif profil == 15000:
    total_entretien_ve = df_entretien.loc[0,['R1','R2','CT']].sum()
  return total_entretien_ve

## Calcul du TCO pour la voiture Electrique 

def tco_ve(modele, region_name, statut,profil):
  price = cost_ve(modele)
  bonus_eco = calcul_aides(region_name,statut)[0]
  aides_region = calcul_aides(region_name,statut)[1] 
  cg_cost = cartegrise_cost_ve(statut,region_name)
  recharge = recharge_cost(modele,profil)
  tvs = 0
  stationnement = prix_stationnement_ve(region_name)[0]
  entretien = entretien_cost_ve (profil)
  tco = (price - (bonus_eco+ aides_region)) + cg_cost + (recharge*5) + (stationnement*5) + (entretien) + (tvs*5)
  return tco


# Associer une categorie de VT à un modele de ve (A / B / C)
# Modele_a
def select_model_a(categorie):
  modele_a = df_vt['modele_ve_a'][list(df_vt['categorie_vt']).index(categorie)]
  return modele_a
# modele_b
def select_model_b(categorie):
  modele_b = df_vt['modele_ve_b'][list(df_vt['categorie_vt']).index(categorie)]
  return modele_b
# modele_c
def select_model_c(categorie):
  modele_c = df_vt['modele_ve_c'][list(df_vt['categorie_vt']).index(categorie)]
  return modele_c

