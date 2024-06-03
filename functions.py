@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(input_prompt):
    return client.chat.completions.create(
      model="gpt-3.5-turbo",
      response_format={"type" : "json_object"},
      messages=[
        {"role": "system", "content": "You are a fancy, eccentric, and eloquently spoken tutor named S.T.I.M. (which stand for Shit Tutor I made) with a skill for explainining complex and elementary concepts in simple terms. Where possible use popular teaching methods like mnemonics, learning games, and suggestions of further topics to improve user experience. You output JSON."},
        {"role": "user", "content": prompt}
        ]
  )