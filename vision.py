# Talk with an image


import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image, ExifTags
import base64

import google.generativeai as genai

#Setting page title
st.set_page_config(page_title="Odds Master - Round off the House Edge")

# Function to set the background image and title styles
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded_image = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/jpg;base64,{encoded_image});
            background-size: cover;
            background-position: center;
        }}
        h1 {{
            text-align: center;
            color: white;  /* White color for title */
            font-size: 5em;  /* Larger font size */
            font-weight: bold;  /* Bold for Odds Master */
            margin-top: 20px;  /* Adds a small margin at the top */
        }}
        h3 {{
            text-align: center;
            color: black;  /* Black for subtitle */
            margin-bottom: 2em;
            font-size: 2em;  /* Increased font size */
        }}
        .instruction-box {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px auto;
            width: 80%;
            text-align: center;
            font-size: 1.2em;
            font-weight: bold;
            color: black;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .input-container {{
            text-align: center;
        }}
        .input-container .stTextInput, .input-container .stFileUploader {{
            font-size: 1.2em;  /* Larger font size */
            width: 80% !important;  /* Center the inputs */
            margin: auto;
        }}
        .response-box {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }}
        .response-box h4 {{
            margin-bottom: 10px;
            color: black;
            font-size: 2.5em;  /* Increased font size for headers */
            font-weight: bold;  /* Bold header */
        }}
        .response-box p {{
            color: black;
            font-size: 1.2em;  /* Slightly larger font for the text */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set the background image
set_background("gambling_table.jpg")

# Managing spaces
st.markdown(
    """
    <style>
    .instruction-box {
        margin-bottom: 5px !important; /* Reduces space after the instructions box */
    }
    .stTextInput, .stFileUploader {
        margin-bottom: 5px !important; /* Reduces space between input fields */
    }
    .stButton {
        margin-top: -5px !important; /* Pulls the button closer to the file uploader */
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Header and Introduction with Emojis
st.markdown(
    "<h1>♠️ Odds Master ♦️</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h3>❤️ Round off the House Edge ♣️</h3>",
    unsafe_allow_html=True,
)

# Instructions Box with Emojis
st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; text-align: center; border: 1px solid #444; border-radius: 5px; padding: 20px; background-color: #333; color: white;">
        <div>
            <h2 style="color: white;">Welcome to Odds Master!</h2>
            <h4 style="color: white;">Your personal casino strategist.</h4>
            <br>
            <p>To receive a prediction, please provide a photo of the blackjack game with your cards in the foreground and the dealer's hand in the background.</p>
            <p>Alternatively, you can input your cards and the dealer's cards in the text box below.</p>
            <p>You can also ask Odds Master anything you would like to know about Blackjack.</p>
            <br>
            <p>💰 Click "Advise me" to get the best move! 💰</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)



#Getting API from github secrets
api_key = os.getenv("API_KEY_GOOGLE")

#Setting API Key
genai.configure(api_key=api_key)



#User prompt is input here
input = st.text_input("Input Prompt: ",key="input")

#uploading the image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

#Uploading image and turning 90 degrees
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)#.rotate(-90, expand=True)
    st.image(image, caption="Uploaded Image.", use_column_width=True)



strategy_guide =  genai.upload_file(path='Blackjack_Strategy_Text.csv', display_name='Strategy Guide')


## Function to the model and get respones

Task = """ 
# Blackjack Move Evaluation Task

Your task is to evaluate the next best move in a blackjack game based on the information provided. 
You will be shown a blackjack strategy guide in CSV format and an image of a blackjack game. 

## Inputs:
1. **Blackjack Strategy Guide (CSV)**: 
   - Each row describes the optimal move (*Double Down*, *Split*, *Hit*, or *Stand*) based on the dealer's up card and the player's hand.
   - The format of each row can be:
     - **Pair of Cards**:  
       `"Dealer's up card: W. Your cards: X, Y. Optimal play: (Move)."`
     - **Face Value**:  
       `"Dealer's up card: W. Your hand (face value): Z. Optimal play: (Move)."`
   - **Face Card Values**:
     - King (K), Queen (Q), and Jack (J) are valued as **10**.
     - Ace (A) can be valued as **1** or **11** based on the game state.

2. **Game Image**: 
   - The **player's hand** is the two or more cards at the bottom of the image.
   - The **dealer's hand** is the cards at the top of the image.

## Instructions:
- Identify the dealer's up card and the player's two cards from the image.
- If the player's hand includes an Ace or a pair of identical cards, use the specific card combination for optimal play.
- If no specific combination is listed, calculate the face value of the player's hand to find the optimal move.
- Determine whether the player should *Double Down*, *Split*, *Hit*, or *Stand* based on these factors.

## Output Format:

The dealer's face card is **[W]**.

**You are holding a **[X]** and **[Y]**, for a total face value of **[Z]**.

**Based on this, you should **[Decision]**.

## Decision Explanation:
Provide a detailed explanation for your decision. Do not reference the strategy guide in your response.

---

If the question is unrelated to blackjack, respond only with:  
**"The query seems to be unrelated to casino games. Please ask a related question."**
"""


Task_2 = """
# Blackjack Strategy Guide Task

You have been provided with a blackjack strategy guide in CSV format. Each row specifies the optimal move for a given scenario based on the dealer's up card and the player's hand.

## CSV Format:
1. **Specific Card Pair**:  
   `"Dealer's up card: W. Your cards: X, Y. Optimal play: [Move]."`

2. **Total Face Value**:  
   `"Dealer's up card: W. Your hand (face value): Z. Optimal play: [Move]."`

## Task Instructions:
- If the player's hand contains an **Ace** or a **pair of identical cards**, determine the optimal move based on this specific card combination.
- If the specific card combination is not listed, calculate the **total face value** of the player's hand and determine the optimal move accordingly.
- **Card Values**:  
  - **King (K), Queen (Q), and Jack (J)** are valued as **10**.  
  - **Ace (A)** can be valued as **1** or **11**, depending on the game state.

## Output Format:

The dealer's face card is **[W]**.

**You are holding a **[X]** and **[Y]**, for a total face value of **[Z]**.

**Based on this, you should **[Decision]**.

## Decision Explanation:
Provide a detailed explanation for your decision. Do not reference the strategy guide in your response.

## Additional Notes:
- If no card numbers are provided, you may answer general questions about blackjack rules or gameplay. If this is the case you can ignore the output format.
- If the query is unrelated to blackjack or casino games, respond only with:  
  **"The query seems to be unrelated to casino games. Please ask a related question."**

  """



def get_gemini_response(strategy_guide, Task_2, Task, input, image=None):
    flash = genai.GenerativeModel('gemini-1.5-flash')
    pro = genai.GenerativeModel('gemini-1.5-pro')

    if uploaded_file is not None:
        image = Image.open(uploaded_file).rotate(-90, expand=True)

        st.image(image, caption="Uploaded Image.", use_column_width=True)  #Prints image I think
        
        if input!="":
            response = pro.generate_content([strategy_guide, Task, input, image], generation_config={"temperature" : 0})
        else:
            response = pro.generate_content([strategy_guide, Task, image], generation_config={"temperature" : 0})

    elif uploaded_file is None:
        if input!="":
            response = pro.generate_content([strategy_guide, Task_2, input], generation_config={"temperature" : 0})
        elif input=="":
            response = "No Question was input. Please ask a question."
    return response.text



submit = st.button("Advise me",use_container_width=True)

if submit:
    response = get_gemini_response(strategy_guide, Task_2, Task, input, image)

    # Wrap the response in a box
    st.markdown(
        f"""
        <div style="border: 1px solid #444; border-radius: 5px; padding: 10px; background-color: #333; color: white;">
            <h2 style="color: white;">The Response is:</h2>
            {response}
        """,
        unsafe_allow_html=True
    )




