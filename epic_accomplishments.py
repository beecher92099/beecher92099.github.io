# This script automates the production of formatted html that can be pasted into an email sent out weekly
# to summarize the accomplishments of the team working on specific Jira Epics.
# It obtains the raw data from Excel files hosted on Sharepoint and sync'ed to the local
# machine running this script.  It parses out the necessary information and then produces the html
# summary in a file, which can be simply pasted into the weekly email.
# This script accomplishes in a few seconds what was previously taking several hours to complete manually.

import os
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import re

#os.chdir('C:\\Users\\beecher\\OneDrive - Cisco\\Documents\\Omega\\Backlog')
os.chdir('C:\\Users\\beecher\\Cisco\\Commerce Lifecycle Product Team - Commerce Lifecycle Product Team')

# Path to the Excel file
file_name = 'Weekly Update - Commerce Lifecycle.xlsx'

# Sheet name or index
sheet_name = 'Current Week'  # You can also use the sheet index, e.g., 0 for the first sheet

# Read the specified sheet into a DataFrame
df = pd.read_excel(file_name, sheet_name=sheet_name)

#We also need to read in Commerce Lifecycle PM Backlog - New.xlsx to get the focus areas
os.chdir('C:\\Users\\beecher\\Cisco\\Commerce Lifecycle Product Team - Backlog')
df2 = pd.read_excel('Commerce Lifecycle PM Backlog - New.xlsx', sheet_name='Offline Data')


#Retain only columns that are needed: 'Epic #', 'Epic Name', 'Commerce PM', 'Accomplishments'
df = df[['Epic #', 'Epic Name', 'Commerce PM', 'Accomplishments','Outcome Priority']]
df2 = df2[[' ItemID', 'Focus Area']] 

#Rename columns
df2.rename(columns={' ItemID':'Epic #'}, inplace=True)

#Merge the two dataframes on 'Epic #'
df = pd.merge(df, df2, on='Epic #', how='left')

# Replace string 'nan' with np.nan
df['Accomplishments'] = df['Accomplishments'].replace('nan', np.nan)

#Delete any rows where Accomplishments is NaN or nan
df = df.dropna(subset=['Accomplishments'])

#Set column 'Accomplishments' to string
df['Accomplishments'] = df['Accomplishments'].astype(str)

#Replace any value of 0 in 'Commerce PM' with 'No PM Assigned'
df['Commerce PM'] = df['Commerce PM'].replace(0, 'No PM Assigned')

#Set column 'One Cisco Backlog' as integer
df['Outcome Priority'] = df['Outcome Priority'].astype(int)

#Show unique values of 'Focus Area'
print(df['Focus Area'].unique())

#Remove any leading or trailing whitespace from 'Accomplishments'
#df['Accomplishments'] = df['Accomplishments'].str.strip()


focus_areas_order = [
        "Offers and Product Launch",
        "Business Model and RTM Enablement",
        "Subscription Lifecycle Management",
        "Commerce Experience",
        "Data, Policy & Compliance"
    ]

# Function to generate the email content in HTML format
def generate_email_content_html(df, focus_areas_order):
    email_content = "<html><body style='font-family: Calibri; font-size: 12px;'>"
    
    # Group the DataFrame by 'Focus Area'
    grouped_df = df.groupby('Focus Area')
    
    # Iterate through the Focus Areas in the specified order
    for focus_area in focus_areas_order:
        if focus_area in grouped_df.groups:
            email_content += f"<h2 style='color: green; font-size: 14px;'>Focus Area: {focus_area}</h2>"  # Add a header for each Focus Area with green color and size 14
            
            # Get the rows for the current Focus Area and sort by 'One Cisco Backlog'
            focus_area_df = grouped_df.get_group(focus_area).sort_values(by='Outcome Priority')
            
            for index, row in focus_area_df.iterrows():
                # First line in bold, wrapped in a div to align with bullet points
                email_content += f"<div style='margin-left: 20px;'><strong>{row['Epic Name']} - Epic {row['Epic #']}, Outcome #{row['Outcome Priority']}, {row['Commerce PM']}</strong></div>"
                #email_content += f"<div style='margin-left: 20px;'><strong>{row['Epic Name']} - Epic {row['Epic #']}, {row['Commerce PM']}</strong></div>"
                
                # Split the accomplishments by newline and add each as a bullet point
                accomplishments = row['Accomplishments'].split('\n')
                email_content += "<ul style='margin-top: 0;'>"
                for accomplishment in accomplishments:
                    # Strip any "- " prefix, "1. ", "2. ", etc., and remove empty lines
                    cleaned_accomplishment = re.sub(r'^\d+\.\s*|- ', '', accomplishment).strip()
                    if cleaned_accomplishment:
                        email_content += f"<li>{cleaned_accomplishment}</li>"
                email_content += "</ul>"
                
                # Blank line separating the next row
                email_content += "<br>"
    
    email_content += "</body></html>"
    return email_content

# Generate the email content
#email_content = generate_email_content(df, focus_areas_order)

# Print the email content
#print(email_content)

# Generate the email content in HTML format
email_content_html = generate_email_content_html(df, focus_areas_order)

os.chdir('C:\\Users\\beecher\\Cisco\\Commerce Lifecycle Product Team - Backlog')

# Save the HTML content to a file
with open("email_content.html", "w") as file:
    file.write(email_content_html)

#show value of first entry in Accomplishments
#print(df['Accomplishments'][1])

# Set the varible 'timestamp' to the current time
timestamp = pd.to_datetime(datetime.now()).tz_localize(None).strftime('%Y-%m-%d %H:%M:%S')

os.chdir('C:\\Users\\beecher\\OneDrive - Cisco\\Documents\\Omega\\Backlog')
#Write to a log file called 'log.txt' a timestamp and the number of rows loaded
with open('log.txt', 'a') as f:
    f.write(f"Epic Accomplishments: {timestamp}\n")

# Exit the script with a status code of 0
sys.exit(0)    
