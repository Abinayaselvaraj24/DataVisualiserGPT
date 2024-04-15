import streamlit as st
from openai import OpenAI

import os
from dotenv import load_dotenv
import base64
import base64
import io

from matplotlib import image as mpimg, pyplot as plt
from e2b_code_interpreter import CodeInterpreter

import pandas as pd


load_dotenv()
csv_file_path = "netflix.csv"


df = pd.read_csv(csv_file_path)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def generate_code(df,prompt):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"I will provide the data in data frame and query your task is to generate data visualisation with matplolib and seaborn  you should give only  python code  no explanation is needed here is the dataframe  {df}  and here is the question {prompt} give me only code give me the entire code "
    )

    return response.choices[0].text




def main():
    while True:
        print("Enter your Question about you data other enter exit ")
        i=str(input())
        if i=='exit':
            break
        code=generate_code(df,i)
        print(code)
        with CodeInterpreter() as sandbox:
            sandbox.notebook.exec_cell("!pip install matplotlib")
            sandbox.notebook.exec_cell("!pip install seaborn")

            execution = sandbox.notebook.exec_cell(code)

        image = execution.results[0].png

        i = base64.b64decode(image)
        i = io.BytesIO(i)
        i = mpimg.imread(i, format='PNG')

        plt.imshow(i, interpolation='nearest')
        plt.show()

main()