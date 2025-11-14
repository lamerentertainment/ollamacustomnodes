import requests
import numpy as np
from PIL import Image
import io
import base64


class OllamaImageDescriber:
    """
    Custom ComfyUI Node für Bildbeschreibung mit Ollama.
    Sendet ein Bild an Ollama und gibt die Beschreibung sowie CLIP Conditioning zurück.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "model": ("STRING", {"default": "llava:latest"}),
                "prompt": (
                    "STRING",
                    {
                        "default": "Describe this image in detail for use as a prompt for Stable Diffusion.",
                        "multiline": True,
                    },
                ),
                "ollama_url": ("STRING", {"default": "http://localhost:11434"}),
                "temperature": (
                    "FLOAT",
                    {"default": 0.7, "min": 0.0, "max": 2.0, "step": 0.1},
                ),
            },
            "optional": {"clip": ("CLIP",)},
        }

    RETURN_TYPES = ("STRING", "CONDITIONING")
    RETURN_NAMES = ("description", "conditioning")
    FUNCTION = "describe_image"
    CATEGORY = "image/ollama"

    def describe_image(self, image, model, prompt, ollama_url, temperature, clip=None):
        """
        Beschreibt ein Bild mit Ollama und gibt Text + CLIP Conditioning zurück.
        """
        try:
            # Bild vorbereiten (PIL Image)
            img_array = (image[0].cpu().numpy() * 255).astype(np.uint8)
            pil_image = Image.fromarray(img_array)

            # Zu Base64 konvertieren
            img_buffer = io.BytesIO()
            pil_image.save(img_buffer, format="PNG")
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode()

            # Ollama API Request
            url = f"{ollama_url}/api/generate"

            payload = {
                "model": model,
                "prompt": prompt,
                "images": [img_base64],
                "temperature": temperature,
                "stream": False,
            }

            print(f"[OllamaImageDescriber] Sende Anfrage zu {url}")
            print(f"[OllamaImageDescriber] Model: {model}")

            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()

            result = response.json()
            description = result.get("response", "").strip()

            print(f"[OllamaImageDescriber] Antwort erhalten: {description[:100]}...")

            # CLIP Conditioning vorbereiten (falls CLIP vorhanden)
            conditioning = None
            if clip is not None:
                try:
                    tokens = clip.tokenize(description)
                    conditioning = clip.encode_from_tokens(tokens, return_pooled=True)
                    print("[OllamaImageDescriber] CLIP Encoding erfolgreich")
                except Exception as e:
                    print(f"[OllamaImageDescriber] CLIP Encoding fehlgeschlagen: {e}")
                    conditioning = None

            # Fallback Conditioning
            if conditioning is None:
                conditioning = [[np.zeros((1, 768), dtype=np.float32)]]

            return (description, conditioning)

        except requests.exceptions.ConnectionError:
            error_msg = (
                f"Fehler: Kann nicht zu Ollama verbinden unter {ollama_url}. Ist Ollama läuft?"
            )
            print(f"[OllamaImageDescriber] {error_msg}")
            return error_msg, [[np.zeros((1, 768), dtype=np.float32)]]

        except Exception as e:
            error_msg = f"Fehler bei Bildbeschreibung: {str(e)}"
            print(f"[OllamaImageDescriber] {error_msg}")
            return error_msg, [[np.zeros((1, 768), dtype=np.float32)]]


NODE_CLASS_MAPPINGS = {
    "OllamaImageDescriber": OllamaImageDescriber,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OllamaImageDescriber": "Ollama Image Describer",
}