from flask import Flask, render_template, jsonify
import nbformat
from nbconvert import HTMLExporter

app = Flask(__name__)

# Suponiendo que tienes una lista de notebooks
notebooks = ["Arboles.ipynb","Pandas.ipynb", "Proyecto.ipynb", "Matplotlib.ipynb", "Regresion_Lineal.ipynb", "Regrecion_logistica.ipynb", "RL_proyecto.ipynb", "Preparacion-del-DataSet.ipynb", "Support-Vector-Machine.ipynb", "Visualizacion-de-Datos.ipynb", "Evaluacion_de_Resultados.ipynb", "Creacion-de-transformadores-y-Pipelines-Personalizados.ipynb"]
# Función para cargar un notebook y convertirlo a HTML
def convert_notebook_to_html(notebook_path):
    try:
        # Leer el archivo del notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = nbformat.read(f, as_version=4)

        # Usar nbconvert para convertir el notebook a HTML
        html_exporter = HTMLExporter()
        body, resources = html_exporter.from_notebook_node(notebook_content)
        
        return body
    except Exception as e:
        print(f"Error al convertir el notebook {notebook_path}: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html', notebooks=notebooks)

@app.route('/notebook/<notebook_name>')
def view_notebook(notebook_name):
    # Aquí puedes elegir cómo obtener el archivo del notebook
    notebook_path = f"notebooks/{notebook_name}"

    try:
        # Convertir el notebook a HTML
        notebook_html = convert_notebook_to_html(notebook_path)
        return render_template('notebook_viewer.html', notebook_html=notebook_html)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
