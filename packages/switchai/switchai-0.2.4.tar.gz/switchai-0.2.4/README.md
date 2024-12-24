# SwitchAI  

SwitchAI is a lightweight and flexible library that provides a standardized interface for interacting with various AI APIs like OpenAI, Anthropic, Mistral, and more. With SwitchAI, you can easily switch between AI providers or use multiple APIs simultaneously, all with a simple and consistent interface.  

## Installation  

You can install just the base `switchai` package, or install a provider's package along with it.

- **Base Package**: This installs just the base `switchai` package without installing any provider's SDK.

  ```bash
  pip install switchai
  ```

- **OpenAI Provider**: This installs `switchai` along with OpenAI's library.

  ```bash
  pip install switchai[openai]
  ```

- **All Providers**: This installs `switchai` along with all provider-specific libraries.

  ```bash
  pip install switchai[all]
  ```

## Getting Started

To use SwitchAI, you will need API keys for the AI providers you intend to interact with. You can set these keys either as environment variables or pass them as configuration to the `SwitchAI` client.  

### Option 1: In Code

```python
from switchai import SwitchAI

client = SwitchAI(provider="openai", model_name="gpt-4", api_key="your_api_key")
```

### Option 2: Environment Variables

Set the API key as an environment variable:

**macOS/Linux:**
```bash
export PROVIDER_API_KEY="your_api_key"
```

**Windows:**
```bash
set PROVIDER_API_KEY="your_api_key"
```

Make sure you follow the correct naming conventions for each provider's API key, as outlined in the [documentation](https://switchai.readthedocs.io/en/latest/api_keys.html). This ensures that SwitchAI can automatically detect and use the appropriate key for the chosen provider.

## Example Usage  

### Chat  

```python
from switchai import SwitchAI

# Initialize the client with the desired AI model
client = SwitchAI(provider="openai", model_name="gpt-4o")

# Send a message and receive a response
response = client.chat(
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

# Print the response
print(response)
```

### Vision  

```python
from switchai import SwitchAI

# Initialize the client with the a vision model
client = SwitchAI(provider="mistral", model_name="pixtral-large-latest")

# Send an image with a question and receive a response
response = client.chat(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image", "image": "path/to/image/file.jpg"},
            ],
        }
    ]
)

# Print the response
print(response)
```

### Text Embedding  

```python
from switchai import SwitchAI

# Initialize the client with the chosen embedding model
client = SwitchAI(provider="google", model_name="models/text-embedding-004")

# Generate embeddings for a list of text inputs
response = client.embed(
    input=[
        "I am feeling great today!",
        "I am feeling sad today."
    ]
)

# Print the response
print(response)
```

### Speech to text  

```python
from switchai import SwitchAI

# Initialize the client with the desired speech-to-text model
client = SwitchAI(provider="deepgram", model_name="nova-2")

# Transcribe an audio file
response = client.transcribe(
    audio_path="path/to/audio/file.wav"
)

# Print the response
print(response)
```

## Documentation  

For full documentation, visit [SwitchAI Documentation](https://switchai.readthedocs.io/).  

## Contributing  

Contributions are always welcome! If you'd like to help enhance SwitchAI, feel free to make a contribution.
