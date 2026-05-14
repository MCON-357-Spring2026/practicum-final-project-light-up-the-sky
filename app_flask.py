import os
import sqlite3
import json
import toml
import google.generativeai as genai
from flask import Flask, render_template, request

# --- NEW VAULT LOADER ---
base_dir = os.path.dirname(os.path.abspath(__file__))
vault_path = os.path.join(base_dir, "vault", "keys.toml")

api_key = None

if os.path.exists(vault_path):
    try:
        secrets = toml.load(vault_path)
        api_key = secrets.get("GEMINI_API_KEY")
        print("✅ Successfully loaded API key from vault.")
    except Exception as e:
        print(f"❌ Error reading vault/keys.toml: {e}")
else:
    # Try Environment Variable (for deployment)
    api_key = os.environ.get("GEMINI_API_KEY")
    print("ℹ️ Vault not found, checking environment variables...")

# CRITICAL STEP: Hand the key to Google
if api_key:
    genai.configure(api_key=api_key)
else:
    print("⚠️ CRITICAL: No API Key found! Analysis will fail.")

# 1. Create the App variable FIRST
app = Flask(__name__)

# 2. Database matching function
def get_matches_from_db(intensity, segment_duration):
    conn = sqlite3.connect('pyro_planner.db')
    cursor = conn.cursor()
    search_pace = str(intensity).lower().strip()
    target_dur = int(segment_duration)

    # 1. We find all fireworks where Pace matches exactly
    # 2. AND where the duration is within 5 seconds of our target (up or down)
    # 3. We shuffle that specific list and pick the top 1
    query = """
            SELECT name, duration
            FROM fireworks
            WHERE LOWER(TRIM(pace)) = ?
              AND ABS(duration - ?) <= 5
            ORDER BY RANDOM()
                LIMIT 1
            """
    cursor.execute(query, (search_pace, target_dur))
    result = cursor.fetchone()

    conn.close()
    return result

# 3. Now you can use @app.route
@app.route('/', methods=['GET', 'POST'])
def index():
    show_data = []  # Initialize empty list

    if request.method == 'POST':
        print("Analyze button clicked!") # Check your terminal for this!

        file = request.files.get('music_file') # Must match HTML 'name'

        if file and file.filename != '':
            print(f"File received: {file.filename}")

            # --- START ANALYSIS ---
            temp_path = "temp_audio.mp3"
            file.save(temp_path)

            try:
                # 1. AI Analysis
                audio_file = genai.upload_file(path=temp_path)
                model = genai.GenerativeModel("gemini-3.1-flash-lite")
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

                response = model.generate_content([prompt, audio_file],
                                                  generation_config={"response_mime_type": "application/json"})

                plan = json.loads(response.text)

                # 2. Match with Database
                for item in plan:
                    s_name = item.get('Segment')
                    s_time = item.get('Timestamp')
                    s_dur = item.get('Length')
                    s_pace = item.get('Pace')

                    # Match with your database
                    match = get_matches_from_db(s_pace, s_dur)

                    if match:
                        selection = f"{match[0]} ({match[1]}s)"
                    else:
                        selection = "⚠️ No Match"

                    # This dictionary must match the keys in your index.html
                    show_data.append({
                        "Segment": s_name,
                        "Timestamp": s_time,
                        "Length": f"{s_dur}s",
                        "Pace": s_pace.capitalize() if s_pace else "Medium",
                        "Firework": selection
                    })
                print("Analysis successful!")

            except Exception as e:
                print(f"Error during analysis: {e}")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

    # CRITICAL: This sends the results back to the page
    return render_template('index.html', plan=show_data)

if __name__ == '__main__':
    # This looks for a 'PORT' variable from the cloud provider
    # If it doesn't find one (like on your laptop), it defaults to 5000
    port = int(os.environ.get("PORT", 5000))

    # host='0.0.0.0' tells the app to be 'public' on the web
    app.run(host='0.0.0.0', port=port)