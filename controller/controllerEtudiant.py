import os
from models.database import get_connection
import re

# Fonction pour afficher la page etudiant.html
def render_etudiant_html(scope=None, receive=None, send=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_Eleve, nomE, prenomE, dateN, classe, adresse, telParent FROM eleves")
        rows = cursor.fetchall()
        conn.close()
        
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        html_path = os.path.join(project_root, 'views', 'etudiant', 'etudiant.html')
        with open(html_path, encoding='utf-8') as f:
            html = f.read()
        
        # Générer les lignes du tableau
        table_rows = "\n".join([
            f"""
            <tr>
                <td class="table-cell">{r[0]}</td> <!-- id_Eleve -->
                <td class="table-cell">{r[1]}</td> <!-- nomE -->
                <td class="table-cell">{r[2]}</td> <!-- prenomE -->
                <td class="table-cell">{r[3]}</td> <!-- dateN -->
                <td class="table-cell">{r[4]}</td> <!-- classe -->
                <td class="table-cell">{r[5]}</td> <!-- adresse -->
                <td class="table-cell">{r[6]}</td> <!-- telParent -->
                <td class=\"table-cell\"><a class=\"delete-button\" href=\"/views/etudiant/delete?id_eleve={r[0]}\">Supprimer</a></td>
            </tr>
            """ for r in rows
        ])
        
        # Remplacer le contenu du tbody avec les vraies lignes
        html = re.sub(r'(<tbody id="studentTable" class="table-body">)[\s\S]*?(</tbody>)', f'\\1{table_rows}\\2', html, flags=re.DOTALL)
        
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
            'headers': [(b'content-type', b'text/html; charset=utf-8')],
            'body': error_html.encode('utf-8')
        }