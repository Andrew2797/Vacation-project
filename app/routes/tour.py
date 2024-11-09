from uuid import uuid4
import random

from flask import Blueprint, render_template, redirect, url_for, request

from app.db import Tour, Session

tour_blueprint = Blueprint("tours", __name__)


@tour_blueprint.get("/")
def index():
    with Session() as session:
        tours = session.query(Tour).filter_by(is_reserved=False).all()
        random.shuffle(tours)
        return render_template("index.html", tours=tours)


@tour_blueprint.route("/add_tour/", methods=["GET", "POST"])
def add_tour():
    with Session() as session:
        if request.method == "POST":
            itinerary = request.form.get("itinerary")
            price = request.form.get("price")
            duration = request.form.get("duration")
            img_url = None
            img_name_orig = None
            img_name = None

            photo = request.files.get("photo")
            if photo and photo.filename:
                img_name_orig = photo.filename
                img_name = uuid4().hex + "." + img_name_orig.split(".")[-1]
                img_url = f"/static/img/{img_name}"
                photo.save("app" + img_url)

            tour = Tour(
                itinerary=itinerary,
                duration=duration,
                price=price,
                img_name=img_name,
                img_name_orig=img_name_orig,
                img_url=img_url
            )
            session.add(tour)
            session.commit()
            return redirect(url_for("tours.manage_tours"))

        return render_template("add_tour.html")


@tour_blueprint.get("/manage_tours/")
def manage_tours():
    with Session() as session:
        tours = session.query(Tour).all()
        return render_template("manage_tours.html", tours=tours)


@tour_blueprint.get("/delete/<int:id>/")
def delete_tour(id):
    with Session() as session:
        tour = session.query(tour).filter_by(id=id).first()
        session.delete(tour)
        session.commit()
        return redirect(url_for("tour.manage_tours"))


@tour_blueprint.route("/edit_tour/<int:id>/", methods=["GET", "POST"])
def edit_tour(id):
    with Session() as session:
        tour = session.query(tour).filter_by(id=id).first()

        if request.method == "POST":
            tour.itinerary = request.form.get("itinerary")
            tour.duration = request.form.get("duration")
            tour.price = request.form.get("price")
            tour.is_reserved = True if request.form.get("is_reserved") else False

            photo = request.files.get("photo")
            if photo and photo.filename:
                tour.img_name_orig = photo.filename
                tour.img_name = uuid4().hex + "." + photo.filename.split(".")[-1]
                tour.img_url = "/static/img/" + tour.img_name
                photo.save("/app" + tour.img_url)

            session.commit()
            return redirect(url_for("tours.manage_tours"))

        return render_template("edit_tour.html", tour=tour)


@tour_blueprint.get("/reserve/<int:id>/")
def reserve(id):
    with Session() as session:
        tour = session.query(Tour).filter_by(id=id).first()
        tour.is_reserved = True
        session.commit()
        return render_template("reserved.html", tour=tour)