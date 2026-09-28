import os
import re
from models.database import get_connection

# Fonction pour afficher la page des transports (table trans)
def render_transports_html(scope=None, receive=None, send=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Requête SQL pour récupérer les données de la table trans avec jointures
        cursor.execute("""
            SELECT 
                t.refTrans, 
                t.dateTrans, 
                e.nomE, 
                v.matricule 
            FROM 
                trans t
            JOIN 
                eleves e ON t.idEleve = e.id_eleve
            JOIN 
                vehicules v ON t.idVehicule = v.idVehicule
        """)
        rows = cursor.fetchall()
        cursor.close()  # Fermez le curseur
        conn.close()    # Fermez la connexion
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        html_path = os.path.join(project_root, 'views', 'transports', 'transport.html')  # Chemin vers le bon fichier
        with open(html_path, encoding='utf-8') as f:
            html = f.read()

        # Trouver le modèle de ligne à remplir
        match = re.search(r'<tbody id="transportTable">\s*(<tr[\s\S]*?</tr>)\s*</tbody>', html)
        if not match:
            row_template = "<tr><td>{{ refTrans }}</td><td>{{ dateTrans }}</td><td>{{ nomE }}</td><td>{{ matriculeVehicule }}</td><td><a href=\"/views/transports/delete?refTrans={{ refTrans }}\">Supprimer</a></td></tr>"
        else:
            row_template = match.group(1)

        # Générer les lignes du tableau
        table_rows = "\n".join([
            row_template.replace("{{ refTrans }}", str(r[0]))
                        .replace("{{ dateTrans }}", str(r[1]))
                        .replace("{{ nomE }}", str(r[2]))
                        .replace("{{ matricule }}", str(r[3]))
                        .replace("{{ matriculeVehicule }}", str(r[3]))
            for r in rows
        ])

        # Remplacer les lignes du tableau dans le HTML
        html = re.sub(r'<tbody id="transportTable">[\s\S]*?</tbody>', f'<tbody id="transportTable">{table_rows}</tbody>', html, flags=re.DOTALL)
        
        return {
            'status': 200,
            'headers': [(b'content-type', b'text/html; charset=utf-8')],
            'body': html.encode('utf-8')
        }
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        error_html = f"<h1>Erreur serveur</h1><pre>{tb}</pre>"
        return {
            'status': 500,
            'headers': [(b'content-type', b'text/html')],
            'body': error_html.encode('utf-8')
        }