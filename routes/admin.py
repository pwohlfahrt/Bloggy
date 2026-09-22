import flask

from database.statistics import get_viewing_time_of_blog

def init_admin(app, admin, logging):

    @admin.route('/admin')
    def admin_console():
        logging.warning("Serving admin console. Is it u?")
        return flask.render_template("admin.html", admin_name=app.config["ADMIN_NAME"])

    @admin.route('/admin/rerun_config')
    def rerun_config():
        logging.warning("Reruning config from admin console. If it`s not you, take actions")
        try:
            app.config.from_pyfile('config.py')
        except Exception as e:
            logging.error(f"reruning config faild: {e}")
            return flask.jsonify({'status': 'error', 'description': e})
        return flask.jsonify({'status': 'ok'})

    @admin.route('/admin/all_blogs')
    def all_blogs():
        return flask.jsonify(app.config["ALL_ARTICLES"])

    @admin.route('/admin/reading_time/<blog>')
    def reading_time(blog: str):
        return flask.jsonify({'status': "ok", 'time': get_viewing_time_of_blog(blog)})
