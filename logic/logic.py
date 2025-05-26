def targetjarak(age, gender):
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

def selisihjarak(target, actual, age):
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

def bminormal(weight, height_cm):
    height_m = height_cm / 100
    return weight / (height_m ** 2)

def hitungresiko(age, gender, bmi, detakbiasa, detakjalan, sistolik, diastolik, olahraga_minggu):
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
    if detakbiasa > 100:
        risk["aritmia"] += 15
        risk["fibrilasi atrium"] += 10
    if detakjalan > 120:
        risk["gagal jantung"] += 10
    if bmi >= 30:
        risk["gagal jantung"] += 10
        risk["penyakit arteri perifer"] += 10
        risk["penyakit jantung koroner"] += 2
        risk["stroke"] += 10
    if sistolik >= 140 or diastolik >= 90:
        risk["hipertensi pulmonal"] += 15
        risk["serangan jantung"] += 10
    if olahraga_minggu < 1:
        risk["penyakit arteri perifer"] += 10
        risk["penyakit jantung koroner"] += 5
    return risk

def totalresiko(tingkatresiko, detakabnormal, jawaban, persentaseresiko):
    base_risk = {
        "aritmia": 5 + tingkatresiko * 3,
        "kardiomiopati": 5 + tingkatresiko * 3,
        "penyakit jantung koroner": 5 + tingkatresiko * 3,
        "gagal jantung": 5 + tingkatresiko * 3,
        "serangan jantung": 5 + tingkatresiko * 3,
        "hipertensi pulmonal": 5 + tingkatresiko * 3,
        "penyakit katup jantung": 5 + tingkatresiko * 3,
        "endokarditis": 5 + tingkatresiko * 3,
        "perikarditis": 5 + tingkatresiko * 3,
        "penyakit arteri perifer": 5 + tingkatresiko * 3,
        "fibrilasi atrium": 5 + tingkatresiko * 3,
        "blok jantung": 5 + tingkatresiko * 3,
        "stroke": 5 + tingkatresiko * 3,
        "cardiac arrest": 5 + tingkatresiko * 3,
        "aterosklerosis": 5 + tingkatresiko * 3
    }

    if detakabnormal:
        base_risk["aritmia"] += 10
        base_risk["gagal jantung"] += 5

    pertanyaan = {
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

    for key, listpenyakit in pertanyaan.items():
        if jawaban.get(key, False):
            for p in listpenyakit:
                base_risk[p] += 5

    for gejalapenyakit, namapenyakit in persentaseresiko.items():
        if gejalapenyakit in base_risk:
            base_risk[gejalapenyakit] += namapenyakit

    for gejalapenyakit in base_risk:
        base_risk[gejalapenyakit] = min(base_risk[gejalapenyakit], 100)

    return base_risk
