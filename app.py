import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

# Streamlit Page Setup
st.set_page_config(page_title="Property Detail PDF Generator", layout="wide")

st.title("🏡 Property Information Sheet PDF Generator")
st.write("बाएं तरफ दी गई फ़ील्ड्स में विवरण भरें और दाहिनी ओर से सीधा PDF डाउनलोड करें।")

# Sidebar for Input Fields
st.sidebar.header("📝 Property Details Fill Karen")

ref_no = st.sidebar.text_input("Ref Number", "Ref #7")
coordinates = st.sidebar.text_input("Location Coordinates", "27.867694, 76.816264")
nature_prop = st.sidebar.text_input("Nature of Property", "Agriculture")
district = st.sidebar.text_input("District", "Alwar (Rajasthan)")
tehsil = st.sidebar.text_input("Tehsil", "Khairthal-Tijara")
road_infra = st.sidebar.text_input("Road Infra", "Road Front 100' Wide")

connectivity = st.sidebar.text_area(
    "Connectivity", 
    "Tijara Jain Mandir se approx 7 KM to Alwar Road\n2 KM inside road (Suitable for Farm House)\nApprox 20 KM from Mumbai Expressway"
)

demand = st.sidebar.text_input("Demand", "60 Lakhs Per Bigha")
total_area = st.sidebar.text_input("Total Area", "129 Bigha (3025 Gaj in 1 Bigha)")
total_amount = st.sidebar.text_input("Total Amount", "77.4 Crore (Approx.) (129 Bigha x ₹60 Lakhs)")


# Function to generate PDF using ReportLab
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Styles (फॉन्ट साइज और स्पेसिंग बढ़ाई गई है)
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=22,         # टाइटल साइज़ बढ़ाया
        leading=26,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1,         # Center
        spaceAfter=20
    )

    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=12,         # हेडर साइज़ (11 से बढ़ाकर 12 किया)
        leading=16,          # लाइन स्पेसिंग बढ़ाई
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1F2937')
    )

    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontSize=11,         # सेल टेक्स्ट साइज़ (10 से बनाकर 11 किया)
        leading=16,          # लाइन स्पेसिंग बढ़ाई ताकि आपस
    
