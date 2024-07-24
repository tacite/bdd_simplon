from sqlalchemy.orm import Session
from sqlalchemy import text

def get_formation_by_source_info(db: Session, source_info: str):
    try:
        result = db.execute(text("""
    SELECT f.titre, 
           fc.designation AS formacode_designation, 
           n.designation AS nsf_designation, 
           r_rs.designation AS rs_designation,
           r_rncp.designation AS rncp_designation,
           f.date_debut, f.duree_jours, f.duree_heures, 
           f.region, f.code_region, f.ville, f.niveau_sortie, 
           f.prix, f.source_info
    FROM formation f
    LEFT JOIN referentiel r_rs ON f.referentiel = r_rs.formation AND r_rs.type = 'rs'
    LEFT JOIN referentiel r_rncp ON f.referentiel = r_rncp.formation AND r_rncp.type = 'rncp'
    JOIN formacode fc ON  f.formacode_id = fc.id
    JOIN certification c ON  f.certification = c.formation
    JOIN nsf n ON f.nsf = n.id
    WHERE f.source_info = :source_info
"""), {'source_info': source_info})

    # Convertir les résultats en dictionnaires
        formations = [dict(row) for row in result.mappings().all()]

        return formations

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_formation_by_region(db: Session, region: str):
    try:
        result = db.execute(text("""
    SELECT f.titre, 
           fc.designation AS formacode_designation, 
           n.designation AS nsf_designation, 
           r_rs.designation AS rs_designation,
           r_rncp.designation AS rncp_designation,
           f.date_debut, f.duree_jours, f.duree_heures, 
           f.region, f.code_region, f.ville, f.niveau_sortie, 
           f.prix, f.source_info
    FROM formation f
    LEFT JOIN referentiel r_rs ON f.referentiel = r_rs.formation AND r_rs.type = 'rs'
    LEFT JOIN referentiel r_rncp ON f.referentiel = r_rncp.formation AND r_rncp.type = 'rncp'
    JOIN formacode fc ON  f.formacode_id = fc.id
    JOIN certification c ON  f.certification = c.formation
    JOIN nsf n ON f.nsf = n.id
    WHERE f.region = :region
"""), {'region': region})

    # Convertir les résultats en dictionnaires
        formations = [dict(row) for row in result.mappings().all()]

        return formations

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_formation_by_formacode(db: Session, code: str):
    try:
        result = db.execute(text("""
    SELECT f.titre, 
           fc.designation AS formacode_designation, 
           n.designation AS nsf_designation, 
           r_rs.designation AS rs_designation,
           r_rncp.designation AS rncp_designation,
           f.date_debut, f.duree_jours, f.duree_heures, 
           f.region, f.code_region, f.ville, f.niveau_sortie, 
           f.prix, f.source_info
    FROM formation f
    LEFT JOIN referentiel r_rs ON f.referentiel = r_rs.formation AND r_rs.type = 'rs'
    LEFT JOIN referentiel r_rncp ON f.referentiel = r_rncp.formation AND r_rncp.type = 'rncp'
    JOIN formacode fc ON  f.formacode_id = fc.id
    JOIN certification c ON  f.certification = c.formation
    JOIN nsf n ON f.nsf = n.id
    WHERE fc.code = :code
"""), {'code': code})

# Convertir les résultats en dictionnaires
        formations = [dict(row) for row in result.mappings().all()]

        return formations

    except Exception as e:
        print(f"An error occurred: {e}")
        return None