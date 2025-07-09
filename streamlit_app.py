import streamlit as st
import langfuse

st.title("Langfuse Secrets Debug")

# Check if secrets are loaded
st.subheader("Secrets Status Check")

try:
    # Check if secrets exist
    if hasattr(st, 'secrets'):
        st.success("✅ Streamlit secrets loaded")
        
        # Check each required key
        required_keys = [
            "OPENAI_API_KEY",
            "OPENAI_MODEL_NAME",
            "API_BASE_URL",
            "LANGFUSE_HOST",
            "LANGFUSE_PUBLIC_KEY",
            "LANGFUSE_SECRET_KEY"
        ]
        
        missing_keys = []
        found_keys = []
        
        for key in required_keys:
            try:
                value = st.secrets[key]
                if value:
                    found_keys.append(key)
                    # Show first 10 chars for verification
                    st.success(f"✅ {key}: {str(value)[:10]}...")
                else:
                    missing_keys.append(key)
                    st.error(f"❌ {key}: EMPTY")
            except KeyError:
                missing_keys.append(key)
                st.error(f"❌ {key}: NOT FOUND")
        
        # Summary
        st.subheader("Summary")
        st.write(f"Found keys: {len(found_keys)}")
        st.write(f"Missing keys: {len(missing_keys)}")
        
        if missing_keys:
            st.error(f"Missing keys: {missing_keys}")
        else:
            st.success("All required keys found!")
            
            # Try to initialize Langfuse only if all keys exist
            st.subheader("Langfuse Connection Test")
            try:
                from langfuse import Langfuse
                langfuse = Langfuse(
                    public_key=st.secrets["LANGFUSE_PUBLIC_KEY"],
                    secret_key=st.secrets["LANGFUSE_SECRET_KEY"],
                    host=st.secrets["LANGFUSE_HOST"]
                )
                langfuse.auth_check()
                st.success("✅ Langfuse connection successful!")
            except Exception as e:
                st.error(f"❌ Langfuse connection failed: {e}")
        
    else:
        st.error("❌ Streamlit secrets not found")
        
except Exception as e:
    st.error(f"❌ Error accessing secrets: {e}")

# Show file location help
st.subheader("Setup Help")
st.code("""
Create file: .streamlit/secrets.toml

Content:
LANGFUSE_PUBLIC_KEY="pk-xxx"
LANGFUSE_SECRET_KEY="sk-xxx"
LANGFUSE_HOST="https://xxx"
OPENAI_API_KEY="sk-xxx"
OPENAI_MODEL_NAME="gpt-4.1-nano"
API_BASE_URL="https://xxx"
""")
