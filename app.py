import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_js_eval import get_geolocation
import hashlib
import json
import asyncio
import requests

# --- Language Translations ---
# Define a dictionary for all UI text translations
# Add more languages and translations as needed.
# Keys should be consistent across languages.
translations = {
    "en": {
        "app_title": "Recipe Vault 📖",
        "welcome_message": "Welcome, {username}! 👋",
        "logout_button": "🚪 Logout",
        "sidebar_header_explore": "Explore the Vault 🚀",
        "nav_submit_recipe": "Submit a Recipe",
        "nav_view_recipes": "View Recipes",
        "nav_food_chatbot": "Food Chatbot",
        "nav_recipe_report": "Recipe Report",
        "login_title": "🔒 Recipe Vault Login",
        "login_prompt": "Please enter your credentials to access the app.",
        "username_label": "Username",
        "password_label": "Password",
        "login_button": "Login",
        "invalid_credentials_error": "Invalid username or password. Please try again.",
        "login_hint": "💡 Hint: Try 'admin' and 'password123' or 'user1' and 'mypassword'",
        "recipe_title_prefix": "🍽️ Recipe:",
        "category_label": "Category:",
        "submitted_by_label": "Submitted by:",
        "primary_corpus_type_label": "Primary Corpus Type:",
        "video_instructions_subheader": "🎥 Video Instructions",
        "video_file_not_found": "Video file not found: {filename}. Please check the 'uploads' folder.",
        "audio_instructions_subheader": "🎙️ Audio Instructions",
        "audio_file_not_found": "Audio file not found: {filename}. Please check the 'uploads' folder.",
        "recipe_image_subheader": "🖼️ Recipe Image",
        "image_file_not_found": "Image file not found: {filename}.",
        "description_subheader": "📝 Description",
        "ingredients_subheader": "📋 Ingredients",
        "preparation_steps_subheader": "👨‍🍳 Preparation Steps",
        "show_text_ingredients_steps": "Click to view Text Ingredients & Steps",
        "back_to_all_recipes_button": "⬅️ Back to All Recipes",
        "all_submitted_recipes_title": "📚 All Submitted Recipes",
        "all_submitted_recipes_prompt": "Browse through all the delicious recipes shared by our community!",
        "no_recipes_submitted_info": "No recipes have been submitted yet. Be the first to share one!",
        "view_specific_recipe_subheader": "🔍 View Specific Recipe Details",
        "no_titles_available_info": "No recipes with titles available to select for detailed viewing.",
        "select_recipe_to_view": "Select a recipe to view details:",
        "recipe_not_found_error": "Recipe with title '{title}' not found in the data. Please select an existing recipe from the dropdown.",
        "no_recipe_selected_warning": "No recipe selected for details. Redirecting to 'View Recipes'.",
        "submit_new_recipe_title": "📋 Submit a New Recipe",
        "submit_new_recipe_prompt": "Share your culinary creations with the community! Fill out the details below.",
        "your_details_subheader": "👤 Your Details",
        "full_name_label": "Full Name",
        "email_label": "Email",
        "geolocation_subheader": "📍 Geolocation (Auto-detected)",
        "your_coordinates_label": "Your approximate coordinates (Latitude, Longitude):",
        "current_geolocation_label": "Current Geolocation", # Hidden label for text_input
        "geolocation_initial_info": "Click 'Refresh Location' to detect your current coordinates.",
        "geolocation_request_pending_info": "Detecting location... Your browser may ask for permission. Please allow it.",
        "geolocation_error_warning": "Location not detected: {message}",
        "geolocation_permission_info": "Please ensure your browser allows location access for this site. Check pop-ups or browser settings (e.g., Privacy and security -> Site settings -> Location).",
        "refresh_location_button": "🔄 Refresh Location",
        "recipe_information_subheader": "📝 Recipe Information",
        "category_input_label": "Category (e.g., Dessert, Main Course, Snack)",
        "recipe_title_input_label": "Recipe Title",
        "description_input_label": "Short Description of Your Recipe",
        "choose_instructions_subheader": "🍲 Choose How to Provide Instructions",
        "select_method_radio": "Select your preferred method:",
        "text_based_option": "Text-based",
        "audio_based_option": "Audio-based",
        "video_based_option": "Video-based",
        "text_instructions_subheader": "✍️ Text Instructions",
        "ingredients_text_area_label": "Ingredients (separate by commas, e.g., '2 cups flour, 1 egg')",
        "preparation_steps_text_area_label": "Preparation Steps (detailed instructions)",
        "text_instructions_caption": "Provide clear text instructions for your recipe.",
        "audio_instructions_upload_label": "Upload an Audio File (.mp3, .wav)",
        "audio_instructions_caption": "Record your recipe instructions as audio. Max file size: 20MB.",
        "optional_text_ingredients_steps": "Optional: Add Text Ingredients & Steps for clarity",
        "video_instructions_upload_label": "Upload a Video File (.mp4, .mov, .avi)",
        "video_instructions_caption": "Upload a video demonstrating your recipe. Max file size: 50MB.",
        "recipe_image_optional_subheader": "🖼️ Recipe Image (Optional)",
        "image_upload_label": "Upload an Image File (.jpg, .png)",
        "image_upload_caption": "A good image makes your recipe more appealing!",
        "submit_recipe_button": "🚀 Submit Recipe",
        "fill_all_details_error": "🚫 Please fill in all required general recipe details (Full Name, Email, Category, Title, Description).",
        "text_instructions_required_error": "🚫 For 'Text-based' corpus, Ingredients and Preparation Steps are required.",
        "audio_file_required_error": "🚫 For 'Audio-based' corpus, an Audio file is required.",
        "video_file_required_error": "🚫 For 'Video-based' corpus, a Video file is required.",
        "save_media_error": "Failed to save media file(s): {error}. Please ensure '{upload_dir}' folder is writable.",
        "recipe_submitted_success": "✅ Recipe submitted successfully! Thank you for sharing.",
        "food_chatbot_title": "🤖 Food Mood Chatbot",
        "food_chatbot_prompt": "Tell me how you're feeling, and I'll suggest some food from your collected recipes!",
        "chatbot_initial_greeting": "Hello there! What kind of food are you in the mood for today? Tell me about your mood!",
        "chatbot_input_placeholder": "How are you feeling?",
        "chatbot_thinking_spinner": "Thinking...",
        "no_recipes_chatbot_info": "No recipes available in your collection yet. Please submit some!",
        "missing_recipe_cols_error": "Recipe data is missing 'Title' or 'Category' columns. Cannot suggest recipes.",
        "no_recipes_submitted_chatbot": "No recipes have been submitted yet. Please submit some recipes first.",
        "error_loading_recipes_chatbot": "Error loading recipes: {error}",
        "unexpected_llm_response": "Sorry, I couldn't generate a food suggestion right now. Unexpected LLM response.",
        "error_calling_llm": "Error from AI: {status_code} - {text}",
        "an_error_occurred": "An error occurred: {error}. Please try again.",
        "report_title": "📊 Recipe Vault Report",
        "report_prompt": "Here's an overview of your recipe collection.",
        "no_data_file_report": "No recipe data file found. Please submit some recipes first to generate a report.",
        "error_loading_report_data": "Error loading recipe data: {error}",
        "no_recipes_report_info": "No recipes have been submitted yet. The report will be available once you add some recipes!",
        "general_statistics_subheader": "General Statistics",
        "total_recipes_metric": "Total Recipes",
        "unique_users_metric": "Unique Users",
        "unique_categories_metric": "Unique Categories",
        "recipe_categories_subheader": "Recipe Categories",
        "no_categories_found": "No categories found.",
        "corpus_type_distribution_subheader": "Corpus Type Distribution",
        "no_corpus_types_recorded": "No corpus types recorded.",
        "geolocation_insights_subheader": "Geolocation Insights",
        "recipes_with_geolocation_metric": "Recipes with Geolocation",
        "recipes_without_geolocation_metric": "Recipes without Geolocation",
        "first_5_geolocation_recipes": "First 5 Recipes with Geolocation:",
        "no_geolocation_recipes_info": "No recipes with detected geolocation yet.",
        "recent_submissions_subheader": "Recent Submissions",
        "no_recent_submissions": "No recent submissions.",
        # Geolocation specific messages
        "unable_get_precise_coords": "Unable to get precise coordinates.",
        "coords_missing_error": "Coordinates data missing from browser response.",
        "geolocation_data_not_available": "Geolocation data not available.",
        "browser_no_coords_error": "Browser did not provide coordinate data.",
        "go_to_label": "Go to:",
        "ingredients_optional_label": "Ingredients (optional)",
        "preparation_steps_optional_label": "Preparation Steps (optional)",
        "not_detected_label": "Not detected", # New key for initial geolocation display
        "report_count_column": "Count", # New key for report table column
    },
    "hi": {
        "app_title": "रेसिपी वॉल्ट 📖",
        "welcome_message": "आपका स्वागत है, {username}! 👋",
        "logout_button": "🚪 लॉगआउट करें",
        "sidebar_header_explore": "वॉल्ट एक्सप्लोर करें 🚀",
        "nav_submit_recipe": "रेसिपी सबमिट करें",
        "nav_view_recipes": "रेसिपी देखें",
        "nav_food_chatbot": "फ़ूड चैटबॉट",
        "nav_recipe_report": "रेसिपी रिपोर्ट",
        "login_title": "🔒 रेसिपी वॉल्ट लॉगिन",
        "login_prompt": "ऐप तक पहुंचने के लिए कृपया अपनी क्रेडेंशियल दर्ज करें।",
        "username_label": "यूज़रनेम",
        "password_label": "पासवर्ड",
        "login_button": "लॉगिन करें",
        "invalid_credentials_error": "अमान्य यूज़रनेम या पासवर्ड। कृपया पुनः प्रयास करें।",
        "login_hint": "💡 संकेत: 'admin' और 'password123' या 'user1' और 'mypassword' आज़माएं।",
        "recipe_title_prefix": "🍽️ रेसिपी:",
        "category_label": "श्रेणी:",
        "submitted_by_label": "द्वारा सबमिट किया गया:",
        "primary_corpus_type_label": "प्राथमिक कॉर्पस प्रकार:",
        "video_instructions_subheader": "🎥 वीडियो निर्देश",
        "video_file_not_found": "वीडियो फ़ाइल नहीं मिली: {filename}। कृपया 'uploads' फ़ोल्डर जांचें।",
        "audio_instructions_subheader": "🎙️ ऑडियो निर्देश",
        "audio_file_not_found": "ऑडियो फ़ाइल नहीं मिली: {filename}। कृपया 'uploads' फ़ोल्डर जांचें।",
        "recipe_image_subheader": "🖼️ रेसिपी इमेज",
        "image_file_not_found": "इमेज फ़ाइल नहीं मिली: {filename}।",
        "description_subheader": "📝 विवरण",
        "ingredients_subheader": "📋 सामग्री",
        "preparation_steps_subheader": "👨‍🍳 तैयारी के चरण",
        "show_text_ingredients_steps": "सामग्री और चरणों को देखने के लिए क्लिक करें",
        "back_to_all_recipes_button": "⬅️ सभी रेसिपी पर वापस",
        "all_submitted_recipes_title": "📚 सभी सबमिट की गई रेसिपी",
        "all_submitted_recipes_prompt": "हमारे समुदाय द्वारा साझा की गई सभी स्वादिष्ट रेसिपी ब्राउज़ करें!",
        "no_recipes_submitted_info": "अभी तक कोई रेसिपी सबमिट नहीं की गई है। सबसे पहले एक साझा करें!",
        "view_specific_recipe_subheader": "🔍 विशिष्ट रेसिपी विवरण देखें",
        "no_titles_available_info": "विस्तृत देखने के लिए कोई शीर्षक वाली रेसिपी उपलब्ध नहीं है।",
        "select_recipe_to_view": "विवरण देखने के लिए एक रेसिपी चुनें:",
        "recipe_not_found_error": "शीर्षक '{title}' वाली रेसिपी डेटा में नहीं मिली। कृपया ड्रॉपडाउन से एक मौजूदा रेसिपी चुनें।",
        "no_recipe_selected_warning": "कोई रेसिपी विवरण के लिए नहीं चुनी गई। 'रेसिपी देखें' पर रीडायरेक्ट किया जा रहा है।",
        "submit_new_recipe_title": "📋 नई रेसिपी सबमिट करें",
        "submit_new_recipe_prompt": "अपनी पाक कला कृतियों को समुदाय के साथ साझा करें! नीचे विवरण भरें।",
        "your_details_subheader": "👤 आपके विवरण",
        "full_name_label": "पूरा नाम",
        "email_label": "ईमेल",
        "geolocation_subheader": "📍 भू-स्थान (स्वचालित रूप से पता चला)",
        "your_coordinates_label": "आपके अनुमानित निर्देशांक (अक्षांश, देशांतर):",
        "current_geolocation_label": "वर्तमान भू-स्थान",
        "geolocation_initial_info": "अपने वर्तमान निर्देशांक का पता लगाने के लिए 'स्थान ताज़ा करें' पर क्लिक करें।",
        "geolocation_request_pending_info": "स्थान का पता लगाया जा रहा है... आपका ब्राउज़र स्थान अनुमति मांग सकता है। कृपया अनुमति दें।",
        "geolocation_error_warning": "स्थान का पता नहीं चला: {message}",
        "geolocation_permission_info": "कृपया सुनिश्चित करें कि आपका ब्राउज़र इस साइट के लिए स्थान पहुंच की अनुमति देता है। पॉप-अप या ब्राउज़र सेटिंग्स (जैसे, गोपनीयता और सुरक्षा -> साइट सेटिंग्स -> स्थान) जांचें।",
        "refresh_location_button": "🔄 स्थान ताज़ा करें",
        "recipe_information_subheader": "📝 रेसिपी जानकारी",
        "category_input_label": "श्रेणी (जैसे, डेज़र्ट, मुख्य व्यंजन, स्नैक)",
        "recipe_title_input_label": "रेसिपी शीर्षक",
        "description_input_label": "अपनी रेसिपी का संक्षिप्त विवरण",
        "choose_instructions_subheader": "🍲 निर्देश प्रदान करने का तरीका चुनें",
        "select_method_radio": "अपनी पसंदीदा विधि चुनें:",
        "text_based_option": "पाठ-आधारित",
        "audio_based_option": "ऑडियो-आधारित",
        "video_based_option": "वीडियो-आधारित",
        "text_instructions_subheader": "✍️ पाठ निर्देश",
        "ingredients_text_area_label": "सामग्री (कॉमा से अलग करें, जैसे, '2 कप आटा, 1 अंडा')",
        "preparation_steps_text_area_label": "तैयारी के चरण (विस्तृत निर्देश)",
        "text_instructions_caption": "अपनी रेसिपी के लिए स्पष्ट पाठ निर्देश प्रदान करें।",
        "audio_instructions_upload_label": "एक ऑडियो फ़ाइल अपलोड करें (.mp3, .wav)",
        "audio_instructions_caption": "अपनी रेसिपी के निर्देश ऑडियो के रूप में रिकॉर्ड करें। अधिकतम फ़ाइल आकार: 20MB।",
        "optional_text_ingredients_steps": "वैकल्पिक: स्पष्टता के लिए पाठ सामग्री और चरण जोड़ें",
        "video_instructions_upload_label": "एक वीडियो फ़ाइल अपलोड करें (.mp4, .mov, .avi)",
        "video_instructions_caption": "अपनी रेसिपी का प्रदर्शन करने वाला एक वीडियो अपलोड करें। अधिकतम फ़ाइल आकार: 50MB।",
        "recipe_image_optional_subheader": "🖼️ रेसिपी इमेज (वैकल्पिक)",
        "image_upload_label": "एक इमेज फ़ाइल अपलोड करें (.jpg, .png)",
        "image_upload_caption": "एक अच्छी इमेज आपकी रेसिपी को और अधिक आकर्षक बनाती है!",
        "submit_recipe_button": "🚀 रेसिपी सबमिट करें",
        "fill_all_details_error": "🚫 कृपया सभी आवश्यक सामान्य रेसिपी विवरण (पूरा नाम, ईमेल, श्रेणी, शीर्षक, विवरण) भरें।",
        "text_instructions_required_error": "🚫 'पाठ-आधारित' कॉर्पस के लिए, सामग्री और तैयारी के चरण आवश्यक हैं।",
        "audio_file_required_error": "🚫 'ऑडियो-आधारित' कॉर्पस के लिए, एक ऑडियो फ़ाइल आवश्यक है।",
        "video_file_required_error": "🚫 'वीडियो-आधारित' कॉर्पस के लिए, एक वीडियो फ़ाइल आवश्यक है।",
        "save_media_error": "मीडिया फ़ाइल(फ़ाइलें) सहेजने में विफल: {error}। कृपया सुनिश्चित करें कि '{upload_dir}' फ़ोल्डर लिखने योग्य है।",
        "recipe_submitted_success": "✅ रेसिपी सफलतापूर्वक सबमिट की गई! साझा करने के लिए धन्यवाद।",
        "food_chatbot_title": "🤖 फ़ूड मूड चैटबॉट",
        "food_chatbot_prompt": "मुझे बताएं कि आप कैसा महसूस कर रहे हैं, और मैं आपके संग्रह से कुछ रेसिपी सुझाऊंगा!",
        "chatbot_initial_greeting": "नमस्ते! आज आप किस तरह के भोजन के मूड में हैं? मुझे अपने मूड के बारे में बताएं!",
        "chatbot_input_placeholder": "आप कैसा महसूस कर रहे हैं?",
        "chatbot_thinking_spinner": "सोच रहा हूँ...",
        "no_recipes_chatbot_info": "आपके संग्रह में अभी कोई रेसिपी उपलब्ध नहीं है। कृपया कुछ सबमिट करें!",
        "missing_recipe_cols_error": "रेसिपी डेटा में 'शीर्षक' या 'श्रेणी' कॉलम गायब हैं। रेसिपी नहीं सुझा सकते।",
        "no_recipes_submitted_chatbot": "अभी तक कोई रेसिपी सबमिट नहीं की गई है। कृपया पहले कुछ रेसिपी सबमिट करें।",
        "error_loading_recipes_chatbot": "रेसिपी लोड करने में त्रुटि: {error}",
        "unexpected_llm_response": "क्षमा करें, मैं अभी भोजन का सुझाव नहीं दे सका। अप्रत्याशित एलएलएम प्रतिक्रिया।",
        "error_calling_llm": "एआई से त्रुटि: {status_code} - {text}",
        "an_error_occurred": "एक त्रुटि हुई: {error}। कृपया पुनः प्रयास करें।",
        "report_title": "📊 रेसिपी वॉल्ट रिपोर्ट",
        "report_prompt": "यहां आपके रेसिपी संग्रह का एक अवलोकन है।",
        "no_data_file_report": "कोई रेसिपी डेटा फ़ाइल नहीं मिली। रिपोर्ट बनाने के लिए कृपया पहले कुछ रेसिपी सबमिट करें।",
        "error_loading_report_data": "रेसिपी डेटा लोड करने में त्रुटि: {error}",
        "no_recipes_report_info": "अभी तक कोई रेसिपी सबमिट नहीं की गई है। रिपोर्ट तब उपलब्ध होगी जब आप कुछ रेसिपी जोड़ेंगे!",
        "general_statistics_subheader": "सामान्य आँकड़े",
        "total_recipes_metric": "कुल रेसिपी",
        "unique_users_metric": "अद्वितीय उपयोगकर्ता",
        "unique_categories_metric": "अद्वितीय श्रेणियाँ",
        "recipe_categories_subheader": "रेसिपी श्रेणियाँ",
        "no_categories_found": "कोई श्रेणी नहीं मिली।",
        "corpus_type_distribution_subheader": "कॉर्पस प्रकार वितरण",
        "no_corpus_types_recorded": "कोई कॉर्पस प्रकार दर्ज नहीं किया गया।",
        "geolocation_insights_subheader": "भू-स्थान अंतर्दृष्टि",
        "recipes_with_geolocation_metric": "भू-स्थान वाली रेसिपी",
        "recipes_without_geolocation_metric": "भू-स्थान के बिना रेसिपी",
        "first_5_geolocation_recipes": "भू-स्थान वाली पहली 5 रेसिपी:",
        "no_geolocation_recipes_info": "अभी तक कोई भू-स्थान वाली रेसिपी नहीं मिली है।",
        "recent_submissions_subheader": "हाल की सबमिशन",
        "no_recent_submissions": "कोई हाल की सबमिशन नहीं।",
        # Geolocation specific messages
        "unable_get_precise_coords": "सटीक निर्देशांक प्राप्त करने में असमर्थ।",
        "coords_missing_error": "ब्राउज़र प्रतिक्रिया से निर्देशांक डेटा गायब है।",
        "geolocation_data_not_available": "भू-स्थान डेटा उपलब्ध नहीं है।",
        "browser_no_coords_error": "ब्राउज़र ने निर्देशांक डेटा प्रदान नहीं किया।",
        "go_to_label": "यहां जाएं:",
        "ingredients_optional_label": "सामग्री (वैकल्पिक)",
        "preparation_steps_optional_label": "तैयारी के चरण (वैकल्पिक)",
        "not_detected_label": "पता नहीं चला",
        "report_count_column": "गणना",
    },
    "ta": { # Tamil Translations
        "app_title": "சமையல் குறிப்பு பெட்டகம் 📖",
        "welcome_message": "வரவேற்பு, {username}! 👋",
        "logout_button": "🚪 வெளியேறு",
        "sidebar_header_explore": "பெட்டகத்தை ஆராயுங்கள் 🚀",
        "nav_submit_recipe": "சமையல் குறிப்பை சமர்ப்பி",
        "nav_view_recipes": "சமையல் குறிப்புகளைப் பார்",
        "nav_food_chatbot": "உணவு சாட்போட்",
        "nav_recipe_report": "சமையல் குறிப்பு அறிக்கை",
        "login_title": "🔒 சமையல் குறிப்பு பெட்டக உள்நுழைவு",
        "login_prompt": "பயன்பாட்டை அணுக உங்கள் சான்றுகளை உள்ளிடவும்.",
        "username_label": "பயனர்பெயர்",
        "password_label": "கடவுச்சொல்",
        "login_button": "உள்நுழை",
        "invalid_credentials_error": "தவறான பயனர்பெயர் அல்லது கடவுச்சொல். மீண்டும் முயற்சிக்கவும்.",
        "login_hint": "💡 குறிப்பு: 'admin' மற்றும் 'password123' அல்லது 'user1' மற்றும் 'mypassword' முயற்சிக்கவும்.",
        "recipe_title_prefix": "🍽️ சமையல் குறிப்பு:",
        "category_label": "வகை:",
        "submitted_by_label": "சமர்ப்பித்தவர்:",
        "primary_corpus_type_label": "முதன்மை கார்பஸ் வகை:",
        "video_instructions_subheader": "🎥 வீடியோ வழிமுறைகள்",
        "video_file_not_found": "வீடியோ கோப்பு காணப்படவில்லை: {filename}. 'uploads' கோப்புறையைச் சரிபார்க்கவும்.",
        "audio_instructions_subheader": "🎙️ ஆடியோ வழிமுறைகள்",
        "audio_file_not_found": "ஆடியோ கோப்பு காணப்படவில்லை: {filename}. 'uploads' கோப்புறையைச் சரிபார்க்கவும்.",
        "recipe_image_subheader": "🖼️ சமையல் குறிப்பு படம்",
        "image_file_not_found": "படம் கோப்பு காணப்படவில்லை: {filename}.",
        "description_subheader": "📝 விளக்கம்",
        "ingredients_subheader": "📋 பொருட்கள்",
        "preparation_steps_subheader": "👨‍🍳 தயாரிப்பு படிகள்",
        "show_text_ingredients_steps": "உரை பொருட்கள் மற்றும் படிகளைக் காண கிளிக் செய்யவும்",
        "back_to_all_recipes_button": "⬅️ அனைத்து சமையல் குறிப்புகளுக்கும் திரும்பு",
        "all_submitted_recipes_title": "📚 சமர்ப்பிக்கப்பட்ட அனைத்து சமையல் குறிப்புகளும்",
        "all_submitted_recipes_prompt": "எங்கள் சமூகத்தால் பகிரப்பட்ட அனைத்து சுவையான சமையல் குறிப்புகளையும் உலாவவும்!",
        "no_recipes_submitted_info": "இதுவரை சமையல் குறிப்புகள் எதுவும் சமர்ப்பிக்கப்படவில்லை. முதலில் ஒன்றை பகிரவும்!",
        "view_specific_recipe_subheader": "🔍 குறிப்பிட்ட சமையல் குறிப்பு விவரங்களைப் பார்",
        "no_titles_available_info": "விரிவான பார்வைக்கு தலைப்புகளுடன் கூடிய சமையல் குறிப்புகள் எதுவும் இல்லை.",
        "select_recipe_to_view": "விவரங்களைப் பார்க்க ஒரு சமையல் குறிப்பைத் தேர்ந்தெடுக்கவும்:",
        "recipe_not_found_error": "தலைப்பு '{title}' கொண்ட சமையல் குறிப்பு தரவுகளில் காணப்படவில்லை. கீழ்தோன்றும் பட்டியலில் இருந்து ஏற்கனவே உள்ள சமையல் குறிப்பைத் தேர்ந்தெடுக்கவும்.",
        "no_recipe_selected_warning": "விவரங்களுக்கு சமையல் குறிப்பு எதுவும் தேர்ந்தெடுக்கப்படவில்லை. 'சமையல் குறிப்புகளைப் பார்' என்பதற்குத் திருப்பி விடப்படுகிறது.",
        "submit_new_recipe_title": "📋 புதிய சமையல் குறிப்பை சமர்ப்பி",
        "submit_new_recipe_prompt": "உங்கள் சமையல் படைப்புகளை சமூகத்துடன் பகிர்ந்து கொள்ளுங்கள்! கீழே உள்ள விவரங்களை நிரப்பவும்.",
        "your_details_subheader": "👤 உங்கள் விவரங்கள்",
        "full_name_label": "முழு பெயர்",
        "email_label": "மின்னஞ்சல்",
        "geolocation_subheader": "📍 புவிஇருப்பிடம் (தானாக கண்டறியப்பட்டது)",
        "your_coordinates_label": "உங்கள் தோராயமான ஆயத்தொலைவுகள் (அட்சரேகை, தீர்க்கரேகை):",
        "current_geolocation_label": "தற்போதைய புவிஇருப்பிடம்",
        "geolocation_initial_info": "உங்கள் தற்போதைய ஆயத்தொலைவுகளைக் கண்டறிய 'இருப்பிடத்தைப் புதுப்பி' என்பதைக் கிளிக் செய்யவும்.",
        "geolocation_request_pending_info": "இருப்பிடம் கண்டறியப்படுகிறது... உங்கள் உலாவி இருப்பிட அணுகலுக்கு அனுமதி கேட்கலாம். தயவுசெய்து அனுமதிக்கவும்.",
        "geolocation_error_warning": "இருப்பிடம் கண்டறியப்படவில்லை: {message}",
        "geolocation_permission_info": "இந்த தளத்திற்கு உங்கள் உலாவி இருப்பிட அணுகலை அனுமதிக்கிறதா என்பதை உறுதிப்படுத்தவும். பாப்-அப்கள் அல்லது உலாவி அமைப்புகளை (எ.கா., தனியுரிமை மற்றும் பாதுகாப்பு -> தள அமைப்புகள் -> இருப்பிடம்) சரிபார்க்கவும்.",
        "refresh_location_button": "🔄 இருப்பிடத்தைப் புதுப்பி",
        "recipe_information_subheader": "📝 சமையல் குறிப்பு தகவல்",
        "category_input_label": "வகை (எ.கா., இனிப்பு, முக்கிய உணவு, சிற்றுண்டி)",
        "recipe_title_input_label": "சமையல் குறிப்பு தலைப்பு",
        "description_input_label": "உங்கள் சமையல் குறிப்பின் சுருக்கமான விளக்கம்",
        "choose_instructions_subheader": "🍲 வழிமுறைகளை எவ்வாறு வழங்குவது என்பதைத் தேர்வுசெய்க",
        "select_method_radio": "உங்களுக்கு விருப்பமான முறையைத் தேர்ந்தெடுக்கவும்:",
        "text_based_option": "உரை அடிப்படையிலான",
        "audio_based_option": "ஆடியோ அடிப்படையிலான",
        "video_based_option": "வீடியோ அடிப்படையிலான",
        "text_instructions_subheader": "✍️ உரை வழிமுறைகள்",
        "ingredients_text_area_label": "பொருட்கள் (காமாவால் பிரிக்கவும், எ.கா., '2 கப் மாவு, 1 முட்டை')",
        "preparation_steps_text_area_label": "தயாரிப்பு படிகள் (விரிவான வழிமுறைகள்)",
        "text_instructions_caption": "உங்கள் சமையல் குறிப்பிற்கு தெளிவான உரை வழிமுறைகளை வழங்கவும்.",
        "audio_instructions_upload_label": "ஒரு ஆடியோ கோப்பை பதிவேற்றவும் (.mp3, .wav)",
        "audio_instructions_caption": "உங்கள் சமையல் குறிப்பு வழிமுறைகளை ஆடியோவாக பதிவு செய்யவும். அதிகபட்ச கோப்பு அளவு: 20MB.",
        "optional_text_ingredients_steps": "விருப்பத்தேர்வு: தெளிவுக்காக உரை பொருட்கள் மற்றும் படிகளைச் சேர்க்கவும்",
        "video_instructions_upload_label": "ஒரு வீடியோ கோப்பை பதிவேற்றவும் (.mp4, .mov, .avi)",
        "video_instructions_caption": "உங்கள் சமையல் குறிப்பை விளக்கும் ஒரு வீடியோவைப் பதிவேற்றவும். அதிகபட்ச கோப்பு அளவு: 50MB.",
        "recipe_image_optional_subheader": "🖼️ சமையல் குறிப்பு படம் (விருப்பத்தேர்வு)",
        "image_upload_label": "ஒரு படக் கோப்பை பதிவேற்றவும் (.jpg, .png)",
        "image_upload_caption": "ஒரு நல்ல படம் உங்கள் சமையல் குறிப்பை மேலும் கவர்ச்சிகரமானதாக ஆக்குகிறது!",
        "submit_recipe_button": "🚀 சமையல் குறிப்பை சமர்ப்பி",
        "fill_all_details_error": "🚫 தேவையான அனைத்து பொதுவான சமையல் குறிப்பு விவரங்களையும் (முழு பெயர், மின்னஞ்சல், வகை, தலைப்பு, விளக்கம்) நிரப்பவும்.",
        "text_instructions_required_error": "🚫 'உரை அடிப்படையிலான' கார்பஸ்க்கு, பொருட்கள் மற்றும் தயாரிப்பு படிகள் தேவை.",
        "audio_file_required_error": "🚫 'ஆடியோ அடிப்படையிலான' கார்பஸ்க்கு, ஒரு ஆடியோ கோப்பு தேவை.",
        "video_file_required_error": "🚫 'வீடியோ அடிப்படையிலான' கார்பஸ்க்கு, ஒரு வீடியோ கோப்பு தேவை.",
        "save_media_error": "மீடியா கோப்பு(களை) சேமிக்க முடியவில்லை: {error}. '{upload_dir}' கோப்புறை எழுதக்கூடியதா என்பதை உறுதிப்படுத்தவும்.",
        "recipe_submitted_success": "✅ சமையல் குறிப்பு வெற்றிகரமாக சமர்ப்பிக்கப்பட்டது! பகிர்ந்தமைக்கு நன்றி.",
        "food_chatbot_title": "🤖 உணவு சாட்போட்",
        "food_chatbot_prompt": "நீங்கள் எப்படி உணர்கிறீர்கள் என்று சொல்லுங்கள், உங்கள் சேகரிப்பில் இருந்து சில சமையல் குறிப்புகளை நான் பரிந்துரைப்பேன்!",
        "chatbot_initial_greeting": "வணக்கம்! இன்று நீங்கள் எந்த வகையான உணவை விரும்புகிறீர்கள்? உங்கள் மனநிலையைப் பற்றி சொல்லுங்கள்!",
        "chatbot_input_placeholder": "நீங்கள் எப்படி உணர்கிறீர்கள்?",
        "chatbot_thinking_spinner": "யோசிக்கிறது...",
        "no_recipes_chatbot_info": "உங்கள் சேகரிப்பில் இதுவரை சமையல் குறிப்புகள் எதுவும் இல்லை. தயவுசெய்து சிலவற்றை சமர்ப்பிக்கவும்!",
        "missing_recipe_cols_error": "சமையல் குறிப்பு தரவுகளில் 'தலைப்பு' அல்லது 'வகை' நெடுவரிசைகள் இல்லை. சமையல் குறிப்புகளை பரிந்துரைக்க முடியாது.",
        "no_recipes_submitted_chatbot": "இதுவரை சமையல் குறிப்புகள் எதுவும் சமர்ப்பிக்கப்படவில்லை. தயவுசெய்து முதலில் சில சமையல் குறிப்புகளை சமர்ப்பிக்கவும்.",
        "error_loading_recipes_chatbot": "சமையல் குறிப்புகளை ஏற்றும்போது பிழை: {error}",
        "unexpected_llm_response": "மன்னிக்கவும், நான் இப்போது ஒரு உணவு பரிந்துரையை உருவாக்க முடியவில்லை. எதிர்பாராத LLM பதில்.",
        "error_calling_llm": "AI இலிருந்து பிழை: {status_code} - {text}",
        "an_error_occurred": "ஒரு பிழை ஏற்பட்டது: {error}. மீண்டும் முயற்சிக்கவும்.",
        "report_title": "📊 சமையல் குறிப்பு பெட்டக அறிக்கை",
        "report_prompt": "உங்கள் சமையல் குறிப்பு தொகுப்பின் மேலோட்டம் இங்கே.",
        "no_data_file_report": "சமையல் குறிப்பு தரவு கோப்பு காணப்படவில்லை. அறிக்கை உருவாக்க முதலில் சில சமையல் குறிப்புகளை சமர்ப்பிக்கவும்.",
        "error_loading_report_data": "சமையல் குறிப்பு தரவை ஏற்றும்போது பிழை: {error}",
        "no_recipes_report_info": "இதுவரை சமையல் குறிப்புகள் எதுவும் சமர்ப்பிக்கப்படவில்லை. நீங்கள் சில சமையல் குறிப்புகளைச் சேர்த்தவுடன் அறிக்கை கிடைக்கும்!",
        "general_statistics_subheader": "பொது புள்ளிவிவரங்கள்",
        "total_recipes_metric": "மொத்த சமையல் குறிப்புகள்",
        "unique_users_metric": "தனிப்பட்ட பயனர்கள்",
        "unique_categories_metric": "தனிப்பட்ட வகைகள்",
        "recipe_categories_subheader": "சமையல் குறிப்பு வகைகள்",
        "no_categories_found": "வகைகள் எதுவும் இல்லை.",
        "corpus_type_distribution_subheader": "கார்பஸ் வகை விநியோகம்",
        "no_corpus_types_recorded": "கார்பஸ் வகைகள் எதுவும் பதிவு செய்யப்படவில்லை.",
        "geolocation_insights_subheader": "புவிஇருப்பிட நுண்ணறிவு",
        "recipes_with_geolocation_metric": "புவிஇருப்பிடத்துடன் கூடிய சமையல் குறிப்புகள்",
        "recipes_without_geolocation_metric": "புவிஇருப்பிடம் இல்லாத சமையல் குறிப்புகள்",
        "first_5_geolocation_recipes": "புவிஇருப்பிடத்துடன் கூடிய முதல் 5 சமையல் குறிப்புகள்:",
        "no_geolocation_recipes_info": "இதுவரை கண்டறியப்பட்ட புவிஇருப்பிடத்துடன் கூடிய சமையல் குறிப்புகள் எதுவும் இல்லை.",
        "recent_submissions_subheader": "சமீபத்திய சமர்ப்பிப்புகள்",
        "no_recent_submissions": "சமீபத்திய சமர்ப்பிப்புகள் எதுவும் இல்லை.",
        "unable_get_precise_coords": "சரியான ஆயத்தொலைவுகளைப் பெற முடியவில்லை.",
        "coords_missing_error": "உலாவி பதிலில் ஆயத்தொலைவு தரவு இல்லை.",
        "geolocation_data_not_available": "புவிஇருப்பிட தரவு கிடைக்கவில்லை.",
        "browser_no_coords_error": "உலாவி ஆயத்தொலைவு தரவை வழங்கவில்லை.",
        "go_to_label": "இங்கு செல்லவும்:",
        "ingredients_optional_label": "பொருட்கள் (விருப்பத்தேர்வு)",
        "preparation_steps_optional_label": "தயாரிப்பு படிகள் (விருப்பத்தேர்வு)",
        "not_detected_label": "கண்டறியப்படவில்லை",
        "report_count_column": "எண்ணிக்கை",
    },
    "te": { # Telugu Translations
        "app_title": "వంటకాల నిధి 📖",
        "welcome_message": "స్వాగతం, {username}! 👋",
        "logout_button": "🚪 లాగ్ అవుట్",
        "sidebar_header_explore": "నిధిని అన్వేషించండి 🚀",
        "nav_submit_recipe": "వంటకాన్ని సమర్పించండి",
        "nav_view_recipes": "వంటకాలను చూడండి",
        "nav_food_chatbot": "ఫుడ్ చాట్‌బాట్",
        "nav_recipe_report": "వంటకాల నివేదిక",
        "login_title": "🔒 వంటకాల నిధి లాగిన్",
        "login_prompt": "యాప్‌ను యాక్సెస్ చేయడానికి దయచేసి మీ ఆధారాలను నమోదు చేయండి.",
        "username_label": "యూజర్‌నేమ్",
        "password_label": "పాస్‌వర్డ్",
        "login_button": "లాగిన్",
        "invalid_credentials_error": "చెల్లని యూజర్‌నేమ్ లేదా పాస్‌వర్డ్. దయచేసి మళ్లీ ప్రయత్నించండి.",
        "login_hint": "💡 సూచన: 'admin' మరియు 'password123' లేదా 'user1' మరియు 'mypassword' ప్రయత్నించండి.",
        "recipe_title_prefix": "🍽️ వంటకం:",
        "category_label": "వర్గం:",
        "submitted_by_label": "సమర్పించినవారు:",
        "primary_corpus_type_label": "ప్రాథమిక కార్పస్ రకం:",
        "video_instructions_subheader": "🎥 వీడియో సూచనలు",
        "video_file_not_found": "వీడియో ఫైల్ కనుగొనబడలేదు: {filename}. దయచేసి 'uploads' ఫోల్డర్‌ను తనిఖీ చేయండి.",
        "audio_instructions_subheader": "🎙️ ఆడియో సూచనలు",
        "audio_file_not_found": "ఆడియో ఫైల్ కనుగొనబడలేదు: {filename}. దయచేసి 'uploads' ఫోల్డర్‌ను తనిఖీ చేయండి.",
        "recipe_image_subheader": "🖼️ వంటకం చిత్రం",
        "image_file_not_found": "చిత్ర ఫైల్ కనుగొనబడలేదు: {filename}.",
        "description_subheader": "📝 వివరణ",
        "ingredients_subheader": "📋 పదార్థాలు",
        "preparation_steps_subheader": "👨‍🍳 తయారీ దశలు",
        "show_text_ingredients_steps": "వచన పదార్థాలు మరియు దశలను చూడటానికి క్లిక్ చేయండి",
        "back_to_all_recipes_button": "⬅️ అన్ని వంటకాలకు తిరిగి వెళ్ళు",
        "all_submitted_recipes_title": "📚 సమర్పించిన అన్ని వంటకాలు",
        "all_submitted_recipes_prompt": "మా సంఘం పంచుకున్న అన్ని రుచికరమైన వంటకాలను బ్రౌజ్ చేయండి!",
        "no_recipes_submitted_info": "ఇప్పటివరకు వంటకాలు ఏవీ సమర్పించబడలేదు. మొదట ఒకదాన్ని పంచుకోండి!",
        "view_specific_recipe_subheader": "🔍 నిర్దిష్ట వంటకం వివరాలను చూడండి",
        "no_titles_available_info": "వివరణాత్మక వీక్షణ కోసం శీర్షికలతో వంటకాలు ఏవీ అందుబాటులో లేవు.",
        "select_recipe_to_view": "వివరాలను చూడటానికి ఒక వంటకాన్ని ఎంచుకోండి:",
        "recipe_not_found_error": "శీర్షిక '{title}'తో వంటకం డేటాలో కనుగొనబడలేదు. దయచేసి డ్రాప్‌డౌన్ నుండి ఇప్పటికే ఉన్న వంటకాన్ని ఎంచుకోండి.",
        "no_recipe_selected_warning": "వివరాల కోసం వంటకం ఏదీ ఎంపిక చేయబడలేదు. 'వంటకాలను చూడండి'కి దారి మళ్లించబడుతోంది.",
        "submit_new_recipe_title": "📋 కొత్త వంటకాన్ని సమర్పించండి",
        "submit_new_recipe_prompt": "మీ పాక సృష్టిని సంఘంతో పంచుకోండి! దిగువ వివరాలను పూరించండి.",
        "your_details_subheader": "👤 మీ వివరాలు",
        "full_name_label": "పూర్తి పేరు",
        "email_label": "ఇమెయిల్",
        "geolocation_subheader": "📍 జియోలొకేషన్ (ఆటో-డిటెక్ట్ చేయబడింది)",
        "your_coordinates_label": "మీ సుమారు కోఆర్డినేట్‌లు (అక్షాంశం, రేఖాంశం):",
        "current_geolocation_label": "ప్రస్తుత జియోలొకేషన్",
        "geolocation_initial_info": "మీ ప్రస్తుత కోఆర్డినేట్‌లను గుర్తించడానికి 'స్థానాన్ని రిఫ్రెష్ చేయి' క్లిక్ చేయండి.",
        "geolocation_request_pending_info": "స్థానం గుర్తించబడుతోంది... మీ బ్రౌజర్ స్థాన అనుమతిని అడగవచ్చు. దయచేసి అనుమతించండి.",
        "geolocation_error_warning": "స్థానం గుర్తించబడలేదు: {message}",
        "geolocation_permission_info": "దయచేసి మీ బ్రౌజర్ ఈ సైట్ కోసం స్థాన యాక్సెస్‌ను అనుమతిస్తుందని నిర్ధారించుకోండి. పాప్-అప్‌లు లేదా బ్రౌజర్ సెట్టింగ్‌లను (ఉదా., గోప్యత మరియు భద్రత -> సైట్ సెట్టింగ్‌లు -> స్థానం) తనిఖీ చేయండి.",
        "refresh_location_button": "🔄 స్థానాన్ని రిఫ్రెష్ చేయి",
        "recipe_information_subheader": "📝 వంటకం సమాచారం",
        "category_input_label": "వర్గం (ఉదా., డెజర్ట్, మెయిన్ కోర్స్, స్నాక్)",
        "recipe_title_input_label": "వంటకం శీర్షిక",
        "description_input_label": "మీ వంటకం యొక్క సంక్షిప్త వివరణ",
        "choose_instructions_subheader": "🍲 సూచనలను ఎలా అందించాలో ఎంచుకోండి",
        "select_method_radio": "మీకు నచ్చిన పద్ధతిని ఎంచుకోండి:",
        "text_based_option": "వచన ఆధారిత",
        "audio_based_option": "ఆడియో ఆధారిత",
        "video_based_option": "వీడియో ఆధారిత",
        "text_instructions_subheader": "✍️ వచన సూచనలు",
        "ingredients_text_area_label": "పదార్థాలు (కామాలతో వేరు చేయండి, ఉదా., '2 కప్పుల పిండి, 1 గుడ్డు')",
        "preparation_steps_text_area_label": "తయారీ దశలు (వివరణాత్మక సూచనలు)",
        "text_instructions_caption": "మీ వంటకం కోసం స్పష్టమైన వచన సూచనలను అందించండి.",
        "audio_instructions_upload_label": "ఒక ఆడియో ఫైల్‌ను అప్‌లోడ్ చేయండి (.mp3, .wav)",
        "audio_instructions_caption": "మీ వంటకం సూచనలను ఆడియోగా రికార్డ్ చేయండి. గరిష్ట ఫైల్ పరిమాణం: 20MB.",
        "optional_text_ingredients_steps": "ఐచ్ఛికం: స్పష్టత కోసం వచన పదార్థాలు మరియు దశలను జోడించండి",
        "video_instructions_upload_label": "ఒక వీడియో ఫైల్‌ను అప్‌లోడ్ చేయండి (.mp4, .mov, .avi)",
        "video_instructions_caption": "మీ వంటకాన్ని ప్రదర్శించే వీడియోను అప్‌లోడ్ చేయండి. గరిష్ట ఫైల్ పరిమాణం: 50MB.",
        "recipe_image_optional_subheader": "🖼️ వంటకం చిత్రం (ఐచ్ఛికం)",
        "image_upload_label": "ఒక చిత్ర ఫైల్‌ను అప్‌లోడ్ చేయండి (.jpg, .png)",
        "image_upload_caption": "మంచి చిత్రం మీ వంటకాన్ని మరింత ఆకర్షణీయంగా చేస్తుంది!",
        "submit_recipe_button": "🚀 వంటకాన్ని సమర్పించండి",
        "fill_all_details_error": "🚫 దయచేసి అన్ని అవసరమైన సాధారణ వంటకం వివరాలను (పూర్తి పేరు, ఇమెయిల్, వర్గం, శీర్షిక, వివరణ) పూరించండి.",
        "text_instructions_required_error": "🚫 'వచన ఆధారిత' కార్పస్ కోసం, పదార్థాలు మరియు తయారీ దశలు అవసరం.",
        "audio_file_required_error": "🚫 'ఆడియో ఆధారిత' కార్పస్ కోసం, ఒక ఆడియో ఫైల్ అవసరం.",
        "video_file_required_error": "🚫 'వీడియో ఆధారిత' కార్పస్ కోసం, ఒక వీడియో ఫైల్ అవసరం.",
        "save_media_error": "మీడియా ఫైల్(లు) సేవ్ చేయడంలో విఫలమైంది: {error}. దయచేసి '{upload_dir}' ఫోల్డర్ వ్రాయదగినదని నిర్ధారించుకోండి.",
        "recipe_submitted_success": "✅ వంటకం విజయవంతంగా సమర్పించబడింది! పంచుకున్నందుకు ధన్యవాదాలు.",
        "food_chatbot_title": "🤖 ఫుడ్ చాట్‌బాట్",
        "food_chatbot_prompt": "మీరు ఎలా ఫీల్ అవుతున్నారో చెప్పండి, నేను మీ సేకరించిన వంటకాల నుండి కొన్నింటిని సూచిస్తాను!",
        "chatbot_initial_greeting": "నమస్తే! ఈరోజు మీరు ఎలాంటి ఆహారం కోసం మూడ్‌లో ఉన్నారు? మీ మూడ్ గురించి చెప్పండి!",
        "chatbot_input_placeholder": "మీరు ఎలా ఫీల్ అవుతున్నారు?",
        "chatbot_thinking_spinner": "ఆలోచిస్తోంది...",
        "no_recipes_chatbot_info": "మీ సేకరణలో ఇంకా వంటకాలు ఏవీ అందుబాటులో లేవు. దయచేసి కొన్నింటిని సమర్పించండి!",
        "missing_recipe_cols_error": "వంటకం డేటాలో 'శీర్షిక' లేదా 'వర్గం' కాలమ్‌లు లేవు. వంటకాలను సూచించలేము.",
        "no_recipes_submitted_chatbot": "ఇప్పటివరకు వంటకాలు ఏవీ సమర్పించబడలేదు. దయచేసి మొదట కొన్ని వంటకాలను సమర్పించండి.",
        "error_loading_recipes_chatbot": "వంటకాలను లోడ్ చేయడంలో లోపం: {error}",
        "unexpected_llm_response": "క్షమించండి, నేను ప్రస్తుతం ఆహార సూచనను రూపొందించలేకపోయాను. ఊహించని LLM ప్రతిస్పందన.",
        "error_calling_llm": "AI నుండి లోపం: {status_code} - {text}",
        "an_error_occurred": "ఒక లోపం సంభవించింది: {error}. దయచేసి మళ్లీ ప్రయత్నించండి.",
        "report_title": "📊 వంటకాల నిధి నివేదన",
        "report_prompt": "మీ వంటకాల సేకరణ యొక్క అవలోకనం ఇక్కడ ఉంది.",
        "no_data_file_report": "వంటకం డేటా ఫైల్ కనుగొనబడలేదు. నివేదికను రూపొందించడానికి దయచేసి మొదట కొన్ని వంటకాలను సమర్పించండి.",
        "error_loading_report_data": "వంటకం డేటాను లోడ్ చేయడంలో లోపం: {error}",
        "no_recipes_report_info": "ఇప్పటివరకు వంటకాలు ఏవీ సమర్పించబడలేదు. మీరు కొన్ని వంటకాలను జోడించిన తర్వాత నివేదిక అందుబాటులో ఉంటుంది!",
        "general_statistics_subheader": "సాధారణ గణాంకాలు",
        "total_recipes_metric": "మొత్తం వంటకాలు",
        "unique_users_metric": "ప్రత్యేక వినియోగదారులు",
        "unique_categories_metric": "ప్రత్యేక వర్గాలు",
        "recipe_categories_subheader": "వంటకాల వర్గాలు",
        "no_categories_found": "వర్గాలు కనుగొనబడలేదు.",
        "corpus_type_distribution_subheader": "కార్పస్ రకం పంపిణీ",
        "no_corpus_types_recorded": "కార్పస్ రకాలు ఏవీ నమోదు చేయబడలేదు.",
        "geolocation_insights_subheader": "జియోలొకేషన్ అంతర్దృష్టులు",
        "recipes_with_geolocation_metric": "జియోలొకేషన్ ఉన్న వంటకాలు",
        "recipes_without_geolocation_metric": "జియోలొకేషన్ లేని వంటకాలు",
        "first_5_geolocation_recipes": "జియోలొకేషన్ ఉన్న మొదటి 5 వంటకాలు:",
        "no_geolocation_recipes_info": "ఇప్పటివరకు గుర్తించబడిన జియోలొకేషన్ ఉన్న వంటకాలు ఏవీ లేవు.",
        "recent_submissions_subheader": "తాజా సమర్పణలు",
        "no_recent_submissions": "తాజా సమర్పణలు ఏవీ లేవు.",
        "unable_get_precise_coords": "ఖచ్చితమైన కోఆర్డినేట్‌లను పొందలేకపోయాము.",
        "coords_missing_error": "బ్రౌజర్ ప్రతిస్పందన నుండి కోఆర్డినేట్ డేటా లేదు.",
        "geolocation_data_not_available": "జియోలొకేషన్ డేటా అందుబాటులో లేదు.",
        "browser_no_coords_error": "బ్రౌజర్ కోఆర్డినేట్ డేటాను అందించలేదు.",
        "go_to_label": "ఇక్కడికి వెళ్లు:",
        "ingredients_optional_label": "పదార్థాలు (ఐచ్ఛికం)",
        "preparation_steps_optional_label": "తయారీ దశలు (ఐచ్ఛికం)",
        "not_detected_label": "గుర్తించబడలేదు",
        "report_count_column": "సంఖ్య",
    },
    "kn": { # Kannada Translations
        "app_title": "ಪಾಕವಿಧಾನ ವಾಲ್ಟ್ 📖",
        "welcome_message": "ಸ್ವಾಗತ, {username}! 👋",
        "logout_button": "🚪 ಲಾಗ್ ಔಟ್",
        "sidebar_header_explore": "ವಾಲ್ಟ್ ಅನ್ನು ಅನ್ವೇಷಿಸಿ 🚀",
        "nav_submit_recipe": "ಪಾಕವಿಧಾನವನ್ನು ಸಲ್ಲಿಸಿ",
        "nav_view_recipes": "ಪಾಕವಿಧಾನಗಳನ್ನು ವೀಕ್ಷಿಸಿ",
        "nav_food_chatbot": "ಆಹಾರ ಚಾಟ್‌ಬಾಟ್",
        "nav_recipe_report": "ಪಾಕವಿಧಾನ ವರದಿ",
        "login_title": "🔒 ಪಾಕವಿಧಾನ ವಾಲ್ಟ್ ಲಾಗಿನ್",
        "login_prompt": "ಅಪ್ಲಿಕೇಶನ್ ಅನ್ನು ಪ್ರವೇಶಿಸಲು ದಯವಿಟ್ಟು ನಿಮ್ಮ ರುಜುವಾತುಗಳನ್ನು ನಮೂದಿಸಿ.",
        "username_label": "ಬಳಕೆದಾರಹೆಸರು",
        "password_label": "ಪಾಸ್ವರ್ಡ್",
        "login_button": "ಲಾಗಿನ್",
        "invalid_credentials_error": "ಅಮಾನ್ಯ ಬಳಕೆದಾರಹೆಸರು ಅಥವಾ ಪಾಸ್ವರ್ಡ್. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "login_hint": "💡 ಸುಳಿವು: 'admin' ಮತ್ತು 'password123' ಅಥವಾ 'user1' ಮತ್ತು 'mypassword' ಪ್ರಯತ್ನಿಸಿ.",
        "recipe_title_prefix": "🍽️ ಪಾಕವಿಧಾನ:",
        "category_label": "ವರ್ಗ:",
        "submitted_by_label": "ಸಲ್ಲಿಸಿದವರು:",
        "primary_corpus_type_label": "ಪ್ರಾಥಮಿಕ ಕಾರ್ಪಸ್ ಪ್ರಕಾರ:",
        "video_instructions_subheader": "🎥 ವೀಡಿಯೊ ಸೂಚನೆಗಳು",
        "video_file_not_found": "ವೀಡಿಯೊ ಫೈಲ್ ಕಂಡುಬಂದಿಲ್ಲ: {filename}. 'uploads' ಫೋಲ್ಡರ್ ಪರಿಶೀಲಿಸಿ.",
        "audio_instructions_subheader": "🎙️ ಆಡಿಯೊ ಸೂಚನೆಗಳು",
        "audio_file_not_found": "ಆಡಿಯೊ ಫೈಲ್ ಕಂಡುಬಂದಿಲ್ಲ: {filename}. 'uploads' ಫೋಲ್ಡರ್ ಪರಿಶೀಲಿಸಿ.",
        "recipe_image_subheader": "🖼️ ಪಾಕವಿಧಾನ ಚಿತ್ರ",
        "image_file_not_found": "ಚಿತ್ರ ಫೈಲ್ ಕಂಡುಬಂದಿಲ್ಲ: {filename}.",
        "description_subheader": "📝 ವಿವರಣೆ",
        "ingredients_subheader": "📋 ಪದಾರ್ಥಗಳು",
        "preparation_steps_subheader": "👨‍🍳 ತಯಾರಿಕೆಯ ಹಂತಗಳು",
        "show_text_ingredients_steps": "ಪಠ್ಯ ಪದಾರ್ಥಗಳು ಮತ್ತು ಹಂತಗಳನ್ನು ವೀಕ್ಷಿಸಲು ಕ್ಲಿಕ್ ಮಾಡಿ",
        "back_to_all_recipes_button": "⬅️ ಎಲ್ಲಾ ಪಾಕವಿಧಾನಗಳಿಗೆ ಹಿಂತಿರುಗಿ",
        "all_submitted_recipes_title": "📚 ಸಲ್ಲಿಸಿದ ಎಲ್ಲಾ ಪಾಕವಿಧಾನಗಳು",
        "all_submitted_recipes_prompt": "ನಮ್ಮ ಸಮುದಾಯದಿಂದ ಹಂಚಿಕೊಳ್ಳಲಾದ ಎಲ್ಲಾ ರುಚಿಕರವಾದ ಪಾಕವಿಧಾನಗಳನ್ನು ಬ್ರೌಸ್ ಮಾಡಿ!",
        "no_recipes_submitted_info": "ಇನ್ನೂ ಯಾವುದೇ ಪಾಕವಿಧಾನಗಳನ್ನು ಸಲ್ಲಿಸಲಾಗಿಲ್ಲ. ಮೊದಲು ಒಂದನ್ನು ಹಂಚಿಕೊಳ್ಳಿ!",
        "view_specific_recipe_subheader": "🔍 ನಿರ್ದಿಷ್ಟ ಪಾಕವಿಧಾನ ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಿ",
        "no_titles_available_info": "ವಿವರವಾದ ವೀಕ್ಷಣೆಗಾಗಿ ಶೀರ್ಷಿಕೆಗಳೊಂದಿಗೆ ಯಾವುದೇ ಪಾಕವಿಧಾನಗಳು ಲಭ್ಯವಿಲ್ಲ.",
        "select_recipe_to_view": "ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಲು ಪಾಕವಿಧಾನವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "recipe_not_found_error": "ಶೀರ್ಷಿಕೆ '{title}' ಹೊಂದಿರುವ ಪಾಕವಿಧಾನ ಡೇಟಾದಲ್ಲಿ ಕಂಡುಬಂದಿಲ್ಲ. ದಯವಿಟ್ಟು ಡ್ರಾಪ್‌ಡೌನ್‌ನಿಂದ ಅಸ್ತಿತ್ವದಲ್ಲಿರುವ ಪಾಕವಿಧಾನವನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "no_recipe_selected_warning": "ವಿವರಗಳಿಗಾಗಿ ಯಾವುದೇ ಪಾಕವಿಧಾನವನ್ನು ಆಯ್ಕೆ ಮಾಡಲಾಗಿಲ್ಲ. 'ಪಾಕವಿಧಾನಗಳನ್ನು ವೀಕ್ಷಿಸಿ' ಗೆ ಮರುನಿರ್ದೇಶಿಸಲಾಗುತ್ತಿದೆ.",
        "submit_new_recipe_title": "📋 ಹೊಸ ಪಾಕವಿಧಾನವನ್ನು ಸಲ್ಲಿಸಿ",
        "submit_new_recipe_prompt": "ನಿಮ್ಮ ಪಾಕಶಾಲೆಯ ಸೃಷ್ಟಿಗಳನ್ನು ಸಮುದಾಯದೊಂದಿಗೆ ಹಂಚಿಕೊಳ್ಳಿ! ಕೆಳಗಿನ ವಿವರಗಳನ್ನು ಭರ್ತಿ ಮಾಡಿ.",
        "your_details_subheader": "👤 ನಿಮ್ಮ ವಿವರಗಳು",
        "full_name_label": "ಪೂರ್ಣ ಹೆಸರು",
        "email_label": "ಇಮೇಲ್",
        "geolocation_subheader": "📍 ಭೌಗೋಳಿಕ ಸ್ಥಳ (ಸ್ವಯಂ ಪತ್ತೆ)",
        "your_coordinates_label": "ನಿಮ್ಮ ಅಂದಾಜು ನಿರ್ದೇಶಾಂಕಗಳು (ಅಕ್ಷಾಂಶ, ರೇಖಾಂಶ):",
        "current_geolocation_label": "ಪ್ರಸ್ತುತ ಭೌಗೋಳಿಕ ಸ್ಥಳ",
        "geolocation_initial_info": "ನಿಮ್ಮ ಪ್ರಸ್ತುತ ನಿರ್ದೇಶಾಂಕಗಳನ್ನು ಪತ್ತೆಹಚ್ಚಲು 'ಸ್ಥಳವನ್ನು ರಿಫ್ರೆಶ್ ಮಾಡಿ' ಕ್ಲಿಕ್ ಮಾಡಿ.",
        "geolocation_request_pending_info": "ಸ್ಥಳವನ್ನು ಪತ್ತೆಹಚ್ಚಲಾಗುತ್ತಿದೆ... ನಿಮ್ಮ ಬ್ರೌಸರ್ ಸ್ಥಳ ಪ್ರವೇಶಕ್ಕೆ ಅನುಮತಿ ಕೇಳಬಹುದು. ದಯವಿಟ್ಟು ಅನುಮತಿಸಿ.",
        "geolocation_error_warning": "ಸ್ಥಳವನ್ನು ಪತ್ತೆಹಚ್ಚಲಾಗಿಲ್ಲ: {message}",
        "geolocation_permission_info": "ನಿಮ್ಮ ಬ್ರೌಸರ್ ಈ ಸೈಟ್‌ಗೆ ಸ್ಥಳ ಪ್ರವೇಶವನ್ನು ಅನುಮತಿಸುತ್ತದೆ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ. ಪಾಪ್-ಅಪ್‌ಗಳು ಅಥವಾ ಬ್ರೌಸರ್ ಸೆಟ್ಟಿಂಗ್‌ಗಳನ್ನು (ಉದಾ., ಗೌಪ್ಯತೆ ಮತ್ತು ಭದ್ರತೆ -> ಸೈಟ್ ಸೆಟ್ಟಿಂಗ್‌ಗಳು -> ಸ್ಥಳ) ಪರಿಶೀಲಿಸಿ.",
        "refresh_location_button": "🔄 ಸ್ಥಳವನ್ನು ರಿಫ್ರೆಶ್ ಮಾಡಿ",
        "recipe_information_subheader": "📝 ಪಾಕವಿಧಾನ ಮಾಹಿತಿ",
        "category_input_label": "ವರ್ಗ (ಉದಾ., ಸಿಹಿ, ಮುಖ್ಯ ಕೋರ್ಸ್, ಸ್ನ್ಯಾಕ್)",
        "recipe_title_input_label": "ಪಾಕವಿಧಾನ ಶೀರ್ಷಿಕೆ",
        "description_input_label": "ನಿಮ್ಮ ಪಾಕವಿಧಾನದ ಸಂಕ್ಷಿಪ್ತ ವಿವರಣೆ",
        "choose_instructions_subheader": "🍲 ಸೂಚನೆಗಳನ್ನು ಹೇಗೆ ಒದಗಿಸಬೇಕೆಂದು ಆಯ್ಕೆಮಾಡಿ",
        "select_method_radio": "ನಿಮ್ಮ ಆದ್ಯತೆಯ ವಿಧಾನವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "text_based_option": "ಪಠ್ಯ ಆಧಾರಿತ",
        "audio_based_option": "ಆಡಿಯೊ ಆಧಾರಿತ",
        "video_based_option": "ವೀಡಿಯೊ ಆಧಾರಿತ",
        "text_instructions_subheader": "✍️ ಪಠ್ಯ ಸೂಚನೆಗಳು",
        "ingredients_text_area_label": "ಪದಾರ್ಥಗಳು (ಅಲ್ಪವಿರಾಮದಿಂದ ಬೇರ್ಪಡಿಸಿ, ಉದಾ., '2 ಕಪ್ ಹಿಟ್ಟು, 1 ಮೊಟ್ಟೆ')",
        "preparation_steps_text_area_label": "ತಯಾರಿಕೆಯ ಹಂತಗಳು (ವಿವರವಾದ ಸೂಚನೆಗಳು)",
        "text_instructions_caption": "ನಿಮ್ಮ ಪಾಕವಿಧಾನಕ್ಕಾಗಿ ಸ್ಪಷ್ಟ ಪಠ್ಯ ಸೂಚನೆಗಳನ್ನು ಒದಗಿಸಿ.",
        "audio_instructions_upload_label": "ಆಡಿಯೊ ಫೈಲ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ (.mp3, .wav)",
        "audio_instructions_caption": "ನಿಮ್ಮ ಪಾಕವಿಧಾನ ಸೂಚನೆಗಳನ್ನು ಆಡಿಯೊ ಆಗಿ ರೆಕಾರ್ಡ್ ಮಾಡಿ. ಗರಿಷ್ಠ ಫೈಲ್ ಗಾತ್ರ: 20MB.",
        "optional_text_ingredients_steps": "ಐಚ್ಛಿಕ: ಸ್ಪಷ್ಟತೆಗಾಗಿ ಪಠ್ಯ ಪದಾರ್ಥಗಳು ಮತ್ತು ಹಂತಗಳನ್ನು ಸೇರಿಸಿ",
        "video_instructions_upload_label": "ವೀಡಿಯೊ ಫೈಲ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ (.mp4, .mov, .avi)",
        "video_instructions_caption": "ನಿಮ್ಮ ಪಾಕವಿಧಾನವನ್ನು ಪ್ರದರ್ಶಿಸುವ ವೀಡಿಯೊವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ. ಗರಿಷ್ಠ ಫೈಲ್ ಗಾತ್ರ: 50MB.",
        "recipe_image_optional_subheader": "🖼️ ಪಾಕವಿಧಾನ ಚಿತ್ರ (ಐಚ್ಛಿಕ)",
        "image_upload_label": "ಚಿತ್ರ ಫೈಲ್ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ (.jpg, .png)",
        "image_upload_caption": "ಒಂದು ಉತ್ತಮ ಚಿತ್ರವು ನಿಮ್ಮ ಪಾಕವಿಧಾನವನ್ನು ಹೆಚ್ಚು ಆಕರ್ಷಕವಾಗಿಸುತ್ತದೆ!",
        "submit_recipe_button": "🚀 ಪಾಕವಿಧಾನವನ್ನು ಸಲ್ಲಿಸಿ",
        "fill_all_details_error": "🚫 ದಯವಿಟ್ಟು ಎಲ್ಲಾ ಅಗತ್ಯ ಸಾಮಾನ್ಯ ಪಾಕವಿಧಾನ ವಿವರಗಳನ್ನು (ಪೂರ್ಣ ಹೆಸರು, ಇಮೇಲ್, ವರ್ಗ, ಶೀರ್ಷಿಕೆ, ವಿವರಣೆ) ಭರ್ತಿ ಮಾಡಿ.",
        "text_instructions_required_error": "🚫 'ಪಠ್ಯ ಆಧಾರಿತ' ಕಾರ್ಪಸ್‌ಗಾಗಿ, ಪದಾರ್ಥಗಳು ಮತ್ತು ತಯಾರಿಕೆಯ ಹಂತಗಳು ಅಗತ್ಯವಿದೆ.",
        "audio_file_required_error": "🚫 'ಆಡಿಯೊ ಆಧಾರಿತ' ಕಾರ್ಪಸ್‌ಗಾಗಿ, ಆಡಿಯೊ ಫೈಲ್ ಅಗತ್ಯವಿದೆ.",
        "video_file_required_error": "🚫 'ವೀಡಿಯೊ ಆಧಾರಿತ' ಕಾರ್ಪಸ್‌ಗಾಗಿ, ವೀಡಿಯೊ ಫೈಲ್ ಅಗತ್ಯವಿದೆ.",
        "save_media_error": "ಮಾಧ್ಯಮ ಫೈಲ್(ಗಳನ್ನು) ಉಳಿಸಲು ವಿಫಲವಾಗಿದೆ: {error}. '{upload_dir}' ಫೋಲ್ಡರ್ ಬರೆಯಲು ಸಾಧ್ಯವಿದೆ ಎಂದು ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ.",
        "recipe_submitted_success": "✅ ಪಾಕವಿಧಾನ ಯಶಸ್ವಿಯಾಗಿ ಸಲ್ಲಿಸಲಾಗಿದೆ! ಹಂಚಿಕೊಂಡಿದ್ದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು.",
        "food_chatbot_title": "🤖 ಆಹಾರ ಚಾಟ್‌ಬಾಟ್",
        "food_chatbot_prompt": "ನೀವು ಹೇಗೆ ಅನಿಸುತ್ತಿದೆ ಎಂದು ಹೇಳಿ, ಮತ್ತು ನಿಮ್ಮ ಸಂಗ್ರಹಿಸಿದ ಪಾಕವಿಧಾನಗಳಿಂದ ನಾನು ಕೆಲವು ಸಲಹೆಗಳನ್ನು ನೀಡುತ್ತೇನೆ!",
        "chatbot_initial_greeting": "ನಮಸ್ತೆ! ಇಂದು ನೀವು ಯಾವ ರೀತಿಯ ಆಹಾರದ ಮೂಡ್‌ನಲ್ಲಿದ್ದೀರಿ? ನಿಮ್ಮ ಮೂಡ್ ಬಗ್ಗೆ ಹೇಳಿ!",
        "chatbot_input_placeholder": "ನೀವು ಹೇಗೆ ಅನಿಸುತ್ತಿದೆ?",
        "chatbot_thinking_spinner": "ಆಲೋಚಿಸುತ್ತಿದೆ...",
        "no_recipes_chatbot_info": "ನಿಮ್ಮ ಸಂಗ್ರಹದಲ್ಲಿ ಇನ್ನೂ ಯಾವುದೇ ಪಾಕವಿಧಾನಗಳು ಲಭ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು ಕೆಲವು ಸಲ್ಲಿಸಿ!",
        "missing_recipe_cols_error": "ಪಾಕವಿಧಾನ ಡೇಟಾದಲ್ಲಿ 'ಶೀರ್ಷಿಕೆ' ಅಥವಾ 'ವರ್ಗ' ಕಾಲಮ್‌ಗಳು ಕಾಣೆಯಾಗಿವೆ. ಪಾಕವಿಧಾನಗಳನ್ನು ಸೂಚಿಸಲು ಸಾಧ್ಯವಿಲ್ಲ.",
        "no_recipes_submitted_chatbot": "ಇನ್ನೂ ಯಾವುದೇ ಪಾಕವಿಧಾನಗಳನ್ನು ಸಲ್ಲಿಸಲಾಗಿಲ್ಲ. ದಯವಿಟ್ಟು ಮೊದಲು ಕೆಲವು ಪಾಕವಿಧಾನಗಳನ್ನು ಸಲ್ಲಿಸಿ.",
        "error_loading_recipes_chatbot": "ಪಾಕವಿಧಾನಗಳನ್ನು ಲೋಡ್ ಮಾಡುವಾಗ ದೋಷ: {error}",
        "unexpected_llm_response": "ಕ್ಷಮಿಸಿ, ನಾನು ಈಗ ಆಹಾರ ಸಲಹೆಯನ್ನು ರಚಿಸಲು ಸಾಧ್ಯವಾಗಲಿಲ್ಲ. ಅನಿರೀಕ್ಷಿತ LLM ಪ್ರತಿಕ್ರಿಯೆ.",
        "error_calling_llm": "AI ನಿಂದ ದೋಷ: {status_code} - {text}",
        "an_error_occurred": "ದೋಷ ಸಂಭವಿಸಿದೆ: {error}. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
        "report_title": "📊 ಪಾಕವಿಧಾನ ವಾಲ್ಟ್ ವರದಿ",
        "report_prompt": "ಇಲ್ಲಿ ನಿಮ್ಮ ಪಾಕವಿಧಾನ ಸಂಗ್ರಹದ ಅವಲೋಕನವಿದೆ.",
        "no_data_file_report": "ಪಾಕವಿಧಾನ ಡೇಟಾ ಫೈಲ್ ಕಂಡುಬಂದಿಲ್ಲ. ವರದಿ ರಚಿಸಲು ದಯವಿಟ್ಟು ಮೊದಲು ಕೆಲವು ಪಾಕವಿಧಾನಗಳನ್ನು ಸಲ್ಲಿಸಿ.",
        "error_loading_report_data": "ಪಾಕವಿಧಾನ ಡೇಟಾವನ್ನು ಲೋಡ್ ಮಾಡುವಾಗ ದೋಷ: {error}",
        "no_recipes_report_info": "ಇನ್ನೂ ಯಾವುದೇ ಪಾಕವಿಧಾನಗಳನ್ನು ಸಲ್ಲಿಸಲಾಗಿಲ್ಲ. ನೀವು ಕೆಲವು ಪಾಕವಿಧಾನಗಳನ್ನು ಸೇರಿಸಿದ ನಂತರ ವರದಿ ಲಭ್ಯವಿರುತ್ತದೆ!",
        "general_statistics_subheader": "ಸಾಮಾನ್ಯ ಅಂಕಿಅಂಶಗಳು",
        "total_recipes_metric": "ಒಟ್ಟು ಪಾಕವಿಧಾನಗಳು",
        "unique_users_metric": "ಅನನ್ಯ ಬಳಕೆದಾರರು",
        "unique_categories_metric": "ಅನನ್ಯ ವರ್ಗಗಳು",
        "recipe_categories_subheader": "ಪಾಕವಿಧಾನ ವರ್ಗಗಳು",
        "no_categories_found": "ಯಾವುದೇ ವರ್ಗಗಳು ಕಂಡುಬಂದಿಲ್ಲ.",
        "corpus_type_distribution_subheader": "ಕಾರ್ಪಸ್ ಪ್ರಕಾರ ವಿತರಣೆ",
        "no_corpus_types_recorded": "ಯಾವುದೇ ಕಾರ್ಪಸ್ ಪ್ರಕಾರಗಳನ್ನು ದಾಖಲಿಸಲಾಗಿಲ್ಲ.",
        "geolocation_insights_subheader": "ಭೌಗೋಳಿಕ ಸ್ಥಳ ಒಳನೋಟಗಳು",
        "recipes_with_geolocation_metric": "ಭೌಗೋಳಿಕ ಸ್ಥಳದೊಂದಿಗೆ ಪಾಕವಿಧಾನಗಳು",
        "recipes_without_geolocation_metric": "ಭೌಗೋಳಿಕ ಸ್ಥಳವಿಲ್ಲದ ಪಾಕವಿಧಾನಗಳು",
        "first_5_geolocation_recipes": "ಭೌಗೋಳಿಕ ಸ್ಥಳದೊಂದಿಗೆ ಮೊದಲ 5 ಪಾಕವಿಧಾನಗಳು:",
        "no_geolocation_recipes_info": "ಇನ್ನೂ ಯಾವುದೇ ಪತ್ತೆಯಾದ ಭೌಗೋಳಿಕ ಸ್ಥಳದೊಂದಿಗೆ ಪಾಕವಿಧಾನಗಳು ಇಲ್ಲ.",
        "recent_submissions_subheader": "ಇತ್ತೀಚಿನ ಸಲ್ಲಿಕೆಗಳು",
        "no_recent_submissions": "ಇತ್ತೀಚಿನ ಸಲ್ಲಿಕೆಗಳು ಯಾವುದೂ ಇಲ್ಲ.",
        "unable_get_precise_coords": "ನಿಖರವಾದ ನಿರ್ದೇಶಾಂಕಗಳನ್ನು ಪಡೆಯಲು ಸಾಧ್ಯವಿಲ್ಲ.",
        "coords_missing_error": "ಬ್ರೌಸರ್ ಪ್ರತಿಕ್ರಿಯೆಯಿಂದ ನಿರ್ದೇಶಾಂಕ ಡೇಟಾ ಕಾಣೆಯಾಗಿದೆ.",
        "geolocation_data_not_available": "ಭೌಗೋಳಿಕ ಸ್ಥಳ ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ.",
        "browser_no_coords_error": "ಬ್ರೌಸರ್ ನಿರ್ದೇಶಾಂಕ ಡೇಟಾವನ್ನು ಒದಗಿಸಲಿಲ್ಲ.",
        "go_to_label": "ಇಲ್ಲಿಗೆ ಹೋಗಿ:",
        "ingredients_optional_label": "ಪದಾರ್ಥಗಳು (ಐಚ್ಛಿಕ)",
        "preparation_steps_optional_label": "ತಯಾರಿಕೆಯ ಹಂತಗಳು (ಐಚ್ಛಿಕ)",
        "not_detected_label": "ಪತ್ತೆಯಾಗಿಲ್ಲ",
        "report_count_column": "ಎಣಿಕೆ",
    }
}

# --- Helper function to get translated text ---
def get_text(key, **kwargs):
    lang = st.session_state.get("selected_language", "en")
    # Fallback to English if key not found in selected language, then to key itself
    text = translations.get(lang, translations["en"]).get(key, translations["en"].get(key, key))
    return text.format(**kwargs)

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
def process_geolocation_result():
    if st.session_state.get("geolocation_status") == "request_pending":
        result = get_geolocation() 

        if result: 
            coords = result.get("coords")
            if coords:
                lat = coords.get("latitude")
                lon = coords.get("longitude")
                if lat is not None and lon is not None:
                    st.session_state["geolocation_status"] = "detected"
                    st.session_state["geolocation_display"] = f"{lat:.6f}, {lon:.6f}"
                    st.session_state["geolocation_value"] = f"{lat:.6f}, {lon:.6f}" 
                else:
                    st.session_state["geolocation_status"] = "error"
                    st.session_state["geolocation_display"] = get_text("unable_get_precise_coords")
                    st.session_state["geolocation_error_message"] = get_text("coords_missing_error")
            else:
                st.session_state["geolocation_status"] = "error"
                st.session_state["geolocation_display"] = get_text("geolocation_data_not_available")
                st.session_state["geolocation_error_message"] = get_text("browser_no_coords_error")
        else:
            pass 

# --- UI Components and Logic ---

def login():
    st.title(get_text("login_title"))
    st.markdown(get_text("login_prompt"))

    username = st.text_input(get_text("username_label"), key="login_username")
    password = st.text_input(get_text("password_label"), type="password", key="login_password")

    if st.button(get_text("login_button"), use_container_width=True):
        if verify_password(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.rerun()
        else:
            st.error(get_text("invalid_credentials_error"))
    st.info(get_text("login_hint"))

def logout():
    if st.sidebar.button(get_text("logout_button"), key="logout_button_sidebar"):
        for key in ["logged_in", "username", "geolocation_status", "geolocation_display", "geolocation_value", "geolocation_error_message", "current_page", "selected_recipe_data", "selected_recipe_title_for_view", "chatbot_messages", "selected_language"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

def display_recipe_details(selected_recipe):
    st.title(get_text("recipe_title_prefix") + f" {selected_recipe['Title']}")
    st.markdown(f"***{get_text('category_label')}*** **{selected_recipe['Category']}**")
    st.caption(f"{get_text('submitted_by_label')} {selected_recipe['Full Name']} ({selected_recipe['Username']}) at {selected_recipe['Timestamp']} from {selected_recipe['Geolocation']}")
    st.markdown(f"***{get_text('primary_corpus_type_label')}*** **{selected_recipe['CorpusType']}**")

    st.divider()

    if selected_recipe['CorpusType'] == 'Video-based' and selected_recipe['VideoFile']:
        st.subheader(get_text("video_instructions_subheader"))
        video_path = os.path.join(UPLOAD_DIR, selected_recipe['VideoFile'])
        if os.path.exists(video_path):
            st.video(video_path, format='video/mp4')
        else:
            st.error(get_text("video_file_not_found", filename=selected_recipe['VideoFile']))
    elif selected_recipe['CorpusType'] == 'Audio-based' and selected_recipe['AudioFile']:
        st.subheader(get_text("audio_instructions_subheader"))
        audio_path = os.path.join(UPLOAD_DIR, selected_recipe['AudioFile'])
        if os.path.exists(audio_path):
            st.audio(audio_path, format='audio/wav')
        else:
            st.error(get_text("audio_file_not_found", filename=selected_recipe['AudioFile']))
    elif selected_recipe['ImageFile']:
        st.subheader(get_text("recipe_image_subheader"))
        image_path = os.path.join(UPLOAD_DIR, selected_recipe['ImageFile'])
        if os.path.exists(image_path):
            st.image(image_path, caption=f"Image for {selected_recipe['Title']}", use_column_width=True)
        else:
            st.info(get_text("image_file_not_found", filename=selected_recipe['ImageFile']))

    st.subheader(get_text("description_subheader"))
    st.write(selected_recipe['Description'])
    
    if selected_recipe['CorpusType'] == 'Text-based' or selected_recipe['CorpusType'] == '':
        st.subheader(get_text("ingredients_subheader"))
        st.markdown(f"_{selected_recipe['Ingredients'].replace(',', ', ')}_")
        st.subheader(get_text("preparation_steps_subheader"))
        st.markdown(selected_recipe['Steps'])
    else:
        with st.expander(get_text("show_text_ingredients_steps")):
            st.subheader(get_text("ingredients_subheader"))
            st.markdown(f"_{selected_recipe['Ingredients'].replace(',', ', ')}_")
            st.subheader(get_text("preparation_steps_subheader"))
            st.markdown(selected_recipe['Steps'])

    st.markdown("---")
    if st.button(get_text("back_to_all_recipes_button"), use_container_width=True, key="back_to_all_recipes_btn"):
        st.session_state["current_page"] = "view_all_recipes"
        st.session_state["selected_recipe_data"] = None
        st.rerun()

def view_all_recipes():
    st.title(get_text("all_submitted_recipes_title"))
    st.markdown(get_text("all_submitted_recipes_prompt"))
    
    df = pd.read_csv(DATA_FILE, dtype={
        "ImageFile": str, "AudioFile": str, "VideoFile": str, "CorpusType": str
    }).fillna('')
    
    if 'Title' in df.columns:
        df['Title'] = df['Title'].astype(str).str.strip()

    if df.empty:
        st.info(get_text("no_recipes_submitted_info"))
    else:
        st.dataframe(df[[
            "Timestamp", "Username", "Title", "Category", "Geolocation", "CorpusType"
        ]], use_container_width=True)

        st.divider()
        st.subheader(get_text("view_specific_recipe_subheader"))
        unique_titles = df["Title"].dropna().unique()
        
        if len(unique_titles) == 0:
            st.info(get_text("no_titles_available_info"))
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
            get_text("select_recipe_to_view"),
            options,
            index=initial_select_index,
            key='view_recipes_selectbox_main'
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
                    st.error(get_text("recipe_not_found_error", title=selected_title_from_widget))
                    st.session_state["selected_recipe_title_for_view"] = ''
                    st.session_state["selected_recipe_data"] = None
        else:
            if st.session_state["current_page"] == "recipe_details":
                st.session_state["current_page"] = "view_all_recipes"
                st.session_state["selected_recipe_data"] = None
                st.session_state["selected_recipe_title_for_view"] = ''
                st.rerun()


def recipe_submission(username):
    st.title(get_text("submit_new_recipe_title"))
    st.markdown(get_text("submit_new_recipe_prompt"))

    st.divider()

    st.subheader(get_text("your_details_subheader"))
    with st.container(border=True):
        full_name = st.text_input(get_text("full_name_label"), key="submit_full_name")
        email = st.text_input(get_text("email_label"), key="submit_email")

    st.subheader(get_text("geolocation_subheader"))
    with st.container(border=True):
        st.write(get_text("your_coordinates_label"))
        st.text_input(get_text("current_geolocation_label"), st.session_state["geolocation_display"], disabled=True, label_visibility="hidden", key="geolocation_display_input")

        if st.session_state["geolocation_status"] == "initial":
            st.info(get_text("geolocation_initial_info"))
        elif st.session_state["geolocation_status"] == "request_pending":
            st.info(get_text("geolocation_request_pending_info"))
        elif st.session_state["geolocation_status"] == "error":
            st.error(get_text("geolocation_error_warning", message=st.session_state['geolocation_error_message']))
            st.info(get_text("geolocation_permission_info"))
        
        if st.button(get_text("refresh_location_button"), use_container_width=True, key="refresh_location_btn"):
            st.session_state["geolocation_status"] = "request_pending"
            st.session_state["geolocation_display"] = "Detecting..."
            st.session_state["geolocation_error_message"] = ""
            st.rerun()

    st.divider()

    st.subheader(get_text("recipe_information_subheader"))
    with st.container(border=True):
        category = st.text_input(get_text("category_input_label"), key="submit_category")
        title = st.text_input(get_text("recipe_title_input_label"), key="submit_title")
        description = st.text_area(get_text("description_input_label"), key="submit_description")

    st.divider()

    st.subheader(get_text("choose_instructions_subheader"))
    corpus_type = st.radio(
        get_text("select_method_radio"),
        (get_text("text_based_option"), get_text("audio_based_option"), get_text("video_based_option")),
        key='corpus_type_selector',
        horizontal=True
    )

    st.markdown("---")

    if corpus_type == get_text("text_based_option"):
        st.subheader(get_text("text_instructions_subheader"))
        ingredients = st.text_area(get_text("ingredients_text_area_label"), key='ingredients_text', height=100)
        steps = st.text_area(get_text("preparation_steps_text_area_label"), key='steps_text', height=200)
        st.caption(get_text("text_instructions_caption"))

    elif corpus_type == get_text("audio_based_option"):
        st.subheader(get_text("audio_instructions_subheader"))
        audio_file = st.file_uploader(get_text("audio_instructions_upload_label"), type=["mp3", "wav"], key='audio_file_uploader')
        st.caption(get_text("audio_instructions_caption"))
        with st.expander(get_text("optional_text_ingredients_steps")):
            ingredients = st.text_area(get_text("ingredients_optional_label"), key='ingredients_audio_opt')
            steps = st.text_area(get_text("preparation_steps_optional_label"), key='steps_audio_opt')

    elif corpus_type == get_text("video_based_option"):
        st.subheader(get_text("video_instructions_subheader"))
        video_file = st.file_uploader(get_text("video_instructions_upload_label"), type=["mp4", "mov", "avi", "webm"], key='video_file_uploader')
        st.caption(get_text("video_instructions_caption"))
        with st.expander(get_text("optional_text_ingredients_steps")):
            ingredients = st.text_area(get_text("ingredients_optional_label"), key='ingredients_video_opt')
            steps = st.text_area(get_text("preparation_steps_optional_label"), key='steps_video_opt')

    st.markdown("---")

    st.subheader(get_text("recipe_image_optional_subheader"))
    image_file = st.file_uploader(get_text("image_upload_label"), type=["jpg", "jpeg", "png"], key='image_file_uploader')
    st.caption(get_text("image_upload_caption"))


    if st.button(get_text("submit_recipe_button"), use_container_width=True, type="primary", key="submit_recipe_btn"):
        validation_passed = True
        error_messages = []

        if not all([full_name.strip(), email.strip(), category.strip(), title.strip(), description.strip()]):
            error_messages.append(get_text("fill_all_details_error"))
            validation_passed = False

        if corpus_type == get_text("text_based_option"):
            if not all([ingredients.strip(), steps.strip()]):
                error_messages.append(get_text("text_instructions_required_error"))
                validation_passed = False
        elif corpus_type == get_text("audio_based_option"):
            if not audio_file:
                error_messages.append(get_text("audio_file_required_error"))
                validation_passed = False
        elif corpus_type == get_text("video_based_option"):
            if not video_file:
                error_messages.append(get_text("video_file_required_error"))
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
            "Geolocation": st.session_state.get("geolocation_value", get_text("not_detected_label")), # Use translated "Not detected"
            "Category": category.strip(),
            "Title": title.strip(),
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

        try:
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
        except Exception as e:
            st.error(get_text("save_media_error", error=e, upload_dir=UPLOAD_DIR))
            return

        st.success(get_text("recipe_submitted_success"))
        st.balloons()
        st.rerun()

# --- Chatbot Section ---
async def food_chatbot_section():
    st.title(get_text("food_chatbot_title"))
    st.markdown(get_text("food_chatbot_prompt"))

    st.divider()

    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = [{"role": "assistant", "content": get_text("chatbot_initial_greeting")}]

    for message in st.session_state.chatbot_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(get_text("chatbot_input_placeholder"), key="chatbot_input"):
        st.session_state.chatbot_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

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
                    recipes_list_str = get_text("no_recipes_chatbot_info")
            else:
                recipes_list_str = get_text("missing_recipe_cols_error")
                
        except FileNotFoundError:
            recipes_list_str = get_text("no_recipes_submitted_chatbot")
        except Exception as e:
            recipes_list_str = get_text("error_loading_recipes_chatbot", error=e)

        with st.chat_message("assistant"):
            with st.spinner(get_text("chatbot_thinking_spinner")):
                try:
                    llm_prompt = f"""
The user's current message is: '{prompt}'.
You need to suggest a recipe from the following list of available recipes based on the user's mood or general request.
If a suitable recipe is not found in the list, you can suggest a general food item or type of cuisine that matches the mood, but prioritize the provided list.

Available Recipes in the app:
{recipes_list_str}

**Instructions for response:**
- If the user's message is a simple greeting (e.g., "hello", "hi", "hey", "good morning", "what's up", "how are you"), respond with a friendly greeting back and then ask them about their mood and what kind of food they are in the mood for.
- Otherwise, based on their mood or query, suggest one recipe from the list (if applicable) and a brief reason why it fits.
- Keep your response concise, around 2-3 sentences.
- Do not ask follow-up questions unless it's the initial mood inquiry after a greeting.
- If you suggest a recipe from the list, just mention its name and why it fits the mood.
"""

                    chatHistory = []
                    chatHistory.append({ "role": "user", "parts": [{ "text": llm_prompt }] })
                    payload = { "contents": chatHistory }
                    
                    apiKey = "AIzaSyA-Juywn6NX2KS4n0417F0GQ8h_E9skpVI" # Your API Key
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
                            llm_response_text = get_text("unexpected_llm_response")
                            st.error(f"LLM response structure unexpected: {result}")
                    else:
                        llm_response_text = get_text("error_calling_llm", status_code=response.status_code, text=response.text)
                        st.error(get_text("error_calling_llm", status_code=response.status_code, text=response.text))

                    st.markdown(llm_response_text)
                    st.session_state.chatbot_messages.append({"role": "assistant", "content": llm_response_text})

                except Exception as e:
                    error_message = get_text("an_error_occurred", error=e)
                    st.error(error_message)
                    st.session_state.chatbot_messages.append({"role": "assistant", "content": error_message})

# --- Recipe Report Function ---
def generate_recipe_report():
    st.title(get_text("report_title"))
    st.markdown(get_text("report_prompt"))

    try:
        df = pd.read_csv(DATA_FILE, dtype={
            "ImageFile": str, "AudioFile": str, "VideoFile": str, "CorpusType": str
        }).fillna('')
        if 'Title' in df.columns:
            df['Title'] = df['Title'].astype(str).str.strip()
    except FileNotFoundError:
        st.warning(get_text("no_data_file_report"))
        return
    except Exception as e:
        st.error(get_text("error_loading_report_data", error=e))
        return

    if df.empty:
        st.info(get_text("no_recipes_report_info"))
        return

    st.subheader(get_text("general_statistics_subheader"))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label=get_text("total_recipes_metric"), value=len(df))
    with col2:
        unique_users = df['Username'].nunique()
        st.metric(label=get_text("unique_users_metric"), value=unique_users)
    with col3:
        unique_categories = df['Category'].nunique()
        st.metric(label=get_text("unique_categories_metric"), value=unique_categories)

    st.divider()

    st.subheader(get_text("recipe_categories_subheader"))
    category_counts = df['Category'].value_counts()
    if not category_counts.empty:
        st.dataframe(category_counts.reset_index().rename(columns={'index': get_text('category_label').replace(':', ''), 'Category': get_text('report_count_column')}), use_container_width=True) # FIXED: Use new key
        st.bar_chart(category_counts)
    else:
        st.info(get_text("no_categories_found"))

    st.divider()

    st.subheader(get_text("corpus_type_distribution_subheader"))
    corpus_type_counts = df['CorpusType'].value_counts()
    if not corpus_type_counts.empty:
        st.dataframe(corpus_type_counts.reset_index().rename(columns={'index': get_text('primary_corpus_type_label').replace(':', ''), 'CorpusType': get_text('report_count_column')}), use_container_width=True) # FIXED: Use new key
        st.pie_chart(corpus_type_counts)
    else:
        st.info(get_text("no_corpus_types_recorded"))

    st.divider()

    st.subheader(get_text("geolocation_insights_subheader"))
    detected_locations = df[df['Geolocation'] != 'Not detected']
    not_detected_locations = df[df['Geolocation'] == 'Not detected']

    col_geo1, col_geo2 = st.columns(2)
    with col_geo1:
        st.metric(label=get_text("recipes_with_geolocation_metric"), value=len(detected_locations))
    with col_geo2:
        st.metric(label=get_text("recipes_without_geolocation_metric"), value=len(not_detected_locations))
    
    if not detected_locations.empty:
        st.write(get_text("first_5_geolocation_recipes"))
        st.dataframe(detected_locations[['Title', 'Geolocation']].head(5), use_container_width=True)
    else:
        st.info(get_text("no_geolocation_recipes_info"))

    st.divider()

    st.subheader(get_text("recent_submissions_subheader"))
    if not df.empty:
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        most_recent = df.sort_values(by='Timestamp', ascending=False).head(5)
        st.dataframe(most_recent[['Timestamp', 'Title', 'Username', 'Category']], use_container_width=True)
    else:
        st.info(get_text("no_recent_submissions"))

# --- Main App Logic (orchestrates page display) ---

def main():
    # Set page configuration at the very beginning
    st.set_page_config(
        page_title=get_text("app_title"),
        page_icon="👨‍🍳",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state for language selection
    if "selected_language" not in st.session_state:
        st.session_state["selected_language"] = "en" # Default to English

    # Language selection in the sidebar (top)
    st.sidebar.subheader("🌐 Language")
    language_options_display = {
        "English": "en",
        "हिन्दी": "hi",
        "தமிழ்": "ta",  # Added Tamil
        "తెలుగు": "te",  # Added Telugu
        "ಕನ್ನಡ": "kn"   # Added Kannada
    }
    
    current_lang_display_name = {v: k for k, v in language_options_display.items()}.get(st.session_state["selected_language"], "English")
    
    selected_language_name_from_widget = st.sidebar.selectbox(
        "Select Language:", # This label is intentionally hardcoded as language selection should always be clear
        options=list(language_options_display.keys()),
        index=list(language_options_display.keys()).index(current_lang_display_name),
        key="language_selector"
    )
    
    if st.session_state["selected_language"] != language_options_display[selected_language_name_from_widget]:
        st.session_state["selected_language"] = language_options_display[selected_language_name_from_widget]
        st.rerun()

    # Initialize other necessary session_state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "geolocation_status" not in st.session_state:
        st.session_state["geolocation_status"] = "initial"
    # FIXED: Initial geolocation display should be a concise translated string
    if "geolocation_display" not in st.session_state:
        st.session_state["geolocation_display"] = get_text("not_detected_label")
    if "geolocation_value" not in st.session_state:
        st.session_state["geolocation_value"] = get_text("not_detected_label") # Also use translated for value
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
        # --- Attractive Sidebar ---
        st.sidebar.image("https://static.thenounproject.com/png/514467-200.png", width=100)
        st.sidebar.markdown(get_text("welcome_message", username=st.session_state['username']))
        st.sidebar.markdown("---")

        st.sidebar.header(get_text("sidebar_header_explore"))

        # Define internal page names and their associated emojis
        # This mapping is language-agnostic
        page_emojis = {
            "submit_recipe": "📝",
            "view_all_recipes": "📚",
            "food_chatbot": "🤖",
            "recipe_report": "📊"
        }

        # Create the list of display options for the radio button
        # Each item will be "Emoji Translated Text"
        display_options_for_radio = []
        for internal_name, emoji in page_emojis.items():
            display_options_for_radio.append(f"{emoji} {get_text(f'nav_{internal_name}')}")

        # Determine the initial index for the radio button
        current_display_for_radio = ""
        if st.session_state["current_page"] == "submit_recipe":
            current_display_for_radio = f"{page_emojis['submit_recipe']} {get_text('nav_submit_recipe')}"
        elif st.session_state["current_page"] in ["view_all_recipes", "recipe_details"]:
            current_display_for_radio = f"{page_emojis['view_all_recipes']} {get_text('nav_view_recipes')}"
        elif st.session_state["current_page"] == "food_chatbot":
            current_display_for_radio = f"{page_emojis['food_chatbot']} {get_text('nav_food_chatbot')}"
        elif st.session_state["current_page"] == "recipe_report":
            current_display_for_radio = f"{page_emojis['recipe_report']} {get_text('nav_recipe_report')}"
        
        initial_sidebar_index = 0
        if current_display_for_radio in display_options_for_radio:
            initial_sidebar_index = display_options_for_radio.index(current_display_for_radio)

        selected_sidebar_option_display = st.sidebar.radio(
            get_text("go_to_label"),
            options=display_options_for_radio,
            index=initial_sidebar_index,
            key="main_navigation",
        )
        
        # Map the selected display option back to its internal state name
        selected_internal_page = ""
        for internal_name, emoji in page_emojis.items():
            translated_text = get_text(f'nav_{internal_name}')
            if selected_sidebar_option_display == f"{emoji} {translated_text}":
                selected_internal_page = internal_name
                break

        st.sidebar.markdown("---")
        logout()

        # Logic for page navigation based on selected_internal_page
        if st.session_state["current_page"] != selected_internal_page:
            st.session_state["current_page"] = selected_internal_page
            st.session_state["selected_recipe_data"] = None
            st.session_state["selected_recipe_title_for_view"] = ''
            st.rerun()

        process_geolocation_result()

        # --- Main Content Display ---
        if st.session_state["current_page"] == "submit_recipe":
            recipe_submission(st.session_state["username"])
        elif st.session_state["current_page"] == "view_all_recipes" or st.session_state["current_page"] == "recipe_details":
            if st.session_state["current_page"] == "recipe_details" and st.session_state["selected_recipe_data"]:
                display_recipe_details(pd.Series(st.session_state["selected_recipe_data"]))
            else:
                view_all_recipes()
        elif st.session_state["current_page"] == "food_chatbot":
            asyncio.run(food_chatbot_section())
        elif st.session_state["current_page"] == "recipe_report":
            generate_recipe_report()

    else:
        login()

if __name__ == "__main__":
    main()
