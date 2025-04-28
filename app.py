import streamlit as st

# Konfigurasi Keycloak
CLIENT_ID = "uin"
REDIRECT_URI = "http://localhost:8601/auth_redirect"

# URL Otentikasi
url = "http://localhost:8180/realms/UNiversitas/protocol/openid-connect/auth?"
url += "scope=openid&"
url += "response_type=code&"
url += f"client_id={CLIENT_ID}&"
url += f"redirect_uri={REDIRECT_URI}"

# Tombol Login
html_button = """
<style>
    .btn {
        background-color:#4169E1;
        color: #fff;
        border:none; 
        border-radius:10px; 
        padding:15px;
        min-height:30px; 
        width: 100%;
    }
</style>
"""
html_button += f'<a href="{url}" target="_self"><button class="btn">Login</button></a>'

# Halaman Streamlit
st.title("Login dengan Keycloak")
st.subheader("Step 1: Initialize the flow")
st.markdown(html_button, unsafe_allow_html=True)

st.subheader("Step 2: Redirect to Keycloak")
st.code(url.replace("&", "&\n"))
