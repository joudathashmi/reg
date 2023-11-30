# Real Estate Market Analyzer - DVA Group 77

DESCRIPTION

Welcome to the the Real Estate Market Analyzer,  a powerful, web-based tool designed for the Greater Sydney region. Our interactive visualization provides valuable insights into historical real estate purchasing trends and offers personalized suburb recommendations tailored to user preferences. These preferences encompass crucial factors such as safety, demographics, transportation, education, health, and development.

Key Features:
Suburb Facts - Explore detailed information about each suburb in the Greater Sydney region. Click on specific suburbs to access a comprehensive overview, including median income, area size, and population.

Network Graph - Visualize a network graph showcasing suburbs and their nearest neighbors. Gain a deeper understanding of suburb relationships based on Euclidean distance.

Liveability Ratings - Dive into liveability metrics derived from surveys and various data sources. Evaluate each suburb's standing in terms of safety, demographics, transportation, education, health, and development.

The root directory of our code repository contains app.py. This is the key file which integrates data from below sources.

| Source File                | Description                                                                                                                     | 
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| simplified_updated.geojson | A GeoJSON file that contains shape files for all Sydney suburbs which are sourced from NSW and reduced in size using QGIS.      |
| liveability.csv            | A CSV file that contains liveability metrics for all suburbs that are consolidated using surveys and other data sources         |
| similar_suburbsJ.csv       | A CSV file that contains nearest five suburbs for each Sydney suburb using Euclidean distance                                   |   
| domain_properties.csv      | A CSV file that contains factual details for all Sydney suburbs (https://www.kaggle.com/datasets/alexlau203/sydney-house-rices).|


Data is read directly from the mentioned files in app.py, which is built in Streamlit.


INSTALLATION - A live version of our project is already available here: https://cse6242projectteam77.streamlit.app/. To run the project locally, follow these steps:

### Step 1: Download Data Files

Download the required data files and include them in the root directory of the CODE repository, i.e., in the same location as `app.py`.

### Step 2: Create Virtual Environment (Optional)

It is recommended to create a virtual environment before installing dependencies. Execute the following commands to create and activate a virtual environment named `myenv`:

------------------------------------------------------
python -m venv myenv
source myenv/bin/activate      # For Unix or MacOS
.\myenv\Scripts\activate       # For Windows
------------------------------------------------------

### Step 3: Install Dependencies

Install the necessary dependencies by running the following command in your terminal. Ensure you have the latest versions of pandas, numpy, scipy, scikit-learn, streamlit, streamlit-folium, matplotlib, and networkx. You can use either pip or conda for installation. Alternatively, use the provided `requirements.txt` file for a local Python environment.

------------------------------------------------------
pip install -r requirements.txt
------------------------------------------------------

### Step 4: Run the Project

From your terminal, execute the following command to run the Streamlit app and generate the required visualizations:

------------------------------------------------------
streamlit run app.py
------------------------------------------------------

### Step 5 (Optional): Set Up Local Python Server

If needed, set up a local Python server from the project directory using the following terminal command. Make sure to run this command from the root directory, i.e., the same directory as `app.py`.

------------------------------------------------------
python -m http.server 8000
------------------------------------------------------

### Step 6: View the Visualization

Open your browser and navigate to [http://localhost:8501/](http://localhost:8501/) to observe the visualization locally.

EXECUTION - Open your web browser and navigate to http://localhost:8501/ to explore the visualization. The app will display three tabs:

Select your suburb: Explore the map and facts about a selected suburb.
Suburbs similar to your choice: View a network graph of suburbs similar to the selected suburb.
Liveability Rating of Suburb: Visualize liveability metrics and a scatter chart for the selected suburb.

Note: Ensure you click on the suburb on the map in the first tab to view further details. This will allow the user to interact with the suburbs map, which is integrated with the network graph and liveability metrics. 

Interact with the Visualizations - In the first tab, adjust the budget range using the slider to filter suburbs based on median income. Explore liveability metrics and scatter charts in the third tab.

Enjoy exploring our project!










