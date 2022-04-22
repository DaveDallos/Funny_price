from flask import Flask, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from flask import Flask, render_template, redirect, make_response, request, session, abort

from data.users import User
# from data import db_session
from data import db_session
from forms.user import LoginForm, RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            user_name=form.name.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/')
@app.route('/funny_price')
def index():
    v3070ti = "static/img/3070ti.jpg"
    v3090 = "static/img/3090.jpg"
    v3080 = "static/img/3080.jpg"
    v1660super = "static/img/1660 SUPER.jpg"
    v3050 = "static/img/3050.jpg"
    v2060 = "static/img/2060.jpg"
    v6700xt = "static/img/6700 XT.jpg"
    v6800xt = "static/img/6800 XT.jpg"
    znachok = "static/img/znachok.png"
    return render_template('up_menu.html', title='Смешные цены',
                           v3070ti=v3070ti, v3090=v3090, v3080=v3080, v1660super=v1660super,
                           znachok=znachok, v3050=v3050, v2060=v2060, v6700xt=v6700xt, v6800xt=v6800xt)


@app.route('/cart')
def cart():
    znachok = "static/img/znachok.png"
    return render_template('cart.html', title="Корзина", cart=[["v3070ti", 1], ["v3090", 1]],
                           znachok=znachok)


@app.route('/info')
def info():
    znachok = "static/img/znachok.png"
    return render_template('info.html', title="Информация", znachok=znachok)


# @app.route('/cart_delete/<int:id>', methods=['GET', 'POST'])
# def news_delete(id):
#     db_sess = db_session.create_session()
#     cartt = db_sess.query(Cart).filter(Cart.id == id,
#                                       Cart.user == current_user
#                                       ).first()
#     if cartt:
#         db_sess.delete(cartt)
#         db_sess.commit()
#     else:
#         abort(404)
#     return redirect('/')


if __name__ == "__main__":
    db_session.global_init("users.db")
    app.run(port=8080, host='127.0.0.1')
