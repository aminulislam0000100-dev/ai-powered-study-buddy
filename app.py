import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import datetime

# --- INITIALIZATION ---
load_dotenv()
# Using st.secrets for deployment or local .env for development
GOOGLE_API_KEY = st.secrets.get("GEMINI_API_KEY", os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="AI Study Buddy + Wellness", page_icon="🎓", layout="wide")

# --- SHARED BRAIN ---
def get_ai_response(prompt, image_data=None):
    # Using the ultra-fast lite model for daily quota efficiency
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    content = [prompt]
    if image_data:
        content.append(image_data[0])
    try:
        response = model.generate_content(content)
        return response.text
    except Exception as e:
        return f"🚨 System Note: {str(e)}"

# --- MAIN LAYOUT ---
st.title("🎓 AI Study Buddy: Holistic Edition")
st.markdown("---")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💡 Concept Explainer", 
    "📅 Study Planner", 
    "📝 Quiz Generator",
    "🏃 Vitality Tracker", 
    "🧠 Mindset Check-in"
])

with tab1:
    st.subheader("💡 Concept Explainer")
    st.write("Upload a file or type a specific question below to get a professional explanation.")

    # 1. File Uploader
    allowed_formats = ["pdf", "jpg", "jpeg", "png"]
    uploaded_file = st.file_uploader(
        "Upload lecture notes or textbook pages", 
        type=allowed_formats,
        help="Supported: PDF, JPG, PNG"
    )

    # 2. NEW: External Question Box (Text Area for longer queries)
    external_question = st.text_area(
        "Enter your question here:", 
        placeholder="e.g., 'What are the three laws of thermodynamics?' or 'Summarize the attached PDF.'",
        height=150
    )

    # 3. Process Button
    if st.button("Start Explanation"):
        # Check if we have at least one input
        if not uploaded_file and not external_question.strip():
            st.warning("⚠️ Please provide a file or type a question.")
        else:
            try:
                with st.spinner("⏳ Analyzing and drafting your explanation..."):
                    img_data = None
                    
                    # Handle File Input if exists
                    if uploaded_file:
                        img_data = [{
                            "mime_type": uploaded_file.type, 
                            "data": uploaded_file.getvalue()
                        }]

                    # Teacher Prompt Construction
                    # We combine both the file context and the external question
                    prompt = f"""
                    Role: Professional Teacher
                    Context: The student has provided a question or material to explain.
                    Student Question: {external_question}
                    
                    Instructions: 
                    - If a file is provided, use it as the primary source.
                    - If only a question is provided, explain the concept from your knowledge base.
                    - Summarize the core concept clearly.
                    - Use bullet points for key terms.
                    - Provide a real-world analogy.
                    """
                    
                    response = get_ai_response(prompt, img_data)

                    # 4. Display Output
                    st.markdown("---")
                    st.success("Explanation Generated!")
                    st.markdown("### 👨‍🏫 Teacher's Breakdown")
                    
                    # Output the result in a clean box
                    st.info(response) 
                    
            except Exception as e:
                st.error(f"🧐 I encountered an issue while reading that file: {e}")
# --- TAB 2 & 3: PLACEHOLDERS ---
with tab2:
    
    st.info("Input your exam dates in the sidebar or here to generate a custom plan.")
    
    st.subheader("📅 Strategic Study Planner")
    
    # --- TOP ROW: DATE SELECTION ---
    date_col1, date_col2 = st.columns(2)
    with date_col1:
        exam_date_cal = st.date_input("Exam Date (Calendar)", datetime.date.today())
    with date_col2:
        exam_date_text = st.text_input("Confirm Date (YYYY-MM-DD)", value=str(exam_date_cal))

    st.markdown("---")

    # --- MAIN ROW: CATEGORY (LEFT) & SUB-OPTIONS (RIGHT) ---
    # We use a [1, 3] ratio: Category is 25% width, Options are 75% width
    col1, col2 = st.columns([1, 3])

    with col1:
        st.write("**Step 1: Category**")
        exam_category = st.radio( "Select Exam Category",["Board Exam", "Entrance Exam", "Competitive Exam"],
            label_visibility="collapsed" # Hides the label to save more space
        )

    with col2:
        st.write("**Step 2: Specific Details**")
        
        # --- SUB-OPTIONS LOGIC ---
        if exam_category == "Board Exam":
            sub_col1, sub_col2, = st.columns(2)
            with sub_col1:
                Category = st.selectbox("Select Category", ["Select Education Level","Higher Secondary Level", "Graduation Level"])
                if Category == "Higher Secondary Level":
                  with sub_col2:
                    stream = st.selectbox("Stream", ["Arts", "Commerce", "Science"])
                else:
                   # Category == (Graduation level)
            #with sub_col2:
                  with sub_col2:
                   degree_level = st.selectbox("Degree Level", ["Bachelor Degree", "Master Degree"])
                   if degree_level == "Bachelor Degree":
                            degree_type = st.selectbox("Course", ["Select Bachelor Degree Type","B.A.", "B.Sc.", "B.Com.", "B.C.A.", "B.Tech.", "B.E."])
                   else:
                           degree_type = st.selectbox("Course", ["Select Master Degree Type","M.A.", "M.Sc.", "M.Com.", "M.C.A.", "M.Tech."])

        elif exam_category == "Entrance Exam":
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                level = st.selectbox("Level", ["UG", "PG"])
            with sub_col2:
                if level == "UG":
                    exam_name = st.selectbox("Entrance", ["CUET UG", "JEE Main", "JEE Advanced", "NEET", "BITSAT", "CLAT", "Other"])
                else:
                    exam_name = st.selectbox("Entrance", ["CUET PG", "NIMCET", "GATE", "CAT", "JAM", "Other"])

        elif exam_category == "Competitive Exam":
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                qualification = st.selectbox("Qualification", ["Non-Graduate", "Graduate"])
            with sub_col2:
                if qualification == "Non-Graduate":
                    exam_name = st.selectbox("Popular Exams", ["SSC GD", "SSC MTS", "SSC CHSL", "State Police", "Indian Army", "Indian Navy", "Indian Airforce"])
                else:
                    exam_name = st.selectbox("Popular Exams", ["UPSC (IAS/IPS)", "State PCS", "SSC CGL", "SSC CPO", "CDS", "IBPS PO", "SBI PO"])

    # --- ACTION BUTTON ---
    st.markdown("---")
    if st.button("🚀 Generate AI Study Roadmap", use_container_width=True):
        with st.spinner("Calculating optimal study hours..."):
            # Collecting dynamic variables
            details = f"{locals().get('degree_type', '')} {locals().get('exam_name', '')} {locals().get('stream', '')}"
            planner_prompt = f"Student preparing for {exam_category} ({details}) on {exam_date_text}. Create a high-efficiency roadmap."
            
            st.markdown("### 🗺️ Your Personalized Roadmap")
            st.markdown(get_ai_response(planner_prompt))
with tab3:
    st.subheader("📝 Practice Quiz Generator")
    
    # --- 1. QUIZ SETTINGS AREA ---
    st.write("### ⚙️ Quiz Configuration")
    q_col1, q_col2 = st.columns([1, 1])
    
    with q_col1:
        # File uploader inside the tab
        quiz_file = st.file_uploader(
            "Upload Study Material (PDF/Image)", 
            type=["pdf", "jpg", "jpeg", "png"],
            key="quiz_file_uploader"
        )
    
    with q_col2:
        # Topic text input
        quiz_topic = st.text_input("OR Enter a Topic:", placeholder="e.g. Ancient Rome, Python Loops...")
        # Difficulty selection
        difficulty = st.select_slider("Select Difficulty", options=["Easy", "Medium", "Hard", "Scholar"])

    # --- 2. SESSION STATE INITIALIZATION ---
    if 'quiz_data' not in st.session_state: st.session_state.quiz_data = []
    if 'quiz_active' not in st.session_state: st.session_state.quiz_active = False
    if 'current_score' not in st.session_state: st.session_state.current_score = 0
    if 'question_index' not in st.session_state: st.session_state.question_index = 0
    if 'quiz_finished' not in st.session_state: st.session_state.quiz_finished = False

    # --- 3. GENERATION LOGIC ---
    ctrl_col1, ctrl_col2 = st.columns(2)
    with ctrl_col1:
        if st.button("🚀 Start 10-Question Round", use_container_width=True):
            if not quiz_file and not quiz_topic:
                st.warning("⚠️ Please upload a file or enter a topic first!")
            else:
                with st.spinner("Teacher Gemini is creating your quiz..."):
                    img_context = None
                    if quiz_file:
                        img_context = [{"mime_type": quiz_file.type, "data": quiz_file.getvalue()}]
                    
                    source_desc = "the uploaded file" if quiz_file else f"the topic: {quiz_topic}"
                    
                    # Engineered prompt for consistent Python list output
                    prompt = f"""
                    Generate a 10-question MCQ quiz at {difficulty} difficulty based on {source_desc}.
                    Output format: Return ONLY a Python list of dictionaries like this:
                    [
                      {{"q": "Question text?", "o": ["Opt1", "Opt2", "Opt3", "Opt4"], "a": "Opt1"}},
                      ...
                    ]
                    Do not include markdown code blocks or any other text.
                    """
                    
                    response = get_ai_response(prompt, img_context)
                    try:
                        # Clean the response string if AI adds markdown backticks
                        clean_response = response.replace("```python", "").replace("```", "").strip()
                        st.session_state.quiz_data = eval(clean_response)
                        st.session_state.quiz_active = True
                        st.session_state.question_index = 0
                        st.session_state.current_score = 0
                        st.session_state.quiz_finished = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to parse quiz. Ensure your input is clear. Error: {e}")

    with ctrl_col2:
        if st.button("🏁 Finish Round", use_container_width=True):
            st.session_state.quiz_finished = True
            st.session_state.quiz_active = False

    st.markdown("---")

    # --- 4. THE QUIZ INTERFACE ---
    if st.session_state.quiz_active and st.session_state.question_index < len(st.session_state.quiz_data):
        idx = st.session_state.question_index
        item = st.session_state.quiz_data[idx]

        st.markdown(f"**Question {idx + 1} of 10**")
        st.write(f"### {item['q']}")
        
        # User selection
        user_choice = st.radio("Choose the correct answer:", item['o'], key=f"active_q_{idx}")

        if st.button("✅ Validate Answer"):
            if user_choice == item['a']:
                st.session_state.current_score += 2
                st.success(f"Correct! +2 points. Total: {st.session_state.current_score}")
            else:
                st.session_state.current_score -= 1
                st.error(f"Incorrect. The right answer was: {item['a']}. -1 point.")
            
            # Logic to advance
            if idx < 9:
                st.session_state.question_index += 1
                st.rerun()
            else:
                st.session_state.quiz_finished = True
                st.session_state.quiz_active = False
                st.rerun()

    # --- 5. RESULTS ---
    if st.session_state.quiz_finished:
        st.balloons()
        st.header("🏆 Final Performance Report")
        final_score = st.session_state.current_score
        st.metric("Total Score", f"{final_score} / 20")
        
        # Performance Feedback Logic
        if final_score >= 18: st.write("🔥 **Unstoppable!** You've mastered this topic.")
        elif final_score >= 12: st.write("👍 **Solid Knowledge.** Review the wrong answers to improve.")
        else: st.write("📖 **More Revision Needed.** Try the Concept Explainer for help.")
        
        if st.button("🔄 Restart Quiz"):
            st.session_state.quiz_data = []
            st.session_state.quiz_finished = False
            st.rerun()
# --- TAB 4: VITALITY TRACKER ---
with tab4:
    st.subheader("🔋 Vitality & Energy Lab")
    st.write("Academic performance is fueled by your body. Track your 'vitals' to optimize focus.")
    
    col1, col2 = st.columns(2)
    with col1:
        sleep = st.slider("Hours of sleep last night", 0, 12, 7)
        water = st.number_input("Water intake (Liters)", 0.0, 5.0, 1.5)
        activity = st.selectbox("Physical Activity", ["None", "Short Walk", "Gym/Sport", "Yoga/Stretching"])
    
    with col2:
        symptoms = st.multiselect("Any physical hurdles?", ["Headache", "Eye Strain", "Back Pain", "Fatigue", "None"])
        energy_level = st.select_slider("Current Physical Energy", options=["Drained", "Low", "Balanced", "High", "Peak"])

    if st.button("Analyze Vitality"):
        with st.spinner("Calculating biological readiness..."):
            prompt = f"Act as a Student Health Coach. Analyze: Sleep {sleep}h, Water {water}L, Activity {activity}, Hurdles {symptoms}. Readiness for intense study?"
            st.success(get_ai_response(prompt))

# --- TAB 5: MINDSET CHECK-IN ---
with tab5:
    st.subheader("🧘 Mindset & Resilience")
    st.write("Your mental state determines your retention.")
    
    mood = st.select_slider("Current mood?", options=["Overwhelmed", "Anxious", "Neutral", "Motivated", "Calm"])
    journal_entry = st.text_area("What's on your mind?", placeholder="I'm worried about...")
    
    if st.button("Seek Perspective"):
        if journal_entry:
            with st.spinner("Analyzing mindset..."):
                prompt = f"Act as a supportive Counselor. Student feels {mood} and says: '{journal_entry}'. Provide a cognitive reframe and 2 micro-habits."
                st.chat_message("assistant").write(get_ai_response(prompt))
        else:
            st.warning("Please share your thoughts first.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Profile Summary")
    st.write(f"**Current Mindset:** {mood}")
    # Simple logic for a progress bar based on sleep
    sleep_score = min(sleep / 8, 1.0)
    st.progress(sleep_score, text=f"Sleep Quality: {int(sleep_score*100)}%")