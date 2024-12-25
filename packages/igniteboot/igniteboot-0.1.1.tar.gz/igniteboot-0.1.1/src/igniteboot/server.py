import uvicorn

def run_server(app, host="127.0.0.1", port=8000):
    uvicorn.run(app, host=host, port=port, log_level="debug", reload=True)
