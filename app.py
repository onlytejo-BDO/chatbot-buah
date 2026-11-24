
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
    "semangka": "Semangka memiliki daging berwarna merah 🍉"

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
    jawaban = "Maaf, Informasi tersebut belum tersedia yaa ."

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
