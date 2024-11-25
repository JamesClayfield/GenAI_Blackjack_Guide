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



strategy_guide =  genai.upload_file(path='Blackjack_Strategy_Text.csv', display_name='Strategy Guide')


## Function to the model and get respones

Task = """ 
You have been shown a black jack strategy guide in CSV format.
Each row represents an optimal move based on the dealer's up card and the user's hand.

The format of each row of the csv is one of the following:

"Dealer's up card: W. Your cards: X, Y. Optimal play: Double Down, Split, Hit, Stay (depends which)."

"Dealer's up card: W. Your hand (face value): Z. Optimal play: Double Down, Split, Hit, Stay (depends which)."

You are also shown an image. The 2 or more cards at the bottom of the image are the player's hand. This is the hand you are meant to evaluate.
The cards at the top of the image are the dealer's cards.

If the player is holding an ace or a pair of the same cards, check the optimal move based on this specific card combination.

It it is not a listed combination, check for the face value to find the optimal move.


King (K), Queen (Q), Jack (J) are equal to 10.


Tell me which cards you see in the dealer's hand. Also tell me the cards you are holding.

Your Task is to evaluate the next best move based on the black jack strategy guide you were shown.

Based on the cards you see and the aforementioned instructions, should the player Double Down, Split, Hit or Stand?


The format of your response should look like this:

The dealer's face card is **W**.

You are holding a **X** and **Y** for a total face value of **Z**.

Based on this you should **(action based on the strategy guide)** !

**Decision Explanation:**

Explain your answer here in detail. Do not mention the strategy guide in your answer.

If the following question is unrelated to Blackjack, ignore all above and only say this: "The query seems to be unrelated to casino games. Please ask a related question."

"""


Task_2 = """
You have been shown a black jack strategy guide in CSV format.
Each row represents an optimal move based on the dealer's up card and the user's hand.

The format of each row of the csv is one of the following:

"Dealer's up card: W. Your cards: X, Y. Optimal play: Double Down, Split, Hit, Stay (depends which)."

"Dealer's up card: W. Your hand (face value): Z. Optimal play: Double Down, Split, Hit, Stay (depends which)."

If the player is holding an ace or a pair of the same cards, check the optimal move based on this specific card combination.

It it is not a listed combination, check for the face value to find the optimal move.

Your task is to act as a Blackjack strategy guide. The player can provide you with their cards and the dealer's face card. 
King (K), Queen (Q), Jack (J) are equal to 10.

Based on the player's cards and the aforementioned instructions, should the player Double Down, Split, Hit or Stand?

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
            response = pro.generate_content([strategy_guide, Task_2, input])
        elif input=="":
            response = "No Questions was input. Please ask a question."
    return response.text

submit = st.button("Advise me")

if submit:
    
    response=get_gemini_response(strategy_guide, Task_2, Task, input,image)
    st.subheader("The Response is")
    st.write(response)







