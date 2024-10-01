from flask import Flask, request, jsonify

app = Flask(__name__)

times = []
campeonatos = []

@app.route('/')
def index():
    return "Seja bem-vindo!"

@app.route('/times', methods=['GET', 'POST'])
def handle_times():
    if request.method == 'GET':
        return jsonify(times)
    elif request.method == 'POST':
        time = request.json
        times.append(time)
        return jsonify({'message': 'Time adicionado com sucesso!'})

@app.route('/campeonatos', methods=['GET', 'POST'])
def handle_campeonatos():
    if request.method == 'GET':
        return jsonify(campeonatos)
    elif request.method == 'POST':
        campeonato = request.json
        campeonatos.append(campeonato)
        return jsonify({'message': 'Campeonato adicionado com sucesso!'})

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Página não encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port='9000')