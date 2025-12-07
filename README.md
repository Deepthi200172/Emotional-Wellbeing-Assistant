### ReAct Architecture (Reasoning + Acting) 

This project includes a complete implementation of the ReAct pattern:

1️⃣ Thought

The agent internally reasons about:

emotional tone

user sentiment

appropriate next steps

whether a tool is needed

These thoughts are not shown to the user.

2️⃣ Action

The agent chooses a tool:

Action: identify_emotion: "I feel lost"


Tools available:

identify_emotion(text)

suggest_coping_method(emotion)

journaling_prompt(emotion)

3️⃣ Observation

Tool is executed in Python, returning grounded output:

Observation: sadness

4️⃣ Answer

Only after reasoning + tool usage does the agent produce the final user-facing response.

🔁 ReAct Agent Loop (5-Turn Controlled Reasoning)

The reasoning pipeline is managed through a custom agent loop:

def react_loop(agent, user_input, max_turns=5):
    ...


This loop:

extracts tool calls using regex

dispatches tools

feeds observations back to LLM

prevents infinite loops

stops when an Answer: appears

This ensures predictability, safety, and grounded behavior.

🛠 Custom Tooling System

Tools follow the ReAct tool spec:

🔹 identify_emotion(text)

Rule-based emotion detection grounded in curated vocabulary and text features.

🔹 suggest_coping_method(emotion)

Fetches emotion-specific suggestions from a structured JSON database.

🔹 journaling_prompt(emotion)

Provides guided self-reflection prompts tailored to the emotional state.
