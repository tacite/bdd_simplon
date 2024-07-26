import requests

# Nom du fichier de sortie
FILE_OUTPUT = "test.csv"

def download_file():
    """
    ## download_file()
    
    Downloads a CSV file from a public API and saves it locally.

    The function makes an HTTP GET request to the API to obtain data in CSV format.
    The data is filtered according to the parameters provided in the request URL.
    The CSV file is then saved locally with the name specified in `FILE_OUTPUT`.
    """
    
    # URL de l'API pour télécharger les données
    url = "https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/csv"
    
    # Paramètres de la requête pour filtrer les données
    params = {
        'where': "libelle_nsf_1 like 'Informatique' and nom_region is not null and code_certifinfo != -1",
        'select': "nom_of,nom_region,type_referentiel,code_inventaire,code_rncp,intitule_certification,code_certifinfo,libelle_niveau_sortie_formation,code_formacode_1,code_formacode_2,code_formacode_3,code_formacode_4,code_formacode_5,libelle_code_formacode_principal,libelle_nsf_1,libelle_nsf_2,libelle_nsf_3,code_nsf_1,code_nsf_2,code_nsf_3,intitule_formation,nombre_heures_total_mean,frais_ttc_tot_mean,code_region"
    }
    
    try:
        # Effectuer la requête GET avec les paramètres spécifiés
        response = requests.get(url, params=params, stream=True)
        
        # Vérifier si la requête a réussi
        response.raise_for_status()
        
        # Ouvrir le fichier en mode binaire pour écrire les données
        with open(FILE_OUTPUT, 'wb') as file:
            # Écrire les données par morceaux (chunks) pour éviter d'utiliser trop de mémoire
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print("Le fichier a été téléchargé avec succès.")
    
    except requests.exceptions.HTTPError as http_err:
        # Gestion des erreurs HTTP
        print(f"Erreur HTTP: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        # Gestion des erreurs de connexion
        print(f"Erreur de connexion: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        # Gestion des erreurs de timeout
        print(f"Erreur de timeout: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        # Gestion des erreurs génériques de requête
        print(f"Erreur de requête: {req_err}")
    except Exception as err:
        # Gestion des erreurs inattendues
        print(f"Erreur inattendue: {err}")

# Exécuter la fonction de téléchargement si le script est exécuté directement
if __name__ == "__main__":
    download_file()
