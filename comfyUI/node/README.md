# Decor8 AI Virtual Staging Node for ComfyUI

Transform empty spaces into beautifully staged interiors using Decor8 AI's virtual staging capabilities directly in ComfyUI.

## Installation

1. Install the node:
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/immex-tech/decor8ai-sdk.git
cd decor8ai-sdk/comfyUI
pip install -r requirements.txt
```

2. Get your API key from [Decor8 AI Platform](https://prod-app.decor8.ai)
3. Set your API key:
```bash
export DECOR8AI_API_KEY=your_api_key_here
```
4. Restart ComfyUI

## Usage

1. Add "Decor8 AI Virtual Staging" node to your workflow
2. Connect an image input
3. Select:
   - Room type (e.g., livingroom, bedroom)
   - Design style (e.g., modern, minimalist)
4. Optional: Configure additional parameters
   - Custom prompt
   - Color scheme
   - Seasonal décor
   - Guidance scale
   - Inference steps

## Example Workflow

See `examples/basic_workflow.json` for a sample workflow.

## Support

- Documentation: https://api-docs.decor8.ai
- Issues: https://github.com/immex-tech/decor8ai-sdk/issues
- Email: decor8@immex.tech 