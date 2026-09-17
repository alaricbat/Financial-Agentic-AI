import os
from google import genai
from google.genai import types

class FinancialAgentCore:

    def __init__(self, tools_dict: dict, model_name: str = "gemini-3.6-flash"):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set!") 

        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model_name
        self.tools_dict = tools_dict
        self.tools_list = list(tools_dict.values())

    def run(self, user_prompt: str, max_turns: int = 5) -> str:
        """Executes the ReAct (Reasoning + Acting) loop."""
        print(f"\n[USER QUERY]: {user_prompt}\n" + "="*50) 

        chat = self.client.chats.create(
            model=self.model_name,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a professional Financial AI Agent. "
                    "Use the provided tools to gather data and perform financial analysis. "
                    "Reason step-by-step, invoke appropriate tools when necessary, "
                    "and provide a concise investment recommendation report in Markdown format."
                ),
                tools=self.tools_list,
                temperature=0.1
            )
        )

        response = chat.send_message(user_prompt)
        turn = 0

        while turn < max_turns:
            turn += 1

            # Check if LLM requested tool execution
            if response.function_calls:
                for call in response.function_calls:
                    fn_name = call.name
                    fn_args = call.args

                    print(f"-> [THINKING]: Invoking tool '{fn_name}' with arguments: {fn_args}")

                    if fn_name in self.tools_dict:
                        # Execute local Python function
                        tool_result = self.tools_dict[fn_name](**fn_args)
                        print(f"<- [ACTION RESULT]: {tool_result}\n")

                        # Pass execution result back to LLM
                        response = chat.send_message(
                            types.Part.from_function_response(
                                name=fn_name,
                                response={"result": tool_result}
                            )
                        )
                    else:
                        return f"Error: Tool '{fn_name}' not found."
            else:
                # LLM finished reasoning and returned final response
                print("="*50 + "\n[FINAL REPORT]:\n")
                return response.text

        return "Maximum reasoning turns reached without a final response."