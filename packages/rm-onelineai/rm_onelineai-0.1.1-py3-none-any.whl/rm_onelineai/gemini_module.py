import google.generativeai as genai

class Gemini:
    @staticmethod
    def basiccall(api_key: str, model_name: str, prompt: str) -> str:
        """
        Makes a call to Gemini API to generate content.

        Args:
            api_key (str): Your Gemini API key.
            model_name (str): The Gemini model name (e.g., 'gemini-pro').
            prompt (str): The input prompt.

        Returns:
            str: Response from Gemini.
        """
        try:
            # Configure the API
            genai.configure(api_key=api_key)
            
            # Initialize the model
            model = genai.GenerativeModel(model_name)
            
            # Generate the response
            response = model.generate_content(prompt)
            
            # Return the text response
            return response.text
            
        except Exception as e:
            return f"Error calling Gemini API: {str(e)}"