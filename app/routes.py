from app import app
from app.forms import LoginForm  # , CommentForm
from flask import render_template, flash, redirect, url_for
# from werkzeug.utils import secure_filename
from flask_user import login_required, roles_required, current_user
# import datetime

NUMBER_OF_ARTICLES = 3


@app.route('/', methods=['GET', 'POST'])
@login_required
def homeworks(page=1):
    return render_template('homeworks.html')


@app.route('/member')
@login_required  # Use of @login_required decorator
def member_page():
    return render_template('member.html', username=current_user.username)


@app.route('/admin')
@roles_required('Admin')
def admin_page():
    return render_template('admin.html', username=current_user.username)


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Published!")
        # title = form.title.data
        # author = form.author.data
        # date = datetime.datetime.now().isoformat()
        # body = form.body.data
        # image = form.image.data
        # filename = secure_filename(image.filename)
        # image.save(os.path.join(
        #     app.instance_path, 'static', filename
        # ))

        # mongo.news.save({
        #     'title': title,
        #     'author': author,
        #     'body': body,
        #     'date': date,
        #     'image': '/static/' + filename
        # })
        return redirect(url_for('index'))
    return render_template('publish.html', title='Publish', form=form)


@app.route('/news/<news_id>', methods=['GET', 'POST'])
def news_post(news_id):
    error_flag = None
    form = None
    post = None
    title = None
    # post = mongo.news.find_one({'_id': ObjectId(news_id)})  # try to find a news article with the given ID

    # if post is None:
    #     print("No post found with the ID: {}".format(news_id))
    #     error_flag = True
    #     # post = {'id': news_id, 'body': 'Not found!'}
    # else:
    #     form = CommentForm()
    #     if form.validate_on_submit():
    #         flash("Comment added!")
    #         author = form.author.data
    #         comment = form.body.data

    #         mongo.news.find_one_and_update(
    #             {'_id': ObjectId(news_id)},
    #             {'$push':
    #                 {'comments':
    #                     {
    #                         'author': author,
    #                         'comment': comment
    #                     }
    #                  }
    #              }
    #         )
    #         return redirect(url_for('news_post', news_id=news_id))
    # return render_template('news_post.html', post=post, title=post['title'], error=error_flag, form=form)
    return render_template('news_post.html', post=post, title=title, error=error_flag, form=form)
