import streamlit as st
from datetime import date, datetime

# Function to handle the first section for user details
def input_user_details():
    # Create the table layout with checkboxes
    st.write(f"### DISC Personality Assessment")
    st.write("""Your Payment has been processed! For any queries, please contact dino.grif@gmail.com""")
    st.write("### Please fill in your details")
    
    # Collect user details
    st.session_state.user_details['name'] = st.text_input("Name *", st.session_state.user_details['name'])
    st.session_state.user_details['user_email'] = st.text_input("Email *", st.session_state.user_details['user_email'])
    # Add the date of birth input
    st.session_state.user_details['date_of_birth'] = st.date_input(
    "Date of Birth", 
    st.session_state.user_details['date_of_birth'], 
    min_value=datetime(1900, 1, 1),  # Allow dates from January 1, 1900
    max_value=datetime.today(),  # Set the maximum date to today
    format="MM/DD/YYYY" 
    )
    st.session_state.user_details['gender'] = st.radio(
        "Gender", options=["Male", "Female"], index=0)
    
    # Always display the Next button
    next_button_clicked = st.button("Next")
    
    # Check if the Next button was clicked without a name provided
    if next_button_clicked and not st.session_state.user_details['name'] or not st.session_state.user_details['user_email']:
        st.error("Name and Email is required to proceed.")
    elif next_button_clicked:
        st.session_state.current_section = 1  # Move to the first question of the DISC assessment
        st.rerun()
    
