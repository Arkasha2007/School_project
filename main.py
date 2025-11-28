import requests
from flask import render_template, request
from data import db_session
from data.intermediate_data import Intermediate_data
from data.products import Products
from api.product_api import product_bp
from api.temporary_api import product_time_bp

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

from data.users import User


def replenishment():
    db_session.global_init('db/product.db')
    session = db_session.create_session()
    query = session.query(Products).all()
    for item in query:
        if item.id < 9:
            item.quantity = item.quantity + 50
        elif 9 <= item.id <= 15:
            item.quantity = item.quantity + 30
        elif 16 <= item.id <= 19:
            item.quantity = item.quantity + 20
        elif item.id > 19:
            item.quantity = item.quantity + 10
    session.commit()


sched = BackgroundScheduler(daemon=True)
sched.add_job(replenishment, 'interval', minutes=5)
sched.start()
count_comment = [1]
plenty_into = [0]
current_user = ['', '', 0]


def intermediate(one_data, two_data, three_data, four_data, five_data, six_data, seven_data, eight_data,
                 nine_data, ten_data, eleven_data, twelve_data, thirteen_data, fourteen_data, fifteen_data,
                 sixteen_data, seventeen_data, eighteen_data, nineteen_data, twenty_data,
                 twenty_one_data, twenty_two_data):
    db_session.global_init('db/product.db')
    session = db_session.create_session()
    query = session.query(Intermediate_data).all()
    for item in query:
        if item.id == 1:
            item.quantity = one_data
        elif item.id == 2:
            item.quantity = two_data
        elif item.id == 3:
            item.quantity = three_data
        elif item.id == 4:
            item.quantity = four_data
        elif item.id == 5:
            item.quantity = five_data
        elif item.id == 6:
            item.quantity = six_data
        elif item.id == 7:
            item.quantity = seven_data
        elif item.id == 8:
            item.quantity = eight_data
        elif item.id == 9:
            item.quantity = nine_data
        elif item.id == 10:
            item.quantity = ten_data
        elif item.id == 11:
            item.quantity = eleven_data
        elif item.id == 12:
            item.quantity = twelve_data
        elif item.id == 13:
            item.quantity = thirteen_data
        elif item.id == 14:
            item.quantity = fourteen_data
        elif item.id == 15:
            item.quantity = fifteen_data
        elif item.id == 16:
            item.quantity = sixteen_data
        elif item.id == 17:
            item.quantity = seventeen_data
        elif item.id == 18:
            item.quantity = eighteen_data
        elif item.id == 19:
            item.quantity = nineteen_data
        elif item.id == 20:
            item.quantity = twenty_data
        elif item.id == 21:
            item.quantity = twenty_one_data
        elif item.id == 22:
            item.quantity = twenty_two_data
    session.commit()


def commentarios(data):
    count_comment[0] = count_comment[0] + 1
    db_session.global_init('db/product.db')
    session = db_session.create_session()
    query = session.query(Products).all()
    for item in query:
        number = int(item.id)
        if 10 >= data[number - 1] >= 0:
            item.average_score = str(float((float(item.average_score) + data[number - 1]) / count_comment[0]))
    session.commit()


def users(information):
    db_session.global_init('db/product.db')
    session = db_session.create_session()
    query = session.query(User).all()
    if not query:
        user = User()
        user.surname = information[0]
        user.name = information[1]
        user.password = information[2]
        user.purchased_goods = 0
        session.add(user)
        session.commit()
    else:
        for item in query:
            if item.surname == information[0] and item.name == information[1] and str(item.password) == str(
                    information[2]):
                current_user[0] = information[0]
                current_user[1] = information[1]
                current_user[2] = item.purchased_goods
                return True
            elif item.surname == information[0] and item.name == information[1] and str(item.password) != str(
                    information[2]):
                return False
        else:
            user = User()
            user.surname = information[0]
            user.name = information[1]
            user.password = information[2]
            user.purchased_goods = 0
            session.add(user)
            session.commit()
            current_user[0] = information[0]
            current_user[1] = information[1]
            current_user[2] = 0
        return True


def plus_shop(plenty):
    db_session.global_init('db/product.db')
    session = db_session.create_session()
    query = session.query(User).all()
    for item in query:
        if item.surname == plenty[0] and item.name == plenty[1]:
            item.purchased_goods = item.purchased_goods + plenty[2]
            current_user[2] = item.purchased_goods
    session.commit()


app = Flask(__name__)
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(product_time_bp, url_prefix='/api')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['GET', 'POST'])
def register():
    global current_user
    current_user = ['', '', 0]
    plenty_into[0] = 0
    return render_template("start_list.html", title='Вход пользователя')


@app.route('/products', methods=['GET', 'POST'])
def index():
    db_session.global_init('db/product.db')
    try:
        plenty = [int(request.form['ware_1']), int(request.form['ware_2']), int(request.form['ware_3']),
                  int(request.form['ware_4']), int(request.form['ware_5']), int(request.form['ware_6']),
                  int(request.form['ware_7']), int(request.form['ware_8']), int(request.form['ware_9']),
                  int(request.form['ware_10']), int(request.form['ware_11']), int(request.form['ware_12']),
                  int(request.form['ware_13']), int(request.form['ware_14']), int(request.form['ware_15']),
                  int(request.form['ware_16']), int(request.form['ware_17']), int(request.form['ware_18']),
                  int(request.form['ware_19']), int(request.form['ware_20']), int(request.form['ware_21']),
                  int(request.form['ware_22'])]
        if plenty.count(0) != len(plenty):
            commentarios(plenty)
    except Exception:
        print('Пока нет отзывов')
    if not plenty_into[0]:
        if users([request.form['surname'], request.form['name'], request.form['password']]):
            product = requests.get('http://localhost:5000/api/products').json()
            plenty_into[0] = 1
            if current_user[2] > 500:
                return render_template("index.html", information=product, surname=current_user[0],
                                       name=current_user[1], shop=current_user[2], title='Товары',
                                       hello_users='Приветствуем почётного покупателя!')
            else:
                return render_template("index.html", information=product, surname=current_user[0],
                                       name=current_user[1], shop=current_user[2], title='Товары')
        return render_template("back.html")
    else:
        print("Yes", current_user)
        product = requests.get('http://localhost:5000/api/products').json()
        plus_shop(current_user)
        return render_template("index.html", information=product, surname=current_user[0],
                               name=current_user[1], shop=current_user[2], title='Товары')


@app.route('/shopping_cart', methods=['GET', 'POST'])
def buy():
    product = requests.get('http://localhost:5000/api/products').json()
    intermediate(
        int(request.form['first_product']), int(request.form['twice_product']), int(request.form['three_product']),
        int(request.form['four_product']), int(request.form['five_product']), int(request.form['six_product']),
        int(request.form['seven_product']), int(request.form['eight_product']), int(request.form['nine_product']),
        int(request.form['ten_product']), int(request.form['eleven_product']), int(request.form['twelve_product']),
        int(request.form['thirteen_product']), int(request.form['fourteen_product']),
        int(request.form['fifteen_product']), int(request.form['sixteen_product']),
        int(request.form['seventeen_product']), int(request.form['eighteen_product']),
        int(request.form['nineteen_product']), int(request.form['twenty_product']),
        int(request.form['twenty_one_product']), int(request.form['twenty_two_product']))
    return render_template('total.html', data=product, product_1=int(request.form['first_product']),
                           product_2=int(request.form['twice_product']), product_3=int(request.form['three_product']),
                           product_4=int(request.form['four_product']), product_5=int(request.form['five_product']),
                           product_6=int(request.form['six_product']), product_7=int(request.form['seven_product']),
                           product_8=int(request.form['eight_product']), product_9=int(request.form['nine_product']),
                           product_10=int(request.form['ten_product']), product_11=int(request.form['eleven_product']),
                           product_12=int(request.form['twelve_product']),
                           product_13=int(request.form['thirteen_product']),
                           product_14=int(request.form['fourteen_product']),
                           product_15=int(request.form['fifteen_product']),
                           product_16=int(request.form['sixteen_product']),
                           product_17=int(request.form['seventeen_product']),
                           product_18=int(request.form['eighteen_product']),
                           product_19=int(request.form['nineteen_product']),
                           product_20=int(request.form['twenty_product']),
                           product_21=int(request.form['twenty_one_product']),
                           product_22=int(request.form['twenty_two_product']), title='Продуктовая корзина',
                           surname=current_user[0], name=current_user[1], shop=current_user[2])


@app.route('/feedback', methods=['GET', 'POST'])
def comment():
    product = requests.get('http://localhost:5000/api/products').json()
    time_product = requests.get('http://localhost:5000/api/temporary').json()
    db_session.global_init('db/product.db')
    session = db_session.create_session()
    query = session.query(Products).all()
    counter = 0
    for item in query:
        number = item.id
        if product['product'][number - 1]['quantity'] > time_product['product_time'][number - 1]['quantity'] > 0:
            item.quantity = item.quantity - time_product['product_time'][number - 1]['quantity']
            counter += time_product['product_time'][number - 1]['quantity']
    session.commit()
    current_user[2] = counter
    return render_template('feedback.html', userful_information=time_product, title='Оставить отзыв')


def main():
    db_session.global_init('db/product.db')
    app.run()


if __name__ == '__main__':
    main()
