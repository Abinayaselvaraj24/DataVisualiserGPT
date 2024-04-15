import streamlit as st
from openai import OpenAI

import os
from dotenv import load_dotenv
import base64
import io

from matplotlib import image as mpimg, pyplot as plt

import pandas as pd


csv_file_path = "netflix.csv"


df = pd.read_csv(csv_file_path)


from e2b_code_interpreter import CodeInterpreter

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)



def ask_and_respond(prompt,):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    encoded_prompt = f"I will provide the data in data frame and query your task is to generate data visualisation with matplolib and seaborn  you should give only  python code  no explanation is needed here is the dataframe  {df}  and here is the question {prompt} give me only code "

    print(encoded_prompt)

    with st.spinner('Processing...'):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": encoded_prompt}
                for m in st.session_state.messages
            ]
        )

    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

    code =response.choices[0].message.content




    with CodeInterpreter() as sandbox:
        sandbox.notebook.exec_cell("!pip install matplotlib")
        sandbox.notebook.exec_cell("!pip install seaborn")
        execution= sandbox.notebook.exec_cell(code)

    image = execution.results[0].png



    i = base64.b64decode(image)
    i = io.BytesIO(i)
    i = mpimg.imread(i, format='PNG')

    plt.imshow(i, interpolation='nearest')
    plt.show()

    plt.imshow(i, interpolation='nearest')
    # plt.savefig("data_vis_image.png")  # Save the image to a file
    # plt.close()
    #
    # image_file_path = "data_vis_image.png"  # Adjust the path if needed
    # if os.path.exists(image_file_path):
    #     st.image(image_file_path, caption='Data Visualization', use_column_width=True)
    # else:
    #     st.error("Image file not found.")




def main():
    start_message = st.chat_message("assistant")
    start_message.write("Hello there, what questions about Crypto can I help you with today?")
    start_message.write("Examples of questions I can answer:")
    examples = [
        "Brief About the Market Trends",
        "Explain about the  Projected growth",
        "What inference I can make ",
    ]
    example_buttons = [start_message.button(example) for example in examples]

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    for example, example_button in zip(examples, example_buttons):
        if example_button:
            ask_and_respond(example)

    chat_input_box = st.chat_input("What would you like to ask about?")
    if chat_input_box:
        ask_and_respond(chat_input_box)


if __name__ == "__main__":
    main()
