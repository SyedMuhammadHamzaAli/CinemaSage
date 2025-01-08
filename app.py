from flask import Flask, render_template, request
from LLMmodel import QAmodel

model = QAmodel()

app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    if request.method == 'POST':
        question = request.form['question']
        answer = model.invoke({'input': question})
        result = answer['answer']
        return result

if __name__ == '__main__':
    app.run(debug=True)
