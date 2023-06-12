from flask import Flask, jsonify, render_template
import pandas as pd
import geojson
from sklearn.preprocessing import MinMaxScaler
import random
from csvloader import main
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


def data_to_geojson(df):
    features = []
    for _, row in df.iterrows():
        geometry = geojson.Point((row["Longitude"], row["Latitude"]))
        properties = row.to_dict()
        properties.pop("Longitude")
        properties.pop("Latitude")
        features.append(geojson.Feature(geometry=geometry, properties=properties))

    return geojson.FeatureCollection(features)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate-data', methods=['GET', 'POST'])
def generate_data():
    if request.method == 'POST':
        toggles = request.get_json()
        print(toggles)
        df = main(toggles)
        if 8 in toggles:
            df_cluster = pd.read_csv('updated_with_state_icu_normalized.csv')
            #Map this based on latitude, longitude, hospital name and show all other details like the previous implementation

            #Logic for the toggle: toggle is passed into main(toggles) and elements other than 
            #8 and 9 are used to generate the heatmap
            #For values 8 and 9, checks are placed to add marker clusters based on the presence of 8
            #For 9, we would like to display an interactive list on the side which can be clicked on
            #and that would lead to the actual pin being highlighted
            #For questions on how what should be included as the marker clusters, refer to the
            #Original heatmap implementation and do something similar for mapbox's frontend
            #updated_with_state_icu_normalized has data for the marker clusters
            geojson_data_cluster = data_to_geojson(df_cluster)
            return jsonify({'main': data_to_geojson(df), 'cluster': geojson_data_cluster})
        else:
            return jsonify({'main': data_to_geojson(df), 'cluster': None})
    else:
        df = pd.read_csv('heatmap_coordinate_data.csv')
        return jsonify({'main': data_to_geojson(df), 'cluster': None})

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/generate-hospital-data')
def generate_hospital_data():
    df = pd.read_csv('updated_with_state_icu_normalized.csv')
    # Convert DataFrame to GeoJSON
    geojson_data = data_to_geojson(df)

    return jsonify(geojson_data)


if __name__ == '__main__':
    app.run(debug=True)