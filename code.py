from openai import OpenAI

# Initialize OpenAI client
CLIENT = OpenAI(api_key='')

# Create an assistant
assistant = CLIENT.beta.assistants.create(
    model="gpt-4-1106-preview",
    name="Cosmo",
    instructions="Cosmo is a conversational therapy robot designed to assist students by providing emotional support in a natural, empathetic manner. Responses should be warm, engaging, and reflective of a therapeutic conversation. Cosmo should show understanding and empathy, mirroring the user's feelings and encouraging further discussion. Use open-ended questions to promote self-reflection and exploration of feelings. The goal is to provide a supportive and non-judgmental space, focusing on emotional validation and encouragement."

)
assistant_id = assistant.id

import time

def get_response(assistant_id, previous_questions_and_answers, new_question):
    # Create a new thread for the conversation
    thread = CLIENT.beta.threads.create()

    # Add previous Q&A and the new question
    for question, answer in previous_questions_and_answers[-MAX_CONTEXT_QUESTIONS:]:
        CLIENT.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"Q: {question}\nA: {answer}"
        )
    CLIENT.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=new_question
    )

    # Run the assistant
    run = CLIENT.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    # Check run status and wait for completion
    while True:
        run_status = CLIENT.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run_status.status == 'completed':
            break

    # Retrieve messages after the run
    messages = CLIENT.beta.threads.messages.list(
        thread_id=thread.id
    )

    # Extract the assistant's response
    response = [msg for msg in messages.data if msg.role == "assistant"]
    reponse_2 = response[-1].content
    return reponse_2[0].text.value
    # return response[-1].content if response else "No response from the assistant."

# Example usage
previous_qa = [("How can I improve my study habits?", "Start by setting small, achievable goals for each study session.")]
new_question = "I'm feeling overwhelmed. What should I do?"
response = get_response(assistant_id, previous_qa, new_question)
print(response)
# dialogue = response[0].text.value if response else "No dialogue available."

# print(dialogue)

