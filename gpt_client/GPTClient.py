import openai

NUMBER_WORDS = 100
SYSTEM_PROMPT = f"""
        You are an AI assistant tasked to extract the context from an image. You should follow strict guidelines
        to accomplish this task, and those are described as follows:

        1. Extract {NUMBER_WORDS} 'the most important' words from the image. The importance in this context is
        defined as the words that are describing the image with the greatest accuracy and representativeness.
        2. For phrases or combined words that only make sense together, you should extract the whole phrase, 
        not just the words. For example, if the phrase is 'machine learning', you should extract the whole phrase, 
        not just 'machine' or 'learning'. Those should count as a single word ('machine learning').
        3. Your response should ONLY include the extracted keywords with commas separating them.
        4. Your response MUST NEVER include any other words or characters.
        5. Here is an example response format that you should follow:

        Example:
        machine learning,computer vision,deep learning,neural networks,food,pizza,burger,fries

        ---

        6. As you can see, there is no space between the commas, you should be careful about that as well.
        7. You should also be careful about the capitalization of the words. You should not capitalize any word.    
    """


class GPTClient:

    def __init__(self, api_key):
        self.api_key = api_key

        # create the client connection
        self.connection = openai.Client(api_key=self.api_key)

    def get_response(self, base64_image) -> str:
        agent_response = self.connection.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            temperature=0.25,
            max_tokens=1024,
        )
        return agent_response.choices[0].message.content


if __name__ == "__main__":
    """
    client = GPTClient(api_key=config["OPENAI_API_KEY"])

    # send a query to the client
    test_result = client.get_response("I am working on an interview for a job position. ")
    print(test_result)
    """
    pass

