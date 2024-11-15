# Talk with an image


import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image

import google.generativeai as genai

api_key = os.getenv("API_KEY_GOOGLE")

genai.configure(api_key=api_key)

## Function to the model and get respones

Task = """ 
Your Task is to evaluate the probability of getting a specified hand in texas hold em poker. 
You are shown an image. This image shows 2 poker cards in front of you. This is the hand you are meant to evaluate. 
The picture also shows 5 community cards. These 5 cards are either in the state of concealed, flop, turn or river. 

Based on the cards you see, the rules of texas hold em poker and bayesian probability, calculate the probability 
of receiving the hand in question by the time the river card is revealed.

"""




def get_gemini_response(input,image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if input!="":
       response = model.generate_content([Task, input,image])
    else:
       response = model.generate_content(Task, image)
    return response.text

##initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini Application")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the image")

## If ask button is clicked

if submit:
    
    response=get_gemini_response(input,image)
    st.subheader("The Response is")
    st.write(response)
