class BlogsContext:
    def __init__(self, content, color_scheme, blog_name, links, all_articles, title=""):
        self.content = content
        self.title = title
        self.color_scheme = color_scheme
        self.blog_name = blog_name
        self.links = links
        self.all_articles = all_articles
