import flask
from database.models import Comment
from database.photos import create_comment
from database.blogs import create_blog_comment, get_blog_comments

def init_comments(app, logger):

    class InvalidData(Exception):
        def __init__(self, description: str) -> None:
            self.description = description

    def validate_data(author: str, content: str):
        if not author or not content:
            logger.warning("Author or content missing in the request.")
            raise InvalidData("Author and content are required.")

        if len(content) > 250:
            raise InvalidData("Content to long.")

        if len(author) > 250:
            raise InvalidData("Author name to long.")

    @app.route('/photos/comments/<photo_name>', methods=['GET'])
    def get_comments(photo_name):
        try:
            comments = Comment.select().where(Comment.photo_name == photo_name).order_by(Comment.created_at.desc())
            comments_list = [{'author': comment.author, 'content': comment.content, 'created_at': comment.created_at} for comment in comments]
            logger.debug(f"Fetched {len(comments_list)} comments for photo: {photo_name}")
            return flask.jsonify(comments_list)
        except Exception as e:
            logger.error(f"An error occurred while fetching comments for photo '{photo_name}': {str(e)}")
            return flask.abort(500)

    @app.route('/photos/comments/<photo_name>', methods=['POST'])
    def add_comment(photo_name):
        try:
            data = flask.request.get_json()
            author = data.get('author')
            content = data.get('content')

            validate_data(author, content)
            
            create_comment(photo_name, author, content)
            logger.debug(f"Added comment by '{author}' for photo: {photo_name}")
            return flask.jsonify({'message': 'Comment added successfully'}), 201
        except InvalidData as e:
            return flask.abort(400, description=e.description)
        except Exception as e:
            logger.error(f"An error occurred while adding a comment for photo '{photo_name}': {str(e)}")
            return flask.abort(500)

    @app.route('/blog/comments/<blog>/<offset>')
    def get_b_comments(blog: str, offset: str | None):
        try:
            if offset is None:
                offset = 0
            else:
                offset = int(offset) #type: ignore
            if offset < 0:
                return flask.abort(400, description="Offset must be a non-negative integer.")
            return flask.jsonify(get_blog_comments(blog, offset))
        except ValueError:
            logger.debug(f"Invalid offset value provided for blog '{blog}': {offset}")
            return flask.abort(400, description="Offset must be a non-negative integer.")
        except Exception as e:
            logger.error(f"Failed to retrive comments for {blog}: {e}")
            return flask.abort(500)
        
    @app.route('/blog/comments/<blog>', methods=['POST'])
    def add_blog_comments(blog: str):
        try:
            data = flask.request.get_json()
            author = data.get('author')
            content = data.get('content')
            reference = data.get('reference')
            if reference in ('', None):
                reference = None
            elif not isinstance(reference, int):
                try:
                    reference = int(reference)
                except (TypeError, ValueError):
                    raise InvalidData("Reference must be a valid comment ID.")

            validate_data(author, content)

            logger.debug(f"Adding comment for blog '{blog}' by '{author}' with reference '{reference}'")
            create_blog_comment(blog, author, content, reference)
            logger.debug(f"Added comment for blog {blog} by {author}")
            return flask.jsonify({'message': 'Comment added successfully'}), 201
        except InvalidData as e:
            logger.debug(f"Invalid data provided for adding comment to blog '{blog}': {e.description}")
            return flask.abort(400, description=e.description)
        except Exception as e:
            logger.error(f"An error occurred while adding a comment for blog '{blog}': {str(e)}")
            return flask.abort(500)