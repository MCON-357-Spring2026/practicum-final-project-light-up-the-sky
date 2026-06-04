# PyroPlanner 🎆🎵

PyroPlanner is an intelligent web application that analyzes raw audio soundtracks using generative AI to automatically slice musical structures and map them against a synchronized, database-matched pyrotechnic firing plan. It reduces hours of manual show choreography down to a single click.

🚀 **Live Deployment:** [Launch PyroPlanner on Vercel](https://practicum-final-project-light-up-th.vercel.app/)
**Confluence Page** https://mcon152.atlassian.net/wiki/spaces/PD/overview?homepageId=88473917
**Jira Page** https://mcon152.atlassian.net/jira/software/c/projects/PD/boards/1

---

## 🛠️ Technology Stack Decisions

| Layer | Technology | Decision |
| :--- | :--- | :--- |
| **Frontend** | HTML5 / Tailwind CSS / Jinja2 Templates | Native Flask template rendering engine chosen for rapid UI generation, seamless form submissions, and direct array iteration (`{% for item in plan %}`). |
| **Backend** | Python Flask | Lightweight web framework selected for fast routing, ease of local development, and seamless integration with the Python Google GenAI SDK. |
| **Database** | SQLite3 (`pyro_planner.db`) | Lightweight, zero-configuration relational database bundled directly with the repository for quick, randomized SQL queries matching pyrotechnics to pace. |
| **Deployment** | Vercel Serverless | Selected for frictionless git-integrated deployment (`vercel --prod`) and automatic HTTPS orchestration. |
| **AI Orchestration** | Google Gemini 3.1 Flash Lite | Chosen for its exceptional speed, low token latency, native JSON schema enforcement, and highly resilient multi-modal capabilities when parsing audio streams. |
| **Export Engine** | fpdf2 (`FPDF`) | Python PDF generation library utilized to stream raw binary byte payloads directly out of system memory (`io.BytesIO()`) using advanced structural data tables. |

---

## 🧠 Model Selection & Dual-Source Security

The core AI pipeline leverages Google's `gemini-3.1-flash-lite` model to process raw audio inputs and execute complex data extraction into structured formats.

To maintain strict security protocols and prevent accidental credential exposure in version control, the application uses a **dual-source credential setup**. It prioritizes a local configuration file (`vault/keys.toml`), and gracefully falls back to system environment variables during cloud deployment:

```python
# Dual-Source Vault Loader
base_dir = os.path.dirname(os.path.abspath(__file__))
vault_path = os.path.join(base_dir, "vault", "keys.toml")
api_key = None

if os.path.exists(vault_path):
    try:
        secrets = toml.load(vault_path)
        api_key = secrets.get("GEMINI_API_KEY")
        print("Successfully loaded API key from vault.")
    except Exception as e:
        print(f"Error reading vault/keys.toml: {e}")
else:
    print("Vault not found, checking environment variables...")
    api_key = os.environ.get("GEMINI_API_KEY")

💾 Database Schema & Algorithmic Matching Logic
PyroPlanner relies on an embedded SQLite database (pyro_planner.db) generated programmatically via a Pandas dataframe conversion from a centralized inventory spreadsheet.

Inventory Table Constraints:
name (TEXT): The commercial name of the firework.
duration (INTEGER): The total length of the firework in seconds.
pace (TEXT): The firing velocity category (slow, medium, or fast).

Strict Relational Query Rules
To guarantee a professional and tightly synchronized performance, the backend database matching function enforces three strict architectural rules:
Pace Uniformity: The firework's pace must exactly match the analyzed intensity of the music segment.
Duration Tolerance: To prevent overlapping into subsequent musical cues, the firework's duration must be at least equal to the segment length, but no more than 5 seconds longer 
Dynamic Variety: Results matching the criteria are randomized natively in SQL using ORDER BY RANDOM() LIMIT 1 to ensure unique show aesthetics on every execution.

def get_matches_from_db(intensity, segment_duration):
    conn = sqlite3.connect('pyro_planner.db')
    cursor = conn.cursor()
    search_pace = str(intensity).lower().strip()
    target_dur = int(segment_duration)

    query = """
        SELECT name, duration 
        FROM fireworks 
        WHERE LOWER(TRIM(pace)) = ? 
          AND (duration - ?) >= 0 
          AND (duration - ?) <= 5
        ORDER BY RANDOM() 
        LIMIT 1
    """
    cursor.execute(query, (search_pace, target_dur, target_dur))
    return cursor.fetchone()

📄 Document Generation Component (PDF Export Engine)
To comply with Vercel's read-only, stateless serverless environment constraints, the final show layout is generated entirely in-memory using an io.BytesIO binary stream. 
It builds a beautiful, native structural table layout via fpdf2 directly to the client browser without hitting server disk storage.

@app.route("/download-pdf", methods=["POST"])
def download_pdf():
    raw_data = session.get("choreography_results", [])
    
    # Initialize in-memory stream and layout properties
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    
    # Title Section Header
    pdf.set_font("Helvetica", style="B", size=18)
    pdf.cell(0, 12, "Pyro Planner Show Timeline", ln=True, align="C")
    pdf.ln(5)
    
    # Structural Table Header Formatting
    headers = ["Segment", "Timestamp", "Length", "Pace", "Assigned Firework"]
    pdf.set_font("Helvetica", size=10)
    
    # Open native fpdf2 structural table container
    with pdf.table(text_align="CENTER") as table:
        header_row = table.row()
        for head in headers:
            header_row.cell(head)
            
        # Dynamically stream data matrix rows into the table grid
        for item in raw_data:
            row = table.row()
            row.cell(str(item.get("segment", "")))
            row.cell(str(item.get("timestamp", "")))
            row.cell(f"{item.get('duration', 0)}s")
            row.cell(str(item.get('pace', "")).upper())
            row.cell(str(item.get('firework', "")))
            
    # Compile raw binary payload out of RAM
    pdf_output = io.BytesIO()
    pdf_output.write(pdf.output())
    pdf_output.seek(0)
    
    return send_file(
        pdf_output,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="firework_show_plan.pdf"
    )

