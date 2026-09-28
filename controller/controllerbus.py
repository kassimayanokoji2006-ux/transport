import os
import re
from models.database import get_connection

# Fonction pour afficher la page bus.html
def render_bus_html(scope=None, receive=None, send=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT idVehicule, matricule, marque, capacite FROM vehicules")
        rows = cursor.fetchall()
        cursor.close()  # Fermez le curseur
        conn.close()    # Fermez la connexion
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        html_path = os.path.join(project_root, 'views', 'bus', 'bus.html')
        with open(html_path, encoding='utf-8') as f:
            html = f.read()
    
        # Trouver le modèle de ligne à remplir
        match = re.search(r'<tbody id="vehicleTable">\s*(<tr[\s\S]*?</tr>)\s*</tbody>', html)
        if not match:
            row_template = ""
        else:
            row_template = match.group(1)
       
        # Générer les lignes du tableau
        table_rows = "\n".join([
            row_template.replace("{{ idVehicule }}", str(r[0]))
                        .replace("{{ matricule }}", str(r[1]))
                        .replace("{{ marque }}", str(r[2]))
                        .replace("{{ capacite }}", str(r[3]))
            for r in rows
        ])
  
        # Remplacer les lignes du tableau dans le HTML
        html = re.sub(r'<tbody id="vehicleTable">[\s\S]*?</tbody>', f'<tbody id="vehicleTable">{table_rows}</tbody>', html, flags=re.DOTALL)
        
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