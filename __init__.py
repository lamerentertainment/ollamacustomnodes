"""
Ollama Custom Nodes for ComfyUI

This package provides custom nodes for integrating Ollama AI models into ComfyUI workflows.

Nodes included:
- OllamaTextGeneration: Generate text using Ollama models
- OllamaVision: Analyze images using Ollama vision models (like LLaVA)
- OllamaModelList: List all available Ollama models
"""

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
__version__ = "1.0.0"
