# bloggy

A lightweight, self-hosted blog engine written in Flask. Write posts in Markdown, drop photos in a folder, and get a full blog with comments, discussion threads, view analytics, and an admin panel.

## Features

- **Markdown blogs** - drop `.md` files into `content/blogs/`, they show up automatically
- **Photo gallery** - drop images into `content/photos/`, served with individual pages
- **Comments** - comment on photos and blogs; blog comments support threaded replies
- **Discussion pages** - a dedicated discussion view per blog post
- **View analytics** - tracks unique views and reading time per blog post
- **Admin panel** - separate app on its own port for managing comments and viewing stats
- **Plugin system** - drop a Python file into `plugins/` to add routes or extend behavior
- **Rate limiting** - 100 requests/minute per IP out of the box
- **Configurable** - blog name, nav links, color scheme, and homepage text all live in `config.py`

## Quick start

Recomended way (docker compose):
```bash
docker compose up -d
```
Advanced setup:

```bash
git clone https://github.com/pwohlfahrt/Bloggy
cd Bloggy

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

mkdir -p logs
mkdir -p content/photos
python main.py
```

The blog runs on [http://localhost:8000](http://localhost:8000) and the admin panel on [http://localhost:7999](http://localhost:7999).

## Project layout

```
bloggy/
├── main.py              # Entry point: wires up routes, plugins, both apps
├── config.py            # All settings (name, ports, theme, homepage text)
├── routes/
│   ├── cdn.py           # Home, blogs list, photos list, photo files, discussions
│   ├── comments.py      # Comment API for photos and blogs
│   ├── statistics.py    # View/reading-time tracking
│   └── admin.py         # Admin panel routes
├── database/
│   ├── models.py        # Peewee models (Comment, Blog_Comment, Views) + SQLite init
│   ├── blogs.py         # Blog comment queries
│   ├── photos.py        # Photo comment queries
│   └── statistics.py    # View queries
├── templates/           # Jinja2 templates
├── content/
│   ├── blogs/           # Your posts (Markdown)
│   └── photos/          # Your images
├── plugins/             # Drop-in plugins
└── data.db              # SQLite database (auto-created)
```

## Configuration

Everything is in `config.py`:

```python
DEBUG = True
APP_PORT = 8000
ADMIN_PORT = 7999
BLOG_NAME = 'My Blog'
NAV_LINKS = [
    {'name': 'Blogs', 'url': '/blogs'},
    {'name': 'Photos', 'url': '/photos'},
]
COLOR_SCHEME = {
    'primary': "#6D159F",
    'secondary': "#6a0a90",
    'background': "#1C0C1E",
    'text': "#F7F7F7"
}
HOMEPAGE_TEXT = { ... }  # eyebrow, heading, intro, feature block
PHOTO_QUOTE = "The best photo is the one you take tomorrow!"
ENABLE_PLUGINS = True
```

Restart the server after changing config - articles and photos are scanned at startup.

## Writing posts

Create a Markdown file in `content/blogs/`:

```bash
content/blogs/my-first-post.md
```

Supports fenced code blocks, syntax highlighting, tables, and a table of contents. Visit `/blog/my-first-post`.

Photos work the same way - put an image in `content/photos/` and it appears under `/photos`.

## Plugins

Create `plugins/my_plugin.py`:

```python
def init_plugin(app, admin, logger):
    @app.route("/hello")
    def hello():
        return "hi from plugin"
```

Every `.py` file in `plugins/` (except `__init__.py`) is imported at startup and its `init_plugin(app, admin, logger)` is called. You get access to both the public and the admin Flask app. Plugins are executed with full trust - only install ones you wrote or trust.

## ⚠️ Security notes

1. Don't expose the admin port to the public internet as-is.
2. Plugins are installed with full trust. Remember to check the code.

## License

Do whatever you want with it.
