import shutil

from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import requests

# from data import db_session
from data import db_session
from data.cart import Cart
from data.users import User
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


@app.route("/payment")
def payment():
    return render_template('payment.html')


@app.route('/')
@app.route('/funny_price')
def index():
    Pummel_Party = "static/img/Pummel_Party.jpg"
    Black_Messa = "static/img/Black_Messa.jpg"
    Tiny_Bunny = "static/img/Tiny_Bunny.jpg"
    Alyx = "static/img/Alyx.jpg"
    Potion_Craft = "static/img/Potion_Craft.jpg"
    GTFO = "static/img/GTFO.jpg"
    High_On_Life = "static/img/High_On_Life.jpg"
    The_Forest = "static/img/The_Forest.jpg"
    znachok = "static/img/znachok.png"
    logo = "static/img/ico/logo.jpg"
    if current_user.is_authenticated:
        userr = current_user.user_name
        logo = f"static/img/ico/{userr}.jpg"
    return render_template('up_menu.html', title='Смешные цены',
                           Pummel_Party=Pummel_Party, Black_Messa=Black_Messa, Tiny_Bunny=Tiny_Bunny, Alyx=Alyx,
                           Potion_Craft=Potion_Craft, GTFO=GTFO, High_On_Life=High_On_Life, The_Forest=The_Forest,
                           ico=logo, znachok=znachok)


@app.route('/cart')
def cart():
    if not current_user.is_authenticated:
        return redirect("/info")
    znachok = "static/img/znachok.png"
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    b = []
    if user.cart:
        a = {}
        for i in user.cart.split(";"):
            if i:
                cartt = db_sess.query(Cart).filter(Cart.id == i).first()
                if cartt.name in a:
                    a[cartt.name][1] += 1
                else:
                    a[cartt.name] = [cartt.name, 1, int(cartt.price), 0, cartt.id]
        for i in a:
            a[i][3] = a[i][1] * a[i][2]
            b.append(a[i])
        db_sess.commit()
    return render_template('cart.html', title="Корзина", cart=b,
                           znachok=znachok)


@app.route('/info')
def info():
    znachok = "static/img/znachok.png"
    return render_template('info.html', title="Информация", znachok=znachok)


# @app.route('/cart_add/<int:id>', methods=['GET', 'POST'])
# def product_add(id):
#     if not current_user.is_authenticated:
#         return redirect("/info")
#     db_sess = db_session.create_session()
#     user = db_sess.query(User).filter(User.id == current_user.id).first()
#     if user.cart != "":
#         user.cart = f"{user.cart};{id}"
#     else:
#         user.cart = id
#     db_sess.commit()
#     return redirect('/')


@app.route('/game/<int:id>', methods=['GET', 'POST'])
def product_add(id):
    logo = "../static/img/ico/logo.jpg"
    znachok = f"../static/img/znachok.png"
    if current_user.is_authenticated:
        userr = current_user.user_name
        logo = f"../static/img/ico/{userr}.jpg"
    if id == 1:
        return render_template('info.html', title="Информация", znachok=znachok, ico=logo)
    return redirect('/')


@app.route('/cart_delete/<int:id>', methods=['GET', 'POST'])
def product_delete(id):
    db_sess = db_session.create_session()
    cartt = db_sess.query(User).filter(User.id == current_user.id).first()
    if cartt:
        a = []
        for i in cartt.cart.split(";"):
            if int(i) != id:
                a.append(i)
            else:
                id = 0
                print(i)
        a = ";".join(a)
        cartt.cart = a
        print(a)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/cart')


@app.route('/input')
def loading_of_picture():
    return render_template('input.html')


@app.route('/inputt', methods=['GET', 'POST'])
def picture():
    f = request.files['file']
    with open(f'static/img/ico/{current_user.user_name}.jpg', 'wb') as file:
        shutil.copyfileobj(f, file)
    return redirect("/")


if __name__ == "__main__":
    db_session.global_init("users.db")
    app.run(port=8080, host='127.0.0.1')
