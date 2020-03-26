from gevent.pywsgi import WSGIServer

from li_permit_plan_form import create_app


if __name__ == '__main__':
    app = create_app()
    http_server = WSGIServer(('0.0.0.0', 8201), app)
    http_server.serve_forever()