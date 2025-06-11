from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the crop data into a Pandas DataFrame
crop_data = pd.read_csv('Crop_recommendation.csv')
crop_data.drop(['Unnamed: 8', 'Unnamed: 9'], axis=1, inplace=True)

# Define the home route
@app.route('/')
def home():
    return render_template('home.html')

# Define the recommendation route
@app.route('/recommend', methods=['POST'])
def recommend():

    def recommend_crop(input_values, crop_data):
        # Calculate the distance between the input values and each crop in the dataset
        distances = ((crop_data.iloc[:, :-1] - input_values)**2).sum(axis=1)
        
        # Find the index of the crop with the minimum distance
        min_index = distances.idxmin()
        
        # Return the label of the crop with the minimum distance
        recommended_crop = crop_data.loc[min_index, 'label']
        
        return recommended_crop

    # Get the input values from the form
    nitrogen = int(request.form['nitrogen'])
    phosphorus = int(request.form['phosphorus'])
    potassium = int(request.form['potassium'])
    temperature = float(request.form['temperature'])
    humidity = float(request.form['humidity'])
    ph = float(request.form['ph'])
    rainfall = float(request.form['rainfall'])

    # Call the recommend_crop function
    recommended_crop = recommend_crop([nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall], crop_data)

    # Render the recommendation template with the recommended crop
    return render_template('home.html', crop=recommended_crop)

if __name__ == '__main__':
    app.run(debug=True)
