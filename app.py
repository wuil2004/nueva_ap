from flask import Flask, render_template, jsonify, url_for
import nbformat
import os
import re
from graphviz import Source
import base64

app = Flask(__name__)

# Directorio donde se encuentran los notebooks
NOTEBOOKS_DIR = "notebooks"
STATIC_IMAGES_DIR = "static/images"

# Lista de notebooks disponibles
notebooks = ["Arboles.ipynb","Proyec_regresion.ipynb"]

def extract_graphs_and_accuracy_from_notebook(notebook_path):
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_content = nbformat.read(f, as_version=4)

        graphs = []
        accuracy = None

        for cell in notebook_content['cells']:
            # Extraer gráficos en formato base64
            if cell['cell_type'] == 'code' and 'outputs' in cell:
                for output in cell['outputs']:
                    if 'data' in output and 'image/png' in output['data']:
                        graphs.append(output['data']['image/png'])
                    # Buscar precisión en las salidas de texto
                    if 'text' in output:
                        if isinstance(output['text'], list):
                            output_text = "".join(output['text'])
                        else:
                            output_text = output['text']
                        match = re.search(r"Precisión del modelo:\s*([\d.]+)", output_text)
                        if match:
                            accuracy = float(match.group(1))

            # Procesar celdas que generen archivos .dot (graphviz)
            if cell['cell_type'] == 'code' and 'source' in cell:
                code = cell['source']
                match = re.search(r"Source\.from_file\(['\"](.+?\.dot)['\"]\)", code)
                if match:
                    dot_file = os.path.join(os.path.dirname(notebook_path), match.group(1))
                    if os.path.exists(dot_file):
                        # Renderizar el archivo .dot a PNG
                        graph = Source.from_file(dot_file)
                        png_path = dot_file.replace(".dot", ".png")
                        graph.render(filename=dot_file.replace(".dot", ""), format="png", cleanup=True)

                        # Leer el archivo PNG y convertirlo a base64
                        if os.path.exists(png_path):
                            with open(png_path, "rb") as img_file:
                                graphs.append(base64.b64encode(img_file.read()).decode('utf-8'))
        return graphs, accuracy
    except Exception as e:
        print(f"Error al procesar el notebook: {str(e)}")
        return [], None

@app.route('/')
def index():
    return render_template('index.html', notebooks=notebooks)

@app.route('/notebook/<notebook_name>')
def show_graphs_and_accuracy(notebook_name):
    notebook_path = os.path.join(NOTEBOOKS_DIR, notebook_name)

    if not os.path.exists(notebook_path):
        return jsonify({"error": f"Notebook {notebook_name} no encontrado en {NOTEBOOKS_DIR}"}), 404

    graphs, accuracy = extract_graphs_and_accuracy_from_notebook(notebook_path)

    # Agregar la imagen PNG manualmente
    static_image_path = url_for('static', filename=f'images/android_malware.png')

    return render_template(
        'graphs.html',
        graphs=graphs,
        accuracy=accuracy,
        notebook_name=notebook_name,
        static_image=static_image_path
    )

if __name__ == '__main__':
    # Obtiene el puerto del entorno, si no está definido usa el 5000 como fallback.
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port, host='0.0.0.0')  # Usa host '0.0.0.0' para aceptar conexiones externas.
