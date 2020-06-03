import mimetypes
import sqlite3


from os import path

from flask import (
    Flask,
    render_template,
    redirect,
    send_from_directory,
    jsonify,
    request,
    session,
    url_for,
)


def main():
    # The path to directory this code is ran in.
    CUR_PATH = path.dirname(path.abspath(__file__))

    # The IP to run server on.
    IP = "127.0.0.1"
    # The port on which server is hosted.
    PORT = 8000
    # !!! FUN !!! DEBUG MODE. Gives access to most stuff on server,
    # very dangerous to be put on production.
    DEBUG = False
    # Secret key used to encrypt requests and stuff.
    SECRET_KEY = ""

    # The directory with all web-related templates.
    template_dir = path.join(CUR_PATH, "../templates")
    # The directory for static files, such as .css, client-side JavaScript.
    static_dir = path.join(CUR_PATH, "../static")

    mimetypes.init()

    # So it's not system-dependant.
    mimetypes.add_type("text/css", ".css")
    mimetypes.add_type("text/javascript", ".js")
    mimetypes.add_type("text/html", ".html")

    CUR_PATH = path.dirname(path.abspath(__file__))
    database_path = path.join(CUR_PATH, "../database")
    orders_db_fn = "orders.db"
    orders_db_fp = path.join(database_path, orders_db_fn)

    app = Flask(__name__, template_folder=template_dir, static_url_path="")
    app.secret_key = SECRET_KEY

    @app.after_request
    def after_request(response):
        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=31536000; includeSubDomains"
        # response.headers['Content-Security-Policy'] = "default-src 'self'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        # response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/login")
    def rlogin():
        return render_template("login.html")

    @app.route("/order-page")
    def order():
        return render_template("order.html")


    @app.route("/registration")
    def registration():
        return render_template("registration.html")

    @app.route("/static/<path:file_path>")
    def send_static(file_path):
        file_mimetype = mimetypes.guess_type(file_path)[0]

        return send_from_directory(
            static_dir,
            file_path,
            mimetype=file_mimetype
        )

    @app.route("/api/v1/order/list", methods=["GET", "POST"])
    def orders_list():
        with sqlite3.connect(orders_db_fp) as con:
            cur = con.cursor()
            orders = cur.execute("SELECT * FROM orders")
            return (str(jsonify(orders)))

    @app.route("/api/v1/order/make_order", methods=["GET", "POST"])
    def make_order():
        order_db = sqlite3.connect(orders_db_fp)
        desc = request.args.get('description')
        cn = request.args.get('company_name')
        mb = request.args.get('min_budget')
        if desc is None or len(desc) == 0:
            desc = "NULL"
        sql = '''
        INSERT INTO orders
        (company_name, min_budget, max_budget, media_ad_type, outdoor_ad_type, product_placement_ad_type, tv_ad_type, radio_ad_type, description_ad_type)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        task = (
            request.args.get('company_name'),
            request.args.get('min_budget'),
            request.args.get('max_budget'),
            request.args.get('media'),
            request.args.get('outdoor'),
            request.args.get('product_placement'),
            request.args.get('tv'),
            request.args.get('radio'),
            desc
        )
        order_db_cursor = order_db.cursor()
        order_db_cursor.execute(sql, task)
        order_db.commit()

        return jsonify({"data": "Everything is fine"})


    print("=====\n" + "Server starting on " + str(IP) + ":" + str(PORT))

    # !!! NB !!! PLEASE SET UP PROPER SSL CERTIFICATE SIGNING.
    app.run(host=IP, port=PORT, debug=DEBUG)

if __name__ == "__main__":
    main()
