from openai import OpenAI

client = OpenAI()


def inference_about_data(data):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="""I will provide  the data based on this  provide code for basic Data visualisation 
        your response format should provide only python coed no explanation is needed
        """
    )

    return response