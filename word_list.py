import sys

def load_word_list(name:str):
    try:
        with open(f"dicts/{name}","r") as f:
            return f.read().strip().split("\n")
    except Exception as e:
        print(str(e))
        sys.exit(-1)
