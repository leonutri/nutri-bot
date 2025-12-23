import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configura a IA com a chave que vamos colocar no Coolify depois
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "Servidor do Nutri-Bot Ativo!"

@app.route('/analisar', methods=['POST'])
def analisar():
    dados = request.json
    tipo = dados.get('tipo') # exame, refeicao ou receita
    conteudo = dados.get('conteudo') # URL da imagem ou texto
    
    prompts = {
        "exame": "Aja como Nutricionista. Leia este exame e liste valores alterados de Glicose, Ferritina e Vitamina D.",
        "refeicao": "Analise a foto. Estime calorias e macros (Proteína, Carbo, Gordura) deste prato.",
        "receita": "Sugira uma receita saudável usando estes ingredientes."
    }
    
    try:
        response = model.generate_content([prompts.get(tipo, "Analise:"), conteudo])
        return jsonify({"resultado": response.text})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
