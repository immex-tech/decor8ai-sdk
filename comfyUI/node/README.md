# Decor8 AI Virtual Staging Node for ComfyUI

[![ComfyUI Registry](https://img.shields.io/badge/ComfyUI-Registry-blue)](https://registry.comfy.org/publishers/decor8ai/nodes/decor8ai-comfyui)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Virtual Staging** and **AI Interior Design** directly in ComfyUI. Transform empty spaces into beautifully staged interiors using **[Decor8 AI](https://www.decor8.ai)**'s powerful **AI room design** technology.

## Features

- **AI Virtual Staging** - Fill empty rooms with furniture and decor
- **AI Interior Design** - Apply 50+ design styles to any room
- **Seamless Integration** - Works natively in ComfyUI workflows
- **Real-time Preview** - See **AI room design** results instantly

## Installation

```bash
comfy node registry-install decor8ai-comfyui
```

Or install manually:
1. Clone this repository into your ComfyUI `custom_nodes` folder
2. Restart ComfyUI

## API Key Required

This node requires an API key from **[Decor8 AI Platform](https://prod-app.decor8.ai)**:

1. Sign up at [prod-app.decor8.ai](https://prod-app.decor8.ai)
2. Choose a prepaid plan or subscribe to pay-as-you-go
3. Get your API key from the dashboard

## Usage

1. Add **"Decor8 AI Virtual Staging"** node to your workflow
2. Connect an image input
3. Enter your API key
4. Select:
   - **Room type** (e.g., LIVINGROOM, BEDROOM, KITCHEN)
   - **Design style** (e.g., MODERN, MINIMALIST, SCANDINAVIAN)
5. Execute to generate **AI interior design** results

## Supported Room Types

| Room Types      |               |               |               |
|-----------------|---------------|---------------|---------------|
| LIVINGROOM      | KITCHEN       | DININGROOM    | BEDROOM       |
| BATHROOM        | KIDSROOM      | FAMILYROOM    | OFFICE        |
| FOYER           | BASEMENT      | GARAGE        | BALCONY       |

## Supported Design Styles

50+ **AI interior design** styles available:

| Styles          |                    |                    |                    |
|-----------------|--------------------|--------------------|--------------------|
| MINIMALIST      | SCANDINAVIAN       | INDUSTRIAL         | BOHO               |
| MODERN          | CONTEMPORARY       | TRADITIONAL        | FARMHOUSE          |
| COASTAL         | MIDCENTURYMODERN   | ARTDECO            | JAPANDI            |

See [full style list](https://api-docs.decor8.ai/) in the API documentation.

## Example Workflow

See `examples/basic_workflow.json` for a sample workflow demonstrating **AI virtual staging** integration.

## Use Cases

- **Real Estate Virtual Staging** - Transform empty property photos with **AI room design**
- **Interior Design Visualization** - Preview **AI interior design** concepts
- **Architectural Rendering** - Enhance architectural visualizations with **AI home decorations**
- **Creative Workflows** - Integrate **AI virtual staging** into ComfyUI pipelines

## Links

- [Decor8 AI Platform](https://www.decor8.ai) - Get started with AI interior design
- [API Documentation](https://api-docs.decor8.ai/) - Complete API reference
- [API Playground](https://api-docs.decor8.ai/playground) - Try the API interactively
- [Pricing & Plans](https://www.decor8.ai) - View pricing options
- [GitHub Repository](https://github.com/immex-tech/decor8ai-sdk) - SDK source code

## Support

- **Documentation:** [api-docs.decor8.ai](https://api-docs.decor8.ai)
- **Issues:** [GitHub Issues](https://github.com/immex-tech/decor8ai-sdk/issues)
- **Email:** [decor8@immex.tech](mailto:decor8@immex.tech)

---

**Keywords:** AI Interior Design, AI Virtual Staging, ComfyUI virtual staging, AI room design, Interior design by AI, AI home decorations, ComfyUI interior design
