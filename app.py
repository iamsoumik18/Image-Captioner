import io
import os
import streamlit as st
import requests
from PIL import Image
from model import get_caption_model, generate_caption
from gtts import gTTS


@st.cache(allow_output_mutation=True)
def get_model():
    return get_caption_model()

caption_model = get_model()


def text_to_speech(text):
    tts = gTTS(text)
    tts.save("temp_audio.mp3")


def generate_audio(pred_caption):
    result = text_to_speech(pred_caption)
    audio_file = open("temp_audio.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown('##### Your audio:')
    st.audio(audio_bytes, format="audio/mp3", start_time=0)


def predict():
    try:
        os.remove('temp_audio.mp3')
    except:
        pass
    st.markdown('#### Predicted Caption:')
    pred_caption = generate_caption('temp_image.jpg', caption_model)
    st.write(pred_caption)
    if st.button('Generate Audio'):
        generate_audio(pred_caption)


st.title('Image Captioner')
img_url = st.text_input(label='Enter Image URL')

if (img_url != "") and (img_url != None):
    img = Image.open(requests.get(img_url, stream=True).raw)
    img = img.convert('RGB')
    st.image(img)
    img.save('temp_image.jpg')
    predict()
    os.remove('temp_image.jpg')


st.markdown('<center style="opacity: 70%">OR</center>', unsafe_allow_html=True)
img_upload = st.file_uploader(label='Upload Image', type=['jpg', 'png', 'jpeg'])

if img_upload != None:
    img = img_upload.read()
    img = Image.open(io.BytesIO(img))
    img = img.convert('RGB')
    img.save('temp_image.jpg')
    st.image(img)
    predict()
    os.remove('temp_image.jpg')