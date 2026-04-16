import streamlit as st
import time
import base64
import json
from datetime import datetime
import os
import matplotlib.pyplot as plt
import time

def typewriter(msg, speed=0.02):
    placeholder = st.empty()
    typed = ""

    for char in msg:
        typed += char
        placeholder.markdown(
            f"<div style='background:#f0f2f6;padding:10px;border-radius:10px;margin:5px 0;'>{typed}</div>",
            unsafe_allow_html=True
        )
        time.sleep(speed)
# -------------------------------
# DATA STORAGE FUNCTIONS
# -------------------------------
def load_data():
    if os.path.exists("patient_data.json"):
        with open("patient_data.json", "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open("patient_data.json", "w") as f:
        json.dump(data, f)

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="PerioSathi", layout="centered")

# -------------------------------
# SESSION STATE
# -------------------------------
if "step" not in st.session_state:
    st.session_state.step = "language"

if "language" not in st.session_state:
    st.session_state.language = None

if "profile_done" not in st.session_state:
    st.session_state.profile_done = False

if "greet_done" not in st.session_state:
    st.session_state.greet_done = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "show_video" not in st.session_state:
    st.session_state.show_video = False
# -------------------------------
# LOGO FUNCTION
# -------------------------------
def get_base64(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

def center_logo():
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center;">
            <img src="data:image/png;base64,{get_base64("logo2.png")}" width="250">
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------
# LANGUAGE DATA
# -------------------------------
lang_data = {
    "English": {
        "title": "PerioSathi",
        "tagline": "Predict. Prevent. Protect.",
        "greet": "Hello, I am your PerioSathi. Let's make your profile.",
        "name": "Name",
        "age": "Age",
        "gender": "Gender",
        "male": "Male",
        "female": "Female",
        "other": "Other",
        "start": "Start Assessment",
        "back": "Change Language"
    },
    "Hindi": {
        "title": "PerioSathi",
        "tagline": "पूर्वानुमान. रोकथाम. सुरक्षा.",
        "greet": "नमस्ते, मैं आपका PerioSathi हूँ। आइए आपकी प्रोफ़ाइल बनाते हैं।",
        "name": "नाम",
        "age": "आयु",
        "gender": "लिंग",
        "male": "पुरुष",
        "female": "महिला",
        "other": "अन्य",
        "start": "मूल्यांकन शुरू करें",
        "back": "भाषा बदलें"
    },
    "Marathi": {
        "title": "PerioSathi",
        "tagline": "भविष्यवाणी. प्रतिबंध. संरक्षण.",
        "greet": "नमस्कार, मी तुमचा PerioSathi आहे. चला तुमची प्रोफाइल तयार करूया.",
        "name": "नाव",
        "age": "वय",
        "gender": "लिंग",
        "male": "पुरुष",
        "female": "महिला",
        "other": "इतर",
        "start": "मूल्यांकन सुरू करा",
        "back": "भाषा बदला"
    }
}

# -------------------------------
# STEP 1: LANGUAGE
# -------------------------------
if st.session_state.step == "language":

    center_logo()

    st.markdown("<h1 style='text-align:center;'>PerioSathi</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>Predict. Prevent. Protect.</h4>", unsafe_allow_html=True)

    st.markdown("### 🌐 Select Language/ भाषा चुनें / भाषा निवडा")

    lang = st.selectbox("", ["English", "Hindi", "Marathi"])

    if st.button("Continue"):
        st.session_state.language = lang
        st.session_state.step = "profile"
        st.rerun()
# -------------------------------
# STEP 2: PROFILE
# -------------------------------
elif st.session_state.step == "profile":

    lang = lang_data[st.session_state.language]

    center_logo()

    st.markdown(f"<h1 style='text-align:center;'>{lang['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align:center;'>{lang['tagline']}</h4>", unsafe_allow_html=True)
    # -------------------------------
    # CHAT GREETING
    # -------------------------------
    if not st.session_state.greet_done:

        message = "🙂 " + lang["greet"]
        placeholder = st.empty()
        text_show = ""

        for char in message:
            text_show += char
            placeholder.markdown(
                f"<div style='background:#f0f2f6;padding:10px;border-radius:10px;width:fit-content'>{text_show}</div>",
                unsafe_allow_html=True
            )
            time.sleep(0.02)

        st.session_state.greet_done = True

    else:
        st.markdown(
            f"<div style='background:#f0f2f6;padding:10px;border-radius:10px;width:fit-content'>🙂 {lang['greet']}</div>",
            unsafe_allow_html=True
        )

   # -------------------------------
    # PROFILE INPUT
    # -------------------------------
    name = st.text_input(lang["name"])
    from datetime import date

    min_date = date(1940, 1, 1)
    max_date = date.today()

    if st.session_state.language == "English":
     dob = st.date_input("Date of Birth", min_value=min_date, max_value=max_date)
    elif st.session_state.language == "Hindi":
     dob = st.date_input("जन्म तिथि", min_value=min_date, max_value=max_date)
    else:
     dob = st.date_input("जन्म तारीख", min_value=min_date, max_value=max_date)
    st.session_state.dob = dob

    age = None
    if dob:
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if st.session_state.language == "English":
            st.write(f"Age: {age} years")
        if st.session_state.language == "Hindi":
            st.write(f"आयु: {age} वर्ष")
        elif st.session_state.language == "Marathi":
            st.write(f"वय: {age} वर्ष")

        st.session_state.age = age

    gender = st.selectbox(lang["gender"], [lang["male"], lang["female"], lang["other"]])

    if name and dob:
        if st.button(lang["start"]):
            st.session_state.profile_done = True
            st.session_state.name = name
            st.session_state.age = age
            st.session_state.step = "assessment"
            st.rerun()

    if st.button(lang["back"]):
        st.session_state.step = "language"
        st.rerun()


# -------------------------------
# STEP 3: ASSESSMENT
# -------------------------------
if st.session_state.step == "assessment":

    lang = st.session_state.language
    base = lang_data[lang]

    center_logo()

    st.markdown(f"<h2 style='text-align:center;'>{base['title']}</h2>", unsafe_allow_html=True)

    # -------------------------------
    # ASSESSMENT DATA (YOUR EXACT STRUCTURE)
    # -------------------------------
    assessment_data = {
        "English": {
            "title": "Assessment",
            "calc": "Calculate Score",

            "q1": ("Tobacco Use", ["Never", "Smoking", "Smokeless", "Both"]),
            "q2": ("Diabetes", ["No", "Controlled", "Uncontrolled"]),
            "q3": ("Bleeding Gums", ["Never", "Sometimes", "Frequent"]),
            "q4": ("Gum Swelling", ["No", "Mild", "Severe"]),
            "q5": ("Gum Recession", ["No", "Teeth root slightly visible", "Root visible with hypersensitivity"]),
            "q6": ("Mobility", ["No", "Slight", "Severe"]),
            "q7": ("Brushing", ["Twice", "Once", "Rarely"]),
            "q8": ("Dental Visit", ["Regular", "Problem only", "Never"]),
        },

        "Hindi": {
            "title": "मूल्यांकन",
            "calc": "स्कोर निकालें",

            "q1": ("तंबाकू सेवन", ["कभी नहीं", "धूम्रपान", "तंबाकू", "दोनों"]),
            "q2": ("मधुमेह", ["नहीं", "नियंत्रित", "अनियंत्रित"]),
            "q3": ("मसूड़ों से खून", ["कभी नहीं", "कभी-कभी", "अक्सर"]),
            "q4": ("मसूड़ों की सूजन", ["नहीं", "हल्की", "गंभीर"]),
            "q5": ("मसूड़े नीचे हटना", ["नहीं", "दांतों की जड़ें दिखने लगी हैं", "जड़ दिखती है और झनझनाहट है"]),
            "q6": ("दांत हिलना", ["नहीं", "हल्का", "ज्यादा"]),
            "q7": ("ब्रश", ["दिन में 2 बार", "दिन में 1 बार", "कभी-कभी"]),
            "q8": ("डेंटल विज़िट", ["नियमित", "समस्या होने पर", "कभी नहीं"]),
        },

        "Marathi": {
            "title": "मूल्यांकन",
            "calc": "स्कोर काढा",

            "q1": ("तंबाखू सेवन", ["कधीच नाही", "धूम्रपान", "तंबाखू", "दोन्ही"]),
            "q2": ("मधुमेह", ["नाही", "नियंत्रित", "अनियंत्रित"]),
            "q3": ("हिरड्यांतून रक्त", ["कधीच नाही", "कधी-कधी", "वारंवार"]),
            "q4": ("हिरड्याची सूज", ["नाही", "हलकी", "तीव्र"]),
            "q5": ("हिरड्या खाली जाणे", ["नाही", "दातांची मुळे दिसत आहेत", "मुळ दिसते आणि झणझणाट होते"]),
            "q6": ("दात हलणे", ["नाही", "हलके", "जास्त"]),
            "q7": ("ब्रश", ["दिवसातून 2 वेळा", "दिवसातून 1 वेळ", "कधी-कधी"]),
            "q8": ("डेंटल भेट", ["नियमित", "समस्या आल्यावर", "कधीच नाही"]),
        }
    }

    data = assessment_data[lang]

    # -------------------------------
    # QUESTIONS UI
    # -------------------------------
    st.markdown(f"### 📝 {data['title']}")

    answers = {}

    for i in range(1, 9):
        q, options = data[f"q{i}"]
        answers[f"q{i}"] = st.selectbox(q, options, key=f"q{i}")

    # -------------------------------
    # CALCULATE BUTTON (NEXT STEP)
    # -------------------------------
    if st.button(data["calc"]):
        st.session_state.answers = answers
        st.session_state.step = "result"
        st.rerun()
    
    # -------------------------------
    # DATA STORAGE FUNCTIONS
    # -------------------------------
    def load_data():
      if os.path.exists("patient_data.json"):
        with open("patient_data.json", "r") as f:
            return json.load(f)
      return {}

    def save_data(data):
      with open("patient_data.json", "w") as f:
        json.dump(data, f)
# -------------------------------
# STEP 4: RESULT
# -------------------------------
if st.session_state.step == "result":

    if st.session_state.show_video:

    # column 9
        if lang == "English":
            st.markdown("### ▶ Brushing Technique (Modified Bass Method)")
        if lang == "Hindi":
            st.markdown("### ▶ सही ब्रश करने की विधि")
        if lang == "Marathi":
            st.markdown("### ▶ योग्य ब्रश करण्याची पद्धत")

    # column 9
        st.video("https://www.youtube.com/watch?v=VdjmGxq-X7M")
        st.caption("Source: Educational video (YouTube)")

    # column 9
        if st.button("⬅ Back"):
           st.session_state.show_video = False
           st.rerun()

        st.stop()

    lang = st.session_state.language
    base = lang_data[lang]

    center_logo()

    # Get stored answers
    answers = st.session_state.answers
 # -------------------------------
    # RELOAD SAME ASSESSMENT DATA
    # -------------------------------
    assessment_data = {
        "English": {
            "low": "Low Risk",
            "mod": "Moderate Risk",
            "high": "High Risk",
            "q1": ["Never", "Smoking", "Smokeless", "Both"],
            "q2": ["No", "Controlled", "Uncontrolled"],
            "q3": ["Never", "Sometimes", "Frequent"],
            "q4": ["No", "Mild", "Severe"],
            "q5": ["No", "Teeth root slightly visible", "Root visible with hypersensitivity"],
            "q6": ["No", "Slight", "Severe"],
            "q7": ["Twice", "Once", "Rarely"],
            "q8": ["Regular", "Problem only", "Never"],
        },

        "Hindi": {
            "low": "कम जोखिम",
            "mod": "मध्यम जोखिम",
            "high": "उच्च जोखिम",
            "q1": ["कभी नहीं", "धूम्रपान", "तंबाकू", "दोनों"],
            "q2": ["नहीं", "नियंत्रित", "अनियंत्रित"],
            "q3": ["कभी नहीं", "कभी-कभी", "अक्सर"],
            "q4": ["नहीं", "हल्की", "गंभीर"],
            "q5": ["नहीं", "दांतों की जड़ें दिखने लगी हैं", "जड़ दिखती है और झनझनाहट है"],
            "q6": ["नहीं", "हल्का", "ज्यादा"],
            "q7": ["दिन में 2 बार", "दिन में 1 बार", "कभी-कभी"],
            "q8": ["नियमित", "समस्या होने पर", "कभी नहीं"],
        },

        "Marathi": {
            "low": "कमी जोखीम",
            "mod": "मध्यम जोखीम",
            "high": "जास्त जोखीम",
            "q1": ["कधीच नाही", "धूम्रपान", "तंबाखू", "दोन्ही"],
            "q2": ["नाही", "नियंत्रित", "अनियंत्रित"],
            "q3": ["कधीच नाही", "कधी-कधी", "वारंवार"],
            "q4": ["नाही", "हलकी", "तीव्र"],
            "q5": ["नाही", "दातांची मुळे दिसत आहेत", "मुळ दिसते आणि झणझणाट होते"],
            "q6": ["नाही", "हलके", "जास्त"],
            "q7": ["दिवसातून 2 वेळा", "दिवसातून 1 वेळ", "कधी-कधी"],
            "q8": ["नियमित", "समस्या आल्यावर", "कधीच नाही"],
        }
    }

    data = assessment_data[lang]
# -------------------------------
    # SCORE CALCULATION (YOUR WEIGHTS)
    # -------------------------------
    score = 0
    score += data["q1"].index(answers["q1"]) * 3
    score += data["q2"].index(answers["q2"]) * 3
    score += data["q3"].index(answers["q3"]) * 2
    score += data["q4"].index(answers["q4"]) * 2
    score += data["q5"].index(answers["q5"]) * 2
    score += data["q6"].index(answers["q6"]) * 2
    score += data["q7"].index(answers["q7"]) * 1
    score += data["q8"].index(answers["q8"]) * 1

    percent = (score / 35) * 100

    # -------------------------------
    # RISK CLASSIFICATION
    # -------------------------------
    if percent >= 66:
     color = "red"
     risk = data["high"]

    if percent >= 33:
     color = "orange"
     risk = data["mod"]

    else:
     color = "green"
     risk = data["low"]

    typewriter("🧠 Based on your responses, your periodontal risk is:")
    time.sleep(0.02)

    st.markdown(
    f"<h2 style='color:{color};'>Risk Score: {score}/35</h2>",
    unsafe_allow_html=True
    )

    st.markdown(
    f"<h3 style='color:{color};'>Risk Percentage: {percent:.1f}%</h3>",
    unsafe_allow_html=True
    )

    st.markdown(
    f"<h3 style='color:{color};'>Risk Level: {risk}</h3>",
    unsafe_allow_html=True
    )

    # -------------------------------
    # GRAPH
    # -------------------------------
    st.markdown("### 📊 Current Risk")
    st.progress(int(percent))

    # -------------------------------
    # SAVE + COMPARE
    # -------------------------------
    data_store = load_data()

    name = st.session_state.name
    age = st.session_state.age
    pid = f"{name}_{age}"

    previous_score = None
    if pid in data_store:
        previous_score = data_store[pid]["score"]

    data_store[pid] = {
        "score": score,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    save_data(data_store)
    # -------------------------------
    # COMPARISON GRAPH
    # -------------------------------
    if previous_score is not None:

        st.markdown("### 📈 Progress Comparison")

        fig, ax = plt.subplots()
        ax.bar(["Previous", "Current"], [previous_score, score])
        ax.set_ylim(0, 35)

        st.pyplot(fig)

        if score < previous_score:
            st.success("Improved")
        if score > previous_score:
            st.error("Worsened")
        else:
            st.info("No change")
# -------------------------------
# EXPLANATION HEADER
# -------------------------------
    if lang == "English":
        st.markdown("### 💬 Explanation")
    if lang == "Hindi":
        st.markdown("### 💬 व्याख्या")
    if lang == "marathi":
        st.markdown("### 💬 स्पष्टीकरण")
 
    recommendations = []
    periodontist_flag = False
# -------------------------------
# TOBACCO
# -------------------------------
    ans = answers.get("q1")
# SMOKING
    if ans in ["Smoking", "धूम्रपान", "धूम्रपान"]:

        if lang == "English":
            typewriter("• You are a smoker. Smoking increases risk of lung disease and worsens gum health.")
            recommendations.append("Reduce smoking and aim to quit completely.")

        if lang == "Hindi":
            typewriter("• आप धूम्रपान करते हैं। इससे फेफड़ों और मसूड़ों पर बुरा प्रभाव पड़ता है।")
            recommendations.append("धूम्रपान कम करते-करते पूरी तरह छोड़ें।")

        if lang == "Marathi":
            typewriter("• तुम्ही धूम्रपान करता. यामुळे फुफ्फुस आणि हिरड्यांवर परिणाम होतो.")
            recommendations.append("धूम्रपान कमी करत करत पूर्णपणे सोडा.")

# SMOKELESS TOBACCO
    if ans in ["Smokeless", "तंबाकू", "तंबाखू"]:

        if lang == "English":
            typewriter("• You use tobacco. It can cause oral cancer and gum disease.")
            recommendations.append("Reduce usage and quit completely.")

        if lang == "Hindi":
            typewriter("• आप तंबाकू का उपयोग करते हैं। इससे मुंह का कैंसर और मसूड़ों की बीमारी हो सकती है।")
            recommendations.append("तंबाकू कम करते-करते पूरी तरह छोड़ें।")

        if lang == "Marathi":
            typewriter("• तुम्ही तंबाखू वापरता. यामुळे कर्करोग आणि हिरड्यांचे आजार होऊ शकतात.")
            recommendations.append("तंबाखू कमी करून सोडा.")


# BOTH
    if ans in ["Both", "दोनों", "दोन्ही"]:

        if lang == "English":
            typewriter("• You use both smoking and tobacco. Risk is very high.")
            recommendations.append("Reduce both and quit completely.")

        if lang == "Hindi":
            typewriter("• आप धूम्रपान और तंबाकू दोनों का उपयोग करते हैं। जोखिम बहुत अधिक है।")
            recommendations.append("दोनों को कम करें और छोड़ दें।")

        if lang == "Marathi":
            typewriter("• तुम्ही दोन्ही वापरता. धोका खूप जास्त आहे.")
            recommendations.append("दोन्ही कमी करून बंद करा.")




# -------------------------------
# DIABETES
# -------------------------------
    ans = answers.get("q2")
# NO DIABETES
    if ans in ["No", "नहीं", "नाही"]:
        age = st.session_state.age
        
        if age >= 40:
            if lang == "English":
                typewriter("• You are above 40 years of age. It is recommended to undergo regular diabetes screening.")
                recommendations.append("Go for regular diabetes screening.")

            if lang == "Hindi":
                typewriter("• आप 40 वर्ष से अधिक आयु के हैं। नियमित मधुमेह जांच करवाने की सलाह दी जाती है।")
                recommendations.append("नियमित मधुमेह जांच करवाएं।")

            if lang == "Marathi":
                typewriter("• तुमचे वय 40 वर्षांपेक्षा जास्त आहे. नियमित मधुमेह तपासणी करा.")
                recommendations.append("नियमित मधुमेह तपासणी करा.")
        if age < 40:
            if lang == "English":
                typewriter("• It is advisable to undergo diabetes screening after 40 years of age.")
                recommendations.append("Go for diabetes screening after 40 years.")

            if lang == "Hindi":
                typewriter("• 40 वर्ष की आयु के बाद मधुमेह जांच करवाना उचित है।")
                recommendations.append("40 वर्ष के बाद मधुमेह जांच करवाएं।")

            if lang == "Marathi":
                typewriter("• 40 वर्षांनंतर मधुमेह तपासणी करणे योग्य आहे.")
                recommendations.append("40 वर्षांनंतर मधुमेह तपासणी करा.")

# CONTROLLED
    if ans in ["Controlled", "नियंत्रित", "नियंत्रित"]:

        if lang == "English":
            typewriter("• Diabetes is controlled. Maintain follow-up.")
            recommendations.append("Continue medication and regular check-up.")

        if lang == "Hindi":
            typewriter("• आपका मधुमेह नियंत्रित है। नियमित जांच जारी रखें।")
            recommendations.append("दवा और जांच जारी रखें।")

        if lang == "Marathi":
            typewriter("• मधुमेह नियंत्रित आहे. नियमित तपासणी करा.")
            recommendations.append("औषधे आणि तपासणी सुरू ठेवा.")


# UNCONTROLLED
    if ans in ["Uncontrolled", "अनियंत्रित", "अनियंत्रित"]:

        if lang == "English":
            typewriter("• Uncontrolled diabetes leads to delayed healing and bone loss.")
            recommendations.append("Follow medical advice strictly.")

        if lang == "Hindi":
            typewriter("• अनियंत्रित मधुमेह से घाव भरने में देरी और हड्डी का नुकसान होता है।")
            recommendations.append("डॉक्टर की सलाह का पालन करें।")

        if lang == "Marathi":
            typewriter("• अनियंत्रित मधुमेहामुळे जखम भरायला उशीर होतो.")
            recommendations.append("डॉक्टरांचा सल्ला पाळा.")
# -------------------------------
# BLEEDING
# -------------------------------
    ans = answers.get("q3")

# NEVER (NORMAL → NO OUTPUT)
    if ans in ["Never", "कभी नहीं", "कधीच नाही"]:
            pass

# SOMETIMES (EARLY SIGN)
    if ans in ["Sometimes", "कभी-कभी", "कधी-कधी"]:

        if lang == "English":
            typewriter("• Occasional bleeding indicates early gum inflammation.")

        if lang == "Hindi":
            typewriter("• कभी-कभी खून आना मसूड़ों की शुरुआती समस्या का संकेत है।")

        if lang == "Marathi":
            typewriter("• कधी-कधी रक्त येणे सुरुवातीची समस्या दर्शवते.")


# FREQUENT (ACTIVE DISEASE)
    if ans in ["Frequent", "अक्सर", "वारंवार"]:

        if lang == "English":
            typewriter("• Frequent bleeding indicates active gum disease.")

        if lang == "Hindi":
            typewriter("• बार-बार खून आना मसूड़ों की बीमारी का संकेत है।")

        if lang == "Marathi":
            typewriter("• वारंवार रक्त येणे हे हिरड्यांच्या आजाराचे लक्षण आहे.")

            periodontist_flag = True


# -------------------------------
# SWELLING
# -------------------------------
    ans = answers.get("q4")

# NO GUM SWELLING (NORMAL)
    if ans in ["No", "नहीं", "नाही"]:
            pass

# MILD GUM SWELLING
    if ans in ["Mild", "हल्की", "हलकी"]:

        if lang == "English":
            typewriter("• Mild swelling may be due to gum inflammation or localized tooth infection.")

        if lang == "Hindi":
            typewriter("• हल्की सूजन मसूड़ों के इन्फेक्शन के शुरुआत का संकेत हो सकती है।")

        if lang == "Marathi":
            typewriter("• हलकी सूज ही हिरड्यांच्या इन्फेक्शनची सुरुवात असू शकते.")


# SEVERE GUM SWELLING
    if ans in ["Severe", "गंभीर", "तीव्र"]:

        if lang == "English":
            typewriter("• Severe swelling indicates gum infection or abscess.")

        if lang == "Hindi":
            typewriter("• गंभीर सूजन मसूड़ों के इन्फेक्शन का संकेत हो सकती है।")

        if lang == "Marathi":
            typewriter("• तीव्र सूज ही हिरड्यांच्या इन्फेक्शनचे लक्षण असू शकते.")

            periodontist_flag = True
# -------------------------------
# RECESSION
# -------------------------------
    ans = answers.get("q5")

# NO GUM RECESSION (NORMAL)
    if ans in ["No", "नहीं", "नाही"]:
            pass

# TEETH ROOT APPEAR LONGER (MODERATE)
    if ans in ["Teeth root slightly visible", "दांतों की जड़ें दिखने लगी हैं", "दातांची मुळे दिसत आहेत"]:

        if lang == "English":
            typewriter("• Gum recession is present. It may lead to sensitivity and future mobility.")

        if lang == "Hindi":
            typewriter("• मसूड़े नीचे हट रहे हैं, आगे चलकर दांत हिलने की संभावना बढ़ सकती है।")

        if lang == "Marathi":
            typewriter("• हिरड्या खाली जात आहेत, पुढे दात हलू शकतात.")

            periodontist_flag = True


# ROOT VISIBLE (SEVERE)
    if ans in ["Root visible with hypersensitivity", "जड़ दिखती है और झनझनाहट है", "मुळ दिसते आणि झणझणाट होते"]:

        if lang == "English":
            typewriter("• Advanced gum recession with possible bone loss.")

        if lang == "Hindi":
            typewriter("• जड़ दिखना गंभीर समस्या का संकेत है।")

        if lang == "Marathi":
            typewriter("• मुळ दिसणे ही गंभीर समस्या आहे.")

            periodontist_flag = True

# -------------------------------
# MOBILITY
# -------------------------------

    ans = answers.get("q6")

# NO MOBILITY (NORMAL)
    if ans in ["No", "नहीं", "नाही"]:
            pass

# SLIGHT MOBILITY
    if ans in ["Slight", "हल्का", "हलके"]:

        if lang == "English":
            typewriter("• Slight tooth mobility indicates weakening of supporting structures.")

        if lang == "Hindi":
            typewriter("• दांत का हल्का हिलना मसूड़ों और हड्डी के कमजोर होने का संकेत है।")

        if lang == "Marathi":
            typewriter("• दात हलके हलत आहेत म्हणजे आधार कमी होत आहे.")

            periodontist_flag = True


# SEVERE MOBILITY
    if ans in ["Severe", "ज्यादा", "जास्त"]:

        if lang == "English":
            typewriter("• Severe tooth mobility indicates a serious condition and risk of tooth loss.")

        if lang == "Hindi":
            typewriter("• दांत का अधिक हिलना एक गंभीर समस्या है और आगे चलकर दांत गिर सकते हैं।")

        if lang == "Marathi":
            typewriter("• दात जास्त हलत आहेत म्हणजे गंभीर स्थिती आहे, पुढे दात पडण्याची शक्यता असते.")

            periodontist_flag = True
# -------------------------------
# BRUSHING
# -------------------------------
    ans = answers.get("q7")

# TWICE (GOOD)
    if ans in ["Twice", "दिन में 2 बार", "दिवसातून 2 वेळा"]:

        if lang == "English":
            typewriter("• Good brushing practice.")
        if lang == "Hindi":
           typewriter("• आप अच्छी तरह से ब्रश करते हैं।")
        if lang == "Marathi":
           typewriter("• तुम्ही योग्य प्रकारे ब्रश करता.")

# ONCE (MODERATE ISSUE)
    if ans in ["Once", "दिन में 1 बार", "दिवसातून 1 वेळ"]:

        if lang == "English":
            typewriter("• Brushing once daily is not adequate.")
            recommendations.append("Brush twice daily using proper technique.")
        if lang == "Hindi":
            typewriter("• दिन में एक बार ब्रश करना पर्याप्त नहीं है।")
            recommendations.append("दिन में दो बार ब्रश करें।")
        if lang == "Marathi":
            typewriter("• दिवसातून एकदाच ब्रश करणे पुरेसे नाही.")
            recommendations.append("दिवसातून दोन वेळा ब्रश करा.")

# NEVER / FINGER (SEVERE ISSUE)
    if ans in ["Rarely", "कभी-कभी", "कधी-कधी"]:

        if lang == "English":
            typewriter("• This is not a proper brushing practice.")
            recommendations.append("Start brushing twice daily with a toothbrush.")
        if lang == "Hindi":
          typewriter("• यह सही ब्रश करने की आदत नहीं है।")
          recommendations.append("टूथब्रश से दिन में दो बार ब्रश करना शुरू करें।")
        if lang == "Marathi":
            typewriter("• ही योग्य ब्रश करण्याची पद्धत नाही.")
            recommendations.append("टूथब्रशने दिवसातून दोन वेळा ब्रश करायला सुरुवात करा.")
    
        if lang == "English":
            if st.button("▶ Learn Proper Brushing Technique"):
               st.session_state.show_video = True
               st.rerun()

        if lang == "Hindi":
            if st.button("▶ सही ब्रश करने की विधि देखें"):
               st.session_state.show_video = True
               st.rerun()

        if lang == "Marathi":
         if st.button("▶ योग्य ब्रश करण्याची पद्धत पहा"):
          st.session_state.show_video = True
          st.rerun()
         
# -------------------------------
# VISIT
# -------------------------------
    ans = answers.get("q8")

# REGULAR
    if ans in ["Regular", "नियमित", "नियमित"]:

        if lang == "English":
            typewriter("• Good, you are on the right path with regular dental visits.")
        if lang == "Hindi":
            typewriter("• अच्छा है, आप सही दिशा में हैं और नियमित जांच कराते हैं।")
        if lang == "Marathi":
            typewriter("• छान, तुम्ही योग्य मार्गावर आहात आणि नियमित तपासणी करता.")

# WHEN NEEDED
    if ans in ["Problem only", "समस्या होने पर", "समस्या आल्यावर"]:

        if lang == "English":
            typewriter("• Visiting dentist only when needed is not ideal.")
            recommendations.append("Go for regular dental check-ups.")
        if lang == "Hindi":
            typewriter("• केवल समस्या होने पर डॉक्टर के पास जाना सही नहीं है।")
            recommendations.append("नियमित जांच करवाएं।")
        if lang == "Marathi":
            typewriter("• फक्त गरज पडल्यावर डॉक्टरांकडे जाणे योग्य नाही.")
            recommendations.append("नियमित तपासणी करा.")

# NEVER
    if ans in ["Never", "कभी नहीं", "कधीच नाही"]:

        if lang == "English":
            typewriter("• Not visiting a dentist can lead to serious dental problems.")
            recommendations.append("You should visit a dentist regularly.")
        if lang == "Hindi":
            typewriter("• कभी भी डॉक्टर के पास न जाना गंभीर समस्या पैदा कर सकता है।")
            recommendations.append("आपको नियमित रूप से डॉक्टर के पास जाना चाहिए।")
        if lang == "Marathi":
            typewriter("• कधीच डॉक्टरांकडे न जाणे गंभीर समस्या निर्माण करू शकते.")
            recommendations.append("तुम्ही नियमितपणे डॉक्टरांकडे जावे.")
# -------------------------------
# RECOMMENDATIONS
# -------------------------------
    if lang == "English":
        st.markdown("### 🦷 Recommendations")
    if lang == "Hindi":
        st.markdown("### 🦷 सुझाव")
    if lang == "Marathi":
        st.markdown("### 🦷 सल्ला")

    for rec in set(recommendations):
        st.write("•", rec)

    if periodontist_flag:
        if lang == "English":
            st.write("• Consult a periodontist.")
        if lang == "Hindi":
            st.write("• पीरियोडॉन्टिस्ट से परामर्श करें।")
        if lang == "Marathi":
            st.write("• हिरड्यांच्या तज्ज्ञांना भेटा.")

# -------------------------------
# REMINDER
# -------------------------------
    if lang == "English":
        st.info("⏰ Please reassess after 1 month.") 
    if lang == "Hindi":
        st.info("⏰ कृपया 1 महीने बाद पुनः जांच करें।")
    if lang == "Marathi":
        st.info("⏰ कृपया 1 महिन्यानंतर पुन्हा तपासा.")

# -------------------------------
# DISCLAIMER
# -------------------------------
    st.markdown("---")

    if lang == "English":
        st.caption("⚠️ This is for educational purposes only. It does not replace a dentist.")
    if lang == "Hindi":
        st.caption("⚠️ यह केवल जानकारी के लिए है, डॉक्टर का विकल्प नहीं है।")
    if lang == "Marathi":
        st.caption("⚠️ हे फक्त माहिती साठी आहे, डॉक्टरांचा पर्याय नाही.")
# -------------------------------
# RESET / NEW PATIENT
# -------------------------------
    
    # -------------------------------
# NEW PATIENT BUTTON
# -------------------------------
    if st.button("➕ New Patient"):

    # reset step FIRST
     st.session_state.step = "language"

    # clear patient-specific data
     st.session_state.name = ""
     st.session_state.age = ""
     st.session_state.dob = None
     st.session_state.answers = {}

    # reset greeting animation (IMPORTANT)
     st.session_state.greet_done = False

     st.rerun()
        
