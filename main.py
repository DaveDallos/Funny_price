from flask import Flask, render_template, url_for

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1')
