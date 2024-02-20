import openai
import streamlit as st
import logging
import random
from openai import OpenAI
from streamlit_drawable_canvas import st_canvas

# Configure OpenAI

client = OpenAI()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize session state variables if they're not already present
if 'text_prompt' not in st.session_state:
    st.session_state['text_prompt'] = ""
if 'generated_image_url' not in st.session_state:
    st.session_state['generated_image_url'] = None
if 'selected_style' not in st.session_state:
    st.session_state['selected_style'] = "Cartoon"  # Default to "Cartoon" or any preferred option

# Set Streamlit page config
st.set_page_config(page_title="Imaginative Idea Generator for Kids", layout="wide")

# App title and header
st.title("🎨 Imaginative Idea Generator for Kids 🚀")

# Function to update the text input field with a random prompt
def update_random_prompt():
    random_prompt = random.choice(prompt_suggestions)
    st.session_state.text_prompt = random_prompt  # Update using dot notation

# Function to generate image from prompt
def generate_image_from_prompt(prompt, style):
    safety_guard = "This is for a children's story, please ensure the content is appropriate for kids aged 1-4. Do not include any text or words in the image. This will be used to help kids draw and doodle so create this with learning and ability to draw image if kid wants to in mind. The child's prompt is:"
    full_prompt = f"{safety_guard} {prompt} Style: {style}."

    logging.info("Starting image generation process...")
    with st.spinner('🖼️ Generating your imaginative idea...'):
        try:
            logging.info(f"Sending prompt to OpenAI API: {full_prompt}")
            response = client.images.generate(
                prompt=full_prompt,
                model="dall-e-3",
                n=1,
                size="1024x1024"
            )
            logging.info("Received response from OpenAI API")
            image_url = response.data[0].url
            logging.info(f"Image generated successfully: {image_url}")
            st.success('🎉 Image generated successfully!')
            return image_url
        except Exception as e:
            logging.error(f"An error occurred during image generation: {e}", exc_info=True)
            st.error(f"An error occurred: {e}")
            return None

# Subheader for inspiration
st.subheader("🌈 Need some inspiration?")

# Button to update the prompt with a random suggestion
st.button("🧚 Give me an idea!", on_click=update_random_prompt)

# Text input for the prompt, directly bound to the session state
text_prompt = st.text_input("🖋️ Type your imaginative idea here:", key='text_prompt')

# Buttons for selecting image style
style_options = ["Cartoon", "Watercolor", "Pastel", "Crayon Drawing", "Sticker Style"]
selected_style = st.radio("🎨 Choose a style for your image:", style_options, index=style_options.index(st.session_state.selected_style), key="selected_style")

# Function to handle the image generation button click
def handle_generate_click():
    generated_image_url = generate_image_from_prompt(st.session_state['text_prompt'], st.session_state['selected_style'])
    if generated_image_url:
        st.session_state['generated_image_url'] = generated_image_url

# Button to generate the image
st.button("🔮 Generate!", on_click=handle_generate_click)

# Display the generated image and sketch area side by side if an image has been generated
if st.session_state['generated_image_url']:
    cols = st.columns(2)  # Create two columns for side by side layout
    with cols[0]:  # First column for the image
        st.image(st.session_state['generated_image_url'], caption="🖼️ Your Imaginative Idea", width=400)
        st.markdown(f"[🎁 Download Image]({st.session_state['generated_image_url']})", unsafe_allow_html=True)
    with cols[1]:  # Second column for the sketch area
        st.header("🖍️ Doodle Your Idea")
        sketch = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",  # Orange with transparency
            stroke_width=10,
            stroke_color="#FFA500",  # Orange
            background_color="#FFFFFF",  # White
            height=400,
            width=400,
            drawing_mode="freedraw",
            display_toolbar=True,
            key="canvas"
        )

# Expanded "Need some inspiration?" section with more prompts
prompt_suggestions = [
    "A magical garden where flowers sing and dance",
    "A friendly monster who loves to paint with rainbow colors",
    "A space adventure to a planet made entirely of desserts",
    "Underwater city where fish can talk and mermaids teach school",
    "A castle in the clouds guarded by flying unicorns",
    "A pirate ship sailing on a sea of stars",
    "A hidden jungle with talking trees and hidden treasures",
    "A fairy village where every leaf is a different color",
    "A music festival organized by animals in the forest",
    "A snowman who dreams of summer and sunbathing on the beach",
    "Dragons baking cakes and cookies in their fiery caves",
    "A superhero squirrel saving the park animals with acorn power",
    "A rainbow bridge connecting two enchanted islands",
    "Aliens visiting Earth to learn about human kids' games",
    "A robot that can turn into any toy to play with",
    "A time machine adventure to meet the dinosaurs",
    "A magical library where books come to life and tell their stories",
    "A secret door in the bedroom leading to a candy land",
    "A circus run by friendly ghosts with magical acts",
    "A space zoo with the most unusual and friendly alien creatures",
    "An underground world with glowing plants and crystal rivers",
    "A treehouse city where kids are the mayors and make the rules",
    "A beach where the sand is soft as powder and the waves sing lullabies",
    "A rainbow-colored waterfall that paints whatever it touches",
    "A friendly giant who carries a garden on his back",
    "Cloud sculpting contests with characters from fairy tales",
    "A tea party with the Queen of Butterflies in a meadow",
    "A magic carpet race around the world’s landmarks",
    "A night sky where stars can be rearranged to create constellations",
    "An ice cream mountain that never melts and has every flavor"
    # Add more prompts as needed
]
