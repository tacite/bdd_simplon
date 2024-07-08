```mermaid
erDiagram
    FORMATIONS {
        int id PK
        string title
        string region
        float min_price
        float maxprice
        int nb_days
        date beginning
        date ending
        string town
        boolean handicap
        string graduation
    }
    FORMACODES {
        int code PK
        string label
    }
    RS {
        int code PK
        string label
    }
    RNCP {
        int code PK
        string label
    }
    NSF {
        string code PK
        string label
    }
    CERTIFICATIONS {
        string code PK
        string label
    }

    FORMATIONS_RS {
        int formation_id FK "FK to FORMATIONS"
        int rs_code FK "FK to RS"
    }
    FORMATIONS_RNCP {
        int formation_id FK "FK to FORMATIONS"
        int rncp_code FK "FK to RNCP"
    }
    FORMATIONS_NFS {
        int formation_id FK "FK to FORMATIONS"
        string nfs_code FK "FK to NFS"
    }
    FORMATIONS_CERTIFICATIONS {
        int formation_id FK "FK to FORMATIONS"
        int certification_code FK "FK to CERTIFICATIONS"
    }
    FORMACODE_RS {
        int formacode_code FK "FK to FORMACODES"
        int rs_code FK "FK to RS"
    }
    FORMACODE_RNCP {
        int formation_id FK "FK to FORMATIONS"
        int rncp_code FK "FK to RNCP"
    }


    MEDIAS ||--o{ MEDIAS_GENDERS : "has"
    GENDERS ||--o{ MEDIAS_GENDERS : "has"
    MEDIAS ||--o{ MEDIAS_PERSONS : "has"
    PERSONS ||--o{ MEDIAS_PERSONS : "has"