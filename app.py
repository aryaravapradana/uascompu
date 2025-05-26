from flask import Flask, render_template, request
import sys
import os

# Tambahkan path ke folder 'logic' jika perlu (khususnya jika struktur kompleks)
# Jika logic.py ada di folder 'logic' sejajar dengan app.py, ini membantu
# sys.path.append(os.path.join(os.path.dirname(__file__), 'logic'))

try:
    from logic.logic import (
        targetjarak, selisihjarak, bminormal,
        hitungresiko, totalresiko
    )
    print(">>> [DEBUG] Berhasil mengimpor fungsi dari logic.py.")
except ImportError as e:
    print(f">>> [DEBUG] GAGAL mengimpor fungsi dari logic.py: {e}")
    print(">>> [DEBUG] Pastikan file 'logic/logic.py' ada dan tidak ada error di dalamnya.")
    # Definisikan fungsi dummy agar aplikasi tidak crash total
    def targetjarak(age, gender): return 9999 # Nilai dummy
    # Anda bisa menambahkan dummy lain jika perlu

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    target = None
    current_umur = None
    current_gender = None

    print("\n--- [DEBUG] Request ke / ---")
    print(f">>> [DEBUG] Metode Request: {request.method}")

    if request.method == 'POST':
        # Tampilkan SEMUA data form yang diterima
        print(f">>> [DEBUG] Data Form Diterima: {request.form}")

        # Ambil data DENGAN NAMA YANG SAMA PERSIS seperti di HTML
        umur_str = request.form.get('umur_target')
        gender = request.form.get('gender_target')

        print(f">>> [DEBUG] Mencoba baca: umur_target='{umur_str}', gender_target='{gender}'")

        # Cek apakah KEDUA nilai ada
        if umur_str and gender:
            try:
                umur = int(umur_str)
                # Panggil fungsi yang diimpor
                target = targetjarak(umur, gender)
                current_umur = umur
                current_gender = gender
                print(f">>> [DEBUG] Kalkulasi BERHASIL: Umur={umur}, Gender={gender}, Target={target}")
            except ValueError:
                print(f">>> [DEBUG] ERROR: Gagal konversi umur '{umur_str}' ke integer.")
                target = None # Set target ke None jika ada error
            except Exception as e:
                print(f">>> [DEBUG] ERROR saat memanggil targetjarak: {e}")
                target = None
        else:
            print(">>> [DEBUG] PERINGATAN: 'umur_target' atau 'gender_target' tidak ada di form POST.")
            target = None

    print(f">>> [DEBUG] Merender index.html dengan target={target}, umur={current_umur}, gender={current_gender}")
    print("--- [DEBUG] Selesai Request / ---\n")

    return render_template('index.html',
                           target=target,
                           umur=current_umur,
                           gender=current_gender)


@app.route('/result', methods=['POST'])
def result():
    print("\n--- [DEBUG] Request ke /result ---")
    print(f">>> [DEBUG] Data Form Diterima: {request.form}")

    # ... Kode /result Anda ...
    try:
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

        bmi = bminormal(berat, tinggi) if tinggi > 0 else 0
        target_value = targetjarak(umur, gender)

        if jog_yes == 'tidak':
            tingkat_parah = selisihjarak(target_value, jarak_tempuh, umur)
            abnormal_hr = False
        else:
            abnormal_hr = hr_jog > 170
            tingkat_parah = 3 if abnormal_hr else 1

        pertanyaan_keys = [
            'riwayat_keluarga', 'nyeri_dada', 'sesak_napas', 'pingsan', 'tekanan_darah_tinggi',
            'diabetes', 'merokok', 'alkohol', 'jantung_berdebar', 'bengkak_kaki',
            'sering_lelah', 'kolesterol_tinggi', 'jarang_olahraga', 'stres_berlebihan', 'sulit_tidur',
            'pusing_saat_berdiri', 'keringat_tanpa_aktivitas', 'sleep_apnea', 'autoimun', 'tiroid',
            'kesemutan', 'sakit_kepala', 'junkfood', 'tinggi_gula'
        ]
        yt_answers = {key: (key in request.form) for key in pertanyaan_keys}

        numeric_risk = hitungresiko(umur, gender, bmi, hr_rest, hr_walk, bp_sys, bp_dia, exercise_freq)
        hasil = totalresiko(tingkat_parah, abnormal_hr, yt_answers, numeric_risk)
        hasil_terurut = sorted(hasil.items(), key=lambda x: x[1], reverse=True)

        print(">>> [DEBUG] Merender result.html")
        return render_template(
            'result.html',
            umur=umur, gender=gender, bmi=bmi, target=target_value,
            tingkat_parah=tingkat_parah, abnormal_hr=abnormal_hr, hasil=hasil_terurut
        )
    except Exception as e:
        print(f">>> [DEBUG] ERROR di /result: {e}")
        return f"Terjadi error: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)