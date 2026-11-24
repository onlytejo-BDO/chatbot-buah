
import streamlit as st

# Pengaturan halaman
st.set_page_config(
    page_title="Chatbot Buah",
    page_icon="🍎"
)

st.title("🍎 Chatbot Pengetahuan Buah")
st.caption("Asisten informasi buah-buahan")

# DATABASE
database = {
    "pisang": "Pisang berwarna kuning 🍌",
    "jeruk": "Jeruk berwarna oranye 🍊",
    "apel": "Apel berwarna merah 🍎",
    "anggur": "Anggur berwarna ungu 🍇",
    "semangka": "Semangka memiliki daging berwarna merah 🍉",
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
    "star apple": "Star apple atau kenitu berwarna ungu atau hijau 🟣",
    "longan": "Longan atau lengkeng berwarna cokelat muda 🟤",
    "persimmon": "Persimmon atau kesemek berwarna oranye cerah 🟠"
}


}

# MENYIMPAN HISTORY CHAT
if "messages" not in st.session_state:
    st.session_state.messages = []

# SIDEBAR
with st.sidebar:
    st.header("💬 Chat History")

    st.write(f"Total pesan: {len(st.session_state.messages)}")

    if st.button("🗑️ Hapus Percakapan"):
        st.session_state.messages = []
        st.rerun()

# MENAMPILKAN HISTORY
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message.get("source"):
            st.caption(message["source"])

# INPUT CHAT
pertanyaan = st.chat_input("Tanyakan sesuatu tentang buah...")

if pertanyaan:

    # PROSES JAWABAN
    jawaban = "Nanya wae anjing! ."

    for kata, informasi in database.items():
        if kata in pertanyaan.lower():
            jawaban = informasi
            break

    # SIMPAN PERTANYAAN
    st.session_state.messages.append({
        "role": "user",
        "content": pertanyaan
    })

    # SIMPAN JAWABAN
    st.session_state.messages.append({
        "role": "assistant",
        "content": jawaban,
        "source": "Sumber: Database Buah"
    })

    st.rerun()
