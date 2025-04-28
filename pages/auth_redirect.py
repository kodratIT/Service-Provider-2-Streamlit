import streamlit as st
import requests
import jwt
from urllib.parse import parse_qs

# Konfigurasi Keycloak
CLIENT_ID = "uin"
CLIENT_SECRET = "9e0yivT9GzcnDTDVVw8Pe6Rlswr7H3Oi"
REALM = "Universitas"
AUTH_SERVER_URL = "http://localhost:8180"
REDIRECT_URI = "http://localhost:8601/auth_redirect"
TOKEN_URL = f"{AUTH_SERVER_URL}/realms/{REALM}/protocol/openid-connect/token"

st.title("Authorization Redirect Handler")
st.subheader("Step 1: Capture Authorization Code")

# Ambil query param dari URL
query_params = st.experimental_get_query_params()
code = query_params.get("code", [None])[0]

if code:
    st.success("Authorization Code captured!")
    st.write("Authorization Code:", code)

    st.subheader("Step 2: Exchange Authorization Code for Tokens")
    body = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    try:
        response = requests.post(TOKEN_URL, data=body)

        if response.status_code == 200:
            tokens = response.json()
            st.write("Token Response:", tokens)

            if "id_token" in tokens:
                st.subheader("Step 3: Decode ID Token")
                id_token = tokens["id_token"]
                decoded_token = jwt.decode(id_token, options={"verify_signature": False})
                st.write("Decoded ID Token:", decoded_token)

                st.subheader("User Attributes")
                attributes = {
                    "Name": decoded_token.get("name"),
                    "Email": decoded_token.get("email"),
                    "Preferred Username": decoded_token.get("preferred_username"),
                    "Roles": decoded_token.get("realm_access", {}).get("roles"),
                    "SSI Attributes": decoded_token.get("ssi_attrs_grouped_array")
                }

                for key, value in attributes.items():
                    st.write(f"**{key}:** {value}")
            else:
                st.error("ID Token not found in the response.")
        else:
            st.error(f"Failed to exchange authorization code. Status: {response.status_code}")
            st.write(response.text)
    except Exception as e:
        st.error("An error occurred during token exchange.")
        st.write(str(e))
else:
    st.error("Authorization Code not found in URL.")
