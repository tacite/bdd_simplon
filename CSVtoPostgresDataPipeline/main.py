import pandas as pd

CSV_NAME = "catalogueformation.csv"
CSV_CLEANED = "data.csv"

def main():
    # ouverture et verification de l'existance du fichier csv
    try:
        df = pd.read_csv(CSV_NAME, sep=';', low_memory=False)
    except FileNotFoundError:
        print("File not Found.")
        exit()

    # suppression des lignes qui ont des valeurs nulles aux colonnes 'libelle_nsf_1' et 'nom_region'
    df.dropna(subset=['libelle_nsf_1', 'nom_region'], inplace=True)
    
    # filtrage : on garde les lignes qui contiennent 'Informatique' dans la colonne 'libelle_nsf_1'
    df = df[df['libelle_nsf_1'].str.contains('Informatique')]
    
    # suppression de BEAUCOUP de colonnes
    df.drop(columns=['date_extract', 'nom_departement', 'nb_action', 'nb_session_active', 'nb_session_a_distance',
                'nombre_heures_total_mean', 'frais_ttc_tot_mean', 'code_departement', 'nbaction_nbheures',
                'coderegion_export', 'points_forts', 'siret', 'numero_formation', 'code_rome_1',
                'code_rome_2', 'code_rome_3', 'code_rome_4', 'code_rome_5'], inplace=True)
    
    # export du dataframe nettoyé 
    df.to_csv(CSV_CLEANED, index=False)
    
if __name__ == "__main__":
    main()