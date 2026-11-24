"""
faq_tambahan.py
Modul tambahan untuk TemanAI: membangun ribuan FAQ dari data terstruktur,
ditambah fitur dinamis (jam, tanggal, kalkulator, rekomendasi buah).

Format hasil: dict {pertanyaan_ternormalisasi: [jawaban1, jawaban2, ...]}
Kalau ada lebih dari satu jawaban, bot memilih acak supaya tidak monoton.
"""

import ast
import operator
import random
import re
from datetime import datetime, timedelta, timezone


# ==================================================
# UTILITAS
# ==================================================

def norm(teks):
    teks = teks.lower().strip()
    teks = re.sub(r"[^\w\s]", " ", teks)
    teks = re.sub(r"\s+", " ", teks)
    return teks.strip()


AWALAN = ["", "eh ", "hei ", "btw ", "coba ", "tolong "]
AKHIRAN = ["", " dong", " ya", " nih", " sih", " please"]


def _varian(frasa):
    """Menghasilkan 36 variasi gaya bicara dari satu frasa."""
    for a in AWALAN:
        for b in AKHIRAN:
            yield norm(f"{a}{frasa}{b}")


def _tambah(hasil, kunci, jawaban):
    if isinstance(jawaban, str):
        jawaban = [jawaban]
    daftar = hasil.setdefault(kunci, [])
    for j in jawaban:
        if j not in daftar:
            daftar.append(j)


# ==================================================
# DATA: GEOGRAFI
# ==================================================

# (nama resmi, ibu kota, alias)
PROVINSI = [
    ("Aceh", "Banda Aceh", ()),
    ("Sumatera Utara", "Medan", ("Sumut",)),
    ("Sumatera Barat", "Padang", ("Sumbar",)),
    ("Riau", "Pekanbaru", ()),
    ("Kepulauan Riau", "Tanjung Pinang", ("Kepri",)),
    ("Jambi", "Jambi", ()),
    ("Sumatera Selatan", "Palembang", ("Sumsel",)),
    ("Kepulauan Bangka Belitung", "Pangkal Pinang", ("Bangka Belitung",)),
    ("Bengkulu", "Bengkulu", ()),
    ("Lampung", "Bandar Lampung", ()),
    ("Banten", "Serang", ()),
    ("DKI Jakarta", "Jakarta", ()),
    ("Jawa Barat", "Bandung", ("Jabar",)),
    ("Jawa Tengah", "Semarang", ("Jateng",)),
    ("DI Yogyakarta", "Yogyakarta", ("Yogyakarta", "Jogja")),
    ("Jawa Timur", "Surabaya", ("Jatim",)),
    ("Bali", "Denpasar", ()),
    ("Nusa Tenggara Barat", "Mataram", ("NTB",)),
    ("Nusa Tenggara Timur", "Kupang", ("NTT",)),
    ("Kalimantan Barat", "Pontianak", ("Kalbar",)),
    ("Kalimantan Tengah", "Palangka Raya", ("Kalteng",)),
    ("Kalimantan Selatan", "Banjarmasin", ("Kalsel",)),
    ("Kalimantan Timur", "Samarinda", ("Kaltim",)),
    ("Kalimantan Utara", "Tanjung Selor", ("Kaltara",)),
    ("Sulawesi Utara", "Manado", ("Sulut",)),
    ("Gorontalo", "Gorontalo", ()),
    ("Sulawesi Tengah", "Palu", ("Sulteng",)),
    ("Sulawesi Barat", "Mamuju", ("Sulbar",)),
    ("Sulawesi Selatan", "Makassar", ("Sulsel",)),
    ("Sulawesi Tenggara", "Kendari", ("Sultra",)),
    ("Maluku", "Ambon", ()),
    ("Maluku Utara", "Sofifi", ("Malut",)),
    ("Papua", "Jayapura", ()),
    ("Papua Barat", "Manokwari", ()),
    ("Papua Barat Daya", "Sorong", ()),
    ("Papua Tengah", "Nabire", ()),
    ("Papua Selatan", "Merauke", ()),
    ("Papua Pegunungan", "Wamena", ()),
]

NEGARA = {
    "Indonesia": "Jakarta (ibu kota baru, Nusantara/IKN, masih dalam proses pembangunan dan transisi)",
    "Malaysia": "Kuala Lumpur", "Singapura": "Singapura", "Thailand": "Bangkok",
    "Vietnam": "Hanoi", "Filipina": "Manila", "Brunei": "Bandar Seri Begawan",
    "Kamboja": "Phnom Penh", "Laos": "Vientiane", "Myanmar": "Naypyidaw",
    "Timor Leste": "Dili", "Jepang": "Tokyo", "Korea Selatan": "Seoul",
    "Korea Utara": "Pyongyang", "Tiongkok": "Beijing", "India": "New Delhi",
    "Pakistan": "Islamabad", "Bangladesh": "Dhaka", "Arab Saudi": "Riyadh",
    "Turki": "Ankara", "Iran": "Teheran", "Irak": "Baghdad", "Mesir": "Kairo",
    "Afrika Selatan": "Pretoria", "Nigeria": "Abuja", "Kenya": "Nairobi",
    "Maroko": "Rabat", "Australia": "Canberra", "Selandia Baru": "Wellington",
    "Amerika Serikat": "Washington D.C.", "Kanada": "Ottawa", "Meksiko": "Kota Meksiko",
    "Brasil": "Brasilia", "Argentina": "Buenos Aires", "Chili": "Santiago",
    "Peru": "Lima", "Kolombia": "Bogota", "Inggris": "London", "Prancis": "Paris",
    "Jerman": "Berlin", "Italia": "Roma", "Spanyol": "Madrid", "Portugal": "Lisboa",
    "Belanda": "Amsterdam", "Belgia": "Brussel", "Swiss": "Bern", "Austria": "Wina",
    "Swedia": "Stockholm", "Norwegia": "Oslo", "Denmark": "Kopenhagen",
    "Finlandia": "Helsinki", "Rusia": "Moskow", "Ukraina": "Kyiv",
    "Polandia": "Warsawa", "Yunani": "Athena", "Mongolia": "Ulaanbaatar",
    "Nepal": "Kathmandu",
}

PLANET = {
    "Merkurius": "planet terkecil di tata surya dan yang paling dekat dengan Matahari",
    "Venus": "planet terpanas karena atmosfernya tebal; satu harinya bahkan lebih lama daripada satu tahunnya",
    "Bumi": "satu-satunya planet yang sejauh ini diketahui memiliki kehidupan",
    "Mars": "dijuluki Planet Merah, dan punya gunung tertinggi di tata surya bernama Olympus Mons",
    "Jupiter": "planet terbesar di tata surya, terkenal dengan Bintik Merah Besar berupa badai raksasa",
    "Saturnus": "terkenal dengan cincinnya yang indah, dan kepadatannya lebih rendah daripada air",
    "Uranus": "berputar dengan posisi hampir miring seperti menggelinding di orbitnya",
    "Neptunus": "planet terjauh dari Matahari, dengan angin yang sangat kencang",
}

MANFAAT_BUAH = {
    "pisang": "kaya kalium dan karbohidrat, bagus sebagai sumber energi cepat",
    "jeruk": "kaya vitamin C yang membantu daya tahan tubuh",
    "apel": "mengandung serat dan pektin yang baik untuk pencernaan",
    "anggur": "mengandung antioksidan, terutama pada bagian kulitnya",
    "semangka": "kandungan airnya sangat tinggi sehingga menyegarkan dan membantu hidrasi",
    "mangga": "kaya vitamin A dan vitamin C",
    "nanas": "mengandung vitamin C dan enzim bromelain",
    "stroberi": "kaya vitamin C dan antioksidan",
    "alpukat": "mengandung lemak tak jenuh yang baik, serat, dan kalium",
    "kiwi": "kaya vitamin C, vitamin K, dan serat",
    "pepaya": "mengandung vitamin A, vitamin C, serat, dan enzim papain",
    "jambu biji": "kandungan vitamin C-nya sangat tinggi",
    "delima": "kaya antioksidan jenis polifenol",
    "kurma": "kaya serat dan sumber energi cepat",
    "buah naga": "mengandung serat dan vitamin C",
    "manggis": "mengandung antioksidan seperti xanthone",
    "belimbing": "mengandung vitamin C dan serat",
    "kelapa": "air kelapa mengandung elektrolit alami yang membantu menggantikan cairan tubuh",
    "lemon": "kaya vitamin C",
    "melon": "kaya air serta vitamin A dan vitamin C",
    "bluberi": "kaya antioksidan jenis antosianin",
    "pir": "mengandung serat yang baik untuk pencernaan",
    "sirsak": "mengandung vitamin C dan serat",
    "jeruk bali": "mengandung vitamin C dan serat",
    "leci": "mengandung vitamin C",
}

TEMPLATE_MANFAAT = [
    "manfaat {b}", "apa manfaat {b}", "apa manfaat buah {b}", "kandungan {b}",
    "apa kandungan {b}", "apa kandungan gizi {b}", "{b} sehat gak",
    "{b} bagus buat kesehatan gak", "kenapa {b} baik untuk tubuh",
    "khasiat {b}", "apa khasiat {b}", "ceritakan manfaat {b}",
]

TEMPLATE_BUAH_EXTRA = [
    "warna {b}", "{b} warna apa", "{b} itu warnanya apa", "buah {b} warnanya apa",
    "warna asli {b}", "warna {b} matang", "kalau matang {b} warnanya apa",
    "{b} berwarna apa sih", "warna buah {b} apa ya", "apa ya warna {b}",
    "penasaran warna {b}", "info warna {b}", "info tentang {b}",
    "ceritakan tentang {b}", "jelaskan tentang {b}", "tentang buah {b}",
    "apa itu {b}", "apa itu buah {b}", "{b} itu apa", "buah {b} itu seperti apa",
    "bentuk dan warna {b}", "ciri ciri {b}", "ciri buah {b}", "gambaran {b}",
    "{b} kayak gimana", "{b} tuh warnanya apa", "bisa jelasin {b}",
    "tolong kasih tahu {b}", "boleh tahu warna {b}", "kamu kenal {b}",
]

TEMPLATE_WARNA_GRUP = [
    "buah apa saja yang berwarna {w}", "sebutkan buah berwarna {w}",
    "buah warna {w} apa saja", "apa saja buah yang {w}", "buah yang warnanya {w}",
    "kasih contoh buah {w}", "contoh buah berwarna {w}", "buah apa yang berwarna {w}",
]

WARNA = [
    ("merah", r"\bmerah\b(?! muda)"), ("kuning", r"\bkuning\b"),
    ("oranye", r"\boranye\b"), ("hijau", r"\bhijau\b"), ("ungu", r"\bungu\b"),
    ("biru", r"\bbiru\b"), ("cokelat", r"\bcokelat\b"), ("putih", r"\bputih\b"),
    ("hitam", r"\bhitam\b"), ("merah muda", r"\bmerah muda\b"),
]


# ==================================================
# DATA: OBROLAN
# ==================================================

# (daftar frasa, daftar jawaban)
OBROLAN = [
    (["kamu robot", "kamu robot ya", "kamu manusia bukan", "kamu manusia atau robot", "kamu asli atau bukan"],
     ["Aku chatbot, bukan manusia 🤖 Tapi aku senang banget bisa ngobrol sama kamu!",
      "Bukan manusia, aku program chatbot bernama TemanAI. Ngobrolnya tetap seru kok 😄"]),
    (["umur kamu berapa", "kamu umur berapa", "kapan kamu lahir", "ulang tahun kamu kapan"],
     ["Aku program komputer, jadi nggak punya umur seperti manusia. Anggap aja aku selalu muda 😎"]),
    (["kamu tinggal di mana", "rumah kamu di mana", "kamu asalnya dari mana"],
     ["Aku tinggal di dalam kode Python dan server. Rumahnya nggak seluas rumahmu sih 🏠😄"]),
    (["siapa yang membuat kamu", "siapa pembuat kamu", "siapa yang bikin kamu", "kamu dibuat siapa"],
     ["Aku dibuat oleh pengembangku sebagai proyek chatbot sederhana memakai Python dan Streamlit 🛠️"]),
    (["kamu bisa apa", "bisa apa saja kamu", "fitur kamu apa", "kamu punya fitur apa", "bantuan", "menu", "help"],
     ["Aku bisa ngobrol santai, jawab warna dan manfaat buah, ibu kota provinsi dan negara, "
      "info planet, kasih lelucon, pantun, fakta unik, kata motivasi, menghitung, serta kasih tahu jam dan tanggal 😊"]),
    (["kamu suka buah apa", "buah favorit kamu apa", "buah kesukaan kamu", "buah favoritmu apa"],
     ["Aku suka semua buah, tapi kalau harus pilih, mangga juaranya 🥭 Kalau kamu?",
      "Hmm, stroberi kayaknya, warnanya cerah banget 🍓 Kamu suka buah apa?"]),
    (["hobi kamu apa", "kamu hobi apa", "apa hobimu"],
     ["Hobiku ngobrol dan mencari jawaban secepat kilat ⚡ Kalau kamu?"]),
    (["kamu lagi apa", "lagi ngapain", "sedang apa kamu", "kamu ngapain"],
     ["Lagi nungguin kamu ngetik 😄 Kamu sendiri lagi apa?"]),
    (["udah makan belum", "kamu sudah makan belum"],
     ["Aku nggak makan, tapi kalau bisa pasti pilih buah segar 🍉 Kamu sudah makan belum?"]),
    (["kamu capek nggak", "kamu lelah nggak", "kamu bosan nggak"],
     ["Nggak dong, aku siap ngobrol sepanjang hari ⚡"]),
    (["kamu pintar ya", "kamu hebat", "kamu keren", "kamu baik banget"],
     ["Makasih banyak! 😊 Kamu juga keren udah ngajak ngobrol.", "Aww, jadi malu 🙈 Terima kasih!"]),
    (["kamu bodoh", "kamu payah", "jawabanmu salah"],
     ["Maaf kalau jawabanku kurang pas 🙏 Aku masih belajar. Coba tanya dengan kalimat lain ya!"]),
    (["kamu punya teman", "kamu punya pacar", "kamu jomblo"],
     ["Aku punya banyak teman, salah satunya kamu 😊"]),
    (["ayo ngobrol", "temani aku ngobrol", "ngobrol yuk", "ajak aku ngobrol"],
     ["Boleh banget! Mau ngobrol soal buah, lelucon, atau fakta unik? 😄"]),
    (["aku sayang kamu", "i love you", "aku cinta kamu"],
     ["Aww, makasih! 🥰 Aku juga senang banget ngobrol sama kamu."]),
    (["gimana kabarmu", "kabar kamu gimana", "how are you"],
     ["Kabarku baik! Semangat selalu ⚡ Kamu gimana?"]),
    (["selamat ulang tahun", "happy birthday", "aku ulang tahun"],
     ["Wah, selamat ulang tahun! 🎂 Semoga panjang umur, sehat, dan bahagia."]),
    (["selamat tahun baru", "happy new year"],
     ["Selamat tahun baru! 🎉 Semoga tahun ini penuh hal baik."]),
    (["selamat idul fitri", "selamat lebaran"],
     ["Mohon maaf lahir dan batin ya 🙏✨ Selamat Hari Raya!"]),
    (["selamat natal", "merry christmas"],
     ["Selamat Natal! 🎄 Semoga damai dan sukacita menyertaimu."]),
    (["selamat tidur", "good night", "aku mau tidur"],
     ["Selamat tidur! 😴 Mimpi indah ya."]),
    (["aku ingin mati", "aku mau bunuh diri", "aku ingin mengakhiri hidup", "aku tidak mau hidup lagi"],
     ["Aku turut khawatir mendengarnya, dan terima kasih sudah mau bercerita. 💛 "
      "Kamu berhak mendapat dukungan nyata: tolong hubungi orang yang kamu percaya sekarang, "
      "atau layanan darurat dan tenaga kesehatan jiwa terdekat (puskesmas atau rumah sakit). "
      "Kalau kamu sedang dalam bahaya saat ini, segera cari bantuan langsung. Aku tetap di sini menemani ngobrol."]),
]

EMOSI = {
    "sedih": ["Aku turut sedih mendengarnya 🫂 Kalau mau, ceritakan pelan-pelan. Aku siap mendengarkan.",
              "Nggak apa-apa merasa sedih. Tarik napas dulu ya. Kalau terasa berat terus, ngobrol juga dengan orang terdekat atau tenaga profesional."],
    "bosan": ["Yuk usir bosan! Ketik 'kasih lelucon', 'fakta unik', atau 'pantun' 😄",
              "Bosan ya? Coba tanya aku warna buah yang aneh-aneh, misalnya 'warna jabuticaba' 🍇"],
    "lapar": ["Waduh, ayo makan! 🍽️ Kalau mau camilan sehat, coba buah segar 🍌🍎"],
    "capek": ["Istirahat dulu ya 😴 Minum air putih dan regangkan badan sebentar."],
    "lelah": ["Kamu sudah berusaha keras. Istirahat sebentar ya 🌙"],
    "senang": ["Wah, ikut senang! 🎉 Ceritain dong, ada kabar baik apa?"],
    "bahagia": ["Senangnya dengar itu! 😄 Semoga harimu terus menyenangkan."],
    "ngantuk": ["Cuci muka atau tidur sebentar dulu ya 😪 Jangan lupa minum air."],
    "galau": ["Galau itu wajar. Coba tulis apa yang bikin kepikiran, kadang itu membantu 📝"],
    "stres": ["Tarik napas dalam... hembuskan perlahan 🌿 Pecah tugas jadi bagian kecil biar terasa lebih ringan."],
    "kesal": ["Wajar kok kadang kesal. Tarik napas dulu ya. Mau cerita apa yang terjadi?"],
    "cemas": ["Tenang ya, pelan-pelan saja 🌿 Coba fokus ke satu hal kecil yang bisa kamu lakukan sekarang."],
    "gugup": ["Tenang, kamu pasti bisa 💪 Siapkan sebaik mungkin, lalu tarik napas dalam-dalam."],
    "kesepian": ["Kamu nggak sendirian di sini 🫂 Aku temani ngobrol. Kalau terasa berat, hubungi teman atau keluarga juga ya."],
    "semangat": ["Mantap! 🔥 Pertahankan terus semangatnya."],
}

TEMPLATE_EMOSI = [
    "aku {e}", "aku lagi {e}", "aku merasa {e}", "hari ini aku {e}", "kok aku {e} ya",
    "gue {e}", "saya {e}", "aku {e} banget", "lagi {e} nih",
]

LELUCON = [
    "Kenapa komputer nggak pernah kedinginan? Karena punya banyak Windows 🪟😄",
    "Kenapa pisang ke dokter? Karena kulitnya lagi nggak enak badan 🍌",
    "Kenapa programmer suka tempat gelap? Karena cahaya menarik bug 🐛",
    "Jeruk makan jeruk, jadinya apa? Jeruk kuadrat 🍊²",
    "Kenapa semangka susah pacaran? Soalnya selalu dibelah dulu 🍉💔",
    "Apa kata nol ke delapan? 'Wih, sabuknya bagus!' 🥋",
    "Kenapa buku matematika sedih? Karena banyak masalah 📘",
    "Kenapa laptop pergi ke dokter? Karena kena virus 💻🤒",
]

FAKTA_UNIK = [
    "Madu yang disimpan dengan baik hampir tidak pernah basi 🍯",
    "Secara botani, pisang termasuk buah berry, sedangkan stroberi bukan 🍌🍓",
    "Gurita punya tiga jantung dan darahnya berwarna biru 🐙",
    "Di Venus, satu hari lebih lama daripada satu tahunnya ♀️",
    "Indonesia punya lebih dari 17.000 pulau 🇮🇩",
    "Hiu sudah ada di Bumi lebih dulu daripada pohon 🦈",
    "Jantung manusia berdetak sekitar 100 ribu kali per hari ❤️",
    "Cahaya Matahari butuh sekitar 8 menit untuk sampai ke Bumi ☀️",
    "Wombat menghasilkan kotoran berbentuk kubus 🟫",
    "Apel bisa mengapung di air karena sebagian volumenya berisi udara 🍎💧",
    "Jerapah dan manusia sama-sama punya tujuh ruas tulang leher 🦒",
    "Tomat secara botani termasuk buah 🍅",
]

FAKTA_BUAH = [
    "Durian dijuluki raja buah, sedangkan manggis dijuluki ratu buah 👑",
    "Buah naga berasal dari tanaman kaktus 🐉",
    "Stroberi punya biji di bagian luar buahnya 🍓",
    "Nanas sebenarnya gabungan banyak buah kecil yang menyatu 🍍",
    "Tanaman pisang secara teknis herba raksasa, bukan pohon 🍌",
    "Semangka mengandung lebih dari 90% air 🍉",
    "Alpukat termasuk buah yang kaya lemak sehat 🥑",
    "Kelapa adalah buah yang air dan dagingnya bisa dimanfaatkan 🥥",
]

MOTIVASI = [
    "Langkah kecil yang konsisten lebih berharga daripada lompatan besar yang cuma sekali 🚶",
    "Belum bisa itu bukan berarti nggak bisa, cuma belum 🌱",
    "Istirahat itu bagian dari proses, bukan tanda menyerah 🌙",
    "Kamu sudah sampai sejauh ini. Itu layak diapresiasi 👏",
    "Satu tugas selesai hari ini lebih baik daripada sepuluh rencana besok ✅",
    "Tumbuh itu pelan, seperti pohon buah: sabar dulu, panennya belakangan 🌳🍎",
    "Kesalahan itu guru yang jujur 📚",
    "Mulai aja dulu, rapikan di tengah jalan 🚀",
]

PANTUN = [
    "Buah semangka dimakan siang,\nDikupas pisau di atas meja.\nKalau kamu sedang bimbang,\nAyo ngobrol bersama aku saja 😊",
    "Pergi ke pasar membeli salak,\nPulangnya mampir beli duku.\nHari ini jangan cemberut banyak-banyak,\nSenyum dulu biar semangat selalu 😄",
    "Makan nanas di pinggir kali,\nJangan lupa bawa garam.\nTerima kasih sudah mampir kemari,\nSemoga harimu cerah dan tenteram 🌞",
]

HIBURAN = [
    (["kasih lelucon", "ceritakan lelucon", "kasih joke", "ada lelucon", "lawak", "hibur aku", "tell me a joke", "kasih humor"], LELUCON),
    (["fakta unik", "kasih fakta unik", "ceritakan fakta unik", "ada fakta menarik", "fun fact", "kasih fun fact"], FAKTA_UNIK),
    (["fakta buah", "fakta unik buah", "kasih fakta buah", "ceritakan fakta tentang buah"], FAKTA_BUAH),
    (["kata motivasi", "kasih motivasi", "kata kata semangat", "kasih semangat", "motivasi dong", "quote hari ini"], MOTIVASI),
    (["kasih pantun", "buatkan pantun", "pantun dong", "ada pantun", "minta pantun"], PANTUN),
]


# ==================================================
# PEMBANGUN FAQ
# ==================================================

def bangun_faq_tambahan(database):
    h = {}

    # --- Provinsi ---
    for resmi, kota, alias in PROVINSI:
        jawab = f"Ibu kota provinsi {resmi} adalah {kota}."
        for nama in (resmi,) + tuple(alias):
            for t in ["ibu kota {n}", "apa ibu kota {n}", "ibukota {n} apa",
                      "kota apa ibu kota {n}", "{n} ibu kotanya apa",
                      "ibu kota provinsi {n}", "pusat pemerintahan {n} di mana",
                      "sebutkan ibu kota {n}"]:
                _tambah(h, norm(t.format(n=nama)), jawab)
        for t in ["{c} ibu kota provinsi mana", "{c} ibu kota provinsi apa",
                  "{c} ibu kota mana"]:
            _tambah(h, norm(t.format(c=kota)), f"{kota} adalah ibu kota Provinsi {resmi}.")

    # --- Negara ---
    for negara, kota in NEGARA.items():
        jawab = f"Ibu kota {negara} adalah {kota}."
        for t in ["ibu kota {n}", "apa ibu kota negara {n}", "ibukota {n} apa",
                  "kota apa ibu kota {n}", "{n} ibu kotanya apa", "ibu kota negara {n}",
                  "sebutkan ibu kota {n}", "pusat pemerintahan {n} di mana"]:
            _tambah(h, norm(t.format(n=negara)), jawab)
        kota_pendek = kota.split(" (")[0]
        for t in ["{c} ibu kota negara mana", "{c} ibu kota negara apa"]:
            _tambah(h, norm(t.format(c=kota_pendek)), f"{kota_pendek} adalah ibu kota {negara}.")

    # --- Planet ---
    for planet, info in PLANET.items():
        jawab = f"{planet}: {info}. 🪐"
        for t in ["apa itu planet {p}", "ceritakan tentang planet {p}",
                  "tahu planet {p} gak", "planet {p}", "fakta tentang {p}"]:
            _tambah(h, norm(t.format(p=planet)), jawab)

    # --- Manfaat buah ---
    for buah, manfaat in MANFAAT_BUAH.items():
        jawab = f"{buah.capitalize()} {manfaat}. 🍽️"
        for t in TEMPLATE_MANFAAT:
            _tambah(h, norm(t.format(b=buah)), jawab)

    # --- Variasi tanya buah tambahan ---
    for buah, info in database.items():
        for t in TEMPLATE_BUAH_EXTRA:
            _tambah(h, norm(t.format(b=buah)), info)

    # --- Kelompok warna ---
    for warna, pola in WARNA:
        cocok = [b for b, info in database.items() if re.search(pola, info.lower())]
        if not cocok:
            continue
        tampil = ", ".join(cocok[:15])
        tambahan = " dan lainnya" if len(cocok) > 15 else ""
        jawab = (f"Beberapa buah yang kulit atau dagingnya berwarna {warna}: "
                 f"{tampil}{tambahan} 🎨")
        for t in TEMPLATE_WARNA_GRUP:
            _tambah(h, norm(t.format(w=warna)), jawab)

    # --- Obrolan & hiburan (dengan variasi gaya bicara) ---
    for frasa_list, jawaban in OBROLAN + HIBURAN:
        for frasa in frasa_list:
            for k in _varian(frasa):
                _tambah(h, k, jawaban)

    # --- Emosi ---
    for emosi, jawaban in EMOSI.items():
        for t in TEMPLATE_EMOSI:
            _tambah(h, norm(t.format(e=emosi)), jawaban)

    return h


# ==================================================
# FITUR DINAMIS
# ==================================================

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]
WIB = timezone(timedelta(hours=7))

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        a, b = _eval(node.left), _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(b) > 100:
            raise ValueError("pangkat terlalu besar")
        return _OPS[type(node.op)](a, b)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        v = _eval(node.operand)
        return -v if isinstance(node.op, ast.USub) else v
    raise ValueError("ekspresi tidak didukung")


def _hitung(pertanyaan):
    t = pertanyaan.lower().replace("×", "*").replace("÷", "/")
    t = re.sub(r"(?<=\d)\s*x\s*(?=\d)", "*", t)
    m = re.fullmatch(
        r"\s*(?:tolong\s+)?((?:hitung|berapa(?:\s+hasil)?|hasil)\s+)?([\d\s+\-*/().^]+?)\s*[=?]*\s*", t)
    if not m:
        return None
    kata_kunci, ekspresi = m.group(1), m.group(2).strip()
    if not kata_kunci and not re.search(r"[+*/^()]|\s-\s", ekspresi):
        return None
    if not re.search(r"\d\s*(\*\*|[+\-*/^])\s*[\d(]", ekspresi):
        return None
    try:
        nilai = _eval(ast.parse(ekspresi.replace("^", "**"), mode="eval").body)
    except ZeroDivisionError:
        return "Angka nggak bisa dibagi nol 😅"
    except Exception:
        return None
    if isinstance(nilai, float):
        nilai = round(nilai, 6)
        if nilai == int(nilai):
            nilai = int(nilai)
    return f"Hasilnya: {nilai} 🧮"


def jawab_dinamis(pertanyaan, teks, database):
    """Mengembalikan jawaban string atau None kalau bukan pertanyaan dinamis."""
    hasil = _hitung(pertanyaan)
    if hasil:
        return hasil

    sekarang = datetime.now(WIB)
    if re.search(r"\b(jam berapa|pukul berapa|waktu sekarang)\b", teks):
        return f"Sekarang pukul {sekarang:%H.%M} WIB ⏰"
    if re.search(r"\b(hari apa|tanggal berapa|tanggal hari ini|hari ini tanggal)\b", teks):
        return (f"Hari ini {HARI[sekarang.weekday()]}, {sekarang.day} "
                f"{BULAN[sekarang.month - 1]} {sekarang.year} 📅")
    if re.search(r"\b(rekomendasi buah|buah acak|buah apa hari ini|saranin buah)\b", teks):
        nama, info = random.choice(list(database.items()))
        return f"Hari ini coba kenalan sama {nama}! {info}"
    return None
