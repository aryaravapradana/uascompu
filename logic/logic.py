def get_target_distance(age, gender):
    if gender == 'pria':
        if age < 25: return 1600
        elif age < 35: return 1500
        elif age < 45: return 1350
        elif age < 55: return 1200
        elif age < 65: return 1000
        else: return 800
    else:
        if age < 25: return 1400
        elif age < 35: return 1300
        elif age < 45: return 1150
        elif age < 55: return 1000
        elif age < 65: return 800
        else: return 650

def evaluate_performance(target, actual, age):
    selisih = target - actual
    if age >= 60:
        if selisih > 400: return 4
        elif selisih > 300: return 3
        elif selisih > 150: return 2
        else: return 1
    else:
        if selisih > 600: return 4
        elif selisih > 400: return 3
        elif selisih > 200: return 2
        else: return 1

def ask_yes_no(question):
    while True:
        answer = input(question + " (ya/tidak): ").strip().lower()
        if answer in ['ya', 'tidak']:
            return answer == 'ya'
        print("Jawab dengan 'ya' atau 'tidak'.")

def ask_number(question, min_val=0, max_val=999):
    while True:
        try:
            value = float(input(question + ": ").strip())
            if min_val <= value <= max_val:
                return value
            print(f"Masukkan angka antara {min_val} dan {max_val}")
        except:
            print("Masukkan angka yang valid.")

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return weight / (height_m ** 2)

def evaluate_numeric_risk(age, gender, bmi, hr_rest, hr_walk, bp_sys, bp_dia, exercise_freq):
    risk = {
        "aritmia": 0,
        "gagal jantung": 0,
        "fibrilasi atrium": 0,
        "penyakit jantung koroner": 0,
        "serangan jantung": 0,
        "hipertensi pulmonal": 0,
        "penyakit arteri perifer": 0,
        "stroke": 0
    }
    if hr_rest > 100:
        risk["aritmia"] += 15
        risk["fibrilasi atrium"] += 10
    if hr_walk > 120:
        risk["gagal jantung"] += 10
    if bmi >= 30:
        risk["gagal jantung"] += 10
        risk["penyakit arteri perifer"] += 10
        risk["penyakit jantung koroner"] += 10
        risk["stroke"] += 10
    if bp_sys >= 140 or bp_dia >= 90:
        risk["hipertensi pulmonal"] += 15
        risk["serangan jantung"] += 10
    if exercise_freq < 1:
        risk["penyakit arteri perifer"] += 10
        risk["penyakit jantung koroner"] += 5
    return risk

def evaluate_total_risk(tingkat_parah, abnormal_hr, ya_tidak_answers, numeric_risk):
    base_risk = {
        "aritmia": 5 + tingkat_parah * 3,
        "kardiomiopati": 5 + tingkat_parah * 3,
        "penyakit jantung koroner": 5 + tingkat_parah * 3,
        "gagal jantung": 5 + tingkat_parah * 3,
        "serangan jantung": 5 + tingkat_parah * 3,
        "hipertensi pulmonal": 5 + tingkat_parah * 3,
        "penyakit katup jantung": 5 + tingkat_parah * 3,
        "endokarditis": 5 + tingkat_parah * 3,
        "perikarditis": 5 + tingkat_parah * 3,
        "penyakit arteri perifer": 5 + tingkat_parah * 3,
        "fibrilasi atrium": 5 + tingkat_parah * 3,
        "blok jantung": 5 + tingkat_parah * 3,
        "stroke": 5 + tingkat_parah * 3
    }

    # Risiko berbasis detak jantung abnormal setelah jogging
    if abnormal_hr:
        base_risk["aritmia"] += 10
        base_risk["gagal jantung"] += 5

    # Tambahan pertanyaan ya/tidak (25 total)
    pertanyaan_penyakit = {
        "riwayat_keluarga": ["penyakit jantung koroner", "serangan jantung", "fibrilasi atrium"],
        "nyeri_dada": ["penyakit jantung koroner", "serangan jantung"],
        "sesak_napas": ["gagal jantung", "hipertensi pulmonal"],
        "pingsan": ["aritmia", "blok jantung"],
        "tekanan_darah_tinggi": ["hipertensi pulmonal", "gagal jantung"],
        "diabetes": ["penyakit jantung koroner", "serangan jantung"],
        "merokok": ["penyakit arteri perifer", "penyakit jantung koroner"],
        "alkohol": ["kardiomiopati"],
        "jantung_berdebar": ["aritmia", "fibrilasi atrium"],
        "bengkak_kaki": ["gagal jantung", "perikarditis"],
        "sering_lelah": ["gagal jantung", "kardiomiopati"],
        "kolesterol_tinggi": ["penyakit jantung koroner"],
        "jarang_olahraga": ["penyakit arteri perifer"],
        "stres_berlebihan": ["aritmia", "serangan jantung"],
        "sulit_tidur": ["fibrilasi atrium"],
        "pusing_saat_berdiri": ["blok jantung"],
        "keringat_tanpa_aktivitas": ["serangan jantung"],
        "sleep_apnea": ["gagal jantung"],
        "autoimun": ["perikarditis", "endokarditis"],
        "tiroid": ["aritmia"],
        "kesemutan": ["penyakit arteri perifer"],
        "sakit_kepala": ["hipertensi pulmonal"],
        "junkfood": ["penyakit jantung koroner"],
        "tinggi_gula": ["kardiomiopati"],
    }

    for key, penyakit_list in pertanyaan_penyakit.items():
        if ya_tidak_answers.get(key, False):
            for p in penyakit_list:
                base_risk[p] += 5

    # Tambahkan risiko numerik
    for k, v in numeric_risk.items():
        if k in base_risk:
            base_risk[k] += v

    for k in base_risk:
        base_risk[k] = min(base_risk[k], 100)

    return base_risk

# === MAIN PROGRAM ===
print("=== Evaluasi Risiko Penyakit Kardiovaskular ===")
umur = int(input("Berapa umur Anda? "))
gender = input("Apa gender Anda? (pria/wanita): ").strip().lower()

# Nilai-nilai numerik
berat = ask_number("Berapa berat badan Anda (kg)?", 30, 200)
tinggi = ask_number("Berapa tinggi badan Anda (cm)?", 100, 250)
hr_rest = ask_number("Berapa detak jantung saat istirahat Anda (bpm)?", 30, 200)
hr_walk = ask_number("Berapa detak jantung saat berjalan santai (bpm)?", 30, 200)
bp_sys = ask_number("Berapa tekanan darah sistolik Anda?", 80, 250)
bp_dia = ask_number("Berapa tekanan darah diastolik Anda?", 40, 150)
exercise_freq = ask_number("Berapa kali Anda olahraga per minggu?", 0, 14)

bmi = calculate_bmi(berat, tinggi)
numeric_risk = evaluate_numeric_risk(umur, gender, bmi, hr_rest, hr_walk, bp_sys, bp_dia, exercise_freq)

# Evaluasi jogging
jarak_target = get_target_distance(umur, gender)
print(f"Target jogging Anda: {jarak_target} meter")
berhasil = ask_yes_no("Apakah Anda berhasil mencapai target jogging?")
if not berhasil:
    jarak_tempuh = ask_number("Berapa meter Anda tempuh sebelum menyerah?", 0, jarak_target)
    tingkat_parah = evaluate_performance(jarak_target, jarak_tempuh, umur)
    abnormal_hr = False
else:
    hr_jog = ask_number("Berapa detak jantung setelah jogging (bpm)?", 50, 220)
    abnormal_hr = hr_jog > 170
    tingkat_parah = 1 if not abnormal_hr else 3

# Pertanyaan ya/tidak (25 total)
pertanyaan_terperinci = {
    "riwayat_keluarga": "Apakah Anda memiliki anggota keluarga (ayah, ibu, saudara) yang pernah mengalami penyakit jantung atau serangan jantung?",
    "nyeri_dada": "Apakah Anda sering merasakan nyeri atau tekanan di bagian dada, terutama saat aktivitas?",
    "sesak_napas": "Apakah Anda mudah sesak napas bahkan saat melakukan aktivitas ringan seperti naik tangga atau berjalan?",
    "pingsan": "Apakah Anda pernah mengalami pingsan atau hampir pingsan tanpa sebab yang jelas?",
    "tekanan_darah_tinggi": "Apakah Anda pernah didiagnosis memiliki tekanan darah tinggi oleh dokter?",
    "diabetes": "Apakah Anda pernah didiagnosis menderita diabetes (gula darah tinggi)?",
    "merokok": "Apakah Anda saat ini merokok atau memiliki riwayat merokok berat?",
    "alkohol": "Apakah Anda rutin mengonsumsi alkohol dalam jumlah sedang hingga berat?",
    "jantung_berdebar": "Apakah Anda sering merasakan jantung berdebar cepat, tidak beraturan, atau terasa 'loncat'?",
    "bengkak_kaki": "Apakah Anda sering mengalami pembengkakan pada kaki, pergelangan, atau perut?",
    "sering_lelah": "Apakah Anda merasa mudah lelah meskipun sudah cukup istirahat?",
    "kolesterol_tinggi": "Apakah Anda pernah didiagnosis memiliki kolesterol tinggi?",
    "jarang_olahraga": "Apakah Anda jarang atau hampir tidak pernah berolahraga dalam seminggu?",
    "stres_berlebihan": "Apakah Anda merasa stres berat atau cemas secara terus-menerus dalam kehidupan sehari-hari?",
    "sulit_tidur": "Apakah Anda sering mengalami kesulitan tidur nyenyak atau sering terbangun di malam hari?",
    "pusing_saat_berdiri": "Apakah Anda sering merasa pusing atau limbung saat bangun dari duduk atau berbaring?",
    "keringat_tanpa_aktivitas": "Apakah Anda sering berkeringat berlebihan tanpa melakukan aktivitas berat?",
    "sleep_apnea": "Apakah Anda sering mendengkur keras dan berhenti bernapas sesaat saat tidur (sleep apnea)?",
    "autoimun": "Apakah Anda memiliki penyakit autoimun seperti lupus atau rheumatoid arthritis?",
    "tiroid": "Apakah Anda memiliki gangguan tiroid seperti hipertiroid atau hipotiroid?",
    "kesemutan": "Apakah Anda sering merasakan kesemutan atau mati rasa pada kaki atau tangan Anda?",
    "sakit_kepala": "Apakah Anda sering mengalami sakit kepala yang cukup berat, terutama jika disertai tekanan darah tinggi?",
    "junkfood": "Apakah Anda sering mengonsumsi makanan cepat saji, gorengan, atau makanan tinggi lemak trans?",
    "tinggi_gula": "Apakah hasil tes gula darah Anda sering menunjukkan kadar yang tinggi?"
}

# Ganti bagian ini dalam program utama:
yt_keys = list(pertanyaan_terperinci.keys())
yt_answers = {}
print("\nJawab dengan ya/tidak:")
for key in yt_keys:
    pertanyaan = pertanyaan_terperinci[key]
    yt_answers[key] = ask_yes_no(pertanyaan)


# Hitung total risiko
hasil = evaluate_total_risk(tingkat_parah, abnormal_hr, yt_answers, numeric_risk)

# Tampilkan hasil
print("\n=== Hasil Evaluasi Analisis Anda ===")
for penyakit, persen in sorted(hasil.items(), key=lambda x: x[1], reverse=True):
    print(f"{penyakit.capitalize()}: {persen}% risiko")

tertinggi = max(hasil.values())
if tertinggi >= 50:
    print("\n⚠️ Mempunyai Resiko tinggi. Segera berkonsultasi dengan spesialis jantung.")
elif tertinggi >= 30:
    print("\n⚠️ Mmempunyai Resiko sedang. Lakukan pemeriksaan lanjutan bila diperlukan.")
else:
    print("\n✅ Mempunyai Resiko rendah. Pertahankan gaya hidup sehat.")
