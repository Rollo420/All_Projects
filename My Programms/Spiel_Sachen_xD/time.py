import datetime

def get_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M:%S")

if __name__ == "__main__":
    import http.server as h

    with h.ThreadingHTTPServer(("", 8080), h.SimpleHTTPRequestHandler) as server:
        server.serve_forever()
