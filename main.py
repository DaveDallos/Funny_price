import shutil

from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

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
    v3070ti = "static/img/3070ti.jpg"
    v3090 = "static/img/3090.jpg"
    v3080 = "static/img/3080.jpg"
    v1660super = "static/img/1660 SUPER.jpg"
    v3050 = "static/img/3050.jpg"
    v2060 = "static/img/2060.jpg"
    v6700xt = "static/img/6700 XT.jpg"
    v6800xt = "static/img/6800 XT.jpg"
    znachok = "static/img/znachok.png"
    logo = "static/img/ico/logo.jpg"
    if current_user.is_authenticated:
        userr = current_user.user_name
        logo = f"static/img/ico/{userr}.jpg"
    return render_template('up_menu.html', title='Смешные цены',
                           v3070ti=v3070ti, v3090=v3090, v3080=v3080, v1660super=v1660super,
                           znachok=znachok, v3050=v3050, v2060=v2060, v6700xt=v6700xt, v6800xt=v6800xt, ico=logo)


@app.route("/phone")
def phone():
    iphone11 = "static/img/phone/iphone 11.jpg"
    iphone12 = "static/img/phone/iphone 12.jpg"
    iphone13 = "static/img/phone/iphone 13 pro max.jpg"
    samsung_galaxy_a52 = "static/img/phone/samsung galaxy a52.jpg"
    samsung_galaxy_s20 = "static/img/phone/samsung galaxy s20.jpg"
    samsung_galaxy_s21 = "static/img/phone/samsung galaxy s21.jpg"
    xiaomi11 = "static/img/phone/xiaomi 11 lite.jpg"
    xiaomi10 = "static/img/phone/xiaomi redmi note 10 pro.jpg"
    znachok = "static/img/znachok.png"
    logo = "static/img/ico/logo.jpg"
    if current_user.is_authenticated:
        userr = current_user.user_name
        logo = f"static/img/ico/{userr}.jpg"
    return render_template("phone.html", title="Смартфоны",
                           iphone11=iphone11, iphone12=iphone12, iphone13=iphone13,
                           samsung_galaxy_a52=samsung_galaxy_a52, samsung_galaxy_s21=samsung_galaxy_s21,
                           samsung_galaxy_s20=samsung_galaxy_s20, xiaomi10=xiaomi10, xiaomi11=xiaomi11,
                           znachok=znachok, ico=logo)


@app.route("/TV")
def tv():
    znachok = "static/img/znachok.png"
    dexp_4k = "static/img/tv/LED DEXP 4k.jpg"
    dexp = "static/img/tv/LED DEXP.jpg"
    iffalcon = "static/img/tv/LED iFFALCON.jpg"
    lg = "static/img/tv/LED LG.jpg"
    tcl = "static/img/tv/LED TCL.jpg"
    samsung = "static/img/tv/LED Samsung.jpg"
    xiaomi = "static/img/tv/LED Xiaomi.jpg"
    xiaomi_mi = "static/img/tv/LED Xiaomi Mi.jpg"
    znachok = "static/img/znachok.png"
    logo = "static/img/ico/logo.jpg"
    if current_user.is_authenticated:
        userr = current_user.user_name
        logo = f"static/img/ico/{userr}.jpg"
    return render_template("tv.html", title="Телевизоры", znachok=znachok,
                           dexp_4k=dexp_4k, dexp=dexp, iffalcon=iffalcon, lg=lg, tcl=tcl, samsung=samsung,
                           xiaomi=xiaomi, xiaomi_mi=xiaomi_mi, ico=logo)


@app.route('/cart')
def cart():
    if not current_user.is_authenticated:
        return redirect("/information")
    znachok = "static/img/znachok.png"
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    b = []
    if user.cart:
        a = {}
        for i in str(user.cart).split(";"):
            if i and i != "None":
                cartt = db_sess.query(Cart).filter(Cart.id == i).first()
                if cartt:
                    if cartt.name in a:
                        a[cartt.name][1] += 1
                    else:
                        a[cartt.name] = [cartt.name, 1, int(cartt.price), 0, cartt.id]
        for i in a:
            a[i][3] = a[i][1] * a[i][2]
            b.append(a[i])
        db_sess.commit()
    logo = "static/img/ico/logo.jpg"
    if current_user.is_authenticated:
        userr = current_user.user_name
        logo = f"static/img/ico/{userr}.jpg"
    return render_template('cart.html', title="Корзина", cart=b,
                           znachok=znachok, ico=logo)


@app.route('/info')
def info():
    znachok = "static/img/znachok.png"
    logo = "static/img/ico/logo.jpg"
    if current_user.is_authenticated:
        userr = current_user.user_name
        logo = f"static/img/ico/{userr}.jpg"
    return render_template('info.html', title="Информация", znachok=znachok, ico=logo)


@app.route('/cart_add/<int:id>', methods=['GET', 'POST'])
def product_add(id):
    if not current_user.is_authenticated:
        return redirect("/information")
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if user and user.cart != "" and user.cart:
        user.cart = f"{user.cart};{id}"
    else:
        user.cart = id
    db_sess.commit()
    return redirect('/cart')


@app.route('/cart_delete/<int:id>', methods=['GET', 'POST'])
def product_delete(id):
    db_sess = db_session.create_session()
    cartt = db_sess.query(User).filter(User.id == current_user.id).first()
    if cartt:
        a = []
        for i in str(cartt.cart).split(";"):
            if i != "None":
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
    logo = "static/img/ico/logo.jpg"
    if current_user.is_authenticated:
        userr = current_user.user_name
        logo = f"static/img/ico/{userr}.jpg"
    return render_template('input.html', ico=logo)


@app.route('/information')
def information():
    logo = "static/img/ico/logo.jpg"
    if current_user.is_authenticated:
        userr = current_user.user_name
        logo = f"static/img/ico/{userr}.jpg"
    return render_template('information.html', ico=logo)


@app.route('/inputt', methods=['GET', 'POST'])
def picture():
    f = request.files['file']
    if f:
        with open(f'static/img/ico/{current_user.user_name}.jpg', 'wb') as file:
            shutil.copyfileobj(f, file)
    return redirect("/")


if __name__ == "__main__":
    db_session.global_init("users.db")
    app.run(port=8080, host='127.0.0.1')
