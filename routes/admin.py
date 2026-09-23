import flask
import os

from database.statistics import get_viewing_time_of_blog, get_latest_comments, unique_views
from database.admin import delete_comment

def init_admin(app, admin, logging):

    @admin.route('/admin')
    def admin_console():
        logging.warning("Serving admin console. Is it u?")
        return flask.render_template(
            "admin.html",
            admin_name=app.config["ADMIN_NAME"],
            color_scheme=app.config["COLOR_SCHEME"]
        )

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

    @admin.route('/admin/unique_views_per_blog')
    def unique_views_per_blog():
        return flask.jsonify({'status': "ok", "res": unique_views()})

    @admin.route('/admin/latest_comments/<num>')
    def latest_comments(num):
        try:
            limit = int(num)
        except ValueError:
            return flask.jsonify({
                'status': 'error',
                'description': 'num must be an integer'
            }), 400

        if limit < 1:
            return flask.jsonify({
                'status': 'error',
                'description': 'num must be greater than zero'
            }), 400

        return flask.jsonify({'status': 'ok', 'comments': get_latest_comments(limit)})

    @admin.route('/admin/delete_comment/<id>')
    def remove_comment(id: int):
        try:
            delete_comment(id)
        except Exception as e:
            logging.error(f"Failed to remove comment: {id}")
            return flask.abort(500)
        return flask.jsonify({'status': "ok"})

    @admin.route('/admin/get_plugins')
    def get_plugins():
        return {
            'isActive': app.config["ENABLE_PLUGINS"],
            'list': [filename for filename in os.listdir("plugins") if filename not in ["__init__.py", "__pycache__"]]
        }