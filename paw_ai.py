from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)


completion = client.chat.completions.create(
  model="nvidia/nemotron-3-ultra-550b-a55b",
  messages=[{"role":"w","content":"Write a limerick about the wonders of GPU computing."}],
  temperature=1,
  top_p=0.95,
  max_tokens=1384,
  extra_body={"chat_template_kwargs":{"enable_thinking":True}},
  stream=True
)

for chunk in completion:
  if not chunk.choices:
    continue
  reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
  if reasoning:
    print(reasoning, end="")
  if chunk.choices[0].delta.content is not None:
    print(chunk.choices[0].delta.content, end="")