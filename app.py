from flask import Flask, request, render_template, send_file
from main import creaGrafica
from io import BytesIO

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            # Leggo i dati dal form
            mesh = request.form["mesh"]
            titolo = request.form["titolo"]
            autore = request.form["autore"]
            testo = request.form["testo"]
            correggi = "correggi" in request.form 

            # Genera l'immagine
            img = creaGrafica(mesh, titolo, testo, autore, correggi)

            # Restituisce l'immagine direttamente come PNG
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return send_file(buffer, mimetype='image/png')

        except Exception as e:
            return f"<h2 style='color:red;'>Errore: {e}</h2><a href='/'>Torna indietro</a>"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

