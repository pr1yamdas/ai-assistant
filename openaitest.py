import openai
from config import apikey

openai.api_key = apikey

response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="Your prompt goes here.",
    temperature=1,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

print(response)



'''
{
  "warning": "This model version is deprecated. Migrate before January 4, 2024 to avoid disruption of service. Learn more https://platform.openai.com/docs/deprecations",
  "id": "cmpl-8LQZ3mHeApflwYD2jwO6qSlN6tZMd",
  "object": "text_completion",
  "created": 1700117693,
  "model": "text-davinci-003",
  "choices": [
    {
      "text": "\n\nDescribe the moment you first realized you wanted to pursue a career in your chosen field.",
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 5,
    "completion_tokens": 20,
    "total_tokens": 25
  }
}
'''