import ticketpy as tp
import streamlit as st
from datetime import datetime   
import pandas as pd

def get_events(tm_client, aritst):

    tm_client = tp.ApiClient(st.session_state["ticketmaster"])

    pages = tm_client.events.find(keyword=aritst)

    timeline_items = []

    for page in pages:
        for event in page:
            event_data = event.json  # Get the event JSON data

            # Extracting details
            # st.write(event_data)    
            artist_name = event_data.get("name")
            start_datetime = event_data.get("dates", {}).get("start", {}).get("dateTime", "No Start Time")
            end_datetime = event_data.get("dates", {}).get("end", {}).get("dateTime", "No End Time")
            # venue_name = event_data.get("_embedded", {}).get("venues").get("name", "Unknown Venue")
            venue_city = event_data.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name", "Unknown City")
            # venue_state = event_data.get("_embedded", {}).get("venues", [{}])[0].get("state", {}).get("name", "Unknown State")
            url = event_data.get("url")


        # Convert to YYYY-MM-DD format
            def format_date(date_str):
                if date_str:
                    try:
                        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
                    except ValueError:
                        return "Invalid Date"
                return None  # Return None if date is missing

            start_date = format_date(start_datetime)
            end_date = format_date(end_datetime) if end_datetime else start_date  # Default to start date if missing

            # Ensure valid start date
            if url:
                timeline_item = {
                    # "id": len(timeline_items) + 1,
                    "Event Title": artist_name,  # Display artist name
                    "Date": start_date,  # Start time in YYYY-MM-DD format
                    "City": venue_city,
                    "Ticketmaster Link": url
                    # "end": end_date  # End time in YYYY-MM-DD format
                    # "group": f"{venue_city}, {venue_state}",  # Grouping by location
                }
                timeline_items.append(timeline_item)

    event_df = pd.DataFrame(timeline_items)

    if not event_df.empty:
        # Display dataframe with clickable links
        st.markdown(f"### 🎟️ {aritst} Related Events")
        st.data_editor(event_df, column_config={"Ticketmaster Link": st.column_config.LinkColumn()})
    else:
        st.write("No events found.")