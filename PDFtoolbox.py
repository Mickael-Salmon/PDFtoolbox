from flask import Flask, request, send_file
from PyPDF2 import PdfMerger
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("pdf_files")

        # Vérifie si des fichiers ont été téléchargés
        if uploaded_files[0].filename == '':
            return 'Aucun fichier sélectionné', 400

        merger = PdfMerger()

        # Chemin où les fichiers PDF intermédiaires seront stockés
        tmp_folder = 'tmp_pdfs'
        os.makedirs(tmp_folder, exist_ok=True)

        for file in uploaded_files:
            filename = secure_filename(file.filename)
            filepath = os.path.join(tmp_folder, filename)
            file.save(filepath)
            merger.append(filepath)

        # Fusionner les fichiers PDF
        output_pdf_path = os.path.join(tmp_folder, 'merged.pdf')
        merger.write(output_pdf_path)
        merger.close()

        # Envoie le fichier PDF fusionné
        return send_file(output_pdf_path, as_attachment=True)

    return '''
    <!doctype html>
    <title>Fusionneur de PDF</title>
    <h1>Fusionneur de PDF</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=pdf_files multiple>
      <input type=submit value=Fusionner>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
