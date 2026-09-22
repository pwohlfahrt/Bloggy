import flask

from database.statistics import add_viewing_blog

def init_stats(app, logger):

    @app.post("/stats/blog_heartbeat/<blog_name>")
    def bheartbeat(blog_name: str):
        remote_ip = flask.request.headers.get('X-Forwarded-For')
        if not remote_ip:
            remote_ip = flask.request.remote_addr

        data = flask.request.get_json(silent=True)
        if not data or "time_spent" not in data:
            return flask.jsonify({
                "status": "error",
                "description": "time_spent is required"
            }), 400

        time_spent = data["time_spent"]

        add_viewing_blog(blog_name, remote_ip, time_spent) #type: ignore

        return flask.jsonify({'status': "ok"})