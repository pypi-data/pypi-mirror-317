from huggingface_hub import InferenceClient
import requests

class KITEModel:
    """
    A wrapper for generating responses from HuggingFace Inference API.
    """
    def __init__(self, name="https://tgi.staging.kite.ume.de"):
        self.client = InferenceClient(base_url=name)
        self.model_info = self.fetch_model_info(f"{name}/info")

    @staticmethod
    def fetch_model_info(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                model_id = data.get("model_id", "Unknown")
                version = data.get("version", "Unknown")
                return f"Model ID: {model_id}, Version: {version}"
            else:
                return f"Failed to fetch data. HTTP Status Code: {response.status}"
        except Exception as e:
            return f"An error occurred: {e}"

    @staticmethod
    def build_prompt(system_prompts: list[str], user_prompts: list[str]) -> str:
        """
        Build a structured prompt for the model with all system prompts first, followed by all user prompts.

        Args:
            system_prompts (list[str]): List of system prompts.
            user_prompts (list[str]): List of user prompts.

        Returns:
            str: A structured prompt string.
        """
        prompt = "<|begin_of_text|>"

        # Add all system prompts first
        for system_prompt in system_prompts:
            prompt += (
                f"<|start_header_id|>system<|end_header_id|>\n{system_prompt}<|eot_id|>"
            )

        # Add all user prompts next
        for user_prompt in user_prompts:
            prompt += (
                f"<|start_header_id|>user<|end_header_id|>\n{user_prompt}<|eot_id|>"
            )

        # Signal where the assistant's response starts
        prompt += "<|start_header_id|>assistant<|end_header_id|>"
        return prompt

    def generate_response(self, system_prompts: list[str], user_prompts: list[str], max_tokens: int = 2048) -> str:
        """
        Generate a response from the model using the structured prompt.
        """
        prompt = self.build_prompt(system_prompts, user_prompts)
        response = self.client.text_generation(prompt, max_new_tokens=max_tokens)
        return response