from flask import Flask, request, jsonify
from src.lexer import LexerInterpreter

app = Flask(__name__)

@app.route('/tokenize', methods=['POST'])
def tokenize():
    # Pega o texto enviado na requisição
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing "text" field in the request'}), 400

    text = data['text']
    lexer = LexerInterpreter(text)

    # Gera a lista de tokens
    tokens = lexer.get_next_token()

    # Formata os tokens como uma lista de dicionários
    tokens_list = [{'type': token[0], 'value': token[1]} for token in tokens]
    
    return jsonify(tokens_list)


if __name__ == '__main__':
    app.run(debug=True)
