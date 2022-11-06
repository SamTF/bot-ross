###### CONSTANTS #################################################
import io
import os
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

###### Creating API Object #################################################
with open('.api_key', 'r') as f:
        api_key = f.read()

ai = client.StabilityInference(key=api_key, verbose=True)

def generate_img(prompt: str, save_to_disk = True, height:int=512, width:int=512) -> io.BytesIO:
    '''
    Generates an image based on a text prompt using Stable Diffusion.
    Returns bytes-like object.
    '''
    answers = ai.generate(
        prompt=prompt,
        height=height,
        width=width
    )

    print(f'[ART_GENERATOR] >>> generating _{prompt}_')

    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                print('[ART_GENERATOR] >>> generation finished!')

                img = Image.open(io.BytesIO(artifact.binary))

                if save_to_disk:
                    img.save(f'{prompt}.png')
                    print('[ART_GENERATOR] >>> saved image to disk')
                    return None
                
                else:
                    generated_img = io.BytesIO()
                    img.save(generated_img, format='PNG')

                    return generated_img

print('[ART_GENERATOR] ___ INITIALISED ___')