import os
import time

import dotenv
import openai

# Set OpenAI API key
dotenv.load_dotenv("../secrets.env")
openai_api_key = os.environ.get("OPENAI_API_KEY")

# Create OpenAI client
client = openai.OpenAI(api_key=openai_api_key)

# Upload training data
training_file = client.files.create(
    file=open("training_data.jsonl", "rb"), purpose="fine-tune"
)

# Create a fine-tuned model
fine_tune_response = client.fine_tuning.jobs.create(
    training_file=training_file.id, model="gpt-3.5-turbo", suffix="network-analysis"
)

# Monitor the fine-tune job status
fine_tune_id = fine_tune_response.id
print(f"Created fine-tune job with ID: {fine_tune_id}")

while True:
    status_response = client.fine_tuning.jobs.retrieve(fine_tune_id)
    status = status_response.status
    if status in ["succeeded"]:
        break
    print(f"Fine-tuning job status: {status}")
    print(f"Fine-tuned model: {status_response.fine_tuned_model}")
    time.sleep(60)  # Check every minute

print("Fine-tuning job completed!")
