from datasets import load_dataset

# Load the dataset with a specific configuration
dataset = load_dataset("open-llm-leaderboard/cognitivecomputations__dolphin-2.9-llama3-8b-details", "cognitivecomputations__dolphin-2.9-llama3-8b__leaderboard_arc_challenge")

# Print the available splits
print("Available splits:", dataset.keys())
