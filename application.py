#Vesion 1.0

# from flask import Flask, render_template, request
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
#
# app = Flask(__name__)
#
# engine = create_engine("postgresql://postgres:blmppes101010@localhost:5432/postgres")
# db = scoped_session(sessionmaker(bind=engine))
#
# @app.route('/')
# def index():
#     flights = db.execute("SELECT * FROM flights").fetchall()
#     return render_template("index.html", flights=flights)
#
# @app.route('/book', methods=["POST"])
# def book():
#     name = request.form.get("name")
#     try:
#         flight_id = int(request.form.get("flight_id"))
#     except ValueError:
#         return render_template("error.html", message="Flight id is invalid!")
#
#     if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
#         return render_template("error.html", message="No flight!")
#     db.execute("INSERT INTO passengers (name, flight_id) VALUES (:name, :flight_id)",
#             {"name": name, "flight_id" : flight_id})
#     db.commit()
#     return render_template("success.html")
#
# @app.route("/flights")
# def flights():
#     flights = db.execute("SELECT * FROM flights").fetchall()
#     return render_template("flights.html", flights=flights)
#
# @app.route("/flights/<int:flight_id>")
# def flight(flight_id):
#     flight = db.execute("SELECT * FROM flights WHERE id= :id", {"id" : flight_id}).fetchone()
#     if flight is None:
#         return render_template("error.html", message="Flight not found")
#
#     passengers = db.execute("SELECT name FROM passengers WHERE flight_id = :flight_id",
#                 {"flight_id": flight_id}).fetchall()
#     return render_template("flight.html", flight=flight, passengers=passengers)
#
# if __name__ == '__main__':
#     app.run()

#Version 2

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:blmppes101010@localhost:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route('/')
def index():
    flights = Flight.query.all()
    return render_template("index.html", flights=flights)

@app.route('/book', methods=["POST"])
def book():
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Flight id is invalid!")

    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.html", message="No flight!")

    flight.add_passenger(name)
    return render_template("success.html", message="You have successfully booked a flight!", 
@app.route("/flights")
def flights():
    flights = Flight.query.all()
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.html", message="Flight not found 404 error")

    passengers = flight.passengers
    return render_template("flight.html", flight=flight, passengers=passengers)

@app.route("/flights/add", methods=["GET", "POST"])
def add_flight():
    origin = request.form.get("origin")
    destination = request.form.get("destination")
    duration = request.form.get("duration")

    if(request.method == "POST"):
        try:
            f = Flight(origin=origin, destination=destination, duration=duration)
            db.session.add(f)
            db.session.commit()

            return render_template("success.html", message="You have successfully added a flight!")
        except:
            return render_template("error.html", message="There was an error!")
    return render_template("add_flight.html")

@app.route("/delete", methods=["GET", "POST"])
def delete_flight():
    id = request.form.get("id")

    try:
        if(request.method == "POST"):
            f = Flight.query.get(id)
            ps = f.passengers
            for p in ps:
                db.session.delete(p)
            db.session.delete(f)
            db.session.commit()

            return render_template("success.html", message="You have successfully deleted a flight!")
    except:
        return render_template("error.html", message="There was an error!")

    return render_template("delete_flight.html")

@app.route("/api/flights/<int:flight_id>", methods=["GET", "POST"])
def flight_api(flight_id):
    flight = Flight.query.get(flight_id)

    if(flight is None):
        return jsonify( {"error" : "Invalid flight's id"} ), 422

    passengers = flight.passengers
    names = []
    for p in passengers:
        names.append(p.name)

    return jsonify({
        "origin": flight.origin,
        "destination": flight.destination,
        "duration": flight.duration,
        "passengers": names
    })

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', message="404 Page not found!",  404
if __name__ == '__main__':
    app.run()
