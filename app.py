from flask import Flask, render_template, request
from logic.logic import (
    targetjarak, selisihjarak, bminormal,
    hitungresiko, totalresiko
)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    target = None
    if request.method == 'POST':
        umur = int(request.form.get('umur'))
        gender = request.form.get('gender')
        target = targetjarak(umur, gender)
    return render_template('index.html', target=target)


@app.route('/result', methods=['POST'])
def result():
    # Ambil data dari form
    umur = int(request.form.get('umur'))
    gender = request.form.get('gender')
    berat = float(request.form.get('berat'))
    tinggi = float(request.form.get('tinggi'))
    hr_rest = float(request.form.get('hr_rest'))
    hr_walk = float(request.form.get('hr_walk'))
    bp_sys = float(request.form.get('bp_sys'))
    bp_dia = float(request.form.get('bp_dia'))
    exercise_freq = float(request.form.get('exercise_freq'))
    jog_yes = request.form.get('jog_yes')
    jarak_tempuh = float(request.form.get('jarak_tempuh') or 0)
    hr_jog = float(request.form.get('hr_jog') or 0)

    # Hitung BMI dan target jogging
    bmi = bminormal(berat, tinggi)
    target = targetjarak(umur, gender)

    # Hitung tingkat parah & HR abnormal
    if jog_yes == 'tidak':
        tingkat_parah = selisihjarak(target, jarak_tempuh, umur)
        abnormal_hr = False
    else:
        abnormal_hr = hr_jog > 170
        tingkat_parah = 3 if abnormal_hr else 1

    # Ambil jawaban checkbox
    pertanyaan_keys = [
        'riwayat_keluarga', 'nyeri_dada', 'sesak_napas', 'pingsan', 'tekanan_darah_tinggi',
        'diabetes', 'merokok', 'alkohol', 'jantung_berdebar', 'bengkak_kaki',
        'sering_lelah', 'kolesterol_tinggi', 'jarang_olahraga', 'stres_berlebihan', 'sulit_tidur',
        'pusing_saat_berdiri', 'keringat_tanpa_aktivitas', 'sleep_apnea', 'autoimun', 'tiroid',
        'kesemutan', 'sakit_kepala', 'junkfood', 'tinggi_gula'
    ]
    yt_answers = {key: (key in request.form) for key in pertanyaan_keys}

    # Hitung risiko numerik & total
    numeric_risk = hitungresiko(umur, gender, bmi, hr_rest, hr_walk, bp_sys, bp_dia, exercise_freq)
    hasil = totalresiko(tingkat_parah, abnormal_hr, yt_answers, numeric_risk)
    hasil_terurut = sorted(hasil.items(), key=lambda x: x[1], reverse=True)

    return render_template(
        'result.html',
        umur=umur,
        gender=gender,
        bmi=bmi,
        target=target,
        tingkat_parah=tingkat_parah,
        abnormal_hr=abnormal_hr,
        hasil=hasil_terurut
    )

if __name__ == '__main__':
    app.run(debug=True)