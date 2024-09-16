from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load the CSV file
df = pd.read_csv('service_desk_data.csv')

# Perform Analysis
avg_tokens = df['TokenIssued'].mean()
avg_priority = df['PriorityNumbersAssigned'].mean()
avg_time_to_desk = df['TimeToServiceDesk(min)'].mean()
avg_service_time = df['ServiceCompletionTime(min)'].mean()
total_face_recognition_issues = df['FacialRecognitionIssues'].sum()
total_records = df.shape[0]
no_face_recognition_issues = max(total_records - total_face_recognition_issues, 0)

# Insights
insights = []

if avg_service_time > avg_tokens:  # Example insight condition
    insights.append("Insight: Service completion is taking longer than expected. Action: Investigate bottlenecks during service to reduce actual time taken.")

if total_face_recognition_issues > 0:
    insights.append("Insight: There are issues with facial recognition. Action: Improve system accuracy or manual fallback processes.")

if avg_time_to_desk > 7:
    insights.append("Insight: Customers are waiting too long to reach the service desk. Action: Consider adding more staff during peak times to reduce wait times.")

# Plotly Graphs
def create_plotly_graph():
    # Pie chart for Facial Recognition Issues
    fig1 = go.Figure(data=[go.Pie(
        labels=['No Issues', 'Issues'],
        values=[no_face_recognition_issues, total_face_recognition_issues],
        hole=0.3
    )])
    fig1.update_layout(title_text='Facial Recognition Issues')

    # Bar plot for Average Tokens Issued and Priority Numbers Assigned
    fig2 = go.Figure(data=[go.Bar(
        x=['Average Tokens Issued', 'Average Priority Numbers Assigned'],
        y=[avg_tokens, avg_priority],
        marker_color=['#66c2a5', '#fc8d62']
    )])
    fig2.update_layout(title_text='Average Tokens Issued and Priority Numbers Assigned')

    # Bar plot for Average Time to Reach Service Desk and Service Completion Time
    fig3 = go.Figure(data=[go.Bar(
        x=['Average Time to Reach Desk', 'Average Service Completion Time'],
        y=[avg_time_to_desk, avg_service_time],
        marker_color=['#8da0cb', '#e78ac3']
    )])
    fig3.update_layout(title_text='Average Time Metrics')

    # Comparison of Average ETA vs. Actual Time Taken
    avg_eta = df['ETA(min)'].mean()
    avg_actual_time = df['ActualTimeTaken(min)'].mean()
    fig4 = go.Figure(data=[go.Bar(
        x=['Average ETA', 'Average Actual Time Taken'],
        y=[avg_eta, avg_actual_time],
        marker_color=['#a6d854', '#ffd92f']
    )])
    fig4.update_layout(title_text='Average ETA vs. Actual Time Taken')

    # Convert figures to JSON
    graph1_json = pio.to_json(fig1)
    graph2_json = pio.to_json(fig2)
    graph3_json = pio.to_json(fig3)
    graph4_json = pio.to_json(fig4)

    return {
        'graphs': {
            'graph1': graph1_json,
            'graph2': graph2_json,
            'graph3': graph3_json,
            'graph4': graph4_json
        },
        'insights': insights
    }

@app.route('/data')
def data():
    data = create_plotly_graph()
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
