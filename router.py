

import os
from controller.controllerEtudiant import render_etudiant_html
from controller.controllertrans import render_transports_html
from controller.controllerbus import render_bus_html
from models.database import get_connection
from models.etudiant import insert_eleve
from models.bus import insert_vehicule
from models.etudiant import delete_eleve
from models.bus import delete_vehicule
from models.transport import delete_transport
from models.etudiant import update_eleve
from models.bus import update_vehicule
from models.transport import update_transport


from models.transport import insert_transport  
import urllib.parse
import json

def serve_html_file(filename):
    def handler(scope, receive, send):
        file_path = os.path.join(os.path.dirname(__file__), filename)
        if not os.path.isfile(file_path):
            return {
                'status': 404,
                'headers': [(b'content-type', b'text/html; charset=utf-8')],
                'body': b'<h1>Page non trouv\xc3\xa9e</h1>'
            }
        with open(file_path, 'rb') as f:
            body = f.read()
        return {
            'status': 200,
            'headers': [(b'content-type', b'text/html; charset=utf-8')],
            'body': body
        }
    return handler
def static_handler_factory(static_dir):
    def static_handler(scope, receive, send):
        rel_path = scope['path'].lstrip('/')
        file_path = os.path.join(os.path.dirname(__file__), rel_path)
        if not os.path.abspath(file_path).startswith(os.path.abspath(static_dir)):
            return {
                'status': 403,
                'headers': [(b'content-type', b'text/plain')],
                'body': b'Forbidden'
            }
        if not os.path.isfile(file_path):
            return {
                'status': 404,
                'headers': [(b'content-type', b'text/plain')],
                'body': b'Not found'
            }
        # Détecter le type MIME
        if file_path.endswith('.css'):
            content_type = b'text/css'
        elif file_path.endswith('.js'):
            content_type = b'application/javascript'
        else:
            content_type = b'application/octet-stream'
        with open(file_path, 'rb') as f:
            body = f.read()
        return {
            'status': 200,
            'headers': [(b'content-type', content_type)],
            'body': body
        }
    return static_handler


def index_handler(scope, receive, send):
    # Charger le fichier et injecter les données dashboard
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Comptes
        cur.execute("SELECT COUNT(*) FROM eleves")
        count_eleves = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM vehicules")
        count_bus = cur.fetchone()[0]
        # 5 derniers transports
        cur.execute(
            """
            SELECT t.refTrans, t.dateTrans, v.matricule, e.nomE
            FROM trans t
            JOIN eleves e ON t.idEleve = e.id_eleve
            JOIN vehicules v ON t.idVehicule = v.idVehicule
            ORDER BY t.dateTrans DESC, t.refTrans DESC
            LIMIT 5
            """
        )
        latest = cur.fetchall()
        cur.close(); conn.close()
    except Exception as db_exc:
        count_eleves = 0
        count_bus = 0
        latest = []

    file_path = os.path.join(os.path.dirname(__file__), 'index.html')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html = f.read()
        # Injecter les compteurs
        html = html.replace('id="nbEtudiants">0', f'id="nbEtudiants">{count_eleves}')
        html = html.replace('id="nbBus">0', f'id="nbBus">{count_bus}')
        # Injecter les 5 dernières lignes
        rows_html = "\n".join([
            f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>" for r in latest
        ])
        html = html.replace('<tbody id="dashboardTransportTable"></tbody>', f'<tbody id="dashboardTransportTable">{rows_html}</tbody>')
        return {
            'status': 200,
            'headers': [(b'content-type', b'text/html; charset=utf-8')],
            'body': html.encode('utf-8')
        }
    except Exception as e:
        return {
            'status': 500,
            'headers': [(b'content-type', b'text/plain')],
            'body': str(e).encode()
        }


def api_stats_handler(scope, receive, send):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM eleves")
        nb_etudiants = int(cursor.fetchone()[0])
        cursor.execute("SELECT COUNT(*) FROM vehicules")
        nb_bus = int(cursor.fetchone()[0])
        cursor.execute("SELECT COUNT(*) FROM trans")
        nb_transports = int(cursor.fetchone()[0])
        cursor.execute("SELECT COUNT(*) FROM trans WHERE DATE(dateTrans) = CURDATE()")
        nb_transports_today = int(cursor.fetchone()[0])
        cursor.close(); conn.close()
        body = json.dumps({
            "nbEtudiants": nb_etudiants,
            "nbBus": nb_bus,
            "nbTransports": nb_transports,
            "nbTransportsToday": nb_transports_today,
        }).encode('utf-8')
        return { 'status': 200, 'headers': [(b'content-type', b'application/json')], 'body': body }
    except Exception as e:
        return { 'status': 500, 'headers': [(b'content-type', b'application/json')], 'body': json.dumps({"error": str(e)}).encode('utf-8') }

def api_latest_transports_handler(scope, receive, send):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT t.refTrans, t.dateTrans, v.matricule, e.nomE
            FROM trans t
            JOIN eleves e ON t.idEleve = e.id_Eleve
            JOIN vehicules v ON t.idVehicule = v.idVehicule
            ORDER BY t.dateTrans DESC
            LIMIT 50
            """
        )
        rows = cursor.fetchall()
        cursor.close(); conn.close()
        latest = [
            {"refTrans": str(r[0]), "dateTrans": str(r[1]), "matricule": str(r[2]), "nomE": str(r[3])}
            for r in rows
        ]
        return { 'status': 200, 'headers': [(b'content-type', b'application/json')], 'body': json.dumps(latest).encode('utf-8') }
    except Exception as e:
        return { 'status': 500, 'headers': [(b'content-type', b'application/json')], 'body': json.dumps({"error": str(e)}).encode('utf-8') }

async def insert_etudiant_handler(scope, receive, send):
  
    if scope["method"] == "POST":
        
        body = b""
        while True:
            message = await receive()
            
            if message["type"] == "http.request":
                body += message.get("body", b"")
                if not message.get("more_body"):
                    break

        data = body.decode("utf-8")
        params = dict(param.split("=") for param in data.split("&"))

        try:
            insert_eleve(
                id_eleve=params.get("id_eleve"),
                nom=params.get("nom"),
                prenom=params.get("prenom"),
                date_naissance=params.get("date_naissance"),
                classe=params.get("classe"),
                adresse=params.get("adresse"),
                tel_parent=params.get("tel_parent"),
            )
            # Redirection vers la page etudiant.html après succès
            await send({
                "type": "http.response.start",
                "status": 303,  # Code de redirection
                "headers": [(b"location", b"/views/etudiant/etudiant.html")],
            })
            await send({
                "type": "http.response.body",
                "body": b"",
            })
        except Exception as e:
            # En cas d'erreur, afficher un message d'erreur
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [(b"content-type", b"text/plain")],
            })
            await send({
                "type": "http.response.body",
                "body": f"Erreur lors de l'insertion : {e}".encode("utf-8"),
            })
    else:
        # Méthode non autorisée
        await send({
            "type": "http.response.start",
            "status": 405,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({
            "type": "http.response.body",
            "body": b"Method Not Allowed",
        })

async def insert_vehicule_handler(scope, receive, send):
    if scope["method"] == "POST":
        body = b""
        while True:
            message = await receive()
            if message["type"] == "http.request":
                body += message.get("body", b"")
                if not message.get("more_body"):
                    break

        data = body.decode("utf-8")
        params = dict(param.split("=") for param in data.split("&"))

        try:
            insert_vehicule(  
                idVehicule=params.get("idVehicule"),
                matricule=params.get("matricule"),
                marque=params.get("marque"),
                capacite=params.get("capacite")
            )
            await send({
                "type": "http.response.start",
                "status": 303,  # Code de redirection
                "headers": [(b"location", b"/views/bus/bus.html")],
            })
            await send({
                "type": "http.response.body",
                "body": b"",
            })
        except Exception as e:
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [(b"content-type", b"text/plain")],
            })
            await send({
                "type": "http.response.body",
                "body": f"Erreur lors de l'insertion : {e}".encode("utf-8"),
            })
    else:
        await send({
            "type": "http.response.start",
            "status": 405,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({
            "type": "http.response.body",
            "body": b"Method Not Allowed",
        })
        
        


async def insert_transport_handler(scope, receive, send):
    if scope["method"] == "POST":
        # Récupération des données envoyées par le formulaire
        body = b""
        while True:
            message = await receive()
            
            if message["type"] == "http.request":
                body += message.get("body", b"")
                if not message.get("more_body"):
                    break

        data = body.decode("utf-8")
        params = dict(param.split("=") for param in data.split("&"))

        ref_trans = params.get("refTrans")
        date_trans = params.get("dateTrans")
        id_eleve = params.get("idEleve")
        id_vehicule = params.get("idVehicule")

        try:
            # Appel de la fonction d'insertion
            insert_transport(
                ref_trans=ref_trans,
                date_trans=date_trans,
                id_eleve=int(id_eleve),  
                id_vehicule=int(id_vehicule),
            )
            await send({
                "type": "http.response.start",
                "status": 303, 
                "headers": [(b"location", b"/views/transports/transport.html")],
            })
            await send({
                "type": "http.response.body",
                "body": b"",
            })
        except Exception as e:
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [(b"content-type", b"text/plain")],
            })
            await send({
                "type": "http.response.body",
                "body": f"Erreur lors de l'insertion : {e}".encode("utf-8"),
            })
    else:
        await send({
            "type": "http.response.start",
            "status": 405,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({
            "type": "http.response.body",
            "body": b"Method Not Allowed",
        })

# Delete handlers
async def delete_etudiant_handler(scope, receive, send):
    if scope["method"] == "GET":
        # Parse query string for id
        query_string = scope.get("query_string", b"").decode("utf-8")
        params = dict(urllib.parse.parse_qsl(query_string))
        id_eleve = params.get("id_eleve")
        ajax = params.get("ajax") == "1"
        if id_eleve is not None:
            try:
                delete_eleve(id_eleve)
            except Exception:
                pass
        if ajax:
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"application/json")],
            })
            await send({"type": "http.response.body", "body": b'{"success": true}'} )
        else:
            await send({
                "type": "http.response.start",
                "status": 303,
                "headers": [(b"location", b"/views/etudiant/etudiant.html")],
            })
            await send({"type": "http.response.body", "body": b""})


async def delete_vehicule_handler(scope, receive, send):
    if scope["method"] == "GET":
        query_string = scope.get("query_string", b"").decode("utf-8")
        params = dict(urllib.parse.parse_qsl(query_string))
        idVehicule = params.get("idVehicule")
        ajax = params.get("ajax") == "1"
        if idVehicule is not None:
            try:
                delete_vehicule(idVehicule)
            except Exception:
                pass
        if ajax:
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"application/json")],
            })
            await send({"type": "http.response.body", "body": b'{"success": true}'} )
        else:
            await send({
                "type": "http.response.start",
                "status": 303,
                "headers": [(b"location", b"/views/bus/bus.html")],
            })
            await send({"type": "http.response.body", "body": b""})
    else:
        await send({
            "type": "http.response.start",
            "status": 405,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({"type": "http.response.body", "body": b"Method Not Allowed"})


async def delete_transport_handler(scope, receive, send):
    if scope["method"] == "GET":
        query_string = scope.get("query_string", b"").decode("utf-8")
        params = dict(urllib.parse.parse_qsl(query_string))
        refTrans = params.get("refTrans")
        ajax = params.get("ajax") == "1"
        if refTrans is not None:
            try:
                delete_transport(refTrans)
            except Exception:
                pass
        if ajax:
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"application/json")],
            })
            await send({"type": "http.response.body", "body": b'{"success": true}'} )
        else:
            await send({
                "type": "http.response.start",
                "status": 303,
                "headers": [(b"location", b"/views/transports/transport.html")],
            })
            await send({"type": "http.response.body", "body": b""})

async def update_etudiant_handler(scope, receive, send):
    if scope["method"] == "POST":
        body = b""
        while True:
            message = await receive()
            if message["type"] == "http.request":
                body += message.get("body", b"")
                if not message.get("more_body"):
                    break
        data = body.decode("utf-8")
        params = dict(param.split("=") for param in data.split("&") if "=" in param)
        try:
            update_eleve(
                id_eleve=params.get("id_eleve"),
                nom=params.get("nom"),
                prenom=params.get("prenom"),
                date_naissance=params.get("date_naissance"),
                classe=params.get("classe"),
                adresse=params.get("adresse"),
                tel_parent=params.get("tel_parent"),
            )
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"application/json")],
            })
            await send({"type": "http.response.body", "body": b'{"success": true}'} )
        except Exception as e:
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [(b"content-type", b"application/json")],
            })
            await send({"type": "http.response.body", "body": ("{\"success\": false, \"error\": \"%s\"}" % str(e)).encode("utf-8")} )
    else:
        await send({
            "type": "http.response.start",
            "status": 405,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({"type": "http.response.body", "body": b"Method Not Allowed"})

async def update_vehicule_handler(scope, receive, send):
    if scope["method"] == "POST":
        body = b""
        while True:
            message = await receive()
            if message["type"] == "http.request":
                body += message.get("body", b"")
                if not message.get("more_body"):
                    break
        data = body.decode("utf-8")
        params = dict(param.split("=") for param in data.split("&") if "=" in param)
        try:
            update_vehicule(
                idVehicule=params.get("idVehicule"),
                matricule=params.get("matricule"),
                marque=params.get("marque"),
                capacite=params.get("capacite"),
            )
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"application/json")],
            })
            await send({"type": "http.response.body", "body": b'{"success": true}'} )
        except Exception as e:
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [(b"content-type", b"application/json")],
            })
            await send({"type": "http.response.body", "body": ("{\"success\": false, \"error\": \"%s\"}" % str(e)).encode("utf-8")} )
    else:
        await send({
            "type": "http.response.start",
            "status": 405,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({"type": "http.response.body", "body": b"Method Not Allowed"})

async def update_transport_handler(scope, receive, send):
    if scope["method"] == "POST":
        body = b""
        while True:
            message = await receive()
            if message["type"] == "http.request":
                body += message.get("body", b"")
                if not message.get("more_body"):
                    break
        data = body.decode("utf-8")
        params = dict(param.split("=") for param in data.split("&") if "=" in param)
        try:
            update_transport(
                ref_trans=params.get("refTrans"),
                date_trans=params.get("dateTrans"),
                id_eleve=params.get("idEleve"),
                id_vehicule=params.get("idVehicule"),
            )
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [(b"content-type", b"application/json")],
            })
            await send({"type": "http.response.body", "body": b'{"success": true}'} )
        except Exception as e:
            await send({
                "type": "http.response.start",
                "status": 500,
                "headers": [(b"content-type", b"application/json")],
            })
            await send({"type": "http.response.body", "body": ("{\"success\": false, \"error\": \"%s\"}" % str(e)).encode("utf-8")} )
    else:
        await send({
            "type": "http.response.start",
            "status": 405,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({"type": "http.response.body", "body": b"Method Not Allowed"})
routes = {
    '/': index_handler,
    '/index.html': index_handler,
    '/views/transports/transport.html': render_transports_html,  # Route pour afficher les transports
    '/views/etudiant/etudiant.html': render_etudiant_html,
    '/views/bus/bus.html': render_bus_html,
    '/views/transports/insert': insert_transport_handler,
    '/views/etudiant/delete': delete_etudiant_handler,
    '/views/bus/delete': delete_vehicule_handler,
    '/views/transports/delete': delete_transport_handler,
    '/views/etudiant/update': update_etudiant_handler,
    '/views/bus/update': update_vehicule_handler,
    '/views/transports/update': update_transport_handler,
    '/views/css/bus.css': static_handler_factory(os.path.join(os.path.dirname(__file__), 'views', 'css')),
    '/views/css/etudiant.css': static_handler_factory(os.path.join(os.path.dirname(__file__), 'views', 'css')),
    '/views/css/style.css': static_handler_factory(os.path.join(os.path.dirname(__file__), 'views', 'css')),
    '/views/js/script.js': static_handler_factory(os.path.join(os.path.dirname(__file__), 'views', 'js')),
    '/views/bus/insert': insert_vehicule_handler,
    '/views/etudiant/insert': insert_etudiant_handler,
    '/api/stats': api_stats_handler,
    '/api/transports/latest': api_latest_transports_handler,
}
class Route(object):
    def __init__(self, path, handler):
        self.path = path
        self.handler = handler
        
class Router(object):
    def __init__(self):
        self.routes = []
        
    def add(self, path, handler):
        self.routes.append(Route(path, handler))
    
    def resolve(self, path):
        for route in self.routes:
            if route.path == path:
                return route.handler
        return None
        
        
        
        
        
        
        
        