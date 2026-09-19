import flask
import markdown
import logging
import datetime

import routes.cdn as cdn
from utils.context_classes import BlogsContext

app = flask.Flask(__name__)
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
        color_scheme=app.config['COLOR_SCHEME'],
        blog_name=app.config['BLOG_NAME'],
        links=app.config['NAV_LINKS'],
        all_articles=app.config['ALL_ARTICLES']
    )
    return flask.render_template('blog.html', **context.__dict__)

if __name__ == '__main__':
    app.config.from_pyfile('config.py')

    cdn.init_cdn(app, logger)

    logger.info(f"Starting Flask app on port {app.config['PORT']} with debug={app.config['DEBUG']}")
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])