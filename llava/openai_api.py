import os
import time
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv


load_dotenv()

client = AsyncOpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


async def create_chat_completion(messages, temperature, model="gpt-4-1106-preview"):
    chat_completion_resp = await client.chat.completions.create(
        messages=messages,
        temperature=temperature,
        model=model
    )
    return chat_completion_resp

async def dispatch_openai_requests(
  messages_list,
  temperature,
):
    return await asyncio.gather(*(create_chat_completion(m, temperature) for m in messages_list))


def call_async(samples, wrap_gen_message, print_result=False):
  message_list = []
  for sample in samples:
    input_msg = wrap_gen_message(sample)
    message_list.append(input_msg)
  
  try:
    predictions = asyncio.run(
      dispatch_openai_requests(
        messages_list=message_list,
        temperature=0.0,
      )
    )
  except Exception as e:
    print(f"Error in call_async: {e}")
    time.sleep(6)
    return []

  results = []
  for sample, prediction in zip(samples, predictions):
    if prediction:
      sample['result'] = prediction.choices[0].message.content
      if print_result:
        print(sample['result'])
      results.append(sample)
  return results