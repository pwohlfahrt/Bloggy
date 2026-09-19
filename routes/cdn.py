import flask

from utils.context_classes import BlogsContext

def init_cdn(app):
    @app.route('/')
    def home():
        return flask.render_template('index.html', color_scheme=app.config['COLOR_SCHEME'], blog_name=app.config['BLOG_NAME'])

    @app.route('/blogs')
    def blogs():
        ctx = BlogsContext(content='',
            color_scheme=app.config['COLOR_SCHEME'],
            blog_name=app.config['BLOG_NAME'],
            links=app.config['NAV_LINKS'],
            all_articles=app.config['ALL_ARTICLES']
        )
        return flask.render_template('blogs.html', **ctx.__dict__)

    @app.route('/photos')
    def photos():
        return flask.render_template('photos.html', color_scheme=app.config['COLOR_SCHEME'], blog_name=app.config['BLOG_NAME'])