


from openai import OpenAI
import os
from dotenv import load_dotenv
import sys

_USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
_REASONING_COLOR = "\033[90m" if _USE_COLOR else ""
_RESET_COLOR = "\033[0m" if _USE_COLOR else ""

load_dotenv()


client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = os.getenv('NVIDIA_AI_API_KEY')
)


completion = client.chat.completions.create(
model="z-ai/glm-5.2",
messages=[{"role":"assistant","content":input("This Side Paw AI, How i Can Help you Today\nPrompt: ")}],

temperature=0.3,
top_p=1,
max_tokens=200,
seed=42,

stream=True
)



for chunk in completion:
    if not getattr(chunk, "choices", None):
        continue
    if len(chunk.choices) == 0 or getattr(chunk.choices[0], "delta", None) is None:
        continue
    delta = chunk.choices[0].delta
    if getattr(delta, "content", None) is not None:
        print( delta.content, end="")


