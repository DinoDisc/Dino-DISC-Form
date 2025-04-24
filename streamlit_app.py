import streamlit as st
import pandas as pd
import json

from user_details import input_user_details
from checkbox_change import on_change_checkbox
from save_selection import save_selections

from graph_most import plot_disc_graph_most
from graph_least import plot_disc_graph_least
from graph_change import plot_disc_graph_change

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from tabulate import tabulate
import smtplib
import streamlit as st

import matplotlib.pyplot as plt

# Load mappings from JSON file
with open('disc_mappings.json', 'r') as f:
    mappings = json.load(f)

# Extract all mappings dynamically
all_mappings = [mappings[f"mapping{i}"] for i in range(1, 25)]  # Adjust range based on the number of mappings in your JSON

# Initialize session state to store user details and selections
if 'user_details' not in st.session_state:
    st.session_state.user_details = {
        "name": "",
        "user_email": "",
        "date_of_birth": None,
        "gender": ""
    }

# Initialize session state to store selections
if 'most_likely' not in st.session_state:
    st.session_state.most_likely = [None] * len(all_mappings)

if 'least_likely' not in st.session_state:
    st.session_state.least_likely = [None] * len(all_mappings)

if 'disc_scores_most' not in st.session_state:
    st.session_state.disc_scores_most = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

if 'disc_scores_least' not in st.session_state:
    st.session_state.disc_scores_least = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

if 'current_section' not in st.session_state:
    st.session_state.current_section = 0  # Start at the first section

if 'same_option_error' not in st.session_state:
    st.session_state.same_option_error = False  # Initialize error flag

if 'user_selections' not in st.session_state:
    st.session_state.user_selections = []
    
if 'assessment_completed' not in st.session_state:
    st.session_state.assessment_completed = False  # Initialize assessment completion status

# Initialize the keys for checkboxes
st.session_state.checkbox_keys = [[[], []] for _ in all_mappings]  # Adjust lists based on the number of mappings

def auto_mail_results(user_name, user_email):
    # Access secrets from the secrets.toml file
    me = st.secrets["email"]["me"]
    password = st.secrets["email"]["password"]
    you = st.secrets["email"]["you"]
    server = st.secrets["email"]["server"]

    # Prepare DISC data for the table
    data = [
        ["Category", "D", "I", "S", "C", "*", "Total"],
        ["Most Likely", st.session_state.disc_scores_most['D'], st.session_state.disc_scores_most['I'], st.session_state.disc_scores_most['S'], st.session_state.disc_scores_most['C'], st.session_state.disc_scores_most['*'], sum(st.session_state.disc_scores_most.values())],
        ["Least Likely", st.session_state.disc_scores_least['D'], st.session_state.disc_scores_least['I'], st.session_state.disc_scores_least['S'], st.session_state.disc_scores_least['C'], st.session_state.disc_scores_least['*'], sum(st.session_state.disc_scores_least.values())],
        ["Difference", st.session_state.disc_scores_most['D'] - st.session_state.disc_scores_least['D'], st.session_state.disc_scores_most['I'] - st.session_state.disc_scores_least['I'], st.session_state.disc_scores_most['S'] - st.session_state.disc_scores_least['S'], st.session_state.disc_scores_most['C'] - st.session_state.disc_scores_least['C'], "-", (st.session_state.disc_scores_most['D'] - st.session_state.disc_scores_least['D']) + (st.session_state.disc_scores_most['I'] - st.session_state.disc_scores_least['I']) + (st.session_state.disc_scores_most['S'] - st.session_state.disc_scores_least['S']) + (st.session_state.disc_scores_most['C'] - st.session_state.disc_scores_least['C'])]
    ]

    # Create plain text and HTML versions of the message
    text = f"""
    This is confirmation of the completion of the DISC Assessment by {user_name}.
    
    Contact {user_name} email: {user_email}.
    Date of Birth: {st.session_state.user_details['date_of_birth']}
    Gender: {st.session_state.user_details['gender']}
    
    DISC Results:

    {tabulate(data, headers="firstrow", tablefmt="grid")}

    """

    html = f"""
    <html><body><p>This is confirmation of the completion of the DISC Assessment by {user_name}.</p>
    <p>Email: {st.session_state.user_details['user_email']}</p>
    <p>Date of Birth: {st.session_state.user_details['date_of_birth']}</p>
    <p>Gender: {st.session_state.user_details['gender']}</p>
    {tabulate(data, headers="firstrow", tablefmt="html")}
    <p>See attached images for the plotted DISC scores:</p>
    <img src="cid:image1"><br>
    </body></html>
    """

    # Construct the email
    message = MIMEMultipart("related")
    message['Subject'] = f"DISC Assessment Results | {user_name}"
    message['From'] = me
    message['To'] = you

    # Attach text and HTML versions of the email
    message_alternative = MIMEMultipart("alternative")
    message.attach(message_alternative)
    message_alternative.attach(MIMEText(text, 'plain'))
    message_alternative.attach(MIMEText(html, 'html'))
    
    # Create a single figure with three subplots
    fig, axs = plt.subplots(1, 3, figsize=(6.5, 2.25), dpi=200)

    values_most = [int(score) for score in most_likely_scores]  
    values_least = [int(score) for score in least_likely_scores]
    values_change = [int(score) for score in difference_scores]

    # Plot each graph on its respective axis
    plot_disc_graph_most(values_most, axs[0])
    plot_disc_graph_least(values_least, axs[1])
    plot_disc_graph_change(values_change, axs[2])
    
    # Save the combined figure
    fig.tight_layout()  # Adjust layout to prevent overlap
    fig.savefig('/tmp/all_disc_graphs.png')
    plt.close(fig)  # Close the figure properly after saving

    # Attach the combined image to the email
    file_path = '/tmp/all_disc_graphs.png'
    cid = 'image1'
    with open(file_path, 'rb') as img_file:
        img = MIMEImage(img_file.read())
        img.add_header('Content-ID', f'<{cid}>')
        message.attach(img)

    # Send the email
    smtp_server = smtplib.SMTP(server)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(me, password)
    smtp_server.sendmail(me, you, message.as_string())
    smtp_server.quit()
    print('Email sent successfully')
    

# Calculate DISC scores after saving selections
def calculate_disc_scores():
    # Initialize DISC scores
    st.session_state.disc_scores_most = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}
    st.session_state.disc_scores_least = {"D": 0, "I": 0, "S": 0, "C": 0, "*": 0}

    # Loop through saved selections to calculate DISC scores
    for selection in st.session_state.user_selections:
        idx = selection["section"]
        most_option = selection["most_likely"]
        least_option = selection["least_likely"]

        most_disc_type = all_mappings[idx][most_option]["most"]
        least_disc_type = all_mappings[idx][least_option]["least"]

        st.session_state.disc_scores_most[most_disc_type] += 1  # Increment for Most Likely
        st.session_state.disc_scores_least[least_disc_type] += 1  # Increment for Least Likely

# Show the form or the result depending on the assessment completion status
if st.session_state.current_section == 0:
    input_user_details()  # First, prompt the user to fill in their details
elif not st.session_state.assessment_completed:
    idx = st.session_state.current_section - 1  # Adjust the section index because the first section is user details
    mapping = all_mappings[idx]

# Calculate progress
    progress = f"{idx + 1}/{len(all_mappings)}"

    # Create the table layout with checkboxes
    st.write(f"### DISC Personality Assessment ({progress})")
    st.write("""Choose the option which best reflects your personality. Select one option as the **most likely** and one option as the **least likely**.""")
    st.write("""This form should be completed within **7 minutes**, or as close to that as possible.""")

    col1, col2, col3 = st.columns([1, 1, 5])

    with col1:
        st.write("**Most Likely**")
        for option in mapping.keys():
            key = f"most_{idx}_{option}"
            st.checkbox("", key=key, on_change=on_change_checkbox, args=(key, idx, 0))
            st.session_state.checkbox_keys[idx][0].append(key)

    with col2:
        st.write("**Least Likely**")
        for option in mapping.keys():
            key = f"least_{idx}_{option}"
            st.checkbox("", key=key, on_change=on_change_checkbox, args=(key, idx, 1))
            st.session_state.checkbox_keys[idx][1].append(key)

    with col3:
        st.write("**Options**")
        for option in mapping.keys():
            st.write(option)

    # Display the same option error message
    if st.session_state.same_option_error:
        st.error("You cannot select the same option for both 'Most Likely' and 'Least Likely'. Please choose different options.")

    # Validation and Submission
    most_likely_selected = any(st.session_state.get(key) for key in st.session_state.checkbox_keys[idx][0])
    least_likely_selected = any(st.session_state.get(key) for key in st.session_state.checkbox_keys[idx][1])

    if most_likely_selected and least_likely_selected:
        if idx < len(all_mappings) - 1:
            # Handle button click before rerendering the UI
            if st.button("Next"):
                save_selections(idx)
                st.session_state.current_section += 1
                st.rerun()  # Force a rerun to immediately update the section
        else:
            if st.button("Submit"):
                save_selections(idx)
                # Reset DISC scores before calculation
                calculate_disc_scores()
                st.session_state.assessment_completed = True
                st.rerun()  # Force a rerun to display the result
    else: 
        st.error("Please make a selection for both 'Most Likely' and 'Least Likely' options.")
# ...

else:
    # Calculate the sum for each row
    sum_most = sum(st.session_state.disc_scores_most.values())
    sum_least = sum(st.session_state.disc_scores_least.values())

    # Calculate the difference between Most Likely and Least Likely (excluding the * column)
    diff_D = st.session_state.disc_scores_most["D"] - st.session_state.disc_scores_least["D"]
    diff_I = st.session_state.disc_scores_most["I"] - st.session_state.disc_scores_least["I"]
    diff_S = st.session_state.disc_scores_most["S"] - st.session_state.disc_scores_least["S"]
    diff_C = st.session_state.disc_scores_most["C"] - st.session_state.disc_scores_least["C"]
    diff_total = diff_D + diff_I + diff_S + diff_C

    # Prepare data for the table including the sum and difference row
    data = {
        "Category": ["Most Likely", "Least Likely", "Difference"],
        "D": [st.session_state.disc_scores_most["D"], st.session_state.disc_scores_least["D"], diff_D],
        "I": [st.session_state.disc_scores_most["I"], st.session_state.disc_scores_least["I"], diff_I],
        "S": [st.session_state.disc_scores_most["S"], st.session_state.disc_scores_least["S"], diff_S],
        "C": [st.session_state.disc_scores_most["C"], st.session_state.disc_scores_least["C"], diff_C],
        "*": [st.session_state.disc_scores_most["*"], st.session_state.disc_scores_least["*"], "-"],  # Exclude * from Difference calculation
        "Total": [sum_most, sum_least, diff_total]  # Add the sum as the final column
    }

    df = pd.DataFrame(data)
        
    # Plot the line graphs
    categories = ["D", "I", "S", "C"]
    most_likely_scores = [st.session_state.disc_scores_most[cat] for cat in categories]
    least_likely_scores = [st.session_state.disc_scores_least[cat] for cat in categories]
    difference_scores = [diff_D, diff_I, diff_S, diff_C]
    
    # Thank you message
    user_name = st.session_state.user_details['name']
    user_email = st.session_state.user_details['user_email']
    auto_mail_results(user_name, user_email)
    st.write(f"### Thank you, {user_name}, for completing the assessment!")
    st.write(f"Your results have been sent to Dino. He will be in contact through {user_email}.")
    st.write("If you have any questions, do not hesitate to reach out at: dino.grif@gmail.com .") 
