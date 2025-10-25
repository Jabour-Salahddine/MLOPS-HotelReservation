import joblib
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash
from config.paths import MODEL_TRAINED_PATH

# ==============================
#  Initialisation de l'app Flask
# ==============================
app = Flask(__name__)


# ==============================
#  Chargement du modèle ML
# ==============================
try:
    loaded_model = joblib.load(MODEL_TRAINED_PATH)
    print(" Modèle chargé avec succès.")
except Exception as e:
    print(" Erreur lors du chargement du modèle :", e)
    loaded_model = None


# ==============================
#  Page principale (Formulaire + Résultat)
# ==============================
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":
        try:
            #  Récupération et conversion des données du formulaire
            features = np.array([[
                int(request.form["lead_time"]),
                int(request.form["no_of_special_request"]),
                float(request.form["avg_price_per_room"]),
                int(request.form["arrival_month"]),
                int(request.form["arrival_date"]),
                int(request.form["market_segment_type"]),
                int(request.form["no_of_week_nights"]),
                int(request.form["no_of_weekend_nights"]),
                int(request.form["type_of_meal_plan"]),
                int(request.form["room_type_reserved"])
            ]])

            #  Prédiction
            if loaded_model is None:
                flash("Le modèle n’a pas pu être chargé.", "danger")
            else:
                prediction = int(loaded_model.predict(features)[0])

        except Exception as e:
            flash(f"Erreur lors de la prédiction : {e}", "danger")

    #  Rendu de la page
    return render_template("index.html", prediction=prediction)


# ==============================
#  Page d'erreur personnalisée
# ==============================
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


# ==============================
#  Lancement de l’application
# ==============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
