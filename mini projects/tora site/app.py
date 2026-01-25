import streamlit as st
import requests

# ------------------- CONFIGURAÇÃO -------------------
st.set_page_config(page_title="ספריית קודש", layout="wide")

# ------------------- CSS FORÇADO -------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@400;700&display=swap');

/* Fundo azul claro e RTL */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom right, #a0c4ff, #80d0ff);
    direction: rtl;
    text-align: right;
    font-family: 'Frank Ruhl Libre', serif;
}

/* Esconder menu e footer do Streamlit */
header.stAppHeader {display: none;}
footer {display: none;}
[data-testid="stAppViewContainer"] > div:first-child {padding-top: 0px;}

/* Sticky header no topo completo */
/* Header full width ocupando todo topo */
#header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100vw;  /* usa 100% da viewport */
    background-color: #1565C0;
    color: white;
    font-size: 50px;
    font-weight: bold;
    text-align: center; /* ou left se quiser à esquerda */
    padding: 15px 0;
    z-index: 9999;
    letter-spacing: 2px;
}


/* Ajuste do container principal para não ficar por baixo do header */
[data-testid="stVerticalBlock"] {
    margin-top: 110px;
}

/* Versículo grande à direita */
.hebrew-big {
    font-size: 48px;
    font-weight: 700;
    text-align: right;
    direction: rtl;
    color: #0D47A1;
    margin: 25px 0;
}

/* Caixa de comentaristas */
.mefarsim-box {
    background: #bbdefb;
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
    font-size: 22px;
    text-align: right;
    direction: rtl;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
}

/* Botão moderno */
.stButton>button {
    width: auto;      /* não ocupa 100% da coluna */
    min-width: 150px; /* largura mínima */
    max-width: 250px; /* largura máxima */
    padding: 8px 15px;
    font-size: 18px;
}
.stButton>button:hover {
    background-color: #0D47A1;
}
           

/* Forçar selects e labels RTL e fontes estilizadas */
.css-1aumxhk, .css-1v3fvcr, .stSelectbox>div>div>div>div { 
    width: auto !important;
    max-width: 250px;
    font-size: 18px;        
    direction: rtl; 
    text-align: right; 
    font-family: 'Frank Ruhl Libre', serif;
    font-size: 20px;
    font-weight: 600;
}

/* Forçar opções dentro dos menus RTL */
.css-10trblm div[role="option"] {
    direction: rtl;
    text-align: right;
    font-family: 'Frank Ruhl Libre', serif;
    font-size: 20px;
}

/* Ajuste para todos os selects aparecerem para baixo consistentemente */
div[data-baseweb="select"] > div > div:first-child {
    direction: rtl;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

# ------------------- TÍTULO FIXO -------------------
st.markdown('<div id="header">📖 ספריית קודש</div>', unsafe_allow_html=True)

# ------------------- FUNÇÕES -------------------
def get_sefaria(ref):
    try:
        url = f"https://www.sefaria.org/api/texts/{ref}?context=0&commentary=0"
        return requests.get(url).json()
    except:
        return None

def int_to_hebrew(n):
    hebrew_letters = ["א","ב","ג","ד","ה","ו","ז","ח","ט","י",
                      "יא","יב","יג","יד","טו","טז","יז","יח","יט","כ"]
    return hebrew_letters[n-1] if 1 <= n <= len(hebrew_letters) else str(n)

# ------------------- MAPA DE LIVROS -------------------
livros = {
    "בראשית": "Bereshit",
    "שמות": "Shemot",
    "ויקרא": "Vayikra",
    "במדבר": "Bamidbar",
    "דברים": "Devarim"
}

# ------------------- FLUXO PROGRESSIVO -------------------
livro_selecionado = st.selectbox("בחר ספר", list(livros.keys()), key="livro")

if livro_selecionado:
    livro_en = livros[livro_selecionado]

    # Etapa 2: Escolher capítulo
    capitulo_data_all = get_sefaria(livro_en)
    total_capitulos = len(capitulo_data_all['he']) if capitulo_data_all and 'he' in capitulo_data_all else 50
    capitulos_he = [int_to_hebrew(i+1) for i in range(total_capitulos)]

    perek_selecionado = st.selectbox("בחר פרק", capitulos_he, key="perek")
    perek_index = capitulos_he.index(perek_selecionado) + 1

    # Etapa 3: Escolher versículo
    capitulo_data = get_sefaria(f"{livro_en}.{perek_index}")
    if capitulo_data and 'he' in capitulo_data:
        total_psukim = len(capitulo_data['he'])
        psukim_he = [int_to_hebrew(i+1) for i in range(total_psukim)]
        pasuk_selecionado = st.selectbox("בחר פסוק", psukim_he, key="pasuk")
        pasuk_index = psukim_he.index(pasuk_selecionado) + 1

        # ------------------- OBTER PASUK -------------------
        ref_pasuk = f"{livro_en}.{perek_index}.{pasuk_index}"
        data = get_sefaria(ref_pasuk)
        if data and 'he' in data:
            st.markdown(f"<div class='hebrew-big'>{data['he']}</div>", unsafe_allow_html=True)

            # ------------------- BOTÃO MEFARSIM COM MENU PROGRESSIVO -------------------
            mostrar_mefarsim = st.button("מפרשים")
            if mostrar_mefarsim:
                mefarsim_lista = {
                    "רש\"י": f"Rashi on {ref_pasuk}",
                    "רמב\"ן": f"Ramban on {ref_pasuk}",
                    "אבן עזרא": f"Ibn Ezra on {ref_pasuk}",
                    "ספורנו": f"Sforno on {ref_pasuk}",
                    "אור החיים": f"Ohr HaChayim on {ref_pasuk}"
                }
                for nome, ref_mefarsim in mefarsim_lista.items():
                    with st.expander(nome):
                        m_data = get_sefaria(ref_mefarsim)
                        if m_data and 'he' in m_data:
                            texto = " ".join(m_data['he']) if isinstance(m_data['he'], list) else m_data['he']
                            st.markdown(f"<div class='mefarsim-box'>{texto}</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='mefarsim-box'>לא נמצא פירוש</div>", unsafe_allow_html=True)
        else:
            st.error("לא נמצא פסוק")
    else:
        st.error("Não foi possível carregar capítulo")
