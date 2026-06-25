import sys
import os
import requests

def generate_3d_model_from_image(image_path, output_path):
    print(f"Generating 3D model from image: {image_path}")
    print(f"Output will be saved to: {output_path}")

    # Here, you would integrate with an AI service or a GitHub Model API
    # that can convert a 2D image into a 3D model (e.g., an OBJ or GLB file).
    # This is a placeholder for the actual AI model interaction.

    # Example using a hypothetical API:
    # api_endpoint = "https://api.github.com/models/image-to-3d"
    # github_token = os.environ.get("GITHUB_TOKEN")

    # if not github_token:
    #     print("Error: GITHUB_TOKEN not found in environment variables.")
    #     sys.exit(1)

    # headers = {
    #     "Authorization": f"token {github_token}",
    #     "Content-Type": "application/json"
    # }

    # with open(image_path, "rb") as f:
    #     image_data = f.read()

    # response = requests.post(api_endpoint, headers=headers, data=image_data)

    # if response.status_code == 200:
    #     with open(output_path, "wb") as f:
    #         f.write(response.content)
    #     print("3D model generated successfully.")
    # else:
    #     print(f"Error generating 3D model: {response.status_code} - {response.text}")
    #     sys.exit(1)

    # Using GitHub Models (GPT-4o) to generate a 3D OBJ mesh representation.
    # Note: GPT-4o cannot directly output binary files like GLB, but it can generate OBJ text.
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Error: GITHUB_TOKEN not found.")
        sys.exit(1)

    # API Endpoint for GitHub Models (OpenAI compatible)
    api_url = "https://models.inference.ai.azure.com/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json"
    }

    # Prompting GPT-4o to generate a simplified OBJ file based on the image description.
    # We use a base-64 encoded image to allow GPT-4o to "see" the mannequin.
    import base64
    
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    base64_image = encode_image(image_path)

    prompt = """
    You are a 3D modeling expert. Analyze the attached image of a human mannequin and generate a 3D OBJ file representing its geometry.
    - Create a low-poly human-shaped mesh (head, torso, arms, legs).
    - Ensure the vertices (v) and faces (f) form a valid manifold 3D object.
    - The output MUST be ONLY the raw OBJ file content.
    - Do not include any text, markdown formatting, or explanation.
    - Start with 'v ' and end with the last 'f ' line.
    """

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "temperature": 0.1
    }

    print("Requesting 3D mesh from GitHub Models...")
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        obj_content = response.json()['choices'][0]['message']['content']
        # Clean up any markdown code blocks if present
        if "```" in obj_content:
            obj_content = obj_content.split("```")[1]
            if obj_content.startswith("obj"):
                obj_content = obj_content[3:]
        
        with open(output_path, "w") as f:
            f.write(obj_content.strip())
        print(f"3D model (OBJ) generated successfully at {output_path}")
    else:
        print(f"Error from GitHub Models: {response.status_code} - {response.text}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate_3d_model.py <input_image_path> <output_obj_path>")
        sys.exit(1)

    input_image = sys.argv[1]
    output_obj = sys.argv[2]

    generate_3d_model_from_image(input_image, output_obj)
