from flask import Flask, render_template, request
from logic import (
    get_target_distance, evaluate_performance, calculate_bmi,
    evaluate_numeric_risk, evaluate_total_risk
)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # echo kembali apa yang dikirim form
    umur = int(request.form.get('umur'))
    gender = request.form.get('gender')
    berat = float(request.form.get('berat'))
    tinggi = float(request.form.get('tinggi'))
    hr_rest = float(request.form.get('hr_rest'))
    hr_walk = float(request.form.get('hr_walk'))
    bp_sys = float(request.form.get('bp_sys'))
    bp_dia = float(request.form.get('bp_dia'))
    exercise_freq = float(request.form.get('exercise_freq'))
    text = request.form.get('test_input', 'NO DATA')
    return f"Received: {text}"

if __name__ == '__main__':
    app.run(debug=True)


