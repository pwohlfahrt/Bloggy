import flask

from utils.context_classes import BlogsContext

def init_cdn(app, logger):
    def make_ctx(content='', title=''):
        return BlogsContext(
            content=content,
            color_scheme=app.config['COLOR_SCHEME'],
            blog_name=app.config['BLOG_NAME'],
            links=app.config['NAV_LINKS'],
            all_articles=app.config['ALL_ARTICLES'],
            title=title,
        )

    @app.route('/')
    def home():
        try:
            ctx = make_ctx(content=app.config["HOMEPAGE_TEXT"])
            res = flask.render_template('index.html', **ctx.__dict__)
            logger.debug("Serving home page.")
            return res
        except Exception as e:
            logger.error(f"An error occurred while serving home page: {str(e)}")
            return flask.abort(500)

    @app.route('/blogs')
    def blogs():
        try:
            ctx = make_ctx()
            res = flask.render_template('blogs.html', **ctx.__dict__)
            logger.debug("Serving blogs page.")
            return res
        except Exception as e:
            logger.error(f"An error occurred while serving blogs page: {str(e)}")
            return flask.abort(500)

    @app.route('/photos')
    def photos():
        try:
            ctx = make_ctx(content=app.config["PHOTOS_NAMES"])
            res = flask.render_template('photos.html', **ctx.__dict__, quote=app.config['PHOTO_QUOTE'])
            logger.debug("Serving photos page.")
            return res
        except Exception as e:
            logger.error(f"An error occurred while serving photos page: {str(e)}")
            return flask.abort(500)

    @app.route('/content/photos/<filename>')
    def serve_photo(filename):
        try:
            logger.debug(f"Serving photo: {filename}")
            return flask.send_from_directory('content/photos', filename)
        except FileNotFoundError:
            logger.info(f"Photo '{filename}' not found.")
            return flask.abort(404)
        except Exception as e:
            logger.error(f"An error occurred while serving photo '{filename}': {str(e)}")
            return flask.abort(500)

    @app.route('/blog/discussions/<blog>')
    def serve_discussion(blog: str):
        try:
            ctx = make_ctx(title=blog)
            logger.debug(f"Serving discussion page for {blog}")
            return flask.render_template('discussion.html', **ctx.__dict__)
        except Exception as e:
            logger.error(f"Error while serving discussion page for {blog}: {e}")
            return flask.abort(500)