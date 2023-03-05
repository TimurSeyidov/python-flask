import datetime
from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from core.models import db_session
from core.models.User import User
from core.models.News import News
from core.forms import RegisterForm, LoginForm, NewsForm
from api.news import main as NewsApiMain

app = Flask(
    __name__,
    template_folder='./templates'
)
app.config['SECRET_KEY'] = 'absdjiasbdian'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)
app.config['SESSION_COOKIE_NAME'] = 'blabla_session'
app.config['SESSION_COOKIE_SECURE'] = True
login_manager = LoginManager()
login_manager.init_app(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    query = db_sess.query(News)
    if not current_user.is_authenticated:
        query = query.filter(News.is_private == False)
    else:
        query = query.filter(
            (News.is_private == False) | (News.user == current_user)
        )
    news = query.order_by(News.created_at.desc())
    return render_template('news/index.html', items=news)


@app.route('/news/add',  methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news/manage.html', title='Добавление новости',
                           form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id: int):
    form = NewsForm()
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(
        News.id == id,
        News.user == current_user
    ).first()
    if request.method == "GET":
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news/manage.html', form=form,
                           title='Редактирование новости')


@app.route('/news/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def news_delete(id: int):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(request.referrer or '/')
    form = RegisterForm()
    is_v = form.validate_on_submit()
    print(is_v)
    if is_v:
        try:
            if form.password.data != form.password_again.data:
                raise Exception('Пароли не совпадают')
            db_sess = db_session.create_session()
            user = db_sess.query(User)\
                .filter(User.email.like(form.email.data))\
                .first()
            print('----', user)
            if user:
                raise Exception('Такой пользователь уже есть')
            user = User(
                name=form.name.data,
                email=form.email.data,
                about=form.about.data
            )
            print(user)
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        except Exception as e:
            print(e)
            return render_template(
                'register.html',
                form=form,
                message=str(e)
            )
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(request.referrer or '/')
    form = LoginForm()
    message = None
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data
        ).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        message="Неправильный логин или пароль"
    return render_template('login.html', title='Авторизация', form=form, message=message)

@app.route('/logout')
def logout():
    if not current_user.is_authenticated:
        return redirect('/login')
    logout_user()
    return redirect('/')





def main():
    db_session.global_init('./db/test.db')
    app.register_blueprint(NewsApiMain.blueprint)
    app.run()

if __name__ == '__main__':
    main()
