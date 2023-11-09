from flask import json, jsonify, request, render_template
from werkzeug.exceptions import default_exceptions, HTTPException
import logging

log = logging.getLogger("app_name." + __name__)


def handle_any_error(e):
    if hasattr(request, 'headers') and 'html' in request.headers.get('Accept', []):
        template = 'layouts/base-error.html'

        data = {
            404: {
                "title": "Pagina/Conteudo não encontrada(o)",
                "message": "A pagina/conteudo que procura não existe ou foi movida."
            },
            401: {
                "title": "Acesso não autorizado",
                "message": "Você não possui acesso a pagina requisitada."
            },
            500: {
                "title": "Erro interno",
                "message": "Algo deu errado na aplicação, tente novamente mais tarde ou contate um administrador."
            }
        }

        return render_template(template, code=e.code, title=data[e.code]['title'], message=data[e.code]['message']), e.code

    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "message": e.description,
    })
    response.content_type = "application/json"
    return response, e.code


def handle_any_exception(e):
    if isinstance(e, HTTPException):
        return e
    log.exception("Uncaught Exception occurred: {}".format(e))
    if hasattr(request, 'headers') and 'html' in request.headers.get('Accept', []):
        template = 'layouts/base-error.html'
        data = {
            500: {
                "title": "Erro interno",
                "message": "Algo deu errado na aplicação, tente novamente mais tarde ou contate um administrador."
            }
        }
        return render_template(template, code=500, title=data[500]['title'], message=data[500]['message']), 500
    return jsonify({
        "code": 500,
        "name": "Internal Server Error",
        "message": "The server encountered an internal error and was unable to complete your request. Either the "
                   "server is overloaded or there is an error in the application.",
    }), 500


def register_error_handler(app):
    for ex in default_exceptions:
        app.register_error_handler(ex, handle_any_error)
    app.register_error_handler(Exception, handle_any_exception)
