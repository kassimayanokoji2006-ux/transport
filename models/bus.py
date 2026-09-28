from models.database import get_connection # Ou le module de votre choix pour se connecter à la base de données

def insert_vehicule(idVehicule,matricule, marque, capacite):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        query = """
            INSERT INTO vehicules (idVehicule, matricule, marque, capacite)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (idVehicule, matricule, marque, capacite))    
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def delete_vehicule(idVehicule):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM vehicules WHERE idVehicule = %s", (idVehicule,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def update_vehicule(idVehicule, matricule, marque, capacite):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            UPDATE vehicules
            SET matricule = %s, marque = %s, capacite = %s
            WHERE idVehicule = %s
            """,
            (matricule, marque, capacite, idVehicule)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()