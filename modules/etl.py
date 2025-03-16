import altair as alt
import pandas as pd
import streamlit as st


def album_type_distro(album_df: pd.DataFrame):

    try:

        album_counts = album_df["Album Type"].value_counts()
        st.subheader("Album Types")
        st.bar_chart(album_counts, y_label="Count", x_label="Type")

    except Exception as e:
        st.error(
            f"🚨 Oops! Something went wrong while retrieving data. Try another search term. \n\nError: {e}"
        )


def album_type_over_time(album_df):

    try:
        # Ensure "Release Date" column is properly formatted
        album_df["Release Date"] = pd.to_datetime(
            album_df["Release Date"], errors="coerce"
        )

        # Extract Year
        album_df["Year"] = album_df["Release Date"].dt.year

        # Group by Year and Album Type, then count occurrences
        album_counts = (
            album_df.groupby(["Title", "Year", "Album Type"])
            .size()
            .reset_index(name="Count")
        )

        # Ensure there is valid data
        if album_counts.empty:
            st.warning("No valid data available for album types over time.")
            return

        # Create Altair Chart
        chart = (
            alt.Chart(album_counts)
            .mark_line(point=True)  # Line chart with points
            .encode(
                x=alt.X("Year:O", title="Year"),  # Discrete ordinal X-axis
                y=alt.Y("Count:Q", title="Number of Albums"),  # Quantitative Y-axis
                color="Album Type:N",  # Different colors for each album type
                tooltip=["Title", "Year", "Album Type", "Count"],  # Hover tooltips
            )
        )
        # Display in Streamlit
        st.subheader("Album Type Distribution Over Time")
        st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.error(
            f"🚨 Oops! Something went wrong while fetching data. Try another search term. \n\nError: {e}"
        )


def track_popularity(sorted_tracks_df, artist):

    # Get the min and max Popularity values
    min_popularity = sorted_tracks_df["Popularity"].min()
    max_popularity = sorted_tracks_df["Popularity"].max()

    chart = (
        alt.Chart(sorted_tracks_df)
        .mark_line(point=True, smooth=True)
        .encode(
            x=alt.X("Release Date:T", title="Release Date", timeUnit="yearmonth"),
            y=alt.Y(
                "Popularity:Q",
                title="Popularity",
                scale=alt.Scale(domain=[min_popularity, max_popularity]),
            ),
            tooltip=list(sorted_tracks_df.columns),
        )
    )

    st.altair_chart(chart, use_container_width=True)


def format_number(value):
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f} B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f} M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f} K"
    else:
        return str(value)
