from models.database import get_connection

def insert_transport(ref_trans, date_trans, id_eleve, id_vehicule):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM eleves WHERE id_Eleve = %s", (id_eleve,))
        if cursor.fetchone()[0] == 0:
            raise ValueError(f"L'ID Élève {id_eleve} n'existe pas.")

        
        cursor.execute("SELECT COUNT(*) FROM vehicules WHERE idVehicule = %s", (id_vehicule,))
        if cursor.fetchone()[0] == 0:
            raise ValueError(f"L'ID Véhicule {id_vehicule} n'existe pas.")
        
        query = """
            INSERT INTO trans (refTrans, dateTrans, idEleve, idVehicule)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (ref_trans, date_trans, id_eleve, id_vehicule))
        conn.commit()
    except Exception as e:

        print(f"Erreur lors de l'insertion : {str(e)}")
        conn.rollback()  # Annuler la transaction en cas d'erreur
    finally:
        cursor.close()
        conn.close()

def delete_transport(ref_trans):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM trans WHERE refTrans = %s", (ref_trans,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def update_transport(ref_trans, date_trans, id_eleve, id_vehicule):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE trans
            SET dateTrans = %s, idEleve = %s, idVehicule = %s
            WHERE refTrans = %s
            """,
            (date_trans, id_eleve, id_vehicule, ref_trans)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()