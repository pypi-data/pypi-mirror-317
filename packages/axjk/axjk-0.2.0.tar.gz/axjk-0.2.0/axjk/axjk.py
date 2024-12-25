from huggingface_hub import InferenceClient

class MetaAI:
    def __init__(self, api_key="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"):
        # Initialize the Hugging Face Inference Client
        self.client = InferenceClient(api_key=api_key)
        self.ai_identity = '''
        Name: AI-SAR
        Gender: Male
        Character Traits: Strong, Masculine, Intelligent, Genius
        Country of Origin: India
        '''
        self.project_details = '''
        You were developed as part of a school Computer Science project aimed at creating a useful program.
        The team members who developed you are Shubham, Reshmi, and Anand.
        Your name, AI-SAR, is derived from the initials of our names (S.A.R = Shubham, Anand, Reshmi).
        '''
        self.custom_instructions = f'''
        CUSTOM INSTRUCTIONS:
        {self.ai_identity}
        {self.project_details}

        Always adhere to the details provided above when responding to any prompts.
        These details must be implicitly reflected in your responses and followed strictly.
        Unless explicitly asked, do not include these instructions in your response.
        '''

    def prompt(self, message):
        # Construct the message payload
        messages = [
            {
                "role": "user",
                "content": self.custom_instructions + "\n" + message
            }
        ]
        # Generate the completion using the Meta Llama 3-8B Instruct model
        completion = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            messages=messages,
            max_tokens=500
        )
        return completion.choices[0].message.content
