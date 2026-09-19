import flask
import markdown

import routes.cdn as cdn
from utils.context_classes import BlogsContext

app = flask.Flask(__name__)

@app.route('/blog/<title>')
def blog(title: str):
    content = ''
    with open(f'content/blogs/{title}.md', 'r') as file:
        content = file.read()

    context = BlogsContext(content=markdown.markdown(content),
        color_scheme=app.config['COLOR_SCHEME'],
        blog_name=app.config['BLOG_NAME'],
        links=app.config['NAV_LINKS'],
        all_articles=app.config['ALL_ARTICLES']
    )
    return flask.render_template('blog.html', **context.__dict__)

if __name__ == '__main__':
    app.config.from_pyfile('config.py')

    cdn.init_cdn(app)

    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])