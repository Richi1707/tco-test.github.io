from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
import numpy as np
from datetime import date

# importer les fonctions

from functions import *

app = Flask(__name__)
api = Api(app)

import pandas as pd
import numpy as np
# API
class ApiTcoClass(Resource):
    def get(self,categorie,region_name,statut,profil):
        price_vt = str(cost_vt (categorie))
        aides_vt = str(0)
        cg_cost = cartegrise_cost_vt(statut,region_name, categorie)
        carburant = carburant_cost_vt(categorie,profil)
        stationnement = str(prix_stationnement_vt(region_name))
        entretien = str(entretien_cost_vt(profil))
        tvs = calcul_tvs_vt(statut, categorie)
        tco = calcul_tco_vt(categorie, region_name, statut,profil)
        modele_a = str(select_model_a(categorie))
        modele_b = str(select_model_b(categorie)) 
        modele_c = str(select_model_c(categorie))
        return {
         'tco_vt' : { 
         'prix' : price_vt,
         'aides' : aides_vt,
         'carte_grise' :cg_cost,
         'carburant' : carburant,
         "stationnement": stationnement,
         "entretien_cost": entretien,
         "tvs_pro" :tvs,
         "TCO" :tco,
         "impact_co2" : str(impact_co2_vt(categorie,profil)[0]),
         "paris_ny" : str(impact_co2_vt(categorie,profil)[1]),

         "tco_ve_modele_a" : { 
             'modele_a' : str(select_model_a(categorie)),
             'prix' : str(cost_ve(modele_a)),
             'bonus_eco' : str(calcul_aides(region_name,statut)[0]),
             'aides_region' : str(calcul_aides(region_name,statut)[1]),
             'carte_grise': str(cartegrise_cost_ve(statut,region_name)),
             'recharge' : str(recharge_cost(modele_a,profil)),
             'tvs_pro': str(0),
             'stationnement' : str(prix_stationnement_ve(region_name)[0]),
             'villes_gratuites': str(prix_stationnement_ve(region_name)[1]),
             'villes_preferentielles' : str(prix_stationnement_ve(region_name)[2]),
             'entretien': str(entretien_cost_ve (profil)),
             'tco_modele_a': str((cost_ve(modele_a) - (calcul_aides(region_name,statut)[0]+ calcul_aides(region_name,statut)[1]))
             + cartegrise_cost_ve(statut,region_name) 
             + (recharge_cost(modele_a,profil)*5) 
             + (prix_stationnement_ve(region_name)[0]*5) 
             + (entretien_cost_ve (profil)) + (0*5)),
             'comparaison_tco_vt_ve': str(round(tco - ((cost_ve(modele_a) - (calcul_aides(region_name,statut)[0]+ calcul_aides(region_name,statut)[1])) 
             + cartegrise_cost_ve(statut,region_name) 
             + (recharge_cost(modele_a,profil)*5)
             + (prix_stationnement_ve(region_name)[0]*5) 
             + (entretien_cost_ve (profil)) + (0*5)),2)),
             'economies_en_pourcentage': str(round((((cost_ve(modele_a) - (calcul_aides(region_name,statut)[0]+ calcul_aides(region_name,statut)[1]) 
             + cartegrise_cost_ve(statut,region_name) 
             + (recharge_cost(modele_a,profil)*5) 
             + (prix_stationnement_ve(region_name)[0]*5) 
             + (entretien_cost_ve (profil)) 
             + (0*5)) - tco)/tco)*100,2)),
             'impact_co2': str(0),
       },
         "tco_ve_modele_b" : { 
             'modele_b' : str(select_model_b(categorie)),
             'prix' : str(cost_ve(modele_b)),
             'bonus_eco' : str(calcul_aides(region_name,statut)[0]),
             'aides_region' : str(calcul_aides(region_name,statut)[1]),
             'carte_grise': str(cartegrise_cost_ve(statut,region_name)),
             'recharge' : str(recharge_cost(modele_b,profil)),
             'tvs_pro': str(0),
             'stationnement' : str(prix_stationnement_ve(region_name)[0]),
             'villes_gratuites': str(prix_stationnement_ve(region_name)[1]),
             'villes_preferentielles' : str(prix_stationnement_ve(region_name)[2]),
             'entretien': str(entretien_cost_ve (profil)),
             'tco_modele_b': str((cost_ve(modele_b) - (calcul_aides(region_name,statut)[0]+ calcul_aides(region_name,statut)[1]))
             + cartegrise_cost_ve(statut,region_name) 
             + (recharge_cost(modele_b,profil)*5) 
             + (prix_stationnement_ve(region_name)[0]*5) 
             + (entretien_cost_ve (profil)) + (0*5)),
             'comparaison_tco_vt_ve': str(round(tco - ((cost_ve(modele_b) - (calcul_aides(region_name,statut)[0]+ calcul_aides(region_name,statut)[1])) 
             + cartegrise_cost_ve(statut,region_name) 
             + (recharge_cost(modele_b,profil)*5)
             + (prix_stationnement_ve(region_name)[0]*5) 
             + (entretien_cost_ve (profil)) + (0*5)),2)),
             'economies_en_pourcentage': str(round((((cost_ve(modele_b) - (calcul_aides(region_name,statut)[0]+ calcul_aides(region_name,statut)[1]) 
             + cartegrise_cost_ve(statut,region_name) 
             + (recharge_cost(modele_b,profil)*5) 
             + (prix_stationnement_ve(region_name)[0]*5) 
             + (entretien_cost_ve (profil)) 
             + (0*5)) - tco)/tco)*100,2)),
             'impact_co2': str(0),
         },
         
         "tco_ve_modele_c" : { 
              'modele_c' : str(select_model_c(categorie)),
              'prix' : str(cost_ve(modele_c)),
              'bonus_eco' : str(calcul_aides(region_name,statut)[0]),
              'aides_region' : str(calcul_aides(region_name,statut)[1]),
              'carte_grise': str(cartegrise_cost_ve(statut,region_name)),
              'recharge' : str(recharge_cost(modele_c,profil)),
              'tvs_pro': str(0),
              'stationnement' : str(prix_stationnement_ve(region_name)[0]),
              'villes_gratuites': str(prix_stationnement_ve(region_name)[1]),
              'villes_preferentielles' : str(prix_stationnement_ve(region_name)[2]),
              'entretien': str(entretien_cost_ve (profil)),
              'tco_modele_c': str((cost_ve(modele_c) - (calcul_aides(region_name,statut)[0]+ calcul_aides(region_name,statut)[1]))
              + cartegrise_cost_ve(statut,region_name) 
              + (recharge_cost(modele_c,profil)*5) 
              + (prix_stationnement_ve(region_name)[0]*5) 
              + (entretien_cost_ve (profil)) + (0*5)),
              'comparaison_tco_vt_ve': str(round(tco - ((cost_ve(modele_c) - (calcul_aides(region_name,statut)[0]+ calcul_aides(region_name,statut)[1])) 
              + cartegrise_cost_ve(statut,region_name) 
              + (recharge_cost(modele_c,profil)*5)
              + (prix_stationnement_ve(region_name)[0]*5) 
              + (entretien_cost_ve (profil)) + (0*5)),2)),
              'economies_en_pourcentage': str(round((((cost_ve(modele_c) - (calcul_aides(region_name,statut)[0]+ calcul_aides(region_name,statut)[1]) 
              + cartegrise_cost_ve(statut,region_name) 
              + (recharge_cost(modele_c,profil)*5) 
              + (prix_stationnement_ve(region_name)[0]*5) 
              + (entretien_cost_ve (profil)) 
              + (0*5)) - tco)/tco)*100,2)),
              'impact_co2': str(0),
         },
         }
         }

api.add_resource(ApiTcoClass, '/<string:categorie>/<string:region_name>/<string:statut>/<int:profil>')

if __name__ == '__main__':
    app.run(debug=True)