import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image as PILImage
from pypdf import PdfWriter, PdfReader
from geopy.geocoders import Nominatim
import io

# Streamlit Page Setup
st.set_page_config(page_title="Property Detail PDF Generator", layout="wide")

st.title("🏡 Property Information Sheet & Blueprint Generator")
st.write("विवरण भरें, ओरिजिनल नक्शा अटैच करें और परफेक्ट पीडीएफ डाउनलोड करें।")

# Session State initialization for persistent memory
if "ref_no" not in st.session_state:
    st.session_state.ref_no = ""
if "coordinates" not in st.session_state:
    st.session_state.coordinates = ""
if "tehsil" not in st.session_state:
    st.session_state.tehsil = ""
if "road_infra" not in st.session_state:
    st.session_state.road_infra = ""
if "connectivity" not in st.session_state:
    st.session_state.connectivity = ""
if "demand" not in st.session_state:
    st.session_state.demand = ""
if "total_area" not in st.session_state:
    st.session_state.total_area = ""
if "total_amount" not in st.session_state:
    st.session_state.total_amount = ""

# Sidebar for Input Fields
st.sidebar.header("📝 Property Details Fill Karen")

ref_no = st.sidebar.text_input("Ref Number", value=st.session_state.ref_no, key="ref_no_input")
st.session_state.ref_no = ref_no

# Location Coordinates Input
coordinates = st.sidebar.text_input("Location Coordinates (Lat, Long)", value=st.session_state.coordinates, key="coord_input")
st.session_state.coordinates = coordinates

# Function to auto-fetch District from Coordinates using Geopy
def get_district_from_coords(coords_text):
    try:
        if not coords_text.strip():
            return ""
        geolocator = Nominatim(user_agent="property_pdf_generator_app_v8")
        location = geolocator.reverse(coords_text.strip(), language='en', timeout=10)
        if location and location.raw.get('address'):
            address = location.raw['address']
            district_name = address.get('state_district') or address.get('county') or address.get('city') or address.get('town')
            state_name = address.get('state', '')
            if district_name:
                return f"{district_name} ({state_name})"
    except Exception:
        pass
    return ""

auto_district = get_district_from_coords(coordinates)

# Dropdown for Nature of Property
nature_options = ["", "Agriculture", "Commercial", "Industrial", "Residential", "All"]
nature_prop = st.sidebar.selectbox("Nature of Property", nature_options)

# District Field
district_options = ["", auto_district, "Alwar (Rajasthan)", "Faridabad (Haryana)", "Gurugram (Haryana)", "Palwal (Haryana)", "Other"]
district_options = [x for x in district_options if x]
district_options = list(dict.fromkeys(district_options))
district = st.sidebar.selectbox("District (Auto-detected / Select)", district_options)

# Tehsil - Blank
tehsil = st.sidebar.text_input("Tehsil", value=st.session_state.tehsil, key="tehsil_input")
st.session_state.tehsil = tehsil

# Road Infra - अब मल्टी-लाइन (Text Area) कर दिया है ताकि नीचे भी लिख सकें
road_infra = st.sidebar.text_area(
    "Road Infra", 
    value=st.session_state.road_infra, 
    key="road_input"
)
st.session_state.road_infra = road_infra

connectivity = st.sidebar.text_area(
    "Connectivity", 
    value=st.session_state.connectivity, 
    key="conn_input"
)
st.session_state.connectivity = connectivity

demand = st.sidebar.text_input("Demand", value=st.session_state.demand, key="demand_input")
st.session_state.demand = demand

total_area = st.sidebar.text_input("Total Area", value=st.session_state.total_area, key="area_input")
st.session_state.total_area = total_area

total_amount = st.sidebar.text_input("Total Amount", value=st.session_state.total_amount, key="amount_input")
st.session_state.total_amount = total_amount

# Extra Custom Fields (Optional)
st.sidebar.markdown("---")
st.sidebar.header("➕ Extra Custom Fields (Optional)")
custom_title_1 = st.sidebar.text_input("Extra Heading 1 (जैसे: Water Source / Other)", "")
custom_desc_1 = st.sidebar.text_area("Extra Details 1", "")

custom_title_2 = st.sidebar.text_input("Extra Heading 2 (जैसे: Legal Status / Remarks)", "")
custom_desc_2 = st.sidebar.text_area("Extra Details 2", "")

# File uploaders for photo/blueprint and extra PDF
st.sidebar.markdown("---")
st.sidebar.header("📎 Attachments (Photo / Blueprint & Extra PDF)")
uploaded_photo = st.sidebar.file_uploader("प्रॉपर्टी का ओरिजिनल नक्शा या फोटो चुनें (JPG, PNG)", type=["jpg", "jpeg", "png"])
uploaded_pdf = st.sidebar.file_uploader("अतिरिक्त पीडीएफ चुनें (जैसे इंतखाब / दस्तावेज़)", type=["pdf"])

# Radio button to choose photo position
photo_layout = st.sidebar.radio(
    "नक्शा कहाँ दिखना चाहिए?",
    ["अलग से पूरे दूसरे पेज पर (Blueprint Page)", "डिटेल के ठीक नीचे (Same Page - Framed Fit)"]
)


# Function to get original image dimensions and proportional fit without color distortion
def get_original_image_info(image_file, max_width, max_height):
    img = PILImage.open(image_file)
    orig_width, orig_height = img.size
    
    aspect = orig_height / orig_width
    width = max_width
    height = width * aspect
    
    if height > max_height:
        height = max_height
        width = height / aspect
        
    return image_file, width, height


# Function to generate main property details PDF
def generate_main_pdf(image_file, layout_choice):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1,
        spaceAfter=15
    )

    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1F2937')
    )

    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#374151')
    )

    story = []

    # Title
    story.append(Paragraph("PROPERTY INFORMATION SHEET & BLUEPRINT", title_style))
    story.append(Spacer(1, 5))

    formatted_connectivity = connectivity.replace("\n", "<br/>")
    formatted_road_infra = road_infra.replace("\n", "<br/>")

    clean_coords = coordinates.strip()
    if clean_coords:
        maps_url = f"https://www.google.com/maps/search/?api=1&query={clean_coords}"
        coord_link_html = f'<a href="{maps_url}" color="#1D4ED8"><u><b>{coordinates} (Click to Open Map)</b></u></a>'
    else:
        coord_link_html = ""

    # Base Table Data
    raw_data = [
        ("LOCATION COORDINATES", coord_link_html),
        ("Nature of Property", nature_prop),
        ("District", district),
        ("Tehsil", tehsil),
        ("Road Infra", formatted_road_infra),
        ("Connectivity", formatted_connectivity),
        ("Demand", demand),
        ("Total Area", total_area),
        ("Total Amount", total_amount)
    ]

    data = []
    for title, val in raw_data:
        if val and str(val).strip():
            data.append([Paragraph(title, header_style), Paragraph(str(val), cell_style)])

    if custom_title_1.strip() and custom_desc_1.strip():
        formatted_desc_1 = custom_desc_1.replace("\n", "<br/>")
        data.append([Paragraph(custom_title_1, header_style), Paragraph(formatted_desc_1, cell_style)])

    if custom_title_2.strip() and custom_desc_2.strip():
        formatted_desc_2 = custom_desc_2.replace("\n", "<br/>")
        data.append([Paragraph(custom_title_2, header_style), Paragraph(formatted_desc_2, cell_style)])

    if data:
        col_widths = [2.2 * inch, 5.0 * inch]
        t = Table(data, colWidths=col_widths)

        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#111827')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
        ]))

        story.append(t)
        story.append(Spacer(1, 10))

    footer_text = f"Property Information Sheet - Ref No: {ref_no}" if ref_no else "Property Information Sheet"
    story.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=cell_style, alignment=1, textColor=colors.gray)))

    # Blueprint / Photo condition keeping original colors intact inside a framed layout
    if image_file is not None:
        if layout_choice == "अलग से पूरे दूसरे पेज पर (Blueprint Page)":
            story.append(PageBreak())
            story.append(Paragraph("OFFICIAL PROPERTY BLUEPRINT / SITE LAYOUT", title_style))
            story.append(Spacer(1, 10))
            
            img_file, img_w, img_h = get_original_image_info(image_file, max_width=7.2*inch, max_height=8.0*inch)
            
            blueprint_table = Table([[Image(img_file, width=img_w, height=img_h)]], colWidths=[7.4 * inch])
            blueprint_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#1E3A8A')),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFFFF')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(blueprint_table)
        else:
            story.append(Spacer(1, 10))
            story.append(Paragraph("PROPERTY SITE BLUEPRINT", ParagraphStyle('SubTitle', parent=styles['Heading2'], fontSize=12, textColor=colors.HexColor('#1E3A8A'))))
            story.append(Spacer(1, 5))
            
            img_file, img_w, img_h = get_original_image_info(image_file, max_width=6.5*inch, max_height=3.5*inch)
            
            blueprint_table = Table([[Image(img_file, width=img_w, height=img_h)]], colWidths=[6.7 * inch])
            blueprint_table.setStyle(TableStyle([
                ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor('#1E3A8A')),
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFFFFF')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(blueprint_table)

    doc.build(story)
    buffer.seek(0)
    return buffer


# Function to merge main PDF with extra uploaded PDF
def get_final_pdf(image_file, layout_choice, extra_pdf_file):
    main_pdf_buffer = generate_main_pdf(image_file, layout_choice)
    
    if extra_pdf_file is not None:
        writer = PdfWriter()
        
        reader_main = PdfReader(main_pdf_buffer)
        for page in reader_main.pages:
            writer.add_page(page)
            
        reader_extra = PdfReader(extra_pdf_file)
        for page in reader_extra.pages:
            writer.add_page(page)
            
        final_buffer = io.BytesIO()
        writer.write(final_buffer)
        final_buffer.seek(0)
        return final_buffer
    else:
        return main_pdf_buffer


# Main Area Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Enter Details Preview")
    st.write(f"**Ref:** {ref_no}")
    st.write(f"**Coordinates:** {coordinates}")
    st.write(f"**District:** {district}")
    st.write(f"**Tehsil:** {tehsil}")
    st.write(f"**Nature of Property:** {nature_prop}")
    
    if custom_title_1.strip():
        st.write(f"**{custom_title_1}:** {custom_desc_1}")
    if custom_title_2.strip():
        st.write(f"**{custom_title_2}:** {custom_desc_2}")
        
    if uploaded_photo is not None:
        st.success("📸 Photo / Blueprint successfully uploaded!")
        st.image(uploaded_photo, caption="Uploaded Blueprint Preview", use_container_width=True)
        
    if uploaded_pdf is not None:
        st.success("📄 Extra PDF attached successfully!")

with col2:
    st.subheader("📄 Generate & Download PDF")
    pdf_bytes = get_final_pdf(uploaded_photo, photo_layout, uploaded_pdf)
    
    st.download_button(
        label="📥 Download Complete PDF",
        data=pdf_bytes,
        file_name=f"Property_Blueprint_{ref_no.replace('#', '') if ref_no else 'sheet'}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
