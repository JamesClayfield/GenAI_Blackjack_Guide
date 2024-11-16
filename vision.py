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
You have been first shown a black jack strategy guide. This shows which cards you should play based on the dealer's visible card and your hand:

- Green (S) means the player must Stand
- Yellow (H) means the player must Hit
- Red (D) means the player must Double Down
- Blue (SP) means player must Split

You are shown an image. The 2 or more cards at the bottom of the image are your hand. This is the hand you are meant to evaluate.
The cards at the top of the image are the dealer's cards. King (K), Queen (Q), Jack (J) are equal to 10.

Please tell me which cards you see in the dealer's hand. Please also tell me the cards you are holding.

Your Task is to evaluate the next best move based on the black jack strategy guide you were shown.

Based on the cards you see and the provided blackjack strategy guide, should I Hit, Stand, Double Down or Split?

The format of your response should look like this:

--------Blackjack Move Optimizer--------

The dealer is showing a **W**

You are holding a **X** and **Y** for a total face value of **Z**.

Based on this you should **(action based on the strategy guide)** !

**Decision Explanation:**

Explain your answer here in detail. Do not mention the strategy guide in your answer.

If the following question is unrelated to Blackjack, ignore all above and only say this: "The query seems to be unrelated to casino games. Please ask a related question."

"""




def get_gemini_response(input,image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if input!="":
       response = model.generate_content([strategy_guide, image, Task, input])
    else:
       response = model.generate_content([strategy_guide, image, Task])
    return response.text

##initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")

st.header("Blackjack Strategy Optimizer")
input=st.text_input("Input Prompt: ",key="input")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

strategy_guide = strategy_guide = genai.upload_file(path='Blackjack Strategy Guide.pdf', display_name='Strategy Guide')

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
