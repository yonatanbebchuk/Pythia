import os

if __name__ == '__main__':
    # os.system("openai tools fine_tunes.prepare_data -f .\\archive\\info.txt")
    # os.system("openai api fine_tunes.create -t .\\archive\\info_prepared.jsonl -m ada")
    os.system("openai api fine_tunes.get -i ft-eOUFyS4y2y9jnjIlpfS9PqYa")
    os.system("openai api fine_tunes.list")
    os.system("openai api completions.create -m ft-eOUFyS4y2y9jnjIlpfS9PqYa -p \"What is my name?\"")