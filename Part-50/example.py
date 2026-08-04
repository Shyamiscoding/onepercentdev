import time

def stream_response(text):
    for word in text.split():
        time.sleep(0.3)
        yield word

for word in stream_response("Generators process data one piece at a time"):
    print(word, end=" ", flush=True)