from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

teams = []
fixtures = []
results = {}
points_table = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    global teams, fixtures, points_table

    if request.method == 'POST':
        team_names = request.form.get('teams').split(',')
        teams = [t.strip() for t in team_names if t.strip()]
        fixtures = [(a, b) for i, a in enumerate(teams) for j, b in enumerate(teams) if i < j]
        points_table = {team: {'P': 0, 'W': 0, 'D': 0, 'L': 0, 'Pts': 0} for team in teams}
        return redirect(url_for('table'))
    return render_template('index.html')

@app.route('/table', methods=['GET', 'POST'])
def table():
    global results, points_table

    if request.method == 'POST':
        team1 = request.form['team1']
        team2 = request.form['team2']
        score1 = int(request.form['score1'])
        score2 = int(request.form['score2'])

        if (team1, team2) not in results:
            points_table[team1]['P'] += 1
            points_table[team2]['P'] += 1

            if score1 > score2:
                points_table[team1]['W'] += 1
                points_table[team2]['L'] += 1
                points_table[team1]['Pts'] += 3
            elif score1 < score2:
                points_table[team2]['W'] += 1
                points_table[team1]['L'] += 1
                points_table[team2]['Pts'] += 3
            else:
                points_table[team1]['D'] += 1
                points_table[team2]['D'] += 1
                points_table[team1]['Pts'] += 1
                points_table[team2]['Pts'] += 1

            results[(team1, team2)] = (score1, score2)

    sorted_table = sorted(points_table.items(), key=lambda x: x[1]['Pts'], reverse=True)
    return render_template('table.html', fixtures=fixtures, table=sorted_table)
