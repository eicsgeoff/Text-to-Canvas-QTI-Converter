import streamlit as st
import io
import zipfile
from text2qti.quiz import Quiz
from text2qti.config import Config

# Page config for a professional look
st.set_page_config(page_title="Canvas QTI Creator", page_icon="📝")

st.title("📝 Text to Canvas QTI Converter")
st.markdown("""
Paste your questions below following the **text2qti** format. 
[View formatting guide](https://github.com/gpoore/text2qti#syntax)
""")

# The input window
user_input = st.text_area(
    "Paste questions here:", 
    height=400, 
    placeholder="1. What is 2+2?\n*a) 4\nb) 5\n\n2. Python is great.\n*a. True\nb. False"
)

# Settings (Optional but helpful)
with st.expander("Advanced Options"):
    quiz_title = st.text_input("Quiz Title", value="Imported Quiz")
    points_per_question = st.number_input("Points per question", value=1.0)

if st.button("Generate QTI Zip"):
    if not user_input.strip():
        st.error("Please paste some text first!")
    else:
        try:
            # 1. Setup text2qti configuration
            config = Config()
            # We add a title to the start of the text as text2qti expects it
            full_text = f"Quiz title: {quiz_title}\n\n{user_input}"
            
            # 2. Process the text
            quiz = Quiz(full_text, config=config)
            
            # 3. Create the ZIP in memory
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w") as zf:
                for filename, content in quiz.qti_files().items():
                    zf.writestr(filename, content)
            
            # 4. Provide the download button
            st.success("Conversion successful!")
            st.download_button(
                label="💾 Download QTI Zip for Canvas",
                data=buf.getvalue(),
                file_name=f"{quiz_title.replace(' ', '_')}.zip",
                mime="application/zip"
            )
            
        except Exception as e:
            st.error(f"Error processing text: {str(e)}")
            st.info("Check your formatting. Ensure questions start with '1.' and correct answers with '*'")