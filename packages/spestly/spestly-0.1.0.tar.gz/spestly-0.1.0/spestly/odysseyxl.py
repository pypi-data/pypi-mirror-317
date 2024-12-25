from gradio_client import Client
from PIL import Image
import os

class OdysseyXL:
    def __init__(self):
        # Initialize the Gradio client with the specific API endpoint
        print("Thank you to John6666 for hosting the OdysseyXL models on his Votepurchase-multiple-model HuggingFace Space!")
        self.client = Client("John6666/votepurchase-multiple-model")
        
        # Define model names for different versions
        self.models = {
            "3.0": "Spestly/OdysseyXL-3.0",
            "4.0": "Spestly/OdysseyXL-4.0"
        }
        


    def generate(
        self,
        model_version,
        prompt,
        negative_prompt,
        preprocessor_name="Canny",
        prompt_ad_a="Hello!!",  # Default value for prompt_ad_a
        negative_prompt_ad_a="Hello!!",  # Default value for negative_prompt_ad_a
        strength_ad_a=0.35,  # Default value for strength_ad_a
        prompt_ad_b="Hello!!",  # Default value for prompt_ad_b
        negative_prompt_ad_b="Hello!!",  # Default value for negative_prompt_ad_b
        strength_ad_b=0.35,  # Default value for strength_ad_b
        # Add any other missing parameters with default values here...
    ):
        # Ensure the model version is valid
        if model_version not in self.models:
            raise ValueError("Model version must be '3.0' or '4.0'.")
        
        model_name = self.models[model_version]

        # Define the parameters to pass to the Gradio client for the prediction
        params = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "seed": 0,
            "randomize_seed": True,
            "width": 1024,
            "height": 1024,
            "guidance_scale": 7,
            "num_inference_steps": 35,
            "model_name": model_name,
            "task": "txt2img",
            "sampler": "Euler",
            "vae": "None",
            "clip_skip": True,
            "strength": 0.55,
            "image_resolution": 1024,
            "controlnet_model": "Automatic",
            "hires_steps": 30,
            "hires_denoising_strength": 0.55,
            "hires_sampler": "Use same sampler",
            "hires_schedule_type": "Use same schedule type",
            "hires_guidance_scale": -1,
            "hires_prompt": prompt,
            "hires_negative_prompt": negative_prompt,
            "gpu_duration": 59,
            "api_name": "/infer",
            "preprocessor_name": preprocessor_name,
            "prompt_ad_a": prompt_ad_a,
            "negative_prompt_ad_a": negative_prompt_ad_a,
            "strength_ad_a": strength_ad_a,
            "prompt_ad_b": prompt_ad_b,
            "negative_prompt_ad_b": negative_prompt_ad_b,
            "strength_ad_b": strength_ad_b,
        }

        # Make the prediction call
        result = self.client.predict(**params)

        # Check if the result is a file path (temporary file)
        if isinstance(result, str) and result.startswith("/private"):
            # It's a temporary file path, so let's read the image from the file
            try:
                image = Image.open(result)
            except Exception as e:
                raise ValueError("Error reading image from file: " + str(e))
        else:
            # Handle unexpected result format (base64 or URL)
            raise ValueError("Unexpected result format: " + str(result))

        return image
