import flask
import markdown

app = flask.Flask(__name__)

class BlogsContext:
    def __init__(self, content, color_scheme, blog_name, links, all_articles):
        self.content = content
        self.color_scheme = color_scheme
        self.blog_name = blog_name
        self.links = links
        self.all_articles = all_articles

@app.route('/')
def home():
    return flask.render_template('index.html', color_scheme=app.config['COLOR_SCHEME'], blog_name=app.config['BLOG_NAME'])

@app.route('/blogs')
def blogs():
    return flask.render_template('blogs.html', color_scheme=app.config['COLOR_SCHEME'], blog_name=app.config['BLOG_NAME'])

@app.route('/photos')
def photos():
    return flask.render_template('photos.html', color_scheme=app.config['COLOR_SCHEME'], blog_name=app.config['BLOG_NAME'])

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
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])