import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Pendaftaran Pasien Klinik AI", layout="centered")
st.title("🩺 Form Pendaftaran Pasien Klinik AI")

# Load data
try:
    df = pd.read_csv("data_pasien.csv")
except:
    df = pd.DataFrame(columns=["No. Medrek", "Nama", "Umur", "Keluhan", "Waktu Daftar"])

# Generate nomor medrek otomatis
nomor_terakhir = len(df) + 1
nomor_medrek = f"MED{nomor_terakhir:03}"

# Kamus keluhan + respon edukatif (multikeluhan + artikel mini)
chatbot_dict = {
    "demam": "**🦠 Demam**\n- Penyebab: infeksi virus/bakteri\n- Saran: minum air putih, istirahat cukup, kompres hangat\n- Hubungi dokter jika: demam > 3 hari atau suhu > 39°C",
    "batuk": "**🌬️ Batuk**\n- Bisa disebabkan flu, alergi, infeksi\n- Saran: banyak minum, hindari asap rokok\n- Ke dokter jika: batuk >1 minggu atau sesak napas",
    "diare": "**💩 Diare**\n- Penyebab: makanan tidak higienis, virus\n- Saran: oralit, hindari makanan pedas dan berminyak\n- Ke dokter jika: diare >3 hari, feses berdarah",
    "asam lambung": "**🔥 Asam Lambung (GERD)**\n- Gejala: nyeri ulu hati, mual setelah makan\n- Saran: makan teratur, hindari kopi & makanan pedas\n- Ke dokter jika: nyeri dada sering kambuh",
    "sakit kepala": "**🧠 Sakit Kepala**\n- Penyebab: kurang tidur, stres, gangguan mata\n- Saran: istirahat, minum cukup, kompres dingin\n- Ke dokter jika: nyeri hebat mendadak atau tidak membaik",
    "vertigo": "**🌀 Vertigo**\n- Rasa berputar akibat gangguan keseimbangan\n- Saran: hindari gerakan mendadak, periksa telinga dalam\n- Ke dokter jika: sering kambuh disertai mual hebat",
    "nyeri haid": "**🌸 Nyeri Haid**\n- Umum terjadi di hari pertama menstruasi\n- Saran: kompres hangat, istirahat, ibuprofen ringan\n- Ke dokter jika: nyeri tidak tertahankan setiap siklus",
    "hipertensi": "**❤️ Hipertensi**\n- Umumnya tanpa gejala\n- Saran: kurangi garam, olahraga rutin, cek tekanan darah\n- Ke dokter jika: tekanan darah >140/90 mmHg secara konsisten",
    "gatal": "**🧴 Gatal-gatal**\n- Penyebab: alergi, infeksi, kulit kering\n- Saran: mandi air dingin, gunakan pelembap, jangan digaruk\n- Ke dokter jika: ruam menyebar atau bernanah",
    "pilek": "**🤧 Pilek/Flu**\n- Penyebab: virus\n- Saran: istirahat, minum hangat, vitamin C\n- Ke dokter jika: pilek >10 hari atau demam tinggi"
}

def chatbot_respon(kalimat):
    kalimat = kalimat.lower()
    respons_list = []
    for keyword, respon in chatbot_dict.items():
        if keyword in kalimat:
            respons_list.append(respon)
    if respons_list:
        return "\n\n".join(respons_list)
    return "Maaf, sistem belum mengenali keluhan ini. Silakan konsultasi langsung ke petugas."

# Form input
with st.form("form_pasien"):
    st.text_input("Nomor Medrek", value=nomor_medrek, disabled=True)
    nama = st.text_input("Nama Lengkap")
    umur = st.number_input("Umur", min_value=0, max_value=120, step=1)
    keluhan = st.text_area("Keluhan Utama")

    # Tampilkan edukasi otomatis berdasarkan input keluhan
    if keluhan:
        st.markdown("**💬 Edukasi dari Chatbot:**")
        st.info(chatbot_respon(keluhan))

    submitted = st.form_submit_button("Daftarkan")

    if submitted:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = pd.DataFrame([[nomor_medrek, nama, umur, keluhan, waktu]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv("data_pasien.csv", index=False)
        st.success(f"Pasien berhasil didaftarkan dengan Nomor Medrek: {nomor_medrek}")

# 🔐 Akses admin
st.markdown("---")
password = st.text_input("🔐 Masukkan password admin untuk melihat data pasien:", type="password")

if password == "doktergibran":
    st.subheader("📋 Daftar Pasien Hari Ini")
    st.dataframe(df)
elif password != "":
    st.error("Password salah!")

# 🤖 Chatbot Edukasi Tambahan (Multikeluhan + Format Artikel)
st.markdown("---")
st.subheader("🤖 Tanya Chatbot Secara Manual")
user_input = st.text_input("Ketik keluhanmu di sini (contoh: saya punya asam lambung dan batuk):")
if user_input:
    st.markdown("**💬 Jawaban Chatbot:**")
    st.info(chatbot_respon(user_input))