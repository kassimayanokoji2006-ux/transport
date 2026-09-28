from router import routes
import uvicorn

import inspect

async def app(scope, receive, send):
    assert scope['type'] == "http"
    path = scope["path"]
    if path in routes:
        # Vérifiez si la fonction est asynchrone
        if callable(routes[path]):
            if inspect.iscoroutinefunction(routes[path]):
                response = await routes[path](scope, receive, send)
            else:
                response = routes[path](scope, receive, send)
        else:
            response = routes[path]
        
        if  response:
           
            # Envoyer la réponse
            await send({
                'type': 'http.response.start',
                'status': response.get('status', 500),
                'headers': response['headers'],
            })
            await send({
                'type': 'http.response.body',
                'body': response['body'],
            })
    else:
        # Route non trouvée
        await send({
            'type': 'http.response.start',
            'status': 404,
            'headers': [(b'content-type', b'text/html; charset=utf-8')],
        })
        await send({
            'type': 'http.response.body',
            'body': '<h1>Page non trouvée</h1>'.encode('utf-8'),
        })



   
if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)