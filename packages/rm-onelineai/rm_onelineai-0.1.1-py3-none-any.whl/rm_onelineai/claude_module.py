from anthropic import Anthropic

class Claude:
    @staticmethod
    def basiccall(api_key: str, model_name: str, prompt: str) -> str:
        """
        Makes a call to Claude API to generate content.

        Args:
            api_key (str): Your Claude API key.
            model_name (str): The Claude model name (e.g., 'claude-3-opus-20240229').
            prompt (str): The input prompt.

        Returns:
            str: Response from Claude.
        """
        try:
            # Initialize the Anthropic client
            client = Anthropic(api_key=api_key)
            
            # Create the message
            message = client.messages.create(
                model=model_name,
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Return the response text
            return message.content[0].text
            
        except Exception as e:
            return f"Error calling Claude API: {str(e)}"