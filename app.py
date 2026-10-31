import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image as PILImage
from pypdf import PdfWriter, PdfReader
import io

# Streamlit Page Setup
st.set_page_config(page_title="Property Detail PDF Generator", layout="wide")

st.title("🏡 Property Information Sheet PDF Generator")
st.write("विवरण भरें, कस्टमाइज़्ड फील्ड्स जोड़ें, फोटो/पीडीएफ अपलोड करें और पीडीएफ डाउनलोड करें।")

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
total_amount = st.sidebar.text_input("Total Amount", "77.4 Crore (Approx.) (129 Bigha x Rs. 60 Lakhs)")

# Extra Custom Fields (अगर खाली छोड़ेंगे तो पीडीएफ में नहीं आएंगे)
st.sidebar.markdown("---")
st.sidebar.header("➕ Extra Custom Fields (Optional)")
custom_title_1 = st.sidebar.text_input("Extra Heading 1 (जैसे: Water Source / Other)", "")
custom_desc_1 = st.sidebar.text_area("Extra Details 1", "")

custom_title_2 = st.sidebar.text_input("Extra Heading 2 (जैसे: Legal Status / Remarks)", "")
custom_desc_2 = st.sidebar.text_area("Extra Details 2", "")

# File uploaders for photo and extra PDF
st.sidebar.markdown("---")
st.sidebar.header("📎 Attachments (Photo & Extra PDF)")
uploaded_photo = st.sidebar.file_uploader("प्रॉपर्टी की फोटो चुनें (JPG, PNG)", type=["jpg", "jpeg", "png"])
uploaded_pdf = st.sidebar.file_uploader("अतिरिक्त पीडीएफ चुनें (जैसे नक्शा / दस्तावेज़)", type=["pdf"])

# Radio button to choose photo position
photo_layout = st.sidebar.radio(
    "फोटो कहाँ दिखनी चाहिए?",
    ["डिटेल के ठीक नीचे (Same Page - Proportional Fit)", "अलग से पूरे दूसरे पेज पर (Full Page - Proportional Fit)"]
)


# Function to calculate proportional image size without stretching
def get_proportional_image(image_file, max_width, max_height):
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
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1,
        spaceAfter=15
    )

    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1F2937')
    )

    cell_style = ParagraphStyle(
        'CellStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#374151')
    )

    story = []

    # Title
    story.append(Paragraph("PROPERTY DETAILS", title_style))
    story.append(Spacer(1, 10))

    formatted_connectivity = connectivity.replace("\n", "<br/>")

    clean_coords = coordinates.strip()
    maps_url = f"https://www.google.com/maps/search/?api=1&query={clean_coords}"
    coord_link_html = f'<a href="{maps_url}" color="#1D4ED8"><u><b>{coordinates} (Click to Open Map)</b></u></a>'

    # Base Table Data
    data = [
        [Paragraph("LOCATION COORDINATES", header_style), Paragraph(coord_link_html, cell_style)],
        [Paragraph("Nature of Property", header_style), Paragraph(nature_prop, cell_style)],
        [Paragraph("District", header_style), Paragraph(district, cell_style)],
        [Paragraph("Tehsil", header_style), Paragraph(tehsil, cell_style)],
        [Paragraph("Road Infra", header_style), Paragraph(road_infra, cell_style)],
        [Paragraph("Connectivity", header_style), Paragraph(formatted_connectivity, cell_style)],
        [Paragraph("Demand", header_style), Paragraph(demand, cell_style)],
        [Paragraph("Total Area", header_style), Paragraph(total_area, cell_style)],
        [Paragraph("Total Amount", header_style), Paragraph(total_amount, cell_style)]
    ]

    # Dynamically add custom field 1 if filled
    if custom_title_1.strip() and custom_desc_1.strip():
        formatted_desc_1 = custom_desc_1.replace("\n", "<br/>")
        data.append([Paragraph(custom_title_1, header_style), Paragraph(formatted_desc_1, cell_style)])

    # Dynamically add custom field 2 if filled
    if custom_title_2.strip() and custom_desc_2.strip():
        formatted_desc_2 = custom_desc_2.replace("\n", "<br/>")
        data.append([Paragraph(custom_title_2, header_style), Paragraph(formatted_desc_2, cell_style)])

    col_widths = [2.4 * inch, 4.8 * inch]
    t = Table(data, colWidths=col_widths)

    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#111827')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
    ]))

    story.append(t)
    story.append(Spacer(1, 15))

    footer_text = f"Property Information Sheet - {ref_no}"
    story.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=cell_style, alignment=1, textColor=colors.gray)))

    # Photo condition with strict aspect ratio lock
    if image_file is not None:
        if layout_choice == "अलग से पूरे दूसरे पेज पर (Full Page - Proportional Fit)":
            story.append(PageBreak())
            story.append(Paragraph("PROPERTY SITE VIEW", title_style))
            story.append(Spacer(1, 10))
            
            img_file, img_w, img_h = get_proportional_image(image_file, max_width=7.2*inch, max_height=8.0*inch)
            img = Image(img_file, width=img_w, height=img_h)
            img.hAlign = 'CENTER'
            story.append(img)
        else:
            story.append(Spacer(1, 15))
            story.append(Paragraph("PROPERTY PHOTO", ParagraphStyle('SubTitle', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#1E3A8A'))))
            story.append(Spacer(1, 8))
            
            img_file, img_w, img_h = get_proportional_image(image_file, max_width=6.5*inch, max_height=3.8*inch)
            img = Image(img_file, width=img_w, height=img_h)
            img.hAlign = 'CENTER'
            story.append(img)

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
    
    if custom_title_1.strip():
        st.write(f"**{custom_title_1}:** {custom_desc_1}")
    if custom_title_2.strip():
        st.write(f"**{custom_title_2}:** {custom_desc_2}")
        
    if uploaded_photo is not None:
        st.success("📸 Photo successfully uploaded!")
        st.image(uploaded_photo, caption="Uploaded Photo Preview", use_container_width=True)
        
    if uploaded_pdf is not None:
        st.success("📄 Extra PDF attached successfully!")

with col2:
    st.subheader("📄 Generate & Download PDF")
    pdf_bytes = get_final_pdf(uploaded_photo, photo_layout, uploaded_pdf)
    
    st.download_button(
        label="📥 Download Complete PDF",
        data=pdf_bytes,
        file_name=f"Property_Details_{ref_no.replace('#', '')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
