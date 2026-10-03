import streamlit as st
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Vedic Astrology & Numerology Engine",
    page_icon="🔮",
    layout="wide"
)

# ---------------------------------------------------------
# Master Databases & Mapping Dictionaries
# ---------------------------------------------------------
CHALDEAN_MAP = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'U': 6, 'V': 6, 'W': 6,
    'O': 7, 'Z': 7,
    'F': 8, 'P': 8
}

PLANET_INFO = {
    1: {
        "planet": "सूर्य (Sun)",
        "traits": "नेतृत्व, स्वाभिमान, ऊर्जा, स्वतंत्रता, ईगो।",
        "health": "सिरदर्द, आंखों की कमजोरी, उच्च रक्तचाप, हृदय संबंधी अड़चनें।",
        "mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः",
        "gem": "माणिक्य (Ruby)",
        "remedy": "तांबे के लोटे से सूर्यदेव को जल दें। गायत्री मंत्र का पाठ करें।"
    },
    2: {
        "planet": "चंद्रमा (Moon)",
        "traits": "भावुकता, कल्पनाशीलता, सौम्यता, चंचल मन, संवेदनशीलता।",
        "health": "मानसिक तनाव, अवसाद/डिप्रेशन, अनिद्रा, सर्दी-जुकाम।",
        "mantra": "ॐ श्रां श्रीं श्रौं सः चंद्रमसे नमः",
        "gem": "मोती (Pearl)",
        "remedy": "सोमवार को शिवलिंग पर कच्चा दूध व जल चढ़ाएं। माता का आशीर्वाद लें।"
    },
    3: {
        "planet": "गुरु (Jupiter)",
        "traits": "ज्ञान, परामर्श, अनुशासन, धर्म, महत्वाकांक्षा।",
        "health": "मोटापा, लीवर विकार, पेट के रोग, अति-विश्वास से हानि।",
        "mantra": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
        "gem": "पुखराज (Yellow Sapphire)",
        "remedy": "गुरुवार को केसर/हल्दी का तिलक लगाएं। चना दाल का दान करें।"
    },
    4: {
        "planet": "राहु (Rahu)",
        "traits": "अचानक बदलाव, लीक से हटकर सोच, संघर्ष, तीव्र बुद्धि।",
        "health": "अचानक धन हानि, मानसिक भ्रम, पाचन संबंधी विकार, कानूनी अड़चनें।",
        "mantra": "ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः",
        "gem": "गोमेद (Hessonite)",
        "remedy": "शनिवार को पक्षियों को बाजरा डालें। कोढ़ी/सफाई कर्मचारी की सेवा करें।"
    },
    5: {
        "planet": "बुध (Mercury)",
        "traits": "बुद्धि, व्यापार, वाणी, चपलता, तर्कशक्ति।",
        "health": "त्वचा रोग, तंत्रिका तंत्र (Nervous System) की कमजोरी, एकाग्रता की कमी।",
        "mantra": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
        "gem": "पन्ना (Emerald)",
        "remedy": "बुधवार को गाय को हरी घास खिलाएं। तुलसी जी में जल अर्पण करें।"
    },
    6: {
        "planet": "शुक्र (Venus)",
        "traits": "लक्जरी, कला, सौंदर्य, सुख-सुविधाएं, प्रेम।",
        "health": "डायबिटीज, किडनी विकार, अत्यधिक विलासिता से हानि।",
        "mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
        "gem": "हीरा (Diamond) / ओपल",
        "remedy": "शुक्रवार को सफेद मिठाई या चावल का दान करें। सुगंधित इत्र का प्रयोग करें।"
    },
    7: {
        "planet": "केतु (Ketu)",
        "traits": "आध्यात्मिकता, शोध, विश्लेषणात्मक सोच, रहस्य, अकेलापन।",
        "health": "त्वचा इंफेक्शन, जोड़ों/पैरों में दर्द, अलगाववाद, धोखा मिलना।",
        "mantra": "ॐ स्रां स्रीं स्रौं सः केतवे नमः",
        "gem": "लहसुनिया (Cat's Eye)",
        "remedy": "चितकबरे कुत्ते को रोटी खिलाएं। गणेश अथर्वशीर्ष का पाठ करें।"
    },
    8: {
        "planet": "शनि (Saturn)",
        "traits": "कड़ी मेहनत, न्याय, ढिलाई/विलंब, संघर्ष, दीर्घकालिक सफलता।",
        "health": "वातरोग, हड्डियों व जोड़ों में दर्द, आलस्य, कार्यों में देरी।",
        "mantra": "ॐ प्रां प्रीं प्रौं सः शनैश्र्चराय नमः",
        "gem": "नीलम (Blue Sapphire)",
        "remedy": "शनिवार को सरसों के तेल का दीपक जलाएं। गरीबों व असहायों की मदद करें।"
    },
    9: {
        "planet": "मंगल (Mars)",
        "traits": "ऊर्जा, साहस, आक्रामकता, भूमि, भ्रातृ सुख।",
        "health": "रक्त संबंधी विकार, दुर्घटना/चोट, अत्यधिक गुस्सा, विवाद।",
        "mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
        "gem": "मूंगा (Red Coral)",
        "remedy": "मंगलवार को सुंदरकांड या हनुमान चालीसा का पाठ करें। लाल मसूर दान करें।"
    }
}

LOSHU_PLANES = {
    "Mental Plane (4-9-2)": ([4, 9, 2], "तीव्र स्मृति, विश्लेषणात्मक क्षमता और कल्पनाशीलता।"),
    "Emotional Plane (3-5-7)": ([3, 5, 7], "सहानुभूति, आध्यात्मिक झुकाव व मजबूत अंतर्ज्ञान।"),
    "Practical Plane (8-1-6)": ([8, 1, 6], "व्यावहारिक सोच, व्यावसायिक सफलता व संपत्ति लाभ।"),
    "Thought Plane (4-3-8)": ([4, 3, 8], "दूरदर्शिता, दूरगामी योजनाएं व नई सोच।"),
    "Will Power Plane (9-5-1)": ([9, 5, 1], "दृढ़ इच्छाशक्ति, सफलता प्राप्त करने का जुनून।"),
    "Action Plane (2-7-6)": ([2, 7, 6], "तुरंत निर्णय लेना, ऊर्जावान निष्पादन।"),
    "Raj Yoga 1 (4-5-6)": ([4, 5, 6], "अत्यंत शुभ! जीवन में राजयोग, धन-संपत्ति व स्थिरता।"),
    "Raj Yoga 2 (2-5-8)": ([2, 5, 8], "भूमि-भवन सुख, रियल एस्टेट में सफलता व आर्थिक मजबूती।")
}

MISSING_REMEDIES = {
    1: "तांबे की बोतल में जल पिएं। लाल कलावा कलाई में बांधें।",
    2: "पानी की बर्बादी न करें। गले में चांदी की चेन या हाथ में चांदी का कड़ा पहनें।",
    3: "पीला रुमाल जेब में रखें। गुरुजनों एवं बड़ों का नित्य सम्मान करें।",
    4: "हाथ में लकड़ी का ब्रेसलेट (Wooden Beads) पहनें। घर में हरे पौधे लगाएं।",
    5: "हरा एवेंचुरिन (Green Aventurine) क्रिस्टल धारण करें। हरा रंग अपनाएं।",
    6: "हाथ में हमेशा कलाई घड़ी (गोल्डन/सिल्वर) पहनें। साफ-सुथरे वस्त्र धारण करें।",
    7: "सफेद या ग्रे रंग के वस्त्र पहनें। बुजुर्गों की सेवा करें।",
    8: "एमिथिस्ट/ब्लैक टूरमलीन ब्रेसलेट पहनें। समय के पाबंद बनें।",
    9: "लाल रंग का प्रयोग बढ़ाएं। मंगलवार को रक्तदान करें या मंदिर में सेवा करें।"
}

RASHI_NAMES = [
    "मेष (Aries)", "वृषभ (Taurus)", "मिथुन (Gemini)", "कर्क (Cancer)",
    "सिंह (Leo)", "कन्या (Virgo)", "तुला (Libra)", "वृश्चिक (Scorpio)",
    "धनु (Sagittarius)", "मकर (Capricorn)", "कुंभ (Aquarius)", "मीन (Pisces)"
]

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------
def reduce_to_single_digit(n):
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_mulank(day):
    return reduce_to_single_digit(day)

def calculate_bhagyank(dob_date):
    dob_str = dob_date.strftime("%Y%m%d")
    total = sum(int(digit) for digit in dob_str)
    return reduce_to_single_digit(total)

def calculate_namank(name):
    clean_name = name.upper().replace(" ", "")
    total = 0
    for char in clean_name:
        if char in CHALDEAN_MAP:
            total += CHALDEAN_MAP[char]
    return reduce_to_single_digit(total) if total > 0 else 0

def get_loshu_grid(dob_date):
    dob_str = dob_date.strftime("%d%m%Y")
    digits = [int(d) for d in dob_str if d != '0']
    
    grid = {i: [] for i in range(1, 10)}
    for d in digits:
        grid[d].append(d)
    return grid, set(digits)

def get_approx_ascendant(birth_time):
    # Standard 2-hour division per Rashi starting from Sunrise ~6:00 AM Aries
    total_minutes = birth_time.hour * 60 + birth_time.minute
    index = (total_minutes // 120) % 12
    return RASHI_NAMES[index]

def generate_pdf_report(name, dob, tob, mulank, bhagyank, namank, ascendant, loshu_grid, missing_nums, conflicts):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1b365d'),
        alignment=1,
        spaceAfter=15
    )
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2c5282'),
        spaceBefore=10,
        spaceAfter=5
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=6
    )

    story.append(Paragraph("<b>Vedic Astrology & Numerology Comprehensive Report</b>", title_style))
    story.append(Spacer(1, 10))

    # Basic Info Table
    data = [
        ["Name", name, "Date of Birth", dob.strftime("%d-%m-%Y")],
        ["Time of Birth", tob.strftime("%H:%M"), "Approx Ascendant", ascendant],
        ["Mulank (Driver)", str(mulank), "Bhagyank (Conductor)", str(bhagyank)],
        ["Namank (Name No)", str(namank), "", ""]
    ]
    t = Table(data, colWidths=[120, 140, 120, 140])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f4f8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))

    # Driver & Conductor Analysis
    story.append(Paragraph("<b>1. Planetary Analysis & Attributes</b>", heading_style))
    p_info = PLANET_INFO[mulank]
    story.append(Paragraph(f"<b>Driver Planet ({p_info['planet']}):</b> {p_info['traits']}", body_style))
    story.append(Paragraph(f"<b>Health Warnings:</b> {p_info['health']}", body_style))
    story.append(Paragraph(f"<b>Vedic Mantra:</b> {p_info['mantra']}", body_style))
    story.append(Paragraph(f"<b>Gemstone:</b> {p_info['gem']} | <b>Remedy:</b> {p_info['remedy']}", body_style))
    story.append(Spacer(1, 10))

    # Missing Numbers & Remedies
    story.append(Paragraph("<b>2. Missing Numbers & Remedial Actions</b>", heading_style))
    if missing_nums:
        for num in sorted(missing_nums):
            story.append(Paragraph(f"<b>Missing Number {num}:</b> {MISSING_REMEDIES[num]}", body_style))
    else:
        story.append(Paragraph("No missing numbers in your Date of Birth grid!", body_style))
    story.append(Spacer(1, 10))

    # Conflicts/Dosha Warnings
    story.append(Paragraph("<b>3. Dosha & Conflict Warnings</b>", heading_style))
    if conflicts:
        for c in conflicts:
            story.append(Paragraph(f"⚠️ <b>{c['title']}:</b> {c['desc']} (<b>Remedy:</b> {c['remedy']})", body_style))
    else:
        story.append(Paragraph("No major anti-combination conflicts detected between Mulank and Bhagyank.", body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ---------------------------------------------------------
# Streamlit UI Layout
# ---------------------------------------------------------
st.title("🔮 वैदिक ज्योतिष एवं अंकशास्त्र कम्प्यूटेशनल सॉफ्टवेयर")
st.markdown("### Vedic Astrology, Numerology & Remedial Engine")
st.write("---")

# Sidebar - User Inputs
st.sidebar.header("📋 जन्म विवरण दर्ज करें (Input Details)")
user_name = st.sidebar.text_input("पूरा नाम (Full Name)", "Sunil Kumar")
dob_date = st.sidebar.date_input("जन्म तिथि (Date of Birth)", datetime.date(1995, 8, 29), min_value=datetime.date(1940, 1, 1))
tob_time = st.sidebar.time_input("जन्म समय (Time of Birth)", datetime.time(10, 30))

if st.sidebar.button("📊 जन्मकुंडली व रिपोर्ट जनरेट करें"):
    # Perform Calculations
    mulank = calculate_mulank(dob_date.day)
    bhagyank = calculate_bhagyank(dob_date)
    namank = calculate_namank(user_name)
    ascendant = get_approx_ascendant(tob_time)
    loshu_grid, present_digits = get_loshu_grid(dob_date)
    missing_nums = set(range(1, 10)) - present_digits
    day_name = dob_date.strftime("%A")

    # Anti-combination & Dosha Check
    conflicts = []
    pair = sorted([mulank, bhagyank])
    if pair == [1, 8]:
        conflicts.append({
            "title": "1 और 8 टकराव (सूर्य - शनि)",
            "desc": "पिता-पुत्र में मतभेद, करियर में अत्यधिक संघर्ष, सरकारी कार्यों में रुकावट।",
            "remedy": "सूर्य देव को नित्य जल दें, नीले कपड़े पहनने से बचें।"
        })
    elif pair == [2, 8]:
        conflicts.append({
            "title": "2 और 8 टकराव (विष योग - चंद्र शनि)",
            "desc": "अत्यधिक मानसिक तनाव, डिप्रेशन, कार्य में बार-बार अड़चनें।",
            "remedy": "सोमवार को शिवलिंग पर जलाभिषेक करें और महामृत्युंजय मंत्र पढ़ें।"
        })
    elif pair == [4, 9]:
        conflicts.append({
            "title": "4 और 9 टकराव (अंगारक योग - राहु मंगल)",
            "desc": "अचानक गुस्सा, दुर्घटना की आशंका, कानूनी अड़चनें।",
            "remedy": "हनुमान चालीसा का रोज पाठ करें। शांत रहें।"
        })

    # Main Page Output Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 मुख्य अंकशास्त्र (Numerology)",
        "🧩 लो-शू ग्रिड (Lo Shu Grid)",
        "🌌 पंचांग व लग्न (Ascendant)",
        "⚠️ दोष व योग (Doshas)",
        "🌿 महा-उपाय व मंत्र (Remedies)"
    ])

    # Tab 1: Core Numerology
    with tab1:
        st.subheader("1. मूलभूत अंकशास्त्र विवरण (Key Numbers)")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("मूलांक (Driver)", mulank, f"ग्रह: {PLANET_INFO[mulank]['planet'].split()[0]}")
        col2.metric("भाग्यांक (Conductor)", bhagyank, f"ग्रह: {PLANET_INFO[bhagyank]['planet'].split()[0]}")
        col3.metric("नामांक (Name No)", namank, "Chaldean System")
        col4.metric("जन्म वार (Day)", day_name)

        st.markdown("---")
        st.write(f"### ☀️ मूलांक {mulank} ({PLANET_INFO[mulank]['planet']}) विस्तृत विश्लेषण:")
        st.write(f"**विशेषता व प्रकृति:** {PLANET_INFO[mulank]['traits']}")
        st.write(f"**संभावित स्वास्थ्य समस्याएं:** {PLANET_INFO[mulank]['health']}")
        st.write(f"**उपयुक्त रत्न:** {PLANET_INFO[mulank]['gem']}")

    # Tab 2: Lo Shu Grid Analysis
    with tab2:
        st.subheader("2. लो-शू ग्रिड 3x3 (Lo Shu Grid Diagram)")
        
        # Format Grid Display
        grid_pos = [
            [4, 9, 2],
            [3, 5, 7],
            [8, 1, 6]
        ]
        
        col_g1, col_g2 = st.columns([1, 1])
        with col_g1:
            st.markdown("#### जन्म तिथि ग्रिड:")
            for row in grid_pos:
                r_str = " | ".join(["".join(str(x) for x in loshu_grid[cell]) if loshu_grid[cell] else " — " for cell in row])
                st.markdown(f"### `[ {r_str} ]` ")

        with col_g2:
            st.markdown("#### सक्रिय योग / प्लेन्स (Active Planes):")
            active_planes = 0
            for p_name, (nums, p_desc) in LOSHU_PLANES.items():
                if set(nums).issubset(present_digits):
                    st.success(f"✅ **{p_name}:** {p_desc}")
                    active_planes += 1
            if active_planes == 0:
                st.info("सामान्य ग्रिड संरचना - कोई विशिष्ट पूर्ण प्लेन योग नहीं है।")

        st.markdown("---")
        st.markdown("#### ❌ अनुपस्थित अंक (Missing Numbers) एवं उनके उपाय:")
        if missing_nums:
            for num in sorted(missing_nums):
                st.warning(f"**अंक {num} अनुपस्थित ({PLANET_INFO[num]['planet']}):** {MISSING_REMEDIES[num]}")
        else:
            st.success("आपकी जन्म तिथि में सभी अंक मौजूद हैं!")

    # Tab 3: Panchang & Ascendant
    with tab3:
        st.subheader("3. पंचांग एवं लग्न विवरण (Panchang & Ascendant Details)")
        st.info(f"**अनुमानित जन्म लग्न (Approx Ascendant):** {ascendant}")
        st.write(f"**जन्म तिथि:** {dob_date.strftime('%d %B %Y')}")
        st.write(f"**जन्म समय:** {tob_time.strftime('%I:%M %p')}")
        st.write("**दशा गणना लॉजिक:** मूलांक स्वामी ग्रह की महादशा का प्रभाव वर्तमान चक्र में अधिक क्रियाशील रहता है।")

    # Tab 4: Doshas & Anti-combinations
    with tab4:
        st.subheader("4. दोष एवं विरोधी संयोजन पहचान (Dosha Detector)")
        if conflicts:
            for c in conflicts:
                st.error(f"⚠️ **{c['title']}**\n\n**प्रभाव:** {c['desc']}\n\n**सटीक उपाय:** {c['remedy']}")
        else:
            st.success("✨ मूलांक और भाग्यांक में कोई प्रत्यक्ष अति-शत्रुता (Anti-combination) नहीं पाई गई।")

    # Tab 5: Remedies & Mantras
    with tab5:
        st.subheader("5. सर्व-उपाय, महामंत्र एवं समाधान (Remedies & Mantras)")
        st.markdown(f"### 📿 मूलांक {mulank} हेतु वैदिक बीज मंत्र:")
        st.code(PLANET_INFO[mulank]['mantra'], language="text")
        st.write(f"**दैनिक उपाय:** {PLANET_INFO[mulank]['remedy']}")

        st.markdown("---")
        st.markdown("### 📿 भाग्यांक {bhagyank} हेतु वैदिक बीज मंत्र:")
        st.code(PLANET_INFO[bhagyank]['mantra'], language="text")
        st.write(f"**दैनिक उपाय:** {PLANET_INFO[bhagyank]['remedy']}")

    # PDF Download Button
    st.markdown("---")
    pdf_file = generate_pdf_report(
        user_name, dob_date, tob_time, mulank, bhagyank, namank, ascendant,
        loshu_grid, missing_nums, conflicts
    )
    st.download_button(
        label="📥 पूरी ज्योतिष रिपोर्ट (PDF) डाउनलोड करें",
        data=pdf_file,
        file_name=f"{user_name.replace(' ', '_')}_Astrology_Report.pdf",
        mime="application/pdf"
    )
else:
    st.info("👈 कृपया बाएं (Sidebar) पैनल में अपना नाम, तिथि और समय दर्ज करके **'जन्मकुंडली व रिपोर्ट जनरेट करें'** पर क्लिक करें।")
