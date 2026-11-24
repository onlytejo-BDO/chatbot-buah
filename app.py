
import streamlit as st

# ==================================================
# 1. PENGATURAN HALAMAN
# ==================================================

st.set_page_config(
    page_title="Chatbot Buah",
    page_icon="🍎",
    layout="centered"
)

st.title("🍎 Chatbot Pengetahuan Buah")
st.caption("Asisten informasi buah-buahan dan teknologi AI")


# ==================================================
# 2. DATABASE BUAH
# ==================================================

database = {
    "pisang": "Pisang berwarna kuning 🍌",
    "jeruk": "Jeruk berwarna oranye 🍊",
    "apel": "Apel berwarna merah 🍎",
    "anggur": "Anggur berwarna ungu 🍇",
    "semangka": "Semangka memiliki daging berwarna merah 🍉",

    # Buah Populer & Tropis
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

    # Buah Tropis & Lokal Indonesia
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

    # Kelompok Sitrus
    "jeruk nipis": "Jeruk nipis berwarna hijau tua 🟢",
    "jeruk bali": "Jeruk bali memiliki daging berwarna merah muda 🩷",
    "jeruk mandarin": "Jeruk mandarin berwarna oranye terang 🍊",
    "yuzu": "Yuzu berwarna kuning cerah 🍋",
    "kumquat": "Kumquat berukuran kecil dan berwarna oranye 🍊",

    # Kelompok Beri
    "rasberi": "Rasberi berwarna merah muda kemerahan 🔴",
    "blackberi": "Blackberi berwarna hitam mengilap ⚫",
    "kranberi": "Kranberi berwarna merah tua 🔴",
    "murbei": "Murbei matang berwarna ungu kehitaman 🟣",
    "goji beri": "Goji beri berwarna merah keoranyean 🔴",
    "acai beri": "Acai beri berwarna ungu gelap 🟣",
    "elderberi": "Elderberi berwarna ungu kehitaman 🟣",

    # Buah Subtropis & Timur Tengah
    "delima": "Delima berkulit merah dengan biji merah delima di dalamnya 🔴",
    "kurma": "Kurma matang berwarna cokelat tua 🟤",
    "tin": "Buah tin berwarna ungu kecokelatan atau hijau 🟣",
    "zaitun": "Zaitun berwarna hijau atau hitam keunguan 🫒",
    "aprikot": "Aprikot berwarna kuning keoranyean 🟠",
    "nektarin": "Nektarin berwarna merah kekuningan 🍑",
    "plum": "Plum berwarna ungu kemerahan gelap 🟣",
    "quince": "Quince berwarna kuning keemasan 🟡",

    # Buah Eksotis
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
# 3. DATABASE FAQ
# ==================================================

faq = {
    # SAPAAN
    "halo": "Halo juga! 👋 Ada yang bisa aku bantu hari ini?",
    "hai": "Hai! Senang bertemu denganmu. Mau ngobrol tentang apa?",
    "hello": "Hello! Ada yang ingin kamu tanyakan?",
    "hi": "Hi! Apa kabar hari ini?",
    "assalamualaikum": "Waalaikumsalam! Semoga harimu menyenangkan 😊",
    "selamat pagi": "Selamat pagi! Semoga aktivitasmu lancar ☀️",
    "selamat siang": "Selamat siang! Jangan lupa istirahat ya.",
    "selamat sore": "Selamat sore! Ada yang bisa aku bantu?",
    "selamat malam": "Selamat malam! Semoga harimu menyenangkan 🌙",

    # PERCAKAPAN UMUM
    "apa kabar": "Aku baik-baik saja! Terima kasih sudah bertanya. Kamu bagaimana?",
    "siapa kamu": "Aku adalah Chatbot Buah, asisten virtual yang siap menjawab pertanyaan tentang buah dan pengetahuan umum.",
    "nama kamu": "Namaku Chatbot Buah! 🍎",
    "kamu siapa": "Aku Chatbot Buah, teman ngobrol virtualmu!",
    "terima kasih": "Sama-sama! Senang bisa membantu 😊",
    "makasih": "Sama-sama! Ada pertanyaan lain?",
    "dadah": "Dadah! Sampai bertemu lagi 👋",
    "sampai jumpa": "Sampai jumpa lagi! Jangan lupa mampir ya.",
    "bye": "Goodbye! Semoga harimu menyenangkan!",
    "apa yang bisa kamu lakukan": "Aku bisa menjawab pertanyaan tentang buah-buahan dan memberikan informasi dasar seputar teknologi AI.",

    # FAQ ARTIFICIAL INTELLIGENCE
    "apa itu ai": "AI (Artificial Intelligence) atau kecerdasan buatan adalah teknologi yang memungkinkan komputer melakukan tugas yang biasanya membutuhkan kecerdasan manusia, seperti memahami bahasa, mengenali gambar, dan memecahkan masalah.",
    "apa itu artificial intelligence": "Artificial Intelligence adalah teknologi yang membuat mesin mampu meniru beberapa kemampuan berpikir dan belajar manusia.",
    "apa itu kecerdasan buatan": "Kecerdasan buatan adalah teknologi yang memungkinkan komputer melakukan tugas cerdas seperti memahami bahasa dan mengenali pola.",
    "apa itu chatbot": "Chatbot adalah program komputer yang dirancang untuk berkomunikasi dengan manusia melalui percakapan teks atau suara.",
    "apa itu chatgpt": "ChatGPT adalah AI buatan OpenAI yang dapat memahami dan menghasilkan teks, menjawab pertanyaan, membantu menulis, belajar, dan berbagai pekerjaan lainnya.",
    "siapa pembuat chatgpt": "ChatGPT dikembangkan oleh OpenAI, perusahaan riset dan pengembangan kecerdasan buatan.",
    "apa itu machine learning": "Machine Learning adalah cabang AI yang memungkinkan komputer mempelajari pola dari data untuk membuat prediksi atau keputusan.",
    "apa itu deep learning": "Deep Learning adalah bagian dari Machine Learning yang menggunakan jaringan saraf tiruan berlapis untuk mempelajari pola kompleks.",
    "apa itu neural network": "Neural Network adalah model komputasi yang terinspirasi dari cara kerja jaringan neuron pada otak manusia.",
    "apa itu generative ai": "Generative AI adalah teknologi AI yang mampu membuat konten baru seperti teks, gambar, musik, video, dan kode.",
    "apa itu prompt": "Prompt adalah instruksi atau pertanyaan yang diberikan kepada AI untuk menghasilkan jawaban tertentu.",
    "apa itu prompt engineering": "Prompt Engineering adalah teknik menyusun instruksi agar AI menghasilkan jawaban yang lebih tepat dan sesuai kebutuhan.",
    "apa manfaat ai": "AI dapat membantu pendidikan, kesehatan, bisnis, analisis data, otomatisasi pekerjaan, dan meningkatkan produktivitas.",
    "apa kekurangan ai": "AI bisa menghasilkan informasi keliru, memiliki bias, bergantung pada kualitas data, dan tidak selalu memahami konteks seperti manusia.",
    "apakah ai bisa berpikir": "AI dapat memproses informasi dan menghasilkan respons yang terlihat seperti penalaran manusia, tetapi cara kerjanya berbeda dari pikiran dan kesadaran manusia.",
    "apakah ai berbahaya": "AI memiliki manfaat besar, tetapi juga memiliki risiko seperti penyebaran informasi salah, pelanggaran privasi, dan penyalahgunaan teknologi.",
    "apakah ai bisa menggantikan manusia": "AI dapat mengotomatisasi beberapa pekerjaan, tetapi banyak pekerjaan tetap membutuhkan kreativitas, empati, tanggung jawab, dan penilaian manusia.",
    "apa itu robot": "Robot adalah mesin yang dirancang untuk melakukan tugas tertentu secara otomatis atau dengan kendali manusia.",
    "apa itu algoritma": "Algoritma adalah serangkaian langkah atau instruksi sistematis untuk menyelesaikan suatu masalah."
}


# ==================================================
# 4. FUNGSI MENCARI JAWABAN
# ==================================================

def cari_jawaban(pertanyaan):
    teks = pertanyaan.lower().strip()

    # Default jika tidak ditemukan
    jawaban = "Maaf, aku belum memahami pertanyaan tersebut. Coba gunakan kalimat yang berbeda ya! 😊"
    sumber = "Sumber: Respons otomatis"

    # Periksa FAQ terlebih dahulu
    for kata, informasi in sorted(
        faq.items(),
        key=lambda item: len(item[0]),
        reverse=True
    ):
        if kata in teks:
            return informasi, "Sumber: Database FAQ"

    # Jika FAQ tidak ditemukan, periksa database buah
    for kata, informasi in sorted(
        database.items(),
        key=lambda item: len(item[0]),
        reverse=True
    ):
        if kata in teks:
            return informasi, "Sumber: Database Buah"

    return jawaban, sumber


# ==================================================
# 5. MENYIMPAN HISTORY CHAT
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ==================================================
# 6. SIDEBAR
# ==================================================

with st.sidebar:
    st.header("💬 Chat History")

    st.write(f"Total pesan: {len(st.session_state.messages)}")

    if st.button("🗑️ Hapus Percakapan"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("📚 Informasi Database")
    st.write(f"Jumlah buah: {len(database)}")
    st.write(f"Jumlah FAQ: {len(faq)}")


# ==================================================
# 7. MENAMPILKAN HISTORY CHAT
# ==================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message.get("source"):
            st.caption(message["source"])


# ==================================================
# 8. INPUT DAN PROSES CHAT
# ==================================================

pertanyaan = st.chat_input("Tanyakan sesuatu tentang buah atau AI...")

if pertanyaan:

    # Cari jawaban
    jawaban, sumber = cari_jawaban(pertanyaan)

    # Simpan pertanyaan pengguna
    st.session_state.messages.append({
        "role": "user",
        "content": pertanyaan
    })

    # Simpan jawaban chatbot
    st.session_state.messages.append({
        "role": "assistant",
        "content": jawaban,
        "source": sumber
    })

    # Refresh tampilan
    st.rerun()
