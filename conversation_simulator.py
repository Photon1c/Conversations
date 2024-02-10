import openai
from dotenv import load_dotenv
import os
import time

load_dotenv(".env")

openai_api_key = os.getenv("OPENAI_API_KEY")

# Set your OpenAI API key
openai.api_key = openai_api_key

client = openai.OpenAI()

def generate_response(conversation, max_tokens=None):
    """
    Generate a response from the language model.

    Args:
    - conversation (list): The conversation
    - max_tokens (int): Maximum number of tokens for the response

    Returns:
    - str: The generated response
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=conversation,
            max_tokens=max_tokens
        )

        # Accessing the response content correctly
        if response.choices:
            first_choice = response.choices[0]
            if hasattr(first_choice, 'message') and hasattr(first_choice.message, 'content'):
                return first_choice.message.content.strip()
        return ""
    except Exception as e:
        print(f"Error generating response: {e}")
        return ""



def converse(agent1_name, agent2_name, referee_name, topic, steps, max_tokens_per_response=35, response_delay=3):
    """
    Simulate a conversation between two agents.

    Args:
    - agent1_name (str): Name for agent 1
    - agent2_name (str): Name for agent 2
    - referee_name (str): Name for the referee
    - topic (str): Topic of conversation
    - steps (int): Number of conversation steps
    - max_tokens_per_response (int): Maximum number of tokens for each response
    - response_delay (int): Delay in seconds before displaying each response

    Returns:
    - list: The complete conversation
    """
    agent1_role = "assistant"
    agent2_role = "assistant"
    referee_role = "system"
    referee_name = "Referee"

    # Initialize conversation with agent introductions and topic
    conversation = [
    {"role": agent1_role, "content": f"{agent1_name}: Hi, I'm {agent1_name}. I'm looking forward to discussing {topic}."},
    {"role": agent2_role, "content": f"{agent2_name}: And I'm {agent2_name}, excited to explore {topic} from different angles."},
    {"role": referee_role, "content": f"{referee_name}: Great to have both of you here! As we delve into {topic}, I'll be here to guide our discussion. Let's keep it informative and respectful."},
    # Example of referee interjecting if one agent interrupts the other
    {"role": referee_role, "content": f"{referee_name}: Hold on, {agent1_name}, let's allow {agent2_name} to finish their point before we move on."},
]


    for step in range(steps):
        # Agent 1's turn
        agent1_message = generate_response(conversation, max_tokens=max_tokens_per_response)
        conversation.append({"role": agent1_role, "content": f"{agent1_message}"})
        print(f"{agent1_name}: {agent1_message}")
        time.sleep(response_delay)

        # Agent 2's turn
        agent2_message = generate_response(conversation, max_tokens=max_tokens_per_response)
        conversation.append({"role": agent2_role, "content": f"{agent2_message}"})
        print(f"{agent2_name}: {agent2_message}")
        time.sleep(response_delay)

    return conversation


# Example conversation with 2 steps, a max_tokens limit of 50 for each response, and a delay of 2 seconds
#agent1_name = "Agent 1"
#agent2_name = "Agent 2"
#referee_name = "Referee"
#topic = "technology"
#completed_conversation = converse(agent1_name, agent2_name, referee_name, topic, steps=2, max_tokens_per_response=50, response_delay=2)

