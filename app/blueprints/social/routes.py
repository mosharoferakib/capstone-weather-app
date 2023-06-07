from flask import render_template, flash, redirect, url_for, g, request
from flask_login import current_user, login_required
from . import bp 


from app.models import Post, User
from app.forms import PostForm


@bp.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        p = Post(body=form.body.data)
        p.user_id = current_user.user_id
        p.commit()
        flash("Post Saved", "success")
        return redirect(url_for('social.user_page',username=current_user.username))
    return render_template('post.jinja', form=form)


@bp.route('/userpage/<username>')
@login_required
def user_page(username):
    user = User.query.filter_by(username=username).first()
    print(f'{user=} {user.username=}')
    user_posts = user.posts
    return render_template('user_page.jinja', title=username, user=user)

@bp.route('/post', methods=['GET', 'POST'])
@login_required
def upload_form():
    return render_template('post.jinja')

@bp.route('/post', methods=['GET', 'POST'])
def upload_file():
    image = request.files['image']
    image.save(image.filename)
    return 'Image uploaded successfully!'
