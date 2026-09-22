import os
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
ALL_ARTICLES = [filename[:-3] for filename in os.listdir('content/blogs') if filename.endswith('.md')]
PHOTOS_NAMES = [filename for filename in os.listdir('content/photos') if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
PHOTO_QUOTE = "The best photo is the one you take tomorrow!"