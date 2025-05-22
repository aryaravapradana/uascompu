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
        "stroke": 0,
        "cardiac arrest": 0
    }
    if hr_rest > 100:
        risk["aritmia"] += 15
        risk["fibrilasi atrium"] += 10
    if hr_walk > 120:
        risk["gagal jantung"] += 10
    if bmi >= 30:
        risk["gagal jantung"] += 10
        risk["penyakit arteri perifer"] += 10
        risk["penyakit jantung koroner"] += 2
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
        "stroke": 5 + tingkat_parah * 3,
        "cardiac arrest": 5 + tingkat_parah * 3,
        "aterosklerosis": 5 + tingkat_parah * 3
    }

    if abnormal_hr:
        base_risk["aritmia"] += 10
        base_risk["gagal jantung"] += 5

    pertanyaan_penyakit = {
        "riwayat_keluarga": ["penyakit jantung koroner", "serangan jantung", "fibrilasi atrium", "cardiac arrest", "aterosklerosis"],
        "nyeri_dada": ["penyakit jantung koroner", "serangan jantung"],
        "sesak_napas": ["gagal jantung", "hipertensi pulmonal"],
        "pingsan": ["aritmia", "blok jantung"],
        "tekanan_darah_tinggi": ["hipertensi pulmonal", "gagal jantung", "aterosklerosis"],
        "diabetes": ["penyakit jantung koroner", "serangan jantung", "aterosklerosis"],
        "merokok": ["penyakit arteri perifer", "penyakit jantung koroner"],
        "alkohol": ["kardiomiopati", "cardiac arrest"],
        "jantung_berdebar": ["aritmia", "fibrilasi atrium"],
        "bengkak_kaki": ["gagal jantung", "perikarditis"],
        "sering_lelah": ["gagal jantung", "kardiomiopati", "cardiac arrest"],
        "kolesterol_tinggi": ["penyakit jantung koroner", "aterosklerosis"],
        "jarang_olahraga": ["penyakit arteri perifer", "stroke"],
        "stres_berlebihan": ["aritmia", "serangan jantung"],
        "sulit_tidur": ["fibrilasi atrium", "stroke"],
        "pusing_saat_berdiri": ["blok jantung"],
        "keringat_tanpa_aktivitas": ["serangan jantung"],
        "sleep_apnea": ["gagal jantung"],
        "autoimun": ["perikarditis", "endokarditis", "aterosklerosis"],
        "tiroid": ["aritmia", "stroke"],
        "kesemutan": ["penyakit arteri perifer"],
        "sakit_kepala": ["hipertensi pulmonal"],
        "junkfood": ["penyakit jantung koroner", "stroke"],
        "tinggi_gula": ["kardiomiopati"]
    }

    for key, penyakit_list in pertanyaan_penyakit.items():
        if ya_tidak_answers.get(key, False):
            for p in penyakit_list:
                base_risk[p] += 5

    for k, v in numeric_risk.items():
        if k in base_risk:
            base_risk[k] += v

    for k in base_risk:
        base_risk[k] = min(base_risk[k], 100)

    return base_risk
