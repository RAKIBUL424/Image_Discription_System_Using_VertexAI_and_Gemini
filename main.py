import streamlit as st
from vertexai.preview.generative_models import GenerativeModel
import vertexai
import tempfile
import os
from PIL import Image as PILImage

# Configure Vertex AI
PROJECT_ID = "your-project-id"
REGION = "us-central1"

vertexai.init(project=PROJECT_ID, location=REGION)

def save_as_supported_format(image_file, output_path):
    with PILImage.open(image_file) as img:
        img = img.convert("RGB")  # Convert to RGB for compatibility
        img.save(output_path, format="PNG")  # Save as PNG

def generate_response(prompt, image_path):
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()
    
    generative_model = GenerativeModel(model_name="gemini-1.0-pro-vision")
    response = generative_model.generate_content([prompt, image_data])
    return response.candidates[0].content.text

def main():
    st.title("Vertex AI with Gemini Pro Vision")
    
    # Image uploader
    img = st.file_uploader("Upload an Image")
    path = None
    if img:
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, f"{img.name}.png")
        save_as_supported_format(img, path)
    
    st.header(":violet[Question]")
    question = st.text_area(label="Enter your Question")
    submit = st.button("Submit")

    if question and submit:
        if not img:
            st.error("Please upload an image before submitting.")
        else:
            try:
                response = generate_response(question, path)
                st.header("Answer")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
