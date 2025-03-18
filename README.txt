TUTORIAL Tobii
Baca "Panduan Lab T-EL untuk Tobii Pro Nano"
 
 
TUTORIAL Instalasi Script Python
 
1. Gunakan Python versi 3.10 (check versi python --version)
2. Buat virtual env
	(python -m venv venv)
3. Aktivasi venv
	(.\venv\Scripts\activate)
4. Install requirements
	(pip install -r requirements.txt)

(optional) Install ffmpeg untuk pydub

TUTORIAL Penggunaan
Lihat help untuk CLI tobii_script.py
	(python tobii_script.py --help)

Disarankan untuk kalibrasi untuk setiap subjek/sesi
Contoh: Melakukan kalibrasi untuk subjek A, jika dalam satu sesi mengambil data dari Subjek A, tidak perlu lakukan kalibrasi lagi.
Contoh: Melakukan kalibrasi untuk subjek A, kemudian A meninggalkan tempat, sebelum mengambil data perlu kalibrasi lagi
Contoh: Melakukan kalibrasi untuk subjek A, kemudian lanjut ke subjek B, perlu kalibrasi lagi sebelum mengambil data

Contoh Penggunaan
python tobii_script.py --calibrate -d 30 --output-csv data_subject_1.csv --save-screenshot

--calibrate = berarti dikalibrasi sebelum mengambil data
-d 30 = durasi 30 (bisa -d atau --duration)
