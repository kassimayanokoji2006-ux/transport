from models.database import get_connection

def insert_eleve(id_eleve, nom, prenom, date_naissance, classe, adresse, tel_parent):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO eleves (id_Eleve, nomE, prenomE, dateN, classe, adresse, telParent)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (id_eleve, nom, prenom, date_naissance, classe, adresse, tel_parent))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def delete_eleve(id_eleve):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM eleves WHERE id_Eleve = %s", (id_eleve,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def update_eleve(id_eleve, nom, prenom, date_naissance, classe, adresse, tel_parent):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE eleves
            SET nomE = %s, prenomE = %s, dateN = %s, classe = %s, adresse = %s, telParent = %s
            WHERE id_Eleve = %s
            """,
            (nom, prenom, date_naissance, classe, adresse, tel_parent, id_eleve)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()