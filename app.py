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
total_amount = st.sidebar.text_input("Total Amount", "77.4 Crore (Approx.) (129 Bigha x Rs. 60 Lakhs)")


# Function to generate PDF using ReportLab
def generate_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1,
        spaceAfter=20
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
    story.append(Spacer(1, 12))

    # Formatted Connectivity Text (Replace newline with <br/>)
    formatted_connectivity = connectivity.replace("\n", "<br/>")

    # Google Maps Clickable Link for Coordinates (बिना इमोजी के, ताकि एरर या बॉक्स न आए)
    clean_coords = coordinates.strip()
    maps_url = f"https://www.google.com/maps/search/?api=1&query={clean_coords}"
    
    coord_link_html = f'<a href="{maps_url}" color="#1D4ED8"><u>{coordinates} (Click to Open Map)</u></a>'

    # Table Data Structure
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

    # Create Table Widths
    col_widths = [2.3 * inch, 4.8 * inch]
    t = Table(data, colWidths=col_widths)

    # Table Padding और Border Styling
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#111827')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
    ]))

    story.append(t)
    story.append(Spacer(1, 25))

    # Footer Reference
    footer_text = f"Property Information Sheet - {ref_no}"
    story.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=cell_style, alignment=1, textColor=colors.gray)))

    # Build Document
    doc.build(story)
    buffer.seek(0)
    return buffer

# Main Area Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Enter Details Preview")
    st.write(f"**Ref:** {ref_no}")
    st.write(f"**Coordinates:** {coordinates}")
    st.write(f"**Nature:** {nature_prop}")
    st.write(f"**District:** {district}")
    st.write(f"**Tehsil:** {tehsil}")
    st.write(f"**Road Infra:** {road_infra}")
    st.write(f"**Connectivity:**")
    st.info(connectivity)
    st.write(f"**Demand:** {demand}")
    st.write(f"**Total Area:** {total_area}")
    st.write(f"**Total Amount:** {total_amount}")

with col2:
    st.subheader("📄 Generate & Download PDF")
    pdf_bytes = generate_pdf()
    
    st.download_button(
        label="📥 Download PDF",
        data=pdf_bytes,
        file_name=f"Property_Details_{ref_no.replace('#', '')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
