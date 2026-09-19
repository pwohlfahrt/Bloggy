import flask

from utils.context_classes import BlogsContext

def init_cdn(app, logger):
    @app.route('/')
    def home():
        try:
            res = flask.render_template('index.html', color_scheme=app.config['COLOR_SCHEME'], blog_name=app.config['BLOG_NAME'])
            logger.debug("Serving home page.")
            return res
        except Exception as e:
            logger.error(f"An error occurred while serving home page: {str(e)}")
            return flask.abort(500)

    @app.route('/blogs')
    def blogs():
        try:
            ctx = BlogsContext(content='',
                color_scheme=app.config['COLOR_SCHEME'],
                blog_name=app.config['BLOG_NAME'],
                links=app.config['NAV_LINKS'],
                all_articles=app.config['ALL_ARTICLES']
            )
            res = flask.render_template('blogs.html', **ctx.__dict__)
            logger.debug("Serving blogs page.")
            return res
        except Exception as e:
            logger.error(f"An error occurred while serving blogs page: {str(e)}")
            return flask.abort(500)

    @app.route('/photos')
    def photos():
        try:
            res = flask.render_template('photos.html', color_scheme=app.config['COLOR_SCHEME'], blog_name=app.config['BLOG_NAME'])
            logger.debug("Serving photos page.")
            return res
        except Exception as e:
            logger.error(f"An error occurred while serving photos page: {str(e)}")
            return flask.abort(500)