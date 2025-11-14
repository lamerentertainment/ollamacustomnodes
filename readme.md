# Ollama Custom Nodes for ComfyUI

Custom nodes for integrating Ollama AI models into your ComfyUI workflows.

## Features

- **Ollama Text Generation**: Generate text using any Ollama text model
- **Ollama Vision**: Analyze images using Ollama vision models (like LLaVA)
- **Ollama Model List**: List all available Ollama models on your system

## Installation

1. Clone this repository into your ComfyUI custom_nodes folder:
   ```bash
   cd ComfyUI/custom_nodes
   git clone <this-repo-url> ollamacustomnodes
   ```

2. Install requirements:
   ```bash
   cd ollamacustomnodes
   pip install -r requirements.txt
   ```

3. Make sure Ollama is installed and running on your system:
   - Download from: https://ollama.ai
   - Pull a model: `ollama pull llama3.2`
   - For vision: `ollama pull llava`

4. Restart ComfyUI

## Usage

### Ollama Text Generation

This node generates text using Ollama models.

**Inputs:**
- `prompt` (STRING): Your text prompt
- `model` (STRING): Model name (e.g., "llama3.2", "mistral", "codellama")
- `temperature` (FLOAT): Controls randomness (0.0-2.0)
- `max_tokens` (INT): Maximum tokens to generate
- `system_prompt` (STRING, optional): System prompt for model behavior
- `seed` (INT, optional): Seed for reproducibility (-1 for random)

**Outputs:**
- `text` (STRING): Generated text

### Ollama Vision

This node analyzes images using vision-capable Ollama models.

**Inputs:**
- `image` (IMAGE): Input image from ComfyUI
- `prompt` (STRING): Question or instruction about the image
- `model` (STRING): Vision model name (e.g., "llava", "bakllava")
- `temperature` (FLOAT): Controls randomness
- `system_prompt` (STRING, optional): System prompt

**Outputs:**
- `description` (STRING): Model's response about the image

### Ollama Model List

Lists all available Ollama models on your system.

**Outputs:**
- `models_list` (STRING): Newline-separated list of model names

## Available Ollama Models

Some popular models you can use:
- `llama3.2` - Latest Llama model
- `mistral` - Mistral AI model
- `codellama` - Code-specialized model
- `llava` - Vision model for image analysis
- `phi3` - Microsoft's Phi-3 model

Pull models with: `ollama pull <model-name>`

## Requirements

- ComfyUI
- Ollama installed and running
- Python packages: ollama

## Troubleshooting

**Nodes don't appear in ComfyUI:**
- Make sure you installed the requirements: `pip install -r requirements.txt`
- Restart ComfyUI completely
- Check the ComfyUI console for error messages

**"Connection refused" errors:**
- Make sure Ollama is running: `ollama serve`
- Check if Ollama is accessible: `ollama list`

**Model not found:**
- Pull the model first: `ollama pull <model-name>`
- Verify it's installed: `ollama list`

## License

MIT
