import requests

FILE_OUTPUT = "test.csv"

def download_file():
    """
    ## download_file()
    
    Downloads a CSV file from an OpenData API and saves it locally.

    The function sends a GET request to the specified API URL with the appropriate query parameters.
    If the request is successful, it writes the content of the downloaded file to a local file named FILE_OUTPUT.

    Parameters:
    None

    Returns:
    None

    Exceptions:
    The function handles the following exceptions:
        - requests.exceptions.HTTPError: HTTP error returned by the request.
        - requests.exceptions.ConnectionError: Connection error.
        - requests.exceptions.Timeout: Request timeout.
        - requests.exceptions.RequestException: Generic request error.
        - Exception: Any other unexpected error.
    """
    # API URL
    url = "https://opendata.caissedesdepots.fr/api/explore/v2.1/catalog/datasets/moncompteformation_catalogueformation/exports/csv"
    
    # Query parameters
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
        
        print("The file has been downloaded")
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error: {req_err}")
    except Exception as err:
        print(f"Unexpected error: {err}")

if __name__ == "__main__":
    """
    Main entry point of the script. Calls the download_file function to download
    and save the CSV file.
    """
    download_file()
