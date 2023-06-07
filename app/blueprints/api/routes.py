from flask import request, jsonify

from . import bp
from app.models import Post, User
from app.blueprints.api.helpers import token_required

@bp.get('/posts')
def api_posts():
    result = []
    posts = Post.query.all()
    for post in posts:
        result.append({
            'id':post.id,
            'body':post.body,
            'timestamp':post.timestamp,
            'auther':post.user_id
            })
    return jsonify(result), 200


# receive posts from single user

@bp.get('/posts/<username>')
def user_posts(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify([{
                'id':post.id,
                'body':post.body,
                'timestamp':post.timestamp,
                'auther':post.user_id
                } for post in user.posts]), 200
    return jsonify({'message':'Invalid Username'}), 404


@bp.get('/post/<post_id>')
@token_required
def get_post(user,post_id):
    try:
        post = Post.query.get(post_id)
        return jsonify({
                'id':post.id,
                'body':post.body,
                'timestamp':post.timestamp,
                'auther':post.user_id
                })
    except:
        return jsonify({'message':'Invalid Post'}), 404


@bp.post('/post')
@token_required
def make_post(user):
    try:
        content = request.json
        post = Post(body=content.get('body'),user_id=user.user_id)
        post.commit()
        return jsonify([{'message':'Post Created','body':post.body}])
    except:
        jsonify([{'message':'invalid form data'}]), 401









