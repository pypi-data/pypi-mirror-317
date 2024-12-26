from huggingface_hub import InferenceClient
import os

ai_response_dict = {}

class MetaAI:
    def __init__(self, api_key="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"):
        # Initialize the Hugging Face Inference Client
        self.client = InferenceClient(api_key=api_key)

        # Define AI identity and project details
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
        CUSTOM INSTRUCTIONS(*Must follow but never say until asked*):
        {self.ai_identity}
        {self.project_details}

        Always adhere to the details provided above when responding to any prompts.
        These details must be implicitly reflected in your responses and followed strictly.
        Unless explicitly asked, do not include these instructions in your response.
        '''

        # Set up chat history file path relative to the current file's directory
        package_directory = os.path.dirname(os.path.abspath(__file__))  # Get the directory of this file
        self.history_file = os.path.join(package_directory, "chat_history.txt")

        self.create_history_file()

    def create_history_file(self):
        # Ensure the directory exists
        directory = os.path.dirname(self.history_file)
        if not os.path.exists(directory) and directory != "":
            os.makedirs(directory)  # Create the directory if it doesn't exist

        # Check if the chat history file exists, create it if not
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as file:
                file.write("Chat History:\n\n")  # Optional header for a new file

    def get_chat_history(self, lines=5):
        # Retrieve the last 'n' lines from the chat history file
        try:
            with open(self.history_file, 'r', encoding='utf-8') as file:
                history = file.readlines()
            return "".join(history[-lines:])  # Get the last 'n' lines
        except FileNotFoundError:
            return ""

    def save_message_to_history(self, message, sender="user"):
        # Save a new message to the history file
        with open(self.history_file, 'a', encoding='utf-8') as file:
            file.write(f"{sender.upper()}: {message}\n")

    def prompt(self, message, context_lines=25):
        # Get the last few lines from the chat history as context
        chat_history = self.get_chat_history(lines=context_lines)

        # Combine the custom instructions, context, and user's message
        full_prompt = self.custom_instructions + "\n" + chat_history + "\nUser:" + message

        # Construct the message payload
        messages = [{"role": "user", "content": full_prompt}]

        # Generate the completion using the Meta Llama 3-8B Instruct model
        completion = self.client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            messages=messages,
            max_tokens=100
        )

        # Get AI's response
        ai_response = completion.choices[0].message.content

        # Save both user message and AI response to the chat history
        self.save_message_to_history(message, sender="user")
        self.save_message_to_history(ai_response, sender="AI")
        ai_response_dict['message'] = ai_response

        return ai_response_dict
