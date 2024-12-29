import google.generativeai as genai

def query_data(data, question):
    """Queries information using Gemini."""
    prompt = f"""
    You are an AI assistant with access to the following information:

    {data}

    Please answer the user's question: "{question}"
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text

def is_name_query(question):
    """Checks if the question is about the assistant's name."""
    prompt = f"""
    You are an AI assistant. Determine if the following question is asking for your name or identity:
    Question: "{question}"
    Respond with "Yes" if it is asking for your name, and "No" if it is not.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip().lower() == "yes"

def is_related_to_data(data, question):
    """Checks if the question relates to the given data."""
    prompt = f"""
    You are an AI assistant with access to the following information:

    {data}

    Determine if the user's question is related to this information:
    Question: "{question}"

    Respond with "Yes" if the question is related to the information, and "No" if it is not.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip().lower() == "yes"

class pbAssistant:
    """Assistant class to manage configurations and handle interactions."""
    def __init__(self, name="Assistant"):
        self.name = name

    def change_name(self, new_name):
        """Changes the assistant's name."""
        self.name = new_name
        print(f"Assistant name changed to {self.name}.")

    def main_execution(self, api_key, data):
        """Runs the main execution loop."""
        genai.configure(api_key=api_key)

        while True:
            user_input = input("Ask a question: ").strip()
            if user_input.lower() in ["exit", "quit", "stop"]:
                print("Exiting...")
                break
            elif is_name_query(user_input):
                print(f"My name is {self.name}.")
            else:
                if is_related_to_data(data, user_input):
                    #print("The question is related to the provided data. Answering from the data...")
                    response = query_data(data, user_input)
                else:
                    #print("The question is not related to the provided data. Querying Gemini...")
                    response = query_data("", user_input)
                print(response)
