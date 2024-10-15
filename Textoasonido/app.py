import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.title("Conversión de Texto a Audio")

# Intenta cargar la imagen
try:
    image = Image.open('masmellow.jpg')
    st.image(image, width=350)
except FileNotFoundError:
    st.error("Imagen 'masmellow.jpg' no encontrada. Asegúrate de que el archivo esté en la ubicación correcta.")

with st.sidebar:
    st.subheader("Escribe y/o selecciona texto para ser escuchado.")

try:
    os.mkdir("temp")
except FileExistsError:
    pass

st.subheader("Una pequeña Fábula.")
st.write('Marshmello, un DJ que nunca hablaba, usaba su música para comunicarse con el mundo. '  
         'Un día, el pájaro Melodía le preguntó por qué no usaba palabras, y Marshmello respondió con una hermosa canción. ' 
         'Al escucharla, Melodía entendió que no todos necesitan hablar para transmitir sus sentimientos. '  
         'La música de Marshmello tocaba el corazón de todos, mostrando que existen muchas formas de expresarse. ' 
         'Mosy.'
        )
           
st.markdown("¿Quieres escucharlo? Copia el texto")
text = st.text_area("Ingrese el texto a escuchar.")

tld = 'com'
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ("Español", "English")
)
lg = 'es' if option_lang == "Español" else 'en'

def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    my_file_name = text[0:20] if len(text) >= 20 else "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("Convertir a Audio"):
    result, output_text = text_to_speech(text, tld, lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("## Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
        return href

    st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio File"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)
