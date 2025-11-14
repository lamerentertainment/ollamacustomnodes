import ollama
import json


class OllamaTextGeneration:
    """
    ComfyUI Custom Node for Ollama Text Generation
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Hello, how are you?"
                }),
                "model": ("STRING", {
                    "default": "llama3.2"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1
                }),
                "max_tokens": ("INT", {
                    "default": 512,
                    "min": 1,
                    "max": 4096,
                    "step": 1
                }),
            },
            "optional": {
                "system_prompt": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 0xffffffffffffffff
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate"
    CATEGORY = "Ollama"

    def generate(self, prompt, model, temperature, max_tokens, system_prompt="", seed=-1):
        try:
            messages = []

            if system_prompt and system_prompt.strip():
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            messages.append({
                "role": "user",
                "content": prompt
            })

            options = {
                "temperature": temperature,
                "num_predict": max_tokens,
            }

            if seed != -1:
                options["seed"] = seed

            response = ollama.chat(
                model=model,
                messages=messages,
                options=options
            )

            generated_text = response['message']['content']

            return (generated_text,)

        except Exception as e:
            error_msg = f"Error generating text with Ollama: {str(e)}"
            print(error_msg)
            return (error_msg,)


class OllamaVision:
    """
    ComfyUI Custom Node for Ollama Vision Models
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Describe this image in detail."
                }),
                "model": ("STRING", {
                    "default": "llava"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1
                }),
            },
            "optional": {
                "system_prompt": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("description",)
    FUNCTION = "analyze_image"
    CATEGORY = "Ollama"

    def analyze_image(self, image, prompt, model, temperature, system_prompt=""):
        try:
            import torch
            import numpy as np
            from PIL import Image
            import io
            import base64

            # Convert ComfyUI image tensor to PIL Image
            # ComfyUI images are in format [batch, height, width, channels] with values 0-1
            i = 255. * image[0].cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

            # Convert to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Encode to base64
            img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')

            messages = []

            if system_prompt and system_prompt.strip():
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })

            messages.append({
                "role": "user",
                "content": prompt,
                "images": [img_base64]
            })

            response = ollama.chat(
                model=model,
                messages=messages,
                options={
                    "temperature": temperature
                }
            )

            description = response['message']['content']

            return (description,)

        except Exception as e:
            error_msg = f"Error analyzing image with Ollama: {str(e)}"
            print(error_msg)
            return (error_msg,)


class OllamaModelList:
    """
    ComfyUI Custom Node to list available Ollama models
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("models_list",)
    FUNCTION = "list_models"
    CATEGORY = "Ollama"
    OUTPUT_NODE = True

    def list_models(self):
        try:
            models = ollama.list()
            model_names = [model['name'] for model in models.get('models', [])]
            models_str = "\n".join(model_names) if model_names else "No models found"
            return (models_str,)
        except Exception as e:
            error_msg = f"Error listing Ollama models: {str(e)}"
            print(error_msg)
            return (error_msg,)


# Node class mappings
NODE_CLASS_MAPPINGS = {
    "OllamaTextGeneration": OllamaTextGeneration,
    "OllamaVision": OllamaVision,
    "OllamaModelList": OllamaModelList,
}

# Node display name mappings
NODE_DISPLAY_NAME_MAPPINGS = {
    "OllamaTextGeneration": "Ollama Text Generation",
    "OllamaVision": "Ollama Vision",
    "OllamaModelList": "Ollama Model List",
}
