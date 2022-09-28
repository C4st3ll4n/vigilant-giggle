from flask import Blueprint, render_template, session, redirect, request, flash, url_for
from flask_login import current_user

import forms
from api.book_client import BookClient

from api.order_client import OrderClient
from api.user_client import UserClient

blueprint = Blueprint("frontend", __name__)


@blueprint.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        session["order"] = OrderClient.get_order_from_session()

    try:
        books = BookClient.get_books()
    except:
        books = {
            "result": []
        }

    return render_template("index.html", books=books)


@blueprint.route("/book/<slug>", methods=["GET", "POST"])
def book_detials(slug):
    book = BookClient.get_book(slug)

    form = forms.ItemForm(book_id=book["id"])
    if request.method == "POST":
        if 'user' not in session:
            flash("Please login")
            return redirect(url_for('frontend.login'))

        order = OrderClient.add_to_cart(book_id=book['id'], )
        print(order)
        session['order'] = order
        flash("Book added to the cart")

    return render_template("book_info.html", book=book, form=form)


@blueprint.route("/register", methods=["POST", "GET"])
def register():
    form = forms.RegistrationForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data

            if UserClient.user_exists(username):
                flash("Please try another username")
                return render_template("register.html", form=form)
            else:
                user = UserClient.create_user(form)
                if user:
                    flash("Registered. Please login.")
                    return redirect(url_for('frontend.login'))
                else:
                    flash("Fail to register")

        else:
            flash("Errors")

    return render_template("register.html", form=form)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            api_key = UserClient.login(form)
            print(api_key)
            if api_key:
                session["user_api_key"] = api_key
                session["user"] = UserClient.get_user()
                order = OrderClient.get_order()
                if order:
                    print(order)
                    session['order'] = order
                flash("Welcome back !")
                return redirect(url_for('frontend.login'))
            else:
                flash("Cannot loggin")
        else:
            flash("Cannot loggin")

    return render_template("login.html", form=form)


@blueprint.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for("frontend.index"))


@blueprint.context_processor
def cart_count():
    count = 0
    order = session.get("order")
    if order and order.get("order_itens"):
        for i in order.get("order_itens"):
            count += i['quantity']
    return {'cart_items': count}


@blueprint.route("/checkout", methods=["GET"])
def checkout():
    if 'user' not in session:
        flash("Please login !")
        return redirect(url_for("frontend.login"))

    if 'order' not in session:
        flash("Cart is empty !")
        return redirect(url_for("frontend.index"))

    order = OrderClient.get_order()

    if len(order['order_itens']) == 0:
        flash("Cart is empty !")
        return redirect(url_for("frontend.index"))

    OrderClient.checkout()
    return redirect(url_for("frontend.thank_you"))


@blueprint.route("/thank-you", methods=["GET"])
def thank_you():
    if 'user' not in session:
        flash("Please login !")
        return redirect(url_for("frontend.login"))

    if 'order' not in session:
        flash("Cart is empty !")
        return redirect(url_for("frontend.index"))

    session.pop("order")
    flash("Processing order")
    return render_template("thankyou.html")
