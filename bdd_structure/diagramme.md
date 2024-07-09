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
    FORMATIONS_NSF {
        int formation_id FK "FK to FORMATIONS"
        string nsf_code FK "FK to NSF"
    }
    FORMATIONS_CERTIFICATIONS {
        int formation_id FK "FK to FORMATIONS"
        string certification_code FK "FK to CERTIFICATIONS"
    }
    FORMACODE_RS {
        int formacode_code FK "FK to FORMACODES"
        int rs_code FK "FK to RS"
    }
    FORMACODE_RNCP {
        int formation_id FK "FK to FORMATIONS"
        int rncp_code FK "FK to RNCP"
    }


    FORMATIONS ||--o{ FORMATIONS_RS : "has"
    RS ||--o{ FORMATIONS_RS : "has"
    FORMATIONS ||--o{ FORMATIONS_RNCP : "has"
    RNCP ||--o{ FORMATIONS_RNCP : "has"
    FORMATIONS ||--o{ FORMATIONS_NSF : "has"
    NSF ||--o{ FORMATIONS_NSF : "has"
    FORMATIONS ||--o{ FORMATIONS_CERTIFICATIONS : "has"
    CERTIFICATIONS ||--o{ FORMATIONS_CERTIFICATIONS : "has"
    FORMACODE ||--o{ FORMACODE_RS : "has"
    RS ||--o{ FORMACODE_RS : "has"
    FORMACODE ||--o{ FORMACODE_RNCP : "has"
    RNCP ||--o{ FORMACODE_RNCP : "has"