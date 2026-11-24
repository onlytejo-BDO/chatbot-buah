import streamlit as st
import re
import random
from rapidfuzz import process, fuzz

from faq_tambahan import bangun_faq_tambahan, jawab_dinamis

# ==================================================
# 1. PENGATURAN HALAMAN
# ==================================================

st.set_page_config(
    page_title="TemanAI - Chatbot Buah",
    page_icon="🍎",
    layout="centered"
)

st.title("🍎 TemanAI")
st.caption("Teman ngobrol dan asisten pengetahuan buah")


# ==================================================
# 2. DATABASE BUAH
# ==================================================

database = {
    "pisang": "Pisang berwarna kuning 🍌",
    "jeruk": "Jeruk berwarna oranye 🍊",
    "apel": "Apel berwarna merah 🍎",
    "anggur": "Anggur berwarna ungu 🍇",
    "semangka": "Semangka memiliki kulit hijau dan daging berwarna merah 🍉",
    "mangga": "Mangga matang berwarna kuning keoranyean 🥭",
    "nanas": "Nanas memiliki daging buah berwarna kuning 🍍",
    "stroberi": "Stroberi berwarna merah cerah 🍓",
    "alpukat": "Alpukat berkulit hijau tua dengan daging hijau kekuningan 🥑",
    "kiwi": "Kiwi berkulit cokelat dengan daging berwarna hijau 🥝",
    "persik": "Persik berwarna merah muda keoranyean 🍑",
    "ceri": "Ceri berwarna merah tua 🍒",
    "pir": "Pir berwarna kuning kehijauan 🍐",
    "lemon": "Lemon berwarna kuning cerah 🍋",
    "kelapa": "Kelapa berkulit hijau atau cokelat dengan daging putih 🥥",
    "melon": "Melon memiliki daging berwarna hijau muda atau oranye 🍈",
    "bluberi": "Bluberi berwarna biru keunguan gelap 🫐",
    "durian": "Durian berkulit hijau berduri dengan daging kuning 🟡",
    "rambutan": "Rambutan berkulit merah berambut dengan daging putih 🔴",
    "manggis": "Manggis berkulit ungu tua dengan daging putih bersih 🟣",
    "salak": "Salak berkulit cokelat bersisik dengan daging putih gading 🟤",
    "duku": "Duku berkulit kuning kecokelatan dengan daging putih bening 🟡",
    "lengkeng": "Lengkeng berkulit cokelat muda dengan daging putih bening 🟤",
    "pepaya": "Pepaya matang memiliki daging berwarna oranye kemerahan 🟠",
    "jambu biji": "Jambu biji memiliki daging berwarna merah muda atau putih 🩷",
    "jambu air": "Jambu air berwarna merah muda atau hijau segar 🔴",
    "belimbing": "Belimbing matang berwarna kuning kehijauan ⭐",
    "nangka": "Nangka memiliki daging buah berwarna kuning cerah 🟡",
    "cempedak": "Cempedak memiliki daging berwarna kuning keoranyean 🟠",
    "sirsak": "Sirsak berkulit hijau berduri lunak dengan daging putih 🟢",
    "srikaya": "Srikaya berkulit hijau berbenjol dengan daging putih 🟢",
    "sawo": "Sawo berwarna cokelat manis 🟤",
    "kedondong": "Kedondong berwarna hijau 🟢",
    "markisa": "Markisa berkulit ungu atau kuning dengan biji berwarna oranye 🟡",
    "buah naga": "Buah naga berkulit merah muda dengan daging merah keunguan atau putih 🐉",
    "leci": "Leci berkulit merah muda kasar dengan daging putih 🩷",
    "kesemek": "Kesemek berwarna oranye kemerahan 🟠",
    "menteng": "Menteng berkulit kuning kecokelatan dengan daging putih 🟡",
    "gandaria": "Gandaria matang berwarna kuning keoranyean 🟠",
    "matoa": "Matoa berkulit hijau kecokelatan dengan daging putih bening 🟢",
    "kecapi": "Kecapi berkulit kuning keemasan dengan daging putih 🟡",
    "jamblang": "Jamblang berwarna ungu kehitaman 🟣",
    "buni": "Buni berwarna merah hingga ungu kehitaman 🔴",
    "ceplukan": "Ceplukan matang berwarna kuning keoranyean 🟡",
    "bidara": "Bidara berwarna hijau kekuningan 🟢",
    "sukun": "Sukun berkulit hijau dengan daging putih kekuningan 🟢",
    "labu": "Labu berwarna oranye cerah 🎃",
    "jeruk nipis": "Jeruk nipis berwarna hijau tua 🟢",
    "jeruk bali": "Jeruk bali memiliki daging berwarna merah muda 🩷",
    "jeruk mandarin": "Jeruk mandarin berwarna oranye terang 🍊",
    "yuzu": "Yuzu berwarna kuning cerah 🍋",
    "kumquat": "Kumquat berukuran kecil dan berwarna oranye 🍊",
    "rasberi": "Rasberi berwarna merah muda kemerahan 🔴",
    "blackberi": "Blackberi berwarna hitam mengilap ⚫",
    "kranberi": "Kranberi berwarna merah tua 🔴",
    "murbei": "Murbei matang berwarna ungu kehitaman 🟣",
    "goji beri": "Goji beri berwarna merah keoranyean 🔴",
    "acai beri": "Acai beri berwarna ungu gelap 🟣",
    "elderberi": "Elderberi berwarna ungu kehitaman 🟣",
    "delima": "Delima berkulit merah dengan biji merah delima di dalamnya 🔴",
    "kurma": "Kurma matang berwarna cokelat tua 🟤",
    "tin": "Buah tin berwarna ungu kecokelatan atau hijau 🟣",
    "zaitun": "Zaitun berwarna hijau atau hitam keunguan 🫒",
    "aprikot": "Aprikot berwarna kuning keoranyean 🟠",
    "nektarin": "Nektarin berwarna merah kekuningan 🍑",
    "plum": "Plum berwarna ungu kemerahan gelap 🟣",
    "quince": "Quince berwarna kuning keemasan 🟡",
    "pepino": "Pepino berwarna kuning pucat dengan garis ungu 🟡",
    "feijoa": "Feijoa berwarna hijau dengan daging putih kekuningan 🟢",
    "kiwano": "Kiwano berkulit oranye berduri dengan daging hijau 🟠",
    "cherimoya": "Cherimoya berkulit hijau bersisik dengan daging putih 🟢",
    "jabuticaba": "Jabuticaba berwarna ungu kehitaman yang tumbuh di batang pohon 🟣",
    "ackee": "Ackee berkulit merah keoranyean dengan daging kuning 🟠",
    "tamarillo": "Tamarillo atau terong belanda berwarna merah keunguan 🔴",
    "miracle fruit": "Miracle fruit berwarna merah kecil 🔴",
    "mangosteen": "Mangosteen atau manggis berwarna ungu gelap 🟣",
    "star apple": "Star Apple atau kenitu berwarna ungu atau hijau 🟣",
    "longan": "Longan atau lengkeng berwarna cokelat muda 🟤",
    "persimmon": "Persimmon atau kesemek berwarna oranye cerah 🟠"
}


# ==================================================
# 3. DATABASE FAQ UMUM
# ==================================================

faq = {
    "halo": "Halo juga! 👋 Ada yang bisa aku bantu hari ini?",
    "hai": "Hai! Senang bertemu denganmu. Mau ngobrol tentang apa?",
    "hello": "Hello! Ada yang ingin kamu tanyakan?",
    "hi": "Hi! Apa kabar hari ini?",
    "assalamualaikum": "Waalaikumsalam! Semoga harimu menyenangkan 😊",
    "selamat pagi": "Selamat pagi! Semoga aktivitasmu lancar ☀️",
    "selamat siang": "Selamat siang! Jangan lupa istirahat ya.",
    "selamat sore": "Selamat sore! Ada yang bisa aku bantu?",
    "selamat malam": "Selamat malam! Semoga harimu menyenangkan 🌙",
    "apa kabar": "Aku baik-baik saja! Terima kasih sudah bertanya. Kamu bagaimana?",
    "siapa kamu": "Aku adalah TemanAI, asisten virtual yang siap menemani percakapanmu. 😊",
    "nama kamu": "Namaku TemanAI! 🍎",
    "kamu siapa": "Aku TemanAI, teman ngobrol virtualmu!",
    "terima kasih": "Sama-sama! Senang bisa membantu 😊",
    "makasih": "Sama-sama! Ada pertanyaan lain?",
    "dadah": "Dadah! Sampai bertemu lagi 👋",
    "sampai jumpa": "Sampai jumpa lagi! Jangan lupa mampir ya.",
    "bye": "Goodbye! Semoga harimu menyenangkan!",
    "apa yang bisa kamu lakukan": "Aku bisa menjawab pertanyaan tentang buah-buahan dan pengetahuan umum sederhana.",
    "apa itu ai": "AI (Artificial Intelligence) atau kecerdasan buatan adalah teknologi yang memungkinkan komputer melakukan tugas yang biasanya membutuhkan kecerdasan manusia.",
    "apa itu artificial intelligence": "Artificial Intelligence adalah teknologi yang membuat mesin mampu meniru beberapa kemampuan berpikir dan belajar manusia.",
    "apa itu kecerdasan buatan": "Kecerdasan buatan adalah teknologi yang memungkinkan komputer melakukan tugas cerdas seperti memahami bahasa dan mengenali pola.",
    "apa itu chatbot": "Chatbot adalah program komputer yang dirancang untuk berkomunikasi dengan manusia melalui percakapan teks atau suara.",
    "apa itu chatgpt": "ChatGPT adalah AI buatan OpenAI yang dapat memahami dan menghasilkan teks.",
    "siapa pembuat chatgpt": "ChatGPT dikembangkan oleh OpenAI.",
    "apa itu machine learning": "Machine Learning adalah cabang AI yang memungkinkan komputer mempelajari pola dari data.",
    "apa itu deep learning": "Deep Learning adalah bagian dari Machine Learning yang menggunakan jaringan saraf tiruan berlapis.",
    "apa itu neural network": "Neural Network adalah model komputasi yang terinspirasi dari jaringan neuron pada otak manusia.",
    "apa itu generative ai": "Generative AI adalah teknologi AI yang mampu membuat konten baru seperti teks, gambar, musik, video, dan kode.",
    "apa itu prompt": "Prompt adalah instruksi atau pertanyaan yang diberikan kepada AI.",
    "apa manfaat ai": "AI dapat membantu pendidikan, kesehatan, bisnis, analisis data, dan otomatisasi pekerjaan.",
    "apa kekurangan ai": "AI bisa menghasilkan informasi keliru, memiliki bias, dan bergantung pada kualitas data.",
    "apakah ai berbahaya": "AI memiliki manfaat besar, tetapi juga memiliki risiko seperti penyebaran informasi salah dan penyalahgunaan teknologi.",
    "apa itu robot": "Robot adalah mesin yang dirancang untuk melakukan tugas tertentu secara otomatis.",
    "apa itu algoritma": "Algoritma adalah serangkaian langkah sistematis untuk menyelesaikan suatu masalah."
}


# ==================================================
# 4. VARIASI PERTANYAAN OTOMATIS
# ==================================================

template_pertanyaan = [
    "apa warna {buah}",
    "{buah} warnanya apa",
    "buah {buah} berwarna apa",
    "gimana warna {buah}",
    "bagaimana warna {buah}",
    "coba jelaskan warna {buah}",
    "warna dari {buah} itu apa",
    "aku mau tahu warna {buah}",
    "lu tahu warna {buah}",
    "kamu tahu warna {buah}",
    "tolong jelaskan warna {buah}",
    "sebutkan warna {buah}",
    "warna buah {buah} seperti apa",
    "kalau {buah} warnanya bagaimana",
    "apa warna kulit {buah}",
    "apa warna daging {buah}",
    "jelaskan penampilan buah {buah}",
    "ceritakan tentang warna {buah}",
    "kasih tahu aku warna {buah}",
    "menurut kamu {buah} warnanya apa"
]

faq_buah_otomatis = {}

for nama_buah, informasi in database.items():
    for template in template_pertanyaan:
        pertanyaan_baru = template.format(buah=nama_buah)
        faq_buah_otomatis[pertanyaan_baru] = informasi

jumlah_faq_buah = len(faq_buah_otomatis)


# ==================================================
# 5. NORMALISASI TEKS
# ==================================================

def normalisasi(teks):
    teks = teks.lower().strip()
    teks = re.sub(r"[^\w\s]", " ", teks)
    teks = re.sub(r"\s+", " ", teks)
    return teks


# ==================================================
# 5B. INDEKS GABUNGAN (FAQ umum + variasi buah + FAQ tambahan)
# ==================================================
# Setiap pertanyaan menyimpan DAFTAR jawaban. Kalau ada lebih dari satu,
# bot memilih acak supaya percakapan tidak monoton.

def bangun_indeks():
    indeks = {}

    def tambah(kunci, daftar_jawaban):
        tersimpan = indeks.setdefault(kunci, [])
        for j in daftar_jawaban:
            if j not in tersimpan:
                tersimpan.append(j)

    for k, v in faq.items():
        tambah(normalisasi(k), [v])

    for k, v in faq_buah_otomatis.items():
        tambah(normalisasi(k), [v])

    tambahan = bangun_faq_tambahan(database)
    for k, v in tambahan.items():
        tambah(k, v)

    return indeks, len(tambahan)


indeks_faq, jumlah_faq_tambahan = bangun_indeks()
daftar_kunci = list(indeks_faq.keys())
urutan_kunci = sorted(daftar_kunci, key=len, reverse=True)  # yang paling spesifik dulu


# ==================================================
# 6. FUNGSI MENCARI JAWABAN
# ==================================================

def cari_jawaban(pertanyaan):

    teks = normalisasi(pertanyaan)

    jawaban_default = (
        "Maaf, aku belum memahami pertanyaan tersebut. "
        "Coba gunakan kalimat yang berbeda ya! 😊 "
        "(Ketik 'bantuan' untuk melihat apa saja yang bisa kutanyakan.)"
    )

    if not teks:
        return jawaban_default, "Sumber: Respons otomatis"

    # PRIORITAS 0: FITUR DINAMIS (kalkulator, jam, tanggal, rekomendasi buah)
    dinamis = jawab_dinamis(pertanyaan, teks, database)
    if dinamis:
        return dinamis, "Sumber: Fitur otomatis"

    # PRIORITAS 1: COCOK PERSIS
    if teks in indeks_faq:
        return random.choice(indeks_faq[teks]), "Sumber: Database FAQ"

    # PRIORITAS 2: FAQ TERKANDUNG DALAM KALIMAT (kunci terpanjang dulu)
    teks_pad = f" {teks} "
    for kunci in urutan_kunci:
        if f" {kunci} " in teks_pad:
            return random.choice(indeks_faq[kunci]), "Sumber: Database FAQ"

    # PRIORITAS 3: NAMA BUAH YANG TEPAT
    nama_buah = list(database.keys())

    for buah in sorted(nama_buah, key=len, reverse=True):
        pola = r"\b" + re.escape(buah) + r"\b"

        if re.search(pola, teks):
            return database[buah], "Sumber: Database Buah"

    # PRIORITAS 4: TYPO PADA PERTANYAAN FAQ
    hasil_faq = process.extractOne(
        teks,
        daftar_kunci,
        scorer=fuzz.token_sort_ratio,
        score_cutoff=85
    )

    if hasil_faq:
        kunci, skor, _ = hasil_faq
        return (
            random.choice(indeks_faq[kunci]),
            f"Sumber: Database FAQ (kemiripan {skor:.0f}%)"
        )

    # PRIORITAS 5: DETEKSI TYPO NAMA BUAH
    kata_pertanyaan = teks.split()
    kandidat = []

    for ukuran in range(1, 4):
        for i in range(len(kata_pertanyaan) - ukuran + 1):
            potongan = " ".join(
                kata_pertanyaan[i:i + ukuran]
            )
            kandidat.append(potongan)

    buah_terbaik = None
    skor_terbaik = 0

    for potongan in kandidat:

        hasil = process.extractOne(
            potongan,
            nama_buah,
            scorer=fuzz.ratio,
            score_cutoff=80
        )

        if hasil:
            nama, skor, index = hasil

            if skor > skor_terbaik:
                buah_terbaik = nama
                skor_terbaik = skor

    if buah_terbaik:
        return (
            database[buah_terbaik],
            f"Sumber: Database Buah (kemiripan {skor_terbaik:.0f}%)"
        )

    # PRIORITAS 6: TIDAK DITEMUKAN
    return jawaban_default, "Sumber: Respons otomatis"


# ==================================================
# 7. CHAT HISTORY
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==================================================
# 8. SIDEBAR
# ==================================================

with st.sidebar:

    st.header("💬 TemanAI")

    st.write(
        f"Total pesan: {len(st.session_state.messages)}"
    )

    if st.button("🗑️ Hapus Percakapan"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("📚 Database")

    st.write(f"Jumlah buah: {len(database)}")
    st.write(f"Jumlah FAQ umum: {len(faq)}")
    st.write(f"Variasi pertanyaan buah: {jumlah_faq_buah}")
    st.write(f"FAQ tambahan: {jumlah_faq_tambahan}")

    st.write(
        f"Total pertanyaan terindeks: {len(indeks_faq)}"
    )
    st.write(
        f"Total variasi jawaban: {sum(len(v) for v in indeks_faq.values())}"
    )

    st.divider()
    st.caption(
        "Coba: 'kasih pantun', 'fakta unik', 'ibu kota Jawa Barat', "
        "'manfaat pisang', 'buah apa saja yang berwarna ungu', "
        "'hitung 12 x 7', 'hari apa sekarang'"
    )


# ==================================================
# 9. MENAMPILKAN CHAT HISTORY
# ==================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if message.get("source"):
            st.caption(message["source"])


# ==================================================
# 10. INPUT CHAT
# ==================================================

pertanyaan = st.chat_input(
    "Tanyakan sesuatu tentang buah atau AI..."
)

if pertanyaan:

    jawaban, sumber = cari_jawaban(pertanyaan)

    st.session_state.messages.append({
        "role": "user",
        "content": pertanyaan
    })

    st.session_state.messages.append({
        "role": "assistant",
        "content": jawaban,
        "source": sumber
    })

    st.rerun()
