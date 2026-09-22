import flask

def init_admin(app, admin, logger):

    @admin.route('/admin/rerun_config')
    def rerun_config():
        logger.warning("Reruning config from admin console. If it`s not you, take actions")
        try:
            app.config.from_pyfile('config.py')
        except Exception as e:
            return flask.jsonify({'status': 'error', 'description': e})
        return flask.jsonify({'status': 'ok'})