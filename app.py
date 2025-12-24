import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configura a IA com a chave que você colocou no Coolify
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "Servidor do Nutri-Bot Ativo!"

# ESSA É A PARTE QUE O BOTPRESS VAI CHAMAR
@app.route('/gerar-plano', methods=['POST'])
def gerar_plano():
    dados = request.json
    user_id = dados.get('user_id') # Recebe o ID do aluno

    # Instrução para a IA criar o plano
    prompt = f"Você é um nutricionista e personal trainer experiente. " \
             f"Gere um plano de treino e dieta resumido para o aluno {user_id}. " \
             f"Seja motivador e profissional."

    response = model.generate_content(prompt)
    
    # Devolve o plano pronto para o Botpress
    return jsonify({"plano_gerado": response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
