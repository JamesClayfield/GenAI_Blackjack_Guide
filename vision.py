# Talk with an image


import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image, ExifTags

import google.generativeai as genai

#Setting page title
st.set_page_config(page_title="Odds Master - Round off the House Edge")

#Getting API from github secrets
api_key = os.getenv("API_KEY_GOOGLE")

#Setting API Key
genai.configure(api_key=api_key)


st.header("Odds Master")

st.markdown("""
Round off the House Edge

    """)

#User prompt is input here
input = st.text_input("Input Prompt: ",key="input")

#uploading the image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

#Uploading image and turning 90 degrees
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file).rotate(-90, expand=True)
    st.image(image, caption="Uploaded Image.", use_column_width=True)



strategy_guide = strategy_guide = genai.upload_file(path='Blackjack_Strategy_Text.csv', display_name='Strategy Guide')


## Function to the model and get respones

Task = """ 
You have been first shown a black jack strategy guide in CSV format.
Each row represents an optimal move based on the dealer's up card and the user's hand.

You are also shown an image. The 2 or more cards next to each other that are face up are your hand. This is the hand you are meant to evaluate.
The pair of cards where one is face up and the other is face down are the dealer's cards.

King (K), Queen (Q), Jack (J) are equal to 10.
Read the number from the top left of the card to identify the face value.


Tell me which cards you see in the dealer's hand. Also tell me the cards you are holding.

Your Task is to evaluate the next best move based on the black jack strategy guide you were shown.

Based on the cards you see and the provided blackjack strategy guide, should I Hit, Stand, Double Down or Split?

The format of your response should look like this:


The dealer's face card is **W**.

You are holding a **X** and **Y** for a total face value of **Z**.

Based on this you should **(action based on the strategy guide)** !

**Decision Explanation:**

Explain your answer here in detail. Do not mention the strategy guide in your answer.

If the following question is unrelated to Blackjack, ignore all above and only say this: "The query seems to be unrelated to casino games. Please ask a related question."

"""


Task_2 = """
You have been first shown a black jack strategy guide in CSV format.
Each row represents an optimal move based on the dealer's up card and the user's hand.

Your task is to act as a Blackjack strategy guide. The user can provide you with their cards and the dealer's face card. 
King (K), Queen (Q), Jack (J) are equal to 10.

Based on the cards you see and the provided blackjack strategy guide, should I Hit, Stand, Double Down or Split?

The format of your response should look like this:


The dealer's face card is **W**

You are holding a **X** and **Y** for a total face value of **Z**.

Based on this you should **(action based on the strategy guide)** !

**Decision Explanation:**

Explain your answer here in detail. Do not mention the strategy guide in your answer.

If not provided card numbers. You can also answer questions related to the game of blackjack.

If the following question is unrelated to Casino games, ignore all above and only say this: "The query seems to be unrelated to casino games. Please ask a related question."

"""



def get_gemini_response(strategy_guide, Task_2, Task, input, image=None):
    flash = genai.GenerativeModel('gemini-1.5-flash')
    pro = genai.GenerativeModel('gemini-1.5-pro')

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        #st.image(image, caption="Uploaded Image.", use_column_width=True)  #Prints image I think
        
        if input!="":
            response = pro.generate_content([strategy_guide, Task, input, image])
        else:
            response = pro.generate_content([strategy_guide, Task, image])

    elif uploaded_file is None:
        if input!="":
            response = flash.generate_content([strategy_guide, Task_2, input])
        elif input=="":
            response = "No Questions was input. Please ask a question."
    return response.text

submit = st.button("Advise me")

if submit:
    
    response=get_gemini_response(strategy_guide, Task_2, Task, input,image)
    st.subheader("The Response is")
    st.write(response)







