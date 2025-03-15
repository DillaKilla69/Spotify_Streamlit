import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

def album_type_distro(df):
    album_counts = df["Album Type"].value_counts()

    st.bar_chart(album_counts, y_label='Count', x_label='Type')







    # Count albums by type
    # album_counts = df["Album Type"].value_counts()

    # # Plot bar chart
    # fig, ax = plt.subplots()
    # album_counts.plot(kind="bar", ax=ax, color=["blue", "green", "red"])
    # ax.set_title("Distribution of Album Types")
    # ax.set_ylabel("Count")
    # ax.set_xlabel("Album Type")

    # st.pyplot(fig)

def track_popularity(sorted_tracks_df, artist):
    
    # Get the min and max Popularity values
    min_popularity = sorted_tracks_df["Popularity"].min()
    max_popularity = sorted_tracks_df["Popularity"].max()

    chart = (
        alt.Chart(sorted_tracks_df)
        .mark_line(point=True, smooth=True)
        .encode(
            x=alt.X(
                "Release Date:T", 
                title="Release Date",
                timeUnit='yearmonth'),
            y=alt.Y(
                "Popularity:Q",
                title="Popularity",
                scale=alt.Scale(
                    domain=[min_popularity, max_popularity]
                ), 
            ),
            tooltip=list(sorted_tracks_df.columns),
        )
        .properties(title=f"{artist} Track Popularity by Release Date")
    )

    st.altair_chart(chart, use_container_width=True)