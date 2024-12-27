import openai

class OpenAI:
    @staticmethod
    def basiccall(api_key: str, model_name: str, prompt: str) -> str:
        """
        Makes a basic call to the OpenAI API.

        Args:
            api_key (str): Your OpenAI API key.
            model_name (str): The name of the OpenAI model (e.g., 'gpt-3.5-turbo').
            prompt (str): The input prompt for the model.

        Returns:
            str: The response text from OpenAI.
        """
        openai.api_key = api_key
        try:
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message['content']
        except Exception as e:
            return f"Error: {str(e)}"
