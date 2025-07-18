import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_js_eval import get_geolocation
import hashlib
import json
import asyncio
import requests

# --- Constants ---
DATA_FILE = "recipes.csv"
UPLOAD_DIR = "uploads"

# Create uploads folder if not exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- Initial CSV setup and column check ---
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=[
        "Timestamp", "Username", "Full Name", "Email", "Geolocation",
        "Category", "Title", "Description", "Ingredients", "Steps",
        "ImageFile", "AudioFile", "VideoFile", "CorpusType"
    ])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)
    required_media_cols = ["ImageFile", "AudioFile", "VideoFile", "CorpusType"]
    for col in required_media_cols:
        if col not in df.columns:
            df[col] = ''
        df[col] = df[col].astype(str).fillna('')
    # Ensure Title column is always string and stripped for robust comparison
    if 'Title' in df.columns:
        df['Title'] = df['Title'].astype(str).str.strip()
    df.to_csv(DATA_FILE, index=False)


# --- User management ---
CREDENTIALS = {
    "admin": hashlib.sha256("password123".encode()).hexdigest(),
    "user1": hashlib.sha256("mypassword".encode()).hexdigest()
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(username, password):
    if username in CREDENTIALS:
        return CREDENTIALS[username] == hash_password(password)
    return False

# --- Geolocation Function ---
# This function will now be called explicitly to process the result of get_geolocation()
# and update the session state with a clear status.
def process_geolocation_result():
    # Only attempt to get geolocation if a request has been triggered
    if st.session_state.get("geolocation_status") == "request_pending":
        result = get_geolocation() # This is where the JS call is initiated. Returns None initially.

        if result: # This block executes on the subsequent rerun when the JS result is available
            coords = result.get("coords")
            if coords:
                lat = coords.get("latitude")
                lon = coords.get("longitude")
                if lat is not None and lon is not None:
                    st.session_state["geolocation_status"] = "detected"
                    st.session_state["geolocation_display"] = f"{lat:.6f}, {lon:.6f}"
                    st.session_state["geolocation_value"] = f"{lat:.6f}, {lon:.6f}" # The value to save to CSV
                else:
                    st.session_state["geolocation_status"] = "error"
                    st.session_state["geolocation_display"] = "Unable to get precise coordinates."
                    st.session_state["geolocation_error_message"] = "Coordinates data missing from browser response."
            else:
                st.session_state["geolocation_status"] = "error"
                st.session_state["geolocation_display"] = "Geolocation data not available."
                st.session_state["geolocation_error_message"] = "Browser did not provide coordinate data."
        else:
            # If result is None here, it means the JS call was just initiated,
            # or permission was denied immediately (e.g., if browser setting is strict).
            # We don't set an error state here, as it will be caught in the next rerun.
            pass # Keep status as "request_pending" or "detecting"

# --- UI Components and Logic ---

def login():
    st.title("🔒 Recipe Vault Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if verify_password(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error("Invalid username or password.")

def logout():
    if st.sidebar.button("Logout", key="logout_button_sidebar"):
        for key in ["logged_in", "username", "geolocation_status", "geolocation_display", "geolocation_value", "geolocation_error_message", "current_page", "selected_recipe_data", "selected_recipe_title_for_view", "chatbot_messages"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def display_recipe_details(selected_recipe):
    st.title(f"🍽️ Recipe: {selected_recipe['Title']}")
    st.write(f"**Category:** {selected_recipe['Category']}")
    st.write(f"**Submitted by:** {selected_recipe['Full Name']} ({selected_recipe['Username']}) at {selected_recipe['Timestamp']} from {selected_recipe['Geolocation']}")
    st.write(f"**Primary Corpus Type:** {selected_recipe['CorpusType']}")

    if selected_recipe['CorpusType'] == 'Video-based' and selected_recipe['VideoFile']:
        video_path = os.path.join(UPLOAD_DIR, selected_recipe['VideoFile'])
        if os.path.exists(video_path):
            st.subheader("🎥 Video Instructions")
            st.video(video_path, format='video/mp4')
        else:
            st.info(f"Video file not found: {selected_recipe['VideoFile']}")
    elif selected_recipe['CorpusType'] == 'Audio-based' and selected_recipe['AudioFile']:
        audio_path = os.path.join(UPLOAD_DIR, selected_recipe['AudioFile'])
        if os.path.exists(audio_path):
            st.subheader("🎙️ Audio Instructions")
            st.audio(audio_path, format='audio/wav')
        else:
            st.info(f"Audio file not found: {selected_recipe['AudioFile']}")
    elif selected_recipe['ImageFile']:
        image_path = os.path.join(UPLOAD_DIR, selected_recipe['ImageFile'])
        if os.path.exists(image_path):
            st.image(image_path, caption=f"Image for {selected_recipe['Title']}", use_column_width=True)
        else:
            st.info(f"Image file not found: {selected_recipe['ImageFile']}")

    st.write(f"**Description:** {selected_recipe['Description']}")
    if selected_recipe['CorpusType'] == 'Text-based' or selected_recipe['CorpusType'] == '':
        st.write(f"**Ingredients:** {selected_recipe['Ingredients']}")
        st.write(f"**Preparation Steps:** {selected_recipe['Steps']}")
    else:
        with st.expander("Show Text Ingredients & Steps"):
            st.write(f"**Ingredients:** {selected_recipe['Ingredients']}")
            st.write(f"**Preparation Steps:** {selected_recipe['Steps']}")

    st.markdown("---")
    if st.button("⬅️ Back to All Recipes"):
        st.session_state["current_page"] = "view_all_recipes"
        st.session_state["selected_recipe_data"] = None
        st.rerun()

def view_all_recipes():
    st.title("📚 All Submitted Recipes")
    df = pd.read_csv(DATA_FILE, dtype={
        "ImageFile": str, "AudioFile": str, "VideoFile": str, "CorpusType": str
    }).fillna('')
    
    if 'Title' in df.columns:
        df['Title'] = df['Title'].astype(str).str.strip()

    if df.empty:
        st.info("No recipes have been submitted yet.")
    else:
        st.dataframe(df[[
            "Timestamp", "Username", "Title", "Category", "Geolocation", "CorpusType"
        ]])

        st.markdown("---")
        st.subheader("View Specific Recipe Details")
        unique_titles = df["Title"].dropna().unique()
        
        if len(unique_titles) == 0:
            st.info("No recipes with titles available to select for detailed viewing.")
            st.session_state["selected_recipe_title_for_view"] = ''
            st.session_state["selected_recipe_data"] = None
            return

        options = [''] + sorted(list(unique_titles))
        current_selected_title = st.session_state.get("selected_recipe_title_for_view", '')

        try:
            initial_select_index = options.index(current_selected_title)
        except ValueError:
            initial_select_index = 0

        selected_title_from_widget = st.selectbox(
            "Select a recipe to view details:",
            options,
            index=initial_select_index,
            key='view_recipes_selectbox'
        )

        if selected_title_from_widget:
            if selected_title_from_widget != current_selected_title:
                matching_recipes = df[df["Title"] == selected_title_from_widget.strip()]

                if not matching_recipes.empty:
                    selected_recipe = matching_recipes.iloc[0]
                    st.session_state["selected_recipe_data"] = selected_recipe.to_dict()
                    st.session_state["selected_recipe_title_for_view"] = selected_title_from_widget
                    st.session_state["current_page"] = "recipe_details"
                    st.rerun()
                else:
                    st.error(f"Recipe with title '{selected_title_from_widget}' not found in the data. Please select an existing recipe from the dropdown.")
                    st.session_state["selected_recipe_title_for_view"] = ''
                    st.session_state["selected_recipe_data"] = None
        else:
            if st.session_state["current_page"] == "recipe_details":
                st.session_state["current_page"] = "view_all_recipes"
                st.session_state["selected_recipe_data"] = None
                st.session_state["selected_recipe_title_for_view"] = ''
                st.rerun()


def recipe_submission(username):
    st.title("📋 Submit a Recipe")

    st.subheader("👤 User Details")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")

    st.subheader("📍 Geolocation (Auto-detected)")
    st.text("Your Coordinates (Latitude, Longitude)")

    # Display geolocation status/value
    st.text_input("Current Geolocation", st.session_state["geolocation_display"], disabled=True, label_visibility="hidden")

    # Provide user guidance based on status
    if st.session_state["geolocation_status"] == "initial":
        st.info("Click 'Refresh Location' to detect your current coordinates.")
    elif st.session_state["geolocation_status"] == "request_pending":
        st.info("Detecting location... Your browser may ask for permission. Please allow it.")
    elif st.session_state["geolocation_status"] == "error":
        st.warning(f"Location not detected: {st.session_state['geolocation_error_message']}")
        st.info("Please ensure your browser allows location access for this site. Check pop-ups or browser settings (e.g., Privacy and security -> Site settings -> Location).")
    
    if st.button("🔄 Refresh Location"):
        st.session_state["geolocation_status"] = "request_pending" # Trigger new request
        st.session_state["geolocation_display"] = "Detecting..." # Immediate feedback
        st.session_state["geolocation_error_message"] = "" # Clear previous error
        st.rerun() # Crucial to trigger the JS call in process_geolocation_result()


    st.subheader("📚 Corpus Category")
    category = st.text_input("Enter category of corpus (e.g. Dessert, Main Course, Snack)")

    st.subheader("📝 Recipe Details")
    title = st.text_input("Recipe Title") # This title will be stripped when saved
    description = st.text_area("Description")

    st.subheader("Select Primary Corpus Type")
    corpus_type = st.radio(
        "Choose how you want to provide recipe instructions:",
        ('Text-based', 'Audio-based', 'Video-based'),
        key='corpus_type_selector'
    )

    ingredients = ""
    steps = ""
    image_file = None
    audio_file = None
    video_file = None

    if corpus_type == 'Text-based':
        st.markdown("---")
        st.subheader("Text Instructions")
        ingredients = st.text_area("Ingredients (separate by commas)", key='ingredients_text')
        steps = st.text_area("Preparation Steps", key='steps_text')
        st.caption("Provide detailed text instructions.")

    elif corpus_type == 'Audio-based':
        st.markdown("---")
        st.subheader("🎙️ Audio Instructions")
        audio_file = st.file_uploader("Choose an audio file...", type=["mp3", "wav"], key='audio_file_uploader')
        st.caption("Record your recipe instructions as audio.")
        with st.expander("Optional: Add Text Ingredients & Steps"):
            ingredients = st.text_area("Ingredients (separate by commas - optional)", key='ingredients_audio_opt')
            steps = st.text_area("Preparation Steps (optional)", key='steps_audio_opt')

    elif corpus_type == 'Video-based':
        st.markdown("---")
        st.subheader("🎥 Video Instructions")
        video_file = st.file_uploader("Choose a video file...", type=["mp4", "mov", "avi", "webm"], key='video_file_uploader')
        st.caption("Upload a video demonstrating your recipe.")
        with st.expander("Optional: Add Text Ingredients & Steps"):
            ingredients = st.text_area("Ingredients (separate by commas - optional)", key='ingredients_video_opt')
            steps = st.text_area("Preparation Steps (optional)", key='steps_video_opt')

    st.markdown("---")
    st.subheader("📷 Recipe Image (Optional for all types)")
    image_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key='image_file_uploader')


    if st.button("Submit Recipe"):
        validation_passed = True
        error_messages = []

        if not all([full_name.strip(), email.strip(), category.strip(), title.strip(), description.strip()]):
            error_messages.append("Please fill in all general recipe details (Full Name, Email, Category, Title, Description).")
            validation_passed = False

        if corpus_type == 'Text-based':
            if not all([ingredients.strip(), steps.strip()]):
                error_messages.append("For 'Text-based' corpus, Ingredients and Preparation Steps are required.")
                validation_passed = False
        elif corpus_type == 'Audio-based':
            if not audio_file:
                error_messages.append("For 'Audio-based' corpus, an Audio file is required.")
                validation_passed = False
        elif corpus_type == 'Video-based':
            if not video_file:
                error_messages.append("For 'Video-based' corpus, a Video file is required.")
                validation_passed = False

        if not validation_passed:
            for msg in error_messages:
                st.error(msg)
            return

        new_data = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Username": username,
            "Full Name": full_name.strip(),
            "Email": email.strip(),
            "Geolocation": st.session_state.get("geolocation_value", "Not detected"), # Use the stored value
            "Category": category.strip(),
            "Title": title.strip(), # Strip title when saving to CSV
            "Description": description.strip(),
            "Ingredients": ingredients.strip(),
            "Steps": steps.strip(),
            "ImageFile": image_file.name if image_file else "",
            "AudioFile": audio_file.name if audio_file else "",
            "VideoFile": video_file.name if video_file else "",
            "CorpusType": corpus_type
        }

        try:
            df = pd.read_csv(DATA_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=[
                "Timestamp", "Username", "Full Name", "Email", "Geolocation",
                "Category", "Title", "Description", "Ingredients", "Steps",
                "ImageFile", "AudioFile", "VideoFile", "CorpusType"
            ])

        for col in ["ImageFile", "AudioFile", "VideoFile", "CorpusType"]:
            if col not in df.columns:
                df[col] = ''
            df[col] = df[col].astype(str).fillna('')
        if 'Title' in df.columns:
            df['Title'] = df['Title'].astype(str).str.strip()


        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        if image_file:
            image_path = os.path.join(UPLOAD_DIR, image_file.name)
            with open(image_path, "wb") as f:
                f.write(image_file.getbuffer())

        if audio_file:
            audio_path = os.path.join(UPLOAD_DIR, audio_file.name)
            with open(audio_path, "wb") as f:
                f.write(audio_file.getbuffer())

        if video_file:
            video_path = os.path.join(UPLOAD_DIR, video_file.name)
            with open(video_path, "wb") as f:
                f.write(video_file.getbuffer())

        st.success("✅ Recipe submitted successfully!")
        st.rerun()

# --- Chatbot Section ---
async def food_chatbot_section():
    st.title("🤖 Food Mood Chatbot")
    st.write("Tell me how you're feeling, and I'll suggest some food from your collected recipes!")

    if "chatbot_messages" not in st.session_state:
        # Initial greeting logic for the first time the chatbot is loaded
        st.session_state.chatbot_messages = [{"role": "assistant", "content": "Hello there! What kind of food are you in the mood for today? Tell me about your mood!"}]

    for message in st.session_state.chatbot_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("How are you feeling?"):
        st.session_state.chatbot_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Load recipes to pass to the LLM
        try:
            recipes_df = pd.read_csv(DATA_FILE, dtype={
                "ImageFile": str, "AudioFile": str, "VideoFile": str, "CorpusType": str
            }).fillna('')
            if 'Title' in recipes_df.columns and 'Category' in recipes_df.columns:
                available_recipes = []
                for index, row in recipes_df.iterrows():
                    available_recipes.append(f"- {row['Title']} ({row['Category']})")
                recipes_list_str = "\n".join(available_recipes)
                if not recipes_list_str:
                    recipes_list_str = "No recipes available in your collection yet."
            else:
                recipes_list_str = "Recipe data is missing 'Title' or 'Category' columns."
                
        except FileNotFoundError:
            recipes_list_str = "No recipes have been submitted yet. Please submit some recipes first."
        except Exception as e:
            recipes_list_str = f"Error loading recipes: {e}"

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Construct the LLM prompt with recipe information and greeting logic
                    llm_prompt = f"""
The user's current message is: '{prompt}'.
You need to suggest a recipe from the following list of available recipes based on the user's mood or general request.
If a suitable recipe is not found in the list, you can suggest a general food item or type of cuisine that matches the mood, but prioritize the provided list.

Available Recipes in the app:
{recipes_list_str}

**Instructions for response:**
- If the user's message is a simple greeting (e.g., "hello", "hi", "hey", "good morning", "what's up"), respond with a friendly greeting back and then ask them about their mood and what kind of food they are in the mood for.
- Otherwise, based on their mood or query, suggest one recipe from the list (if applicable) and a brief reason why it fits.
- Keep your response concise, around 2-3 sentences.
- Do not ask follow-up questions unless it's the initial mood inquiry after a greeting.
- If you suggest a recipe from the list, just mention its name and why it fits the mood.
"""

                    chatHistory = []
                    chatHistory.append({ "role": "user", "parts": [{ "text": llm_prompt }] })
                    payload = { "contents": chatHistory }
                    
                    # IMPORTANT: Replace YOUR_ACTUAL_API_KEY_HERE with your actual Google Generative AI API Key
                    apiKey = "AIzaSyA-Juywn6NX2KS4n0417F0GQ8h_E9skpVI"
                    apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={apiKey}"

                    response = await asyncio.to_thread(
                        requests.post,
                        apiUrl,
                        headers={'Content-Type': 'application/json'},
                        data=json.dumps(payload)
                    )

                    if response.status_code == 200:
                        result = response.json()
                        if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
                            llm_response_text = result["candidates"][0]["content"]["parts"][0]["text"]
                        else:
                            llm_response_text = "Sorry, I couldn't generate a food suggestion right now. Unexpected LLM response."
                            st.error(f"LLM response structure unexpected: {result}")
                    else:
                        llm_response_text = f"Error from AI: {response.status_code} - {response.text}"
                        st.error(f"Error calling LLM: {response.status_code} - {response.text}")

                    st.markdown(llm_response_text)
                    st.session_state.chatbot_messages.append({"role": "assistant", "content": llm_response_text})

                except Exception as e:
                    error_message = f"An error occurred: {e}. Please try again."
                    st.error(error_message)
                    st.session_state.chatbot_messages.append({"role": "assistant", "content": error_message})

# --- Main App Logic (orchestrates page display) ---

def main():
    st.set_page_config(page_title="Recipe Vault", page_icon="📖", layout="wide")

    # Initialize all necessary session_state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Geolocation related session state variables
    if "geolocation_status" not in st.session_state:
        st.session_state["geolocation_status"] = "initial" # Can be "initial", "request_pending", "detected", "error"
    if "geolocation_display" not in st.session_state:
        st.session_state["geolocation_display"] = "Click 'Refresh Location' to detect."
    if "geolocation_value" not in st.session_state: # Stores the actual value to save to CSV
        st.session_state["geolocation_value"] = "Not detected"
    if "geolocation_error_message" not in st.session_state:
        st.session_state["geolocation_error_message"] = ""


    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "submit_recipe"
    if "selected_recipe_data" not in st.session_state:
        st.session_state["selected_recipe_data"] = None
    if "selected_recipe_title_for_view" not in st.session_state:
        st.session_state["selected_recipe_title_for_view"] = ''
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []


    if st.session_state["logged_in"]:
        st.sidebar.write(f"👋 Hello, **{st.session_state['username']}**!")
        logout()

        st.sidebar.header("Navigation")
        page_options = ("Submit a Recipe", "View Recipes", "Food Chatbot")

        initial_sidebar_index = 0
        if st.session_state["current_page"] in ["view_all_recipes", "recipe_details"]:
            initial_sidebar_index = 1
        elif st.session_state["current_page"] == "food_chatbot":
            initial_sidebar_index = 2

        selected_sidebar_option = st.sidebar.radio(
            "Go to:",
            page_options,
            key="main_navigation",
            index=initial_sidebar_index
        )

        if selected_sidebar_option == "Submit a Recipe":
            if st.session_state["current_page"] != "submit_recipe":
                st.session_state["current_page"] = "submit_recipe"
                st.session_state["selected_recipe_data"] = None
                st.session_state["selected_recipe_title_for_view"] = ''
                st.rerun()
        elif selected_sidebar_option == "View Recipes":
            if st.session_state["current_page"] not in ["view_all_recipes", "recipe_details"]:
                st.session_state["current_page"] = "view_all_recipes"
                st.session_state["selected_recipe_data"] = None
                st.session_state["selected_recipe_title_for_view"] = ''
                st.rerun()
        elif selected_sidebar_option == "Food Chatbot":
            if st.session_state["current_page"] != "food_chatbot":
                st.session_state["current_page"] = "food_chatbot"
                st.session_state["selected_recipe_data"] = None
                st.session_state["selected_recipe_title_for_view"] = ''
                st.rerun()
        
        # Process geolocation result if a request was pending on the previous rerun
        # This needs to be outside the page-specific if-blocks but after session_state init
        process_geolocation_result()


        if st.session_state["current_page"] == "submit_recipe":
            recipe_submission(st.session_state["username"])
        elif st.session_state["current_page"] == "view_all_recipes":
            view_all_recipes()
        elif st.session_state["current_page"] == "recipe_details":
            if st.session_state["selected_recipe_data"]:
                display_recipe_details(pd.Series(st.session_state["selected_recipe_data"]))
            else:
                st.warning("No recipe selected for details. Redirecting to 'View Recipes'.")
                st.session_state["current_page"] = "view_all_recipes"
                st.session_state["selected_recipe_title_for_view"] = ''
                st.rerun()
        elif st.session_state["current_page"] == "food_chatbot":
            asyncio.run(food_chatbot_section())

    else:
        login()

if __name__ == "__main__":
    main()