import openai
import streamlit as st
from openai import OpenAI
import logging
import random
from PIL import Image
import requests
from streamlit_drawable_canvas import st_canvas

# Configure OpenAI
client = OpenAI()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set Streamlit page config
st.set_page_config(page_title="Imaginative Idea Generator for Kids", layout="wide")

# Define a key for the text input widget and initialize the session state for the text prompt
text_input_key = 'text_prompt_key'
if 'text_prompt' not in st.session_state:
    st.session_state['text_prompt'] = ""
if 'generated_image_url' not in st.session_state:
    st.session_state['generated_image_url'] = None

# Function to update the text input field with a random prompt
def update_random_prompt():
    random_prompt = random.choice(prompt_suggestions)
    st.session_state['text_prompt'] = random_prompt

# Function to handle button clicks for generating the image
def handle_button_clicks():
    if st.button("🧚 Give me an idea!"):
        update_random_prompt()

    if st.button("🔮 Generate!"):
        generated_image_url = generate_image_from_prompt(st.session_state['text_prompt'], selected_style)
        if generated_image_url:
            st.session_state['generated_image_url'] = generated_image_url

# Function to generate image from prompt
def generate_image_from_prompt(prompt, style):
    safety_guard = "This is for a children's story, please ensure the content is appropriate for kids aged 1-4. Do not include any text or words in the image. This will be used to help kids draw and doodle so create this with learning and ability to draw image if kid wants to in mind. The child's prompt is:"
    full_prompt = f"{safety_guard} {prompt} Style: {style}."

    logging.info("Starting image generation process...")
    with st.spinner('🖼️ Generating your imaginative idea...'):
        try:
            logging.info(f"Sending prompt to OpenAI API: {full_prompt}")
            response = client.images.generate(
                model="dall-e-3",
                prompt=full_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            logging.info("Received response from OpenAI API")
            image_url = response.data[0].url
            logging.info(f"Image generated successfully: {image_url}")
            st.success('🎉 Image generated successfully!')
            return image_url
        except Exception as e:  # Catching a more general exception
            logging.error(f"An error occurred during image generation: {e}", exc_info=True)
            st.error(f"An error occurred: {e}")
            return None



# App title and header
st.title("🎨 Imaginative Idea Generator for Kids 🚀")

# Placeholder frame for the generated image
placeholder_frame = st.empty()

# Shape for the frame
st.markdown("<div class='frame-shape'></div>", unsafe_allow_html=True)

# Sketch area for doodling
st.header("🖍️ Doodle Your Idea")
sketch = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Orange with transparency
    stroke_width=10,
    stroke_color="#FFA500",  # Orange
    background_color="#FFFFFF",  # White
    height=400,  # Adjusted height to match the output image
    width=400,   # Adjusted width to match the output image
    drawing_mode="freedraw",
    display_toolbar=True,
    key="canvas"
)

# Text input for the prompt, using the session state to set its value
text_prompt = st.text_input("🖋️ Type your imaginative idea here:", value=st.session_state['text_prompt'], key=text_input_key)

# Buttons for selecting image style
style_options = ["Cartoon", "Watercolor", "Pastel", "Crayon Drawing", "Sticker Style"]
selected_style = st.radio("🎨 Choose a style for your image:", style_options, index=0, key="style_radio")

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
]

# Expanded "Need some inspiration?" section with more prompts
st.subheader("🌈 Need some inspiration?")

# Generate magic button
handle_button_clicks()

# Display the generated image
if st.session_state['generated_image_url']:
    placeholder_frame.image(st.session_state['generated_image_url'], caption="🖼️ Your Imaginative Idea", width=400, use_column_width=False)
    st.markdown(f"[🎁 Download Image]({st.session_state['generated_image_url']})", unsafe_allow_html=True)
