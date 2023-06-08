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
    else:
        df = pd.read_csv('heatmap_coordinate_data.csv')
    geojson_data = data_to_geojson(df)
    return jsonify(geojson_data)

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