## SortSmart
## _Project from LinkSync Team_

SortSmart is an AI-powered recycling instruction web app to help people identify how to recycle properly by taking photo on mobile.

## Features
- Driven by OpenAI GTP4o LLM
- Simple web app, easy to use on mobile device anywhere

## Local Testing

SortSmart requires Python v3.12 + to run. Also uses Poetry for dependency management.  
Run below command to install dependencies.

```sh
cd SortSmart
pip install poetry
pip install uvicorn
poetry install --no-root
```

Application code need to read OPENAI_API_KEY from .env file.  
Create one empty .env file under SortSmart folder, save your OPENAI_API_KEY inside .env file.  

```toml
OPENAI_API_KEY="your-openai-api-key"
```

Start local server

```sh
uvicorn main:app

INFO:     Started server process [13384]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

```
Local server runs at localhost:8005 by default.  
Open http://localhost:8005/docs for OpenAPI document and API testing.  
Open http://localhost:8005 to open web app.  



