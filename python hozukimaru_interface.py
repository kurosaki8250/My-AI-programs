import random

# Define a dictionary of possible responses
responses = {
    "calculate the first 100 prime numbers and plot them": {
        "code": "prime_numbers = [2]\nfor num in range(3, 101):\n    for prime in prime_numbers:\n        if num % prime == 0:\n            break\n    else:\n        prime_numbers.append(num)\nplt.plot(prime_numbers)\nplt.show()",
        "output": "Prime numbers from 2 to 100 plotted on a graph."
    },
    "give a speech about ai and read it with voice": {
        "code": "speech = 'Artificial intelligence is a rapidly growing field that has the potential to revolutionize many aspects of our lives. From self-driving cars to medical diagnosis, AI is making a big impact. However, it's important to remember that AI is a tool created by humans, and it's up to us to ensure that it's used ethically and responsibly.'\nos.system('say ' + speech)",
        "output": "A speech about AI has been generated and read aloud."
    },
    "Find out the height of Eiffel Tower": {
        "code": "height = 330\nprint('The height of the Eiffel Tower is', height, 'meters.')",
        "output": "The height of the Eiffel Tower is 330 meters."
    }
}

# Get user input
user_input = input("Give me a task...")

# Check if the user input matches any of the predefined responses
if user_input in responses:
    # Execute the code and print the output
    exec(responses[user_input]["code"])
    print(responses[user_input]["output"])
else:
    print("I'm sorry, I don't know how to do that.")