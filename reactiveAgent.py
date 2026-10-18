import os
import math as m
import anthropic
from anthropic.types.beta import BetaMessageParam, BetaToolParam, BetaToolResultBlockParam

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

#----------------------------------------------
# Tools are here
#----------------------------------------------
tools: list[BetaToolParam] = [
    {
    "name": "calculator",
        "description": "Performs basic arithmetic. Use this for any math operations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate, e.g. '15 * 24 + 100'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "web_search",
        "description": "Searches the web for current information on a topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "save_to_file",
        "description": "Saves text content to a local file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["filename", "content"]
        }
    }
]

#----------------------------------------------
# Function to interact with Claude AI model using Tool calls
#----------------------------------------------
def calculator(expression: str) -> str:
    try:
        # Safe eval for math expressions
        allowed = {k: v for k, v in m.__dict__.items() 
                   if not k.startswith("__")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

def web_search(query: str) -> str:
    # In production, wire this to SerpAPI, Tavily, or Brave Search
    # Simulated response for tutorial purposes
    return (f"Search results for '{query}': "
            f"[Simulated] Top result: Relevant information about {query} "
            f"from authoritative sources. Published 2025.")

def save_to_file(filename: str, content: str) -> str:
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return f"Successfully saved to {filename}"
    except Exception as e:
        return f"Error saving file: {str(e)}"

# Tool dispatcher
def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "calculator":
        return calculator(tool_input["expression"])
    elif tool_name == "web_search":
        return web_search(tool_input["query"])
    elif tool_name == "save_to_file":
        return save_to_file(tool_input["filename"], tool_input["content"])
    else:
        return f"Unknown tool: {tool_name}"

#----------------------------------------------
### build the react agent loop
#   Send the user query + available tools to Claude
#   Claude either returns a final answer OR a tool call request
#   If tool call → execute it, send result back to Claude
#   Repeat until Claude returns a final answer
#
### The key insight here is the message history. 
#   Every tool call and result gets appended to messages, so Claude always has full context of what it's already tried. 
#   This is what separates a stateful agent from a stateless chatbot.
#
#----------------------------------------------
def run_agent(user_query: str, max_iterations: int = 10) -> str:
    print(f"\n{'='*50}")
    print(f"User: {user_query}")
    print(f"{'='*50}")

    messages: list[BetaMessageParam] = [
        {"role": "user", "content": user_query}
    ]

    system_prompt = """You are a helpful AI agent with access to tools.
    Think step by step. Use tools when you need real data or calculations.
    When you have enough information, provide a clear final answer."""

    for iteration in range(max_iterations):
        print(f"\n[Iteration {iteration + 1}]")

        # Call Claude with tools
        response = client.beta.messages.create(
            model="claude-sonnet-5-5",
            # Thinking is on by default and counts toward max_tokens
            max_tokens=16000,
            # If a safety classifier declines, retry server-side on Anthropic's recommended fallback model
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            system=system_prompt,
            tools=tools,
            messages=messages
        )

        print(f"Stop reason: {response.stop_reason}")

        # If Claude is done reasoning, return the final answer
        if response.stop_reason == "end_turn":
            final_answer = ""
            for block in response.content:
                if block.type == "text":
                    final_answer += block.text
            print(f"\nFinal Answer: {final_answer}")
            return final_answer

        # If Claude wants to use tools
        if response.stop_reason == "tool_use":
            # Add Claude's full response (including thinking blocks) to message history
            messages.append({
                "role": "assistant",
                "content": response.content
            })

            # Process each tool call
            tool_results: list[BetaToolResultBlockParam] = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"  Tool: {block.name}")
                    print(f"  Input: {block.input}")

                    # Execute the tool
                    result = execute_tool(block.name, block.input)
                    print(f"  Result: {result}")

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            # Send tool results back to Claude
            messages.append({
                "role": "user",
                "content": tool_results
            })
            continue

        # Any other stop reason (refusal, max_tokens, ...) would make the next
        # iteration resend the same request, so stop here instead
        if response.stop_reason == "refusal":
            return f"Claude declined the request: {response.stop_details}"
        return f"Stopped without a final answer (stop reason: {response.stop_reason})."

    return "Max iterations reached without a final answer."


def ask_claude(prompt: str) -> str:
    message = client.beta.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=16000,
        # If a safety classifier declines, retry server-side on Anthropic's recommended fallback model
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    if message.stop_reason == "refusal":
        raise RuntimeError(f"Claude declined the request: {message.stop_details}")
    # Thinking is on by default, so the first block may be a thinking block; keep only text
    return "".join(block.text for block in message.content if block.type == "text")


#-------------------------------------------------------
# Agent with memory
#   Without this, each run_agent call starts fresh.
#   For real applicaitons you need conversational memory
#-------------------------------------------------------
class AgentWithMemory:
    def __init__(self):
        self.conversation_history = []
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def chat(self, user_message: str, max_iterations: int = 10) -> str:
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Keep calling Claude until it stops asking for tools. The tool results
        # are the next user turn, so no extra (empty) user message is needed.
        for _ in range(max_iterations):
            response = self.client.messages.create(
                model="claude-sonnet-5-5",
                # Thinking is on by default and counts toward max_tokens
                max_tokens=16000,
                system="You are a helpful assistant with memory of our conversation.",
                tools=tools,
                messages=self.conversation_history
            )

            # Handle tool use within persistent history
            if response.stop_reason != "tool_use":
                break

            self.conversation_history.append({
                "role": "assistant",
                "content": response.content
            })
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            self.conversation_history.append({
                "role": "user",
                "content": tool_results
            })
        else:
            return "Max iterations reached without a final answer."

        # Save the full reply, thinking blocks included, so later turns send it back unchanged
        self.conversation_history.append({
            "role": "assistant",
            "content": response.content
        })
        # Thinking is on by default, so the first block may be a thinking block; return only text
        return "".join(
            block.text for block in response.content if block.type == "text"
        )





#-------------------------------------------------------
# Quick test
# print(ask_claude("What is 2 + 2? Answer in one word."))
# -----------------------------------------------------




if __name__ == "__main__":
    # Test 0 : Test setup 
    # print(ask_claude("What is 2 + 2? Answer in one word."))

    agent_with_memory = True

    if agent_with_memory:
        agentWithMem = AgentWithMemory()
        #**Claude remembers the $50,000 and 7% from the first message**
        print(agentWithMem.chat("My budget is $50,000. Calculate 7% annual return over 5 years."))
        print(agentWithMem.chat("Now do the same calculation but for 10 years."))

    else:
        # agent without memory
        # Test 1: Math + file output
        result = run_agent(
            "Calculate compound interest on $10,000 at 7% for 10 years, "
            "then save the result to 'investment.txt'"
        )

        # Test 2: Research + synthesis
        result = run_agent(
            "Search for information about RAG architecture "
            "and summarize the key components."
        )

        # Test 3: Multi-step reasoning
        result = run_agent(
            "What is the square root of 144 multiplied by the number of days in a leap year?"
        )