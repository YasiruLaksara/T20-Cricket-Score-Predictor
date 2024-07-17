from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the model
pipe = pickle.load(open('pipe.pkl', 'rb'))

teams = [
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa', 
    'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka'
]

venues = ['Melbourne Cricket Ground', 'Bay Oval', 'Eden Park', 'The Rose Bowl',
 'Central Broward Regional Park Stadium Turf Ground',
 'Dubai International Cricket Stadium', 'Sheikh Zayed Stadium',
 'Sydney Cricket Ground', 'Westpac Stadium', 'Seddon Park',
 'Kensington Oval, Bridgetown', 'R Premadasa Stadium',
 'R.Premadasa Stadium, Khettarama', 'Old Trafford', 'SuperSport Park',
 'Newlands', 'Wankhede Stadium', 'Eden Gardens', 'Kingsmead',
 'Pallekele International Cricket Stadium', 'Zahur Ahmed Chowdhury Stadium',
 'New Wanderers Stadium', 'Kennington Oval', 'Trent Bridge',
 'Beausejour Stadium, Gros Islet', 'Shere Bangla National Stadium']

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        batting_team = request.form['batting_team']
        bowling_team = request.form['bowling_team']
        venue = request.form['venue']
        current_score = int(request.form['current_score'])
        overs = float(request.form['overs'])
        wickets = int(request.form['wickets'])
        last_five = int(request.form['last_five'])

        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        current_run_rate = current_score / overs

        input_df = pd.DataFrame(
            {'batting_team': [batting_team], 'bowling_team': [bowling_team], 'venue': [venue], 
             'current_score': [current_score], 'balls_left': [balls_left], 
             'wickets_left': [wickets], 'current_run_rate': [current_run_rate], 'last_five': [last_five]}
        )

        result = pipe.predict(input_df)
        prediction = int(result[0])

    return render_template('index.html', teams=sorted(teams), venues=sorted(venues), prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)