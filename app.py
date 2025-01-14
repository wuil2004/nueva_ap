from flask import Flask, render_template, jsonify
import os
import nbformat
from nbconvert import HTMLExporter

app = Flask(__name__)

# Lista de notebooks
notebooks = [
    "Arboles.ipynb", "Pandas.ipynb", "Proyecto.ipynb", 
    "Matplotlib.ipynb", "Regresion_Lineal.ipynb", 
    "Regrecion_logistica.ipynb", "RL_proyecto.ipynb", 
    "Preparacion-del-DataSet.ipynb", "Support-Vector-Machine.ipynb", 
    "Visualizacion-de-Datos.ipynb", "Evaluacion_de_Resultados.ipynb", 
    "Creacion-de-transformadores-y-Pipelines-Personalizados.ipynb"
]

# Función para cargar un notebook y convertirlo a HTML mostrando solo las salidas
def convert_notebook_to_html_with_outputs(notebook_path):
    try:
        # Leer el archivo del notebook
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = nbformat.read(f, as_version=4)

        # Filtrar las celdas para que solo incluyan las salidas
        for cell in notebook_content['cells']:
            if cell['cell_type'] == 'code':
                # Vaciar el contenido del código
                cell['source'] = ''
        
        # Convertir el notebook a HTML
        html_exporter = HTMLExporter()
        body, resources = html_exporter.from_notebook_node(notebook_content)
        
        return body
    except Exception as e:
        print(f"Error al procesar el notebook {notebook_path}: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html', notebooks=notebooks)

@app.route('/notebook/<notebook_name>')
def view_notebook(notebook_name):
    notebook_path = f"notebooks/{notebook_name}"

    try:
        # Convertir el notebook a HTML mostrando solo las salidas
        notebook_html = convert_notebook_to_html_with_outputs(notebook_path)
        return render_template('notebook_viewer.html', notebook_html=notebook_html)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Lee el puerto desde las variables de entorno (para Render u otros servicios)
    port = int(os.environ.get("PORT", 5000))  # Usa el puerto 5000 como predeterminado
    app.run(debug=True, host='0.0.0.0', port=port)
