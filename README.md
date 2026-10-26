# GenAI ChatBot (Docker Deployment)

A tiny [Streamlit](https://streamlit.io/) chatbot that sends your messages and chat history to an OpenAI model and shows the reply. It is built as a beginner demo for packaging a GenAI app with Docker.

## Project Structure

```
Docker Deployment/
├── app.py             # Streamlit chatbot
├── Dockerfile         # Image definition
├── requirements.txt   # Python dependencies
├── .env.example       # Template for environment variables
├── .env               # Your real key (never committed, never copied into the image)
├── .dockerignore      # Files excluded from the Docker build context
└── .gitignore         # Files excluded from Git
```

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running
- An [OpenAI API key](https://platform.openai.com/api-keys)
- (Optional, for running without Docker) Python 3.12+

## Configuration

The app reads its settings from environment variables:

| Variable         | Description                                  | Default       |
|------------------|----------------------------------------------|---------------|
| `OPENAI_API_KEY` | Your OpenAI API key (required)               | none          |
| `OPENAI_MODEL`   | OpenAI chat model to use                     | `gpt-4o-mini` |

1. Copy the template:

   ```bash
   cp .env.example .env
   ```

   On Windows (PowerShell): `copy .env.example .env`

2. Open `.env` and paste your key:

   ```dotenv
   OPENAI_API_KEY=sk-your-key-here
   OPENAI_MODEL=gpt-4o-mini
   ```

> **Security:** `.env` is listed in both `.gitignore` and `.dockerignore`, so your key is not committed to Git and is not baked into the Docker image. Never put the key in the Dockerfile.

## Run with Docker

### 1. Build the image

```bash
docker build -t genai_chatbot .
```

### 2. Run the container

```bash
docker run -d --rm -p 8501:8501 --env-file .env genai_chatbot
```

Or give the container a name so it is easy to stop:

```bash
docker run -d --rm -p 8501:8501 --env-file .env --name chatbot_docker genai_chatbot
```

What the flags do:

- `-d` runs the container in the background
- `--rm` removes the container automatically when it stops
- `-p 8501:8501` maps port 8501 on your machine to the container
- `--env-file .env` passes your variables in at startup
- `--name chatbot_docker` names the container

### 3. Open the app

Go to <http://localhost:8501> in your browser.

## Useful Docker Commands

```bash
docker ps                        # list running containers
docker logs chatbot_docker       # view app logs
docker stop chatbot_docker       # stop the container (it is removed because of --rm)
docker images                    # list images
docker rmi genai_chatbot         # delete the image
```

## Run Locally (without Docker)

```bash
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # macOS / Linux

pip install -r requirements.txt
streamlit run app.py
```

Locally, `python-dotenv` loads variables from your `.env` file automatically.

## How It Works

1. `app.py` loads settings from the environment (or `.env` locally).
2. Chat history is kept in `st.session_state` for the current browser tab.
3. Each message, plus the history, is sent to the OpenAI Chat Completions API with a short system prompt.
4. The reply is displayed in the chat window.

## Troubleshooting

- **"No OpenAI API key found":** Make sure `.env` exists and contains `OPENAI_API_KEY`, and that you passed `--env-file .env` to `docker run`.
- **"The OpenAI request failed":** Check that your API key is valid, the model name is correct, and your network connection works.
- **Port already in use:** Map a different host port, e.g. `-p 8502:8501`, then open <http://localhost:8502>.
- **Changes to `.env` not picked up:** Stop the container and run it again; environment variables are read only at startup.

## Tech Stack

- Python 3.12 (slim Docker image)
- Streamlit
- OpenAI Python SDK
- python-dotenv