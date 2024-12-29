

def default_middleware(client_address, method, path, body, query):
    print(f"[{client_address[0]}:{client_address[1]}] Path: {path} | Method: {method}")

