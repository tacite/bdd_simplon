import requests

FILE_OUTPUT = "data/test.csv"

def download_file():
    # url de l'api
    url = "https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/csv"
    
    # parametres de la requete 
    params = {
        'where': "libelle_nsf_1 like 'Informatique' and nom_region is not null and code_certifinfo != -1",
        'select': "nom_of,nom_region,type_referentiel,code_inventaire,code_rncp,intitule_certification,code_certifinfo,libelle_niveau_sortie_formation,code_formacode_1,code_formacode_2,code_formacode_3,code_formacode_4,code_formacode_5,libelle_code_formacode_principal,libelle_nsf_1,libelle_nsf_2,libelle_nsf_3,code_nsf_1,code_nsf_2,code_nsf_3,intitule_formation,nombre_heures_total_mean,frais_ttc_tot_mean,code_region"
        }
    
    try:
        response = requests.get(url, params=params, stream=True)
        response.raise_for_status()
        
        with open(FILE_OUTPUT, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
            file.close()
        print("le fichier a été telechargé")
    
    except requests.exceptions.HTTPError as http_err:
        print(f"http error: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"connection error: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"timeout error: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f'une erreur: {req_err}')
    except Exception as err:
        print(f"erreur innatendu {err}")
    
if __name__ == "__main__":
    download_file()