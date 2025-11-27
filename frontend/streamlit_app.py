
import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image


API_URL = "http://localhost:8000"


# ----------------------
# Page Config
# ----------------------
st.set_page_config(layout="wide", page_title="FloatChat — Ocean Data Explorer", page_icon="🌊")


# ----------------------
# Professional Ocean-themed styling
# ----------------------
page_bg_img = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #0c1821 0%, #1e3a52 35%, #2d5a87 100%);
    color: #f8fafc;
    font-family: 'Inter', sans-serif;
}

/* Header styling */
.header-container {
    background: rgba(15, 32, 39, 0.8);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(0, 198, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.header-title {
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #ffffff;
    margin-bottom: 0.5rem;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.header-subtitle {
    font-size: 1.5rem;
    color: #94a3b8;
    font-weight: 400;
    letter-spacing: 0.5px;
}

/* Info panel */
.info-panel {
    background: linear-gradient(135deg, rgba(0, 198, 255, 0.08) 0%, rgba(0, 114, 255, 0.12) 100%);
    backdrop-filter: blur(20px);
    border-radius: 18px;
    padding: 1.5em 2em;
    margin-bottom: 2em;
    color: #e2e8f0;
    border: 1px solid rgba(0, 198, 255, 0.25);
    box-shadow: 0 8px 32px rgba(0, 198, 255, 0.1);
    font-size: 1.2rem;
    line-height: 1.7;
}

/* Chat messages */
.user-msg, .bot-msg {
    padding: 18px 22px;
    border-radius: 18px;
    margin: 14px 0;
    width: fit-content;
    max-width: 85%;
    font-size: 1.25rem;
    line-height: 1.6;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    backdrop-filter: blur(10px);
}

.user-msg {
    background: linear-gradient(135deg, #38bdf8 0%, #0ea5e9 100%);
    color: #ffffff;
    align-self: flex-end;
    border-bottom-right-radius: 6px;
    margin-left: auto;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.bot-msg {
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    color: #f1f5f9;
    align-self: flex-start;
    border-bottom-left-radius: 6px;
    border: 1px solid rgba(0, 198, 255, 0.3);
}

/* Input section */
.input-section {
    background: rgba(15, 32, 39, 0.6);
    backdrop-filter: blur(15px);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid rgba(0, 198, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

.input-title {
    color: #e2e8f0;
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Map container */
.map-container {
    background: rgba(15, 32, 39, 0.6);
    backdrop-filter: blur(15px);
    border-radius: 16px;
    padding: 1rem;
    border: 1px solid rgba(0, 198, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    margin: 1rem 0;
}

.map-title {
    color: #e2e8f0;
    font-size: 1.35rem;
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Data table styling */
.stDataFrame {
    background: rgba(15, 32, 39, 0.4) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(0, 198, 255, 0.2) !important;
}

.stDataFrame table {
    background-color: rgba(15, 32, 39, 0.6) !important;
    backdrop-filter: blur(10px) !important;
}

.stDataFrame th {
    background: rgba(0, 198, 255, 0.1) !important;
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

.stDataFrame td {
    color: #cbd5e1 !important;
}

/* Button styling */
.stButton>button {
    background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    border: none !important;
    padding: 0.85em 2.2em !important;
    margin-top: 1em !important;
    font-size: 1.15rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(14, 165, 233, 0.3) !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(14, 165, 233, 0.4) !important;
}

/* Input field styling */
.stTextInput>div>div>input {
    background: rgba(248, 250, 252, 0.95) !important;
    color: #1e293b !important;
    border-radius: 12px !important;
    font-size: 1.2rem !important;
    border: 2px solid rgba(0, 198, 255, 0.3) !important;
    backdrop-filter: blur(10px) !important;
    padding: 0.85rem 1.1rem !important;
}

.stTextInput>div>div>input:focus {
    border-color: #0ea5e9 !important;
    box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
}

/* Expander styling */
.streamlit-expanderHeader {
    background: rgba(0, 198, 255, 0.1) !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

/* Footer */
.footer {
    background: rgba(15, 32, 39, 0.6);
    backdrop-filter: blur(15px);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    color: #94a3b8;
    font-size: 1rem;
    margin-top: 3rem;
    border: 1px solid rgba(0, 198, 255, 0.2);
}

.footer a {
    color: #38bdf8 !important;
    text-decoration: none !important;
    font-weight: 500 !important;
}

.footer a:hover {
    color: #0ea5e9 !important;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(15, 32, 39, 0.3);
}

::-webkit-scrollbar-thumb {
    background: rgba(0, 198, 255, 0.5);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 198, 255, 0.7);
}

/* Spinner customization */
.stSpinner > div {
    border-top-color: #0ea5e9 !important;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Header Container
st.markdown("""
<div class='header-container'>
    <div style='display: flex; align-items: center; gap: 1rem;'>
        <div style='font-size: 4rem;'>🌊</div>
        <div>
            <div class='header-title'>FloatChat</div>
            <div class='header-subtitle'>Advanced Ocean Data Intelligence Platform</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Info Panel
st.markdown("""
<div class='info-panel'>
    <div style='display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;'>
        <div style='font-size: 2rem;'>🤖</div>
        <div style='font-size: 1.4rem; font-weight: 600; color: #38bdf8;'>Intelligent Ocean Data Assistant</div>
    </div>
    <div style='display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.5rem; margin-top: 1rem;'>
        <div>
            <div style='font-weight: 600; color: #0ea5e9; margin-bottom: 0.5rem;'>🔍 What is this?</div>
            <div>Advanced RAG-powered assistant for ARGO ocean float data exploration and analysis.</div>
        </div>
        <div>
            <div style='font-weight: 600; color: #0ea5e9; margin-bottom: 0.5rem;'>💡 How to use?</div>
            <div>Ask natural language questions about ocean profiles, locations, timeframes, or specific measurements.</div>
        </div>
        <div>
            <div style='font-weight: 600; color: #0ea5e9; margin-bottom: 0.5rem;'>📊 Example Query</div>
            <div style='font-style: italic;'>"Show temperature profiles in the Pacific Ocean during 2023"</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ----------------------
# Session State
# ----------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ----------------------
# Two-column layout: left for input, right for chat/results
# ----------------------
left_col, right_col = st.columns([1, 2], gap="large")


# ----------------------
# User Input in Left Column
# ----------------------
with left_col:
    st.markdown("""
    <div class='input-section'>
        <div class='input-title'>
            <span>💬</span> Ask Your Question
            <span style='font-size: 0.8rem; color: #94a3b8; font-weight: 400; margin-left: auto;' title='Try asking about locations, years, temperatures, or float IDs!'>💡 Need help?</span>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form(key="query_form", clear_on_submit=True):
        user_query = st.text_input(
            "",
            placeholder="e.g. Show me temperature profiles in the Atlantic Ocean during summer 2023",
            label_visibility="collapsed"
        )
        submit_button = st.form_submit_button("🚀 Analyze Data")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Quick suggestions
    st.markdown("""
    <div style='margin-top: 1.5rem; padding: 1rem; background: rgba(15, 32, 39, 0.4); border-radius: 12px; border: 1px solid rgba(0, 198, 255, 0.15);'>
        <div style='font-weight: 600; color: #38bdf8; margin-bottom: 0.8rem; font-size: 1.1rem;'>💡 Quick Suggestions</div>
        <div style='display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.95rem;'>
            <div style='color: #cbd5e1; cursor: pointer; padding: 0.3rem; border-radius: 6px;' onclick=''>📍 "Profiles near coordinates 20°N, 65°E"</div>
            <div style='color: #cbd5e1; cursor: pointer; padding: 0.3rem; border-radius: 6px;' onclick=''>🌡️ "Temperature trends in Arctic waters"</div>
            <div style='color: #cbd5e1; cursor: pointer; padding: 0.3rem; border-radius: 6px;' onclick=''>📈 "Salinity measurements in 2023"</div>
            <div style='color: #cbd5e1; cursor: pointer; padding: 0.3rem; border-radius: 6px;' onclick=''>🏝️ "Deep ocean profiles > 2000m depth"</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if submit_button and user_query.strip():
        st.session_state.chat_history.append({"role": "user", "message": user_query})
        with st.spinner("Thinking..."):
            try:
                resp = requests.post(f"{API_URL}/chat", json={"question": user_query}).json()
                bot_message = resp.get("response", "No response received.")
                results_df = pd.DataFrame(resp.get("results", []))
                st.session_state.chat_history.append({"role": "bot", "message": bot_message, "data": results_df})
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to backend. Error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")


# ----------------------
# Display Chat/Results in Right Column
# ----------------------
with right_col:
    for chat_idx, chat in enumerate(st.session_state.chat_history):
        if chat["role"] == "user":
            st.markdown(f"<div class='user-msg'><b>You:</b> {chat['message']}</div>", unsafe_allow_html=True)
        elif chat["role"] == "bot":
            st.markdown(f"<div class='bot-msg'><b>Bot:</b> {chat['message']}</div>", unsafe_allow_html=True)

            # Display DataFrame if available
            if "data" in chat and not chat["data"].empty:
                with st.expander(f"Show Data Table - Response {chat_idx + 1}", expanded=True):
                    st.dataframe(chat["data"], use_container_width=True)

                # Display map if coordinates exist
                if 'latitude' in chat["data"].columns and 'longitude' in chat["data"].columns:
                    df_map = chat["data"].dropna(subset=['latitude', 'longitude'])
                    if not df_map.empty:
                        st.markdown("""
                        <div class='map-container'>
                            <div class='map-title'>
                                <span>🗺️</span> Profile Locations Interactive Map
                                <span style='font-size: 0.9rem; color: #94a3b8; font-weight: 400; margin-left: auto;'>{} locations found</span>
                            </div>
                        """.format(len(df_map)), unsafe_allow_html=True)
                        
                        # Create reliable map
                        center_lat, center_lon = df_map['latitude'].mean(), df_map['longitude'].mean()
                        
                        # Start with a basic, reliable map
                        m = folium.Map(
                            location=[center_lat, center_lon],
                            zoom_start=4,
                            tiles='cartodbpositron'
                        )
                        
                        # Try to add enhanced features, but don't break if they fail
                        try:
                            # Add additional tile layers
                            folium.TileLayer('OpenStreetMap', name='Street Map').add_to(m)
                            folium.TileLayer('cartodbdark_matter', name='Dark Theme').add_to(m)
                            folium.LayerControl(position='topright').add_to(m)
                        except:
                            # If enhanced features fail, continue with basic map
                            pass
                        
                        # Add simple but effective markers
                        for idx, row in df_map.iterrows():
                            try:
                                # Build simple popup with all available data
                                popup_html = f"""
                                <div style='font-family: Arial, sans-serif; min-width: 250px; max-width: 300px;'>
                                    <h4 style='margin: 0 0 10px 0; color: #0ea5e9;'>🌊 ARGO Profile #{idx + 1}</h4>
                                """
                                
                                # Add all available data in a simple format
                                for col in row.index:
                                    value = row[col]
                                    if pd.notna(value):
                                        # Format numbers nicely
                                        if isinstance(value, float):
                                            if 'lat' in col.lower() or 'lon' in col.lower():
                                                formatted_value = f"{value:.4f}°"
                                            elif 'temp' in col.lower():
                                                formatted_value = f"{value:.2f}°C" 
                                            else:
                                                formatted_value = f"{value:.3f}"
                                        else:
                                            formatted_value = str(value)
                                        
                                        popup_html += f"<b>{col.replace('_', ' ').title()}:</b> {formatted_value}<br>"
                                
                                popup_html += "</div>"
                                
                                # Build enhanced tooltip with specific fields
                                tooltip_parts = []
                                
                                # Profile ID
                                for col in row.index:
                                    if 'profile' in col.lower() and 'id' in col.lower():
                                        if pd.notna(row[col]):
                                            tooltip_parts.append(f"ID: {row[col]}")
                                        break
                                else:
                                    tooltip_parts.append(f"Profile #{idx + 1}")
                                
                                # Date
                                for col in row.index:
                                    if 'date' in col.lower():
                                        if pd.notna(row[col]):
                                            tooltip_parts.append(f"Date: {row[col]}")
                                        break
                                
                                # Time
                                for col in row.index:
                                    if 'time' in col.lower():
                                        if pd.notna(row[col]):
                                            tooltip_parts.append(f"Time: {row[col]}")
                                        break
                                
                                # Coordinates (Lat/Lon)
                                tooltip_parts.append(f"Lat: {row['latitude']:.4f}°")
                                tooltip_parts.append(f"Lon: {row['longitude']:.4f}°")
                                
                                # Ocean
                                for col in row.index:
                                    if 'ocean' in col.lower():
                                        if pd.notna(row[col]):
                                            tooltip_parts.append(f"Ocean: {row[col]}")
                                        break
                                
                                # Profile Type
                                for col in row.index:
                                    if ('profile' in col.lower() and 'type' in col.lower()) or 'type' in col.lower():
                                        if pd.notna(row[col]):
                                            tooltip_parts.append(f"Type: {row[col]}")
                                        break
                                
                                # Create formatted tooltip
                                tooltip_html = "<br>".join(tooltip_parts)
                                
                                # Create simple marker
                                folium.CircleMarker(
                                    [row['latitude'], row['longitude']],
                                    radius=8,
                                    color="#0284c7",
                                    weight=2,
                                    fill=True,
                                    fill_color="#0ea5e9",
                                    fill_opacity=0.8,
                                    popup=folium.Popup(popup_html, max_width=320),
                                    tooltip=folium.Tooltip(tooltip_html, sticky=True)
                                ).add_to(m)
                                
                            except Exception as e:
                                # Ultimate fallback - very basic marker
                                folium.Marker(
                                    [row['latitude'], row['longitude']],
                                    popup=f"Profile #{idx + 1}",
                                    tooltip=f"Profile #{idx + 1}"
                                ).add_to(m)
                        
                        # Add optional enhanced features (won't break if they fail)
                        try:
                            from folium.plugins import Fullscreen
                            Fullscreen(position='topleft').add_to(m)
                        except:
                            pass
                        
                        # Display the map
                        map_data = st_folium(
                            m, 
                            use_container_width=True, 
                            height=500,
                            key=f"map_{chat_idx}_{len(df_map)}"
                        )
                        
                        # Show simple map interaction info
                        if map_data and map_data.get('last_object_clicked'):
                            st.success("🎯 Click on any marker to see detailed profile information!")
                        
                        # Enhanced Map statistics and features info
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"""
                            <div style='background: rgba(0, 198, 255, 0.1); padding: 0.8rem; border-radius: 8px; margin-top: 0.5rem;'>
                                <div style='font-weight: 600; color: #38bdf8; margin-bottom: 0.5rem; font-size: 0.95rem;'>📊 Map Statistics</div>
                                <div style='font-size: 0.85rem; color: #cbd5e1;'>
                                    📍 <strong>{len(df_map)}</strong> profiles displayed<br>
                                    🌐 Lat: <strong>{df_map['latitude'].min():.2f}°</strong> to <strong>{df_map['latitude'].max():.2f}°</strong><br>
                                    🌐 Lon: <strong>{df_map['longitude'].min():.2f}°</strong> to <strong>{df_map['longitude'].max():.2f}°</strong>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div style='background: rgba(0, 198, 255, 0.1); padding: 0.8rem; border-radius: 8px; margin-top: 0.5rem;'>
                                <div style='font-weight: 600; color: #38bdf8; margin-bottom: 0.5rem; font-size: 0.95rem;'>🛠️ Map Features</div>
                                <div style='font-size: 0.85rem; color: #cbd5e1;'>
                                    🔄 Multiple tile layers<br>
                                    📏 Distance measurement<br>
                                    🔍 Fullscreen & Mini map<br>
                                    🎯 Click markers for details
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)

# ----------------------
# Enhanced Footer
# ----------------------
st.markdown("""
<div class='footer'>
    <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;'>
        <div style='display: flex; align-items: center; gap: 1rem;'>
            <div style='font-size: 1.5rem;'>🌊</div>
            <div>
                <div style='font-weight: 600; font-size: 1.1rem;'>FloatChat</div>
                <div style='font-size: 0.9rem; color: #64748b;'>Advanced Ocean Data Intelligence Platform</div>
            </div>
        </div>
        <div style='display: flex; gap: 2rem; align-items: center;'>
            <div style='text-align: center;'>
                <div style='font-weight: 600; color: #38bdf8;'>SIH 2025</div>
                <div style='font-size: 0.8rem;'>Smart India Hackathon</div>
            </div>
            <div style='text-align: center;'>
                <a href='https://argo.ucsd.edu/' target='_blank' style='color: #38bdf8; text-decoration: none; font-weight: 500;'>
                    🔗 ARGO Project
                </a>
                <div style='font-size: 0.8rem; color: #64748b;'>Learn More</div>
            </div>
        </div>
    </div>
    <div style='margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(0, 198, 255, 0.2); text-align: center; font-size: 0.85rem; color: #64748b;'>
        Powered by RAG Technology • Real-time Ocean Data Analysis • Interactive Visualizations
    </div>
</div>
""", unsafe_allow_html=True)
