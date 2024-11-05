import plotly_express as px
# Create the choropleth map

def create_map(df):
    
    fig = px.choropleth(
        data_frame=df,
        locations="country_iso_3",  
        locationmode='ISO-3',  
        color="is_present",
        color_continuous_scale="Blues",
        hover_name="available_markets",
        title="Countries Present in Dataset"
    )