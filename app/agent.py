import re
import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import identify_emotion, suggest_coping_method, journaling_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

TOOLS = {
    "identify_emotion": identify_emotion,
    "suggest_coping_method": suggest_coping_method,
    "journaling_prompt": journaling_prompt,
}

ACTION_RE = re.compile(r"Action:\s*(\w+):\s*\"?(.*?)\"?\s*$")

SYSTEM_PROMPT = """
You are an Emotional Wellbeing ReAct Agent.

Your goals:
- Understand the user's emotional tone.
- Offer gentle, safe emotional guidance.
- Suggest coping strategies based on the emotion.
- Suggest journaling prompts when helpful.

Use this internal format:

Thought: <reasoning>
Action: <tool_name>: "<input>"
Observation: <response>

When replying to the user:

Answer: <final message>

Allowed Tools:
- identify_emotion
- suggest_coping_method
- journaling_prompt
"""

class Agent:
    def __init__(self):
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def __call__(self, user_input: str):
        self.messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
        )
        content = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": content})
        return content


def react_loop(agent: Agent, user_input: str, max_turns: int = 5):
    message = user_input

    for _ in range(max_turns):
        reply = agent(message)

        match = ACTION_RE.search(reply)
        if not match:
            if "Answer:" in reply:
                return reply.split("Answer:", 1)[-1].strip()
            return reply.strip()

        tool_name, tool_input = match.groups()
        tool_func = TOOLS.get(tool_name)

        if tool_func:
            observation = tool_func(tool_input)
        else:
            observation = f"Unknown tool: {tool_name}"

        message = f"Observation: {observation}"

    return "I’m sorry, I couldn’t understand. Can you rephrase?"


def create_agent_response(user_message: str):
    agent = Agent()
    return react_loop(agent, user_message)

