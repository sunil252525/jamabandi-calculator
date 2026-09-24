import streamlit as st

# वेब पेज की सेटिंग
st.set_page_config(page_title="हरियाणा जमाबंदी हिस्सा कैलकुलेटर", page_icon="🌾", layout="centered")

st.title("🌾 हरियाणा जमाबंदी एवं भू-लेख हिस्सा कैलकुलेटर")
st.write("इस ऐप से आप जमाबंदी के अनुसार कुल रकबे में से किसी हिस्सेदार की ज़मीन का सटीक हिस्सा निकाल सकते हैं।")

st.divider()

# 1. कुल रकबा इनपुट
st.subheader("1. कुल ज़मीन का रकबा दर्ज करें")
col1, col2, col3 = st.columns(3)

with col1:
    total_kanal = st.number_input("कनाल", min_value=0, value=4, step=1)
with col2:
    total_marla = st.number_input("मरला", min_value=0, max_value=19, value=12, step=1)
with col3:
    total_sarsahi = st.number_input("सरसाही", min_value=0.0, max_value=8.99, value=6.0, step=0.01)

st.divider()

# 2. हिस्सा (Fractional Share) इनपुट
st.subheader("2. व्यक्ति का हिस्सा (Share) दर्ज करें")
col_num, col_den = st.columns(2)

with col_num:
    numerator = st.number_input("अंश (Numerator - जैसे 25)", min_value=1, value=25, step=1)
with col_den:
    denominator = st.number_input("हर (Denominator - जैसे 120)", min_value=1, value=120, step=1)

# गणना बटन
if st.button("हिस्सा निकालें (Calculate)", type="primary"):
    # कुल सरसाही की गणना
    # 1 कनाल = 180 सरसाही, 1 मरला = 9 सरसाही
    total_sarsahi_sum = (total_kanal * 180) + (total_marla * 9) + total_sarsahi
    
    # हिस्सेदार की सरसाही
    person_sarsahi = total_sarsahi_sum * (numerator / denominator)
    
    # वापस कनाल और मरला में परिवर्तन
    res_marla_total = person_sarsahi / 9.0
    res_kanal = int(res_marla_total // 20)
    res_marla = int(res_marla_total % 20)
    res_sarsahi = person_sarsahi - ((res_kanal * 180) + (res_marla * 9))
    
    # वर्ग फीट और वर्ग गज में गणना
    # 1 सरसाही = 30.25 वर्ग फीट
    sq_ft = person_sarsahi * 30.25
    sq_yards = sq_ft / 9.0
    
    st.divider()
    st.success("### 📊 गणना का परिणाम:")
    
    # परिणाम प्रदर्शित करना
    st.metric(label="व्यक्ति के हिस्से का कुल रकबा", value=f"{res_kanal} कनाल {res_marla} मरला {res_sarsahi:.2f} सरसाही")
    
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric("कुल सरसाही", f"{person_sarsahi:.2f}")
    with res_col2:
        st.metric("वर्ग फीट (Sq. Ft.)", f"{sq_ft:,.2f}")
    with res_col3:
        st.metric("वर्ग गज (Sq. Yards)", f"{sq_yards:,.2f}")

st.divider()
st.caption("नोट: 1 कनाल = 20 मरले | 1 मरला = 9 सरसाही | 1 सरसाही = 30.25 वर्ग फीट")
