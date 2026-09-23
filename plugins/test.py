import flask

def init_plugin(app, admin, logger):
    @app.route("/test")
    def test_route():
        return "hi from plugin"