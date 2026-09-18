import os

import flask
import markdown

app = flask.Flask(__name__)

class Settings:
    def __init__(self):
        self.DEBUG = True
        self.PORT = 8000
        self.BLOG_NAME = 'My Blog'
        self.NAV_LINKS = [
            {'name': 'Blogs', 'url': '/blogs'},
            {'name': 'Photos', 'url': '/photos'},
        ]
        self.COLOR_SCHEME = {
            'primary': "#6D159F",
            'secondary': "#6a0a90",
            'background': "#1C0C1E",
            'text': "#F7F7F7"
        }
        self.ALL_ARTICLES = [filename[:-3] for filename in os.listdir('content/blogs') if filename.endswith('.md')]

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
    app.config.from_object(Settings())
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'])