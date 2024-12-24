# Prim Voices API Python Client

A Python client for interacting with the Prim Voices API.

## Installation

```bash
pip install primvoices
```

## Usage

```python
from primvoices import Client
from primvoices.models import ClientConfig

# Initialize the client
client = Client(ClientConfig(
    api_key='your-api-key',
    # Optional: override the base URL
    # base_url='https://custom-api-url.com'
))

# Using context manager (recommended)
with Client(ClientConfig(api_key='your-api-key')) as primvoices:
    # Your code here
    pass

# Working with Voices
async def voice_examples():
    # List all voices
    voices = client.voices.list()
    print('Your voices:', voices.data)

    # List public voices
    public_voices = client.voices.list_public()
    print('Public voices:', public_voices.data)

    # Create a new voice
    new_voice = client.voices.create({
        'name': 'My Custom Voice',
        'sample_url': 'https://example.com/sample.wav',
        'verified': True  # Required: User must explicitly verify they have permission to use this voice
    })
    print('Created voice:', new_voice.data)

    # Get a specific voice
    voice = client.voices.retrieve('voice_id')
    print('Voice details:', voice.data)

    # Get a public voice
    public_voice = client.voices.retrieve_public('public_voice_id')
    print('Public voice details:', public_voice.data)

# Working with Generations
async def generation_examples():
    # List all generations
    generations = client.generations.list()
    print('All generations:', generations.data)

    # Create a new text-to-speech generation
    new_generation = client.generations.create({
        'voice_id': 'voice_id',
        'text': 'Hello, this is a test generation.',
        'quality': 'high',
        'notes': 'Read in a friendly tone'
    })
    print('Created generation:', new_generation.data)

    # Create a voice cloning generation
    voice_clone = client.generations.create({
        'voice_id': 'voice_id',
        'source_url': 'https://example.com/source-audio.wav',
        'quality': 'voice'
    })
    print('Created voice clone:', voice_clone.data)

    # Get a specific generation
    generation = client.generations.retrieve('generation_id')
    print('Generation details:', generation.data)
```

## API Resources

### Voices

- `client.voices.list()` - List all voices for the authenticated user
- `client.voices.list_public()` - List all public voices
- `client.voices.create(params)` - Create a new voice
- `client.voices.retrieve(voice_id)` - Get a specific voice
- `client.voices.retrieve_public(voice_id)` - Get a specific public voice
- `client.voices.delete(voice_id)` - Delete a voice

### Generations

- `client.generations.list()` - List all generations
- `client.generations.create(params)` - Create a new generation
- `client.generations.retrieve(generation_id)` - Get a specific generation
- `client.generations.delete(generation_id)` - Delete a generation

## Development

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT 
