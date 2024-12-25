![Header](https://raw.githubusercontent.com/Aayan-Mishra/Images/refs/heads/main/API%20(1).png)

# Spestly: OdysseyXL Python Package 🌟🌐🚀

This is the Python package for generating high-quality images using the OdysseyXL models hosted on Hugging Face Spaces. These models are designed to produce stunning, realistic outputs for a variety of creative tasks. 📷🎨👩‍🎨

![Grid](https://raw.githubusercontent.com/Aayan-Mishra/Images/refs/heads/main/OdysseyXL%20FINAL.png)

## Features 🔧👨‍🔬

- OdysseyXL 3.0 and 4.0 support: Choose between different model versions for your projects.
- Customizable prompts: Provide detailed prompts and negative prompts to refine your image generation.
- High-resolution output: Generate images up to 1024x1024 resolution.
- Easy integration: Simple API for seamless integration into your projects.

## Installation 📝🛠️🌐

You can install the package directly from PyPI (after uploading):

```bash
pip install spestly
```

## Usage 🎨🔄💡

Here is an example of how to use the spestly package:

```python
from spestly import OdysseyXL

# Initialize the OdysseyXL object
odysseyxl = OdysseyXL()

# Define the prompt and negative prompt
prompt = (
    "An amateur cellphone photography of a black Ferrari. "
    "f8.0, Samsung Galaxy, noise, jpeg artefacts, poor lighting, low light, "
    "underexposed, high contrast"
)
negative_prompt = (
    "(octane render, render, drawing, anime, bad photo, bad photography:1.3), "
    "(worst quality, low quality, blurry:1.2), "
    "(bad teeth, deformed teeth, deformed lips), "
    "(bad anatomy, bad proportions:1.1), "
    "(deformed iris, deformed pupils), "
    "(deformed eyes, bad eyes), "
    "(deformed face, ugly face, bad face), "
    "(deformed hands, bad hands, fused fingers), "
    "morbid, mutilated, mutation, disfigured"
)

# Generate the image using the OdysseyXL model version 3.0
image = odysseyxl.generate(
    model_version="3.0",
    prompt=prompt,
    negative_prompt=negative_prompt,
)

# Save the generated image
image.save("output.png")

# Display the generated image
image.show()
```

## Parameters 🔀🎨📈

### **generate** Method Parameters:

- model_version (str): The version of the OdysseyXL model to use ("3.0" or "4.0").

- prompt (str): The input text prompt for image generation.

- negative_prompt (str): The negative prompt to avoid unwanted elements in the image.

Additional optional parameters are available for advanced customization.

## Contributing 🛠️🎓🚀

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with your changes.

## License 🔒🔧🌐

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments 👨‍🔬🎨🌟

A big thank you to John6666 for hosting the OdysseyXL models on his Hugging Face Space (votepurchase-multiple-model). 📢🔗🌈

Contact 📧📲📊

For questions or support, contact aayan.mishra@proton.me or open an issue on GitHub. 🚀🌐🔄

