# ComfyUI Ollama Image Describer

Custom ComfyUI Node für Bildbeschreibung mit Ollama. Sendet ein Bild an Ollama und gibt die Beschreibung sowie CLIP Conditioning zurück.

## Installation

### Automatisch (empfohlen)
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/dein-username/ollama_image_describer.git
cd ollama_image_describer
pip install -r requirements.txt
```

### Manuell
1. Erstelle `ComfyUI/custom_nodes/ollama_image_describer/`
2. Kopiere alle Dateien dorthin
3. Installiere Dependencies: `pip install -r requirements.txt`

## Voraussetzungen

- **Ollama läuft** auf `http://localhost:11434` (oder andere URL)
- **Multimodales Modell installiert**:
```bash
ollama pull llava:latest
# oder
ollama pull bakllava
```

## Node-Inputs

| Input | Typ | Standard | Beschreibung |
|-------|-----|---------|--------------|
| `image` | IMAGE | - | Bild von Load Image oder anderen Nodes |
| `model` | STRING | `llava:latest` | Ollama Modellname |
| `prompt` | STRING | Detaillierte Beschreibung | Dein Prompt für die Bildbeschreibung |
| `ollama_url` | STRING | `http://localhost:11434` | Ollama API URL |
| `temperature` | FLOAT | 0.7 | Kreativität (0.0-2.0) |
| `clip` | CLIP (optional) | - | CLIP Model für Conditioning |

## Node-Outputs

| Output | Typ | Beschreibung |
|--------|-----|-------------|
| `description` | STRING | Text-Beschreibung des Bildes |
| `conditioning` | CONDITIONING | CLIP Conditioning für KSampler |

## Beispiel-Workflow
```
Load Image
    ↓
Ollama Image Describer (mit CLIP)
    ↓
    ├→ Description (TEXT) → weitere Verarbeitung
    └→ Conditioning → KSampler
```

## Gute Prompts

- `"Describe this image in detail for use as a prompt for Stable Diffusion."`
- `"What do you see in this image? Be specific and descriptive."`
- `"Describe the subject, style, composition, colors, and mood of this image."`
- `"Create a detailed artistic description suitable for image generation."`

## Empfohlene Modelle

- **llava:latest** (7B) - Schnell, gute Qualität ⭐
- **llava:13b** - Bessere Qualität, langsamer
- **bakllava** - Alternative mit guter Performance

## Troubleshooting

**Fehler: "Kann nicht zu Ollama verbinden"**
- Überprüfe: `ollama list` (Modell installiert?)
- Überprüfe: `ollama serve` läuft im Hintergrund
- Überprüfe URL in Node Settings

**Zu langsam**
- Nutze kleineres Modell (`llava:latest` statt `llava:13b`)
- Erhöhe `temperature` für schnellere Antworten

**Schlechte Beschreibungen**
- Optimiere deinen `prompt`
- Nutze besseres Modell

## Lizenz

MIT

## Support

Probleme? Issues erstellen auf GitHub!
```

**`.gitignore`:**
```
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.env
.DS_Store
*.pyc        