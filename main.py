import flask
import markdown
import logging
import datetime
from threading import Thread

import routes.cdn as cdn
import routes.comments as comments
import routes.statistics as statistics
import routes.admin as admin_route

from database.models import init_db
from utils.context_classes import BlogsContext

app = flask.Flask(__name__)
admin = flask.Flask("admin")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if app.config.get('DEBUG', False) else logging.INFO)
logger.addHandler(logging.FileHandler(f'logs/{datetime.datetime.now().strftime("%Y-%m-%d")}.log'))

@app.route('/blog/<title>')
def blog(title: str):
    content = ''
    try:
        with open(f'content/blogs/{title}.md', 'r') as file:
            content = file.read()
    except FileNotFoundError:
        logger.info(f"Blog post '{title}' not found.")
        return flask.abort(404)
    except Exception as e:
        logger.error(f"An error occurred while fetching blog post '{title}': {str(e)}")
        return flask.abort(500)

    content = markdown.markdown(content, extensions=['fenced_code', 'codehilite', 'tables', 'toc'])
    

    context = BlogsContext(content=content,
        title=title,
        color_scheme=app.config['COLOR_SCHEME'],
        blog_name=app.config['BLOG_NAME'],
        links=app.config['NAV_LINKS'],
        all_articles=app.config['ALL_ARTICLES']
    )
    return flask.render_template('blog.html', **context.__dict__)

@app.route('/photo/<filename>')
def photo(filename: str):
    if filename not in app.config['PHOTOS_NAMES']:
        logger.info(f"Photo '{filename}' not found.")
        return flask.abort(404)
    try:
        ctx = BlogsContext(content=filename,
            color_scheme=app.config['COLOR_SCHEME'],
            blog_name=app.config['BLOG_NAME'],
            links=app.config['NAV_LINKS'],
            all_articles=app.config['ALL_ARTICLES']
        )
        res = flask.render_template('photo.html', **ctx.__dict__)
        logger.debug(f"Serving photo page for: {filename}")
        return res
    except Exception as e:
        logger.error(f"An error occurred while serving photo page for '{filename}': {str(e)}")
        return flask.abort(500)

if __name__ == '__main__':
    app.config.from_pyfile('config.py')

    init_db()
    cdn.init_cdn(app, logger)
    comments.init_comments(app, logger)
    statistics.init_stats(app, logging)
    admin_route.init_admin(app, admin, logger)

    logger.info(f"Starting Flask app on port {app.config['APP_PORT']} with debug={app.config['DEBUG']}")

    Thread(
        target=lambda: admin.run(
            debug=app.config['DEBUG'],
            use_reloader=False,
            port=app.config['ADMIN_PORT']
        ),
        daemon=True
    ).start()
    app.run(
        debug=app.config['DEBUG'],
        use_reloader=False,
        port=app.config['APP_PORT']
    )