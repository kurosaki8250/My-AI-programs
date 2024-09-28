from transformers import WhisperProcessor, WhisperForConditionalGeneration

# Define the model name
model_name = "openai/whisper-large-v2"

# Download and save the processor and model locally
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)

# Optionally, you can save the model to a local directory
processor.save_pretrained("local_whisper_processor")
model.save_pretrained("local_whisper_model")

print("Model and processor downloaded and saved locally.")
