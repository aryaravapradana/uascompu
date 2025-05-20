from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # echo kembali apa yang dikirim form
    text = request.form.get('test_input', 'NO DATA')
    return f"Received: {text}"

if __name__ == '__main__':
    app.run(debug=True)

# testing 
