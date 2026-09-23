import flask
from database.models import Comment
from database.photos import create_comment

def init_comments(app, logger):
    @app.route('/comments/<photo_name>', methods=['GET'])
    def get_comments(photo_name):
        try:
            comments = Comment.select().where(Comment.photo_name == photo_name).order_by(Comment.created_at.desc())
            comments_list = [{'author': comment.author, 'content': comment.content, 'created_at': comment.created_at} for comment in comments]
            logger.debug(f"Fetched {len(comments_list)} comments for photo: {photo_name}")
            return flask.jsonify(comments_list)
        except Exception as e:
            logger.error(f"An error occurred while fetching comments for photo '{photo_name}': {str(e)}")
            return flask.abort(500)

    @app.route('/comments/<photo_name>', methods=['POST'])
    def add_comment(photo_name):
        try:
            data = flask.request.get_json()
            author = data.get('author')
            content = data.get('content')
            if not author or not content:
                logger.warning("Author or content missing in the request.")
                return flask.abort(400, description="Author and content are required.")

            if len(content) > 250:
                return flask.abort(400, description="Content to long.")

            if len(author) > 250:
                return flask.abort(400, description="Author name to long.")
            
            create_comment(photo_name, author, content)
            logger.debug(f"Added comment by '{author}' for photo: {photo_name}")
            return flask.jsonify({'message': 'Comment added successfully'}), 201
        except Exception as e:
            logger.error(f"An error occurred while adding a comment for photo '{photo_name}': {str(e)}")
            return flask.abort(500)