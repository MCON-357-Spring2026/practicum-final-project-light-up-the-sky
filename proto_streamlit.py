import streamlit as st
import sqlite3
import json
import random
import google.generativeai as genai
import os

# --- INITIALIZE GEMINI ---
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("API Key not found! Check your .streamlit/secrets.toml file.")

st.set_page_config(page_title="PyroPlanner", page_icon="🎆", layout="wide")

st.title("PyroPlanner")
st.subheader("Automated Firework Choreography")

# --- DATABASE LOGIC ---
def get_matches_from_db(intensity, segment_duration):
    conn = sqlite3.connect('pyro_planner.db')
    cursor = conn.cursor()
    search_pace = str(intensity).lower().strip()
    target_dur = int(segment_duration)

    query = """
            SELECT name, duration
            FROM fireworks
            WHERE LOWER(TRIM(pace)) = ?
            ORDER BY ABS(duration - ?) ASC
                LIMIT 1
            """
    cursor.execute(query, (search_pace, target_dur))
    result = cursor.fetchone()
    conn.close()
    return result

# --- SIDEBAR: Upload & Input ---
with st.sidebar:
    st.header("1. Upload Music")
    uploaded_file = st.file_uploader("Choose an MP3 file", type=['mp3', 'wav'])

    st.header("2. AI Control")
    analyze_btn = st.button("Analyze & Generate Show")

    st.divider()
    st.info("The AI will analyze your music and generate a timestamped script with matching fireworks.")

# --- MAIN LOGIC ---
if analyze_btn and uploaded_file:
    plan = None
    tmp_path = "temp_audio_upload.mp3"

    with open(tmp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.status("AI is processing audio...", expanded=True) as status:
        try:
            st.write("Uploading to Google AI Studio...")
            audio_file = genai.upload_file(path=tmp_path)
            model = genai.GenerativeModel(model_name="gemini-3.1-flash-lite")

            prompt = """
                Analyze this music for a firework show. 
                Break it into segments (Intro, Verse, Chorus, etc.).
                
                Return ONLY a JSON array of objects. Each object must include:
                1. "Segment": The name of the musical part.
                2. "Timestamp": The start and end time (e.g., "0:00 - 0:15"). This must be cumulative.
                3. "Length": The duration of the segment in seconds.
                4. "Pace": The intensity (exactly 'slow', 'medium', or 'fast').
                5. "Firework": The name of a firework from the database that matches the Pace.
                
                Example: [{"Segment": "Chorus 1", "Timestamp": "0:00 - 0:20", "Length": 20, "Pace": "fast", "Firework": "Crossfire 500"}]
                
                Important Note for Pace: This classification should reflect the suggested firing 
                frequency and emotional energy of the pyrotechnics required to match the orchestration, 
                not the BPM of the song.
                """

            st.write("Analyzing rhythm and intensity...")
            response = model.generate_content([prompt, audio_file],
                                              generation_config={"response_mime_type": "application/json"})

            plan = json.loads(response.text)
            status.update(label="Analysis Complete!", state="complete", expanded=False)

        except Exception as e:
            st.error(f"Error during AI analysis: {e}")
        finally:
            if os.path.exists(tmp_path):
                try: os.remove(tmp_path)
                except: pass

    # --- TABLE DISPLAY ---
    if plan:
        show_data = []
        for item in plan:
            # Grabbing the keys that match your prompt exactly
            s_name = item.get('Segment', 'Unknown')
            s_time = item.get('Timestamp', '0:00')
            s_dur = item.get('Length', 0)
            s_pace = str(item.get('Pace', 'medium')).lower().strip()

            # Match with database
            match = get_matches_from_db(s_pace, s_dur)

            if match:
                selection = f"{match[0]} ({match[1]}s)"
            else:
                selection = "⚠️ No Match Found"

            # Create dictionary for Streamlit table
            show_data.append({
                "Segment": s_name,
                "Time (Start-End)": s_time,
                "Duration": f"{s_dur}s",
                "Pace": s_pace.capitalize(),
                "Selected Firework": selection
            })

        st.success("✨ Choreography Ready!")
        # Using st.table for a clean, uniform look
        st.table(show_data)
else:
    if not uploaded_file:
        st.info("Please upload an MP3 in the sidebar to get started.")