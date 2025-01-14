from flask import Flask, render_template, jsonify
import nbformat
import os

app = Flask(__name__)

# Directorio donde se encuentran los notebooks
NOTEBOOKS_DIR = "notebooks"

# Lista de notebooks disponibles
notebooks = ["Arboles.ipynb", "Pandas.ipynb", "Proyecto.ipynb", "Regresion_Lineal.ipynb"]

def extract_graphs_from_notebook(notebook_path):
    """
    Extrae gráficos en formato base64 de un notebook Jupyter.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = nbformat.read(f, as_version=4)
        
        graphs = []
        for cell in notebook_content['cells']:
            if cell['cell_type'] == 'code' and 'outputs' in cell:
                for output in cell['outputs']:
                    if 'data' in output and 'image/png' in output['data']:
                        graphs.append(output['data']['image/png'])
        
        return graphs
    except Exception as e:
        print(f"Error al procesar el notebook {notebook_path}: {str(e)}")
        return []

@app.route('/')
def index():
    """
    Página principal que lista los notebooks disponibles.
    """
    return render_template('index.html', notebooks=notebooks)

@app.route('/notebook/<notebook_name>')
def show_graphs(notebook_name):
    """
    Muestra las gráficas extraídas del notebook especificado.
    """
    notebook_path = os.path.join(NOTEBOOKS_DIR, notebook_name)
    
    if not os.path.exists(notebook_path):
        return jsonify({"error": f"Notebook {notebook_name} no encontrado"}), 404

    graphs = extract_graphs_from_notebook(notebook_path)
    if not graphs:
        return jsonify({"error": f"No se encontraron gráficos en {notebook_name}"}), 404

    return render_template('graphs.html', graphs=graphs, notebook_name=notebook_name)

if __name__ == '__main__':
    app.run(debug=True)
