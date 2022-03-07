import uvicorn


if __name__ == '__main__':
    uvicorn.run("web3_server:app", host="127.0.0.1", port=5000)