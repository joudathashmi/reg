import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import folium
from streamlit_folium import folium_static
from matplotlib.ticker import FuncFormatter

# Create a Streamlit app
APP_TITLE = 'Real Estate Market Guide'

st.set_page_config(
    layout = 'wide',
    page_title=APP_TITLE,
    page_icon=":house:",
    #vertical_scroll="none" 
)

st.title(APP_TITLE)

APP_SUB_TITLE = 'Sydney Suburb Data Visualization'

DEFAULT_SUBURB = "Sydney"

def display_map(df):

    map = folium.Map(location=[-33.86, 151.209], zoom_start=10, scrollWheelZoom=False, tiles='CartoDB positron')  
    
    choropleth = folium.Choropleth(
        geo_data='data/simplified_updated.geojson',
        data=df,
        columns=('suburb', 'is_below_threshold'),  # Use the new property
        key_on='feature.properties.LOC_NAME',
        line_opacity=0.8,
        fill_color='YlGn',  # Adjust the color palette as needed
        fill_opacity=0.7,
        legend_name='Suburb Median Income',
        highlight=True,
    )
    choropleth.geojson.add_to(map)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['LOC_NAME'], labels=False)
    )  

    st_map = st_folium(map, width=700, height=450)

    state_name = ''
    if st_map['last_active_drawing']:
        state_name = st_map['last_active_drawing']['properties']['LOC_NAME']
    return state_name

def display_facts(df, year, quarter, report_type, state_name, field, title, string_format='${:,}', is_median=False):
    df = df[(df['Year'] == year) & (df['Quarter'] == quarter)]
    df = df[df['Report Type'] == report_type]
    if state_name:
        df = df[df['State Name'] == state_name]
    df.drop_duplicates(inplace=True)
    if is_median:
        total = df[field].sum() / len(df[field]) if len(df) else 0
    else:
        total = df[field].sum()
    st.metric(title, string_format.format(round(total)))

def prepare_data_for_line_chart(df, suburb_name):
    # Filter data for the selected suburb
    selected_suburb_data = df[df['suburb'] == suburb_name]
    
    # Group by year and calculate median house price
    median_price_by_year = selected_suburb_data.groupby('Year')['price'].median().reset_index()
    median_price_by_year['Year'] = median_price_by_year['Year'].astype(int)
    return median_price_by_year

def create_bar_chart(df,selected_suburb):
    suburb_data = df[df['suburb'] == selected_suburb]

    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots(figsize=(8, 5))
    columns = df.columns[2:]  # Exclude the 'suburb' column
    values = suburb_data.iloc[0][2:]  # Exclude the 'suburb' column
    ax.barh(columns, values)

    # Customize the layout of the bar chart

    ax.set_xlabel('Metrics')
    ax.set_ylabel('Value')
    ax.set_title(f'Liveability Metrics for {selected_suburb}')

    return plt

def create_scatter_chart(df, selected_suburb):
    # Filter the DataFrame for the selected suburb
    suburb_data = df[df['suburb'] == selected_suburb]

    # Create the scatter plot using Matplotlib
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.scatter(df['Liveability'], df['Median Price'], label='Other Suburbs', alpha=0.7)
    ax.scatter(suburb_data['Liveability'], suburb_data['Median Price'], label=selected_suburb, color='red', marker='o', s=100)
    ax.set_xlabel('Liveability')
    ax.set_ylabel('Median Price')
    ax.set_title(f'Scatter Chart: Liveability vs. Price for {selected_suburb}')
    ax.legend()
        # Customize the y-axis label format to display values in millions
    formatter = FuncFormatter(lambda x, _: f'{int(x / 1e6)}M')
    ax.yaxis.set_major_formatter(formatter)

    return fig

# Define a function to get the "km from cbd" for a given suburb
def get_km_from_cbd(suburb_name, df):
    if suburb_name:
        suburb_data = df[df['suburb'] == suburb_name]
        if not suburb_data.empty:
            return suburb_data.iloc[0]['km_from_cbd']
    # Return the default value if suburb not found or not selected
    return "0.31"  

# Define a function to get the "suburb_sqkm" for a given suburb
def get_suburb_sqkm(suburb_name, df):
    if suburb_name:
        suburb_data = df[df['suburb'] == suburb_name]
        if not suburb_data.empty:
            return suburb_data.iloc[0]['suburb_sqkm']
    # Return the default value if suburb not found or not selected
    return "2.94"  

# Define a function to get the "suburb_population" for a given suburb
def get_suburb_population(suburb_name, df):
    if suburb_name:
        suburb_data = df[df['suburb'] == suburb_name]
        if not suburb_data.empty:
            return suburb_data.iloc[0]['suburb_population']
    # Return the default value if suburb not found or not selected
    return "17,252"  

def load_network_data():
    df = pd.read_csv('data/similar_suburbsJ.csv')  
    return df

def create_network_graph(df, selected_suburb):
    # Create a NetworkX graph
    G = nx.Graph()

    # Add nodes and edges 
    for index, row in df.iterrows():
        suburb = row['suburb']
        nearest_suburbs = row['nearest_suburbs'].split(',')
        for neighbor in nearest_suburbs:
            G.add_edge(suburb, neighbor)

    # Define positions for nodes using a custom layout (you can experiment with different layouts)
    pos = nx.spring_layout(G, seed=42)

    # Create a Plotly figure for the network graph
    fig = go.Figure()

    # Add nodes to the figure
    for node, (x, y) in pos.items():
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", text=node, marker=dict(size=10)))

    # Add edges to the figure
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines"))

    # Customize the layout and appearance of the graph
    fig.update_layout(
        showlegend=False,
        hovermode="closest",
        title=f"Network Graph for {selected_suburb}",
        title_x=0.5,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )

    return fig

def create_network_graph_matplotlib(df, selected_suburb):
    # Create a NetworkX graph
    G = nx.Graph()

    # Add nodes and edges
    for index, row in df.iterrows():
        suburb = row['suburb']
        nearest_suburbs = row['nearest_suburbs'].split(',')
        for neighbor in nearest_suburbs:
            G.add_edge(suburb, neighbor)

    # Define positions for nodes using a custom layout (you can experiment with different layouts)
    pos = nx.spring_layout(G, seed=42)

    # Create a Matplotlib figure for the network graph
    plt.figure(figsize=(10, 10))

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=100, node_color='blue', alpha=0.7)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5)

    # Add labels for nodes
    labels = {node: node for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=6, font_color='black')

    # Customize the appearance of the graph
    plt.title(f"Network Graph for {selected_suburb}")
    plt.axis('off')

    # Save the Matplotlib figure or display it in  Streamlit app
    # You can save it to a file using plt.savefig('network_graph.png')
    # Or display it in  Streamlit app using plt.show()

    return plt



def main():

    tab1, tab2, tab3 = st.tabs(["Select your suburb", "Suburbs similar to your choice","Liveability Rating of Suburb"])

    with tab1:
        #st.set_page_config(APP_TITLE)
        col1, col2 = st.columns(2)

        # Load Sydney suburb GeoJSON data
        #with open("data/syd.json", "r") as json_file:
        #    data = json.load(json_file)

        csv_data = pd.read_csv("data/domain_properties.csv")
        csv_data['Date'] = pd.to_datetime(csv_data['date_sold'])  # Convert the date column to datetime

        with col1:
            #st.slider("Select your budget range", 0, 100000, 50)
            median_income_threshold = st.slider("Budget Range", 150000, 100000, 16000)
            csv_data['is_below_threshold'] = csv_data['suburb_median_income'] < median_income_threshold
            st.write("Click suburb on map to explore further")
            #st.write("")
            suburb_name = display_map(csv_data)

        with col2:
            #Display Metrics
            suburb_to_display = suburb_name if suburb_name else DEFAULT_SUBURB
            st.subheader(f'{suburb_to_display} Facts')
            # Get the "km from cbd" value
            km_from_cbd = get_km_from_cbd(suburb_name, csv_data)
            st.info(f'Distance(km) from CBD: {km_from_cbd}')

            # Get the "km from cbd" value
            suburb_sqkm = get_suburb_sqkm(suburb_name, csv_data)
            st.info(f'Suburb Area: {suburb_sqkm}')

            # Get the "suburb_population" value
            suburb_population = get_suburb_population(suburb_name, csv_data)
            st.info(f'Population: {suburb_population}')

            suburb_to_display = suburb_name if suburb_name else DEFAULT_SUBURB
            median_price_data = prepare_data_for_line_chart(csv_data, suburb_to_display)
            # Create the line chart
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(median_price_data['Year'], median_price_data['price'], marker='o')
            ax.set_xlabel('Year')
            ax.set_ylabel('Median House Price')
            ax.set_title(f'Median House Price in {suburb_to_display} Over the Years')
            formatter = FuncFormatter(lambda x, _: f'{int(x / 1e6)}M')
            ax.yaxis.set_major_formatter(formatter)
            # Display the line chart in col2
            st.pyplot(fig) 

    with tab2:
        df = load_network_data()

        # Filter the data to include only the selected or default suburb
        suburb_to_display = suburb_name if suburb_name else DEFAULT_SUBURB
        selected_suburb_data = df[(df['suburb'] == suburb_to_display) | (df['nearest_suburbs'].str.contains(suburb_to_display))]

        # Display the network graph
        if not selected_suburb_data.empty:
            #network_graph = create_network_graph(selected_suburb_data, suburb_to_display)
            #st.plotly_chart(network_graph)
            network_graph = create_network_graph_matplotlib(selected_suburb_data, suburb_to_display)
            st.pyplot(network_graph)
    
    with tab3:
        col1, col2 = st.columns(2)

        with col1:
            # Loading data for the bar chart
            data_for_bar_chart = pd.read_csv("data/liveability.csv")

            if not suburb_name:
                suburb_name = "Sydney"

            # Display the selected suburb
            #st.write(f"Selected Suburb: {suburb_name}")

            # Display the bar chart for the selected suburb
            bar_chart = create_bar_chart(data_for_bar_chart, suburb_name)
            st.pyplot(bar_chart)
        
        with col2:
            if not suburb_name:
                suburb_name = "Sydney"

            # Display the selected suburb
            #st.write(f"Selected Suburb: {suburb_name}")

            # Display the bar chart for the selected suburb
            scatter_chart = create_scatter_chart(data_for_bar_chart, suburb_name)
            st.pyplot(scatter_chart)
    

if __name__ == "__main__":
    main()


