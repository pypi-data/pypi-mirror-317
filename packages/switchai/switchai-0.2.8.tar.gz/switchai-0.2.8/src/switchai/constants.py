SUPPORTED_MODELS = {
    "openai": {
        "chat": ["gpt-4o-mini", "gpt-4o", "o1-preview", "o1-mini", "gpt-4"],
        "embed": ["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"],
        "transcribe": ["whisper-1"],
        "generate_image": ["dall-e-3", "dall-e-2"],
    },
    "mistral": {
        "chat": [
            "mistral-large-latest",
            "mistral-small-latest",
            "pixtral-large-latest",
            "pixtral-12b",
            "open-mistral-7b",
            "open-mixtral-8x7b",
            "open-mixtral-8x22b",
        ],
        "embed": ["mistral-embed"],
    },
    "xai": {"chat": ["grok-beta", "grok-vision-beta"]},
    "anthropic": {"chat": ["claude-3-5-sonnet-latest", "claude-3-5-haiku-latest", "claude-3-opus-latest"]},
    "google": {
        "chat": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.5-flash-8b"],
        "embed": ["models/text-embedding-004", "models/embedding-001"],
    },
    "deepgram": {
        "transcribe": [
            "nova-2",
            "nova",
            "enhanced",
            "base",
            "whisper-tiny",
            "whisper-small",
            "whisper-base",
            "whisper-medium",
            "whisper-large",
        ]
    },
    "voyageai": {
        "embed": [
            "voyage-3-large",
            "voyage-3",
            "voyage-3-lite",
            "voyage-code-3",
            "voyage-finance-2",
            "voyage-law-2",
            "voyage-code-2",
        ]
    },
    "replicate": {
        "transcribe": ["openai/whisper"],
        "generate_image": ["black-forest-labs/flux-schnell", "stability-ai/sdxl"],
    },
}

API_KEYS_NAMING = {
    "openai": "OPENAI_API_KEY",
    "mistral": "MISTRAL_API_KEY",
    "xai": "XAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GEMINI_API_KEY",
    "deepgram": "DEEPGRAM_API_KEY",
    "voyageai": "VOYAGE_API_KEY",
    "replicate": "REPLICATE_API_TOKEN",
}
