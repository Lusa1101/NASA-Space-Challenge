import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from fpdf import FPDF
import base64
import functions

# Load moon and mars data
moon_data = pd.read_csv(r'C:\Users\omphu\Documents\Datasets\space_apps_2024_seismic_detection\data\lunar\training\data\S12_GradeA\second.csv')
moon_good_data = functions.good_data(moon_data, 'velocity(m/s)')

mars_data = pd.read_csv(r'C:\Users\omphu\Documents\Datasets\space_apps_2024_seismic_detection\data\mars\training\data\XB.ELYSE.02.BHV.2022-01-02HR04_evid0006.csv')
#mars_good_data = filter.good_data(mars_data, 'velocity(c/s)')

# Initialize Dash app with Bootstrap for better styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Utility function to create a downloadable PDF report
def generate_pdf_report(data_summary, selected_event, planet):
    pdf = FPDF()
    pdf.add_page()

    # Add Title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="Seismic Report", ln=True, align='C')

    # Add Event Type and Planet
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt=f"Planet: {planet.title()}", ln=True)

    # Add Data Summary
    pdf.set_font('Arial', '', 12)
    pdf.ln(10)
    for stat_name, stat_value in data_summary.items():
        pdf.cell(200, 10, txt=f"{stat_name}: {stat_value:.2f}", ln=True)

    # Save PDF to file
    pdf.output('seismic_report.pdf')

# Layout of the app
app.layout = html.Div(children=[
    # Main Header
    html.H1("NASA SPACE APPS CHALLENGE HACKATHON",
            style={'text-align': 'center', 'color': 'white', 'font-family': 'Arial',
                   'background-color': '#1f3b4d', 'padding': '20px', 'border-radius': '5px'}),

    # Sub Header
    html.H2("Seismic Detection Across the Solar System",
            style={'text-align': 'center', 'color': '#FFFFFF', 'font-family': 'Arial',
                   'background-color': '#2e5766', 'padding': '10px', 'margin-top': '0'}),

    # Background galaxy image
    html.Div([
        html.Label("Select Planet:", style={'color': 'white', 'font-size': '16px', 'font-family': 'Arial'}),
        dcc.Dropdown(
            id='planet-dropdown',
            options=[
                {'label': 'Moon', 'value': 'moon'},
                {'label': 'Mars', 'value': 'mars'}
            ],
            value='moon',  # Default value
            style={'width': '60%', 'margin': 'auto', 'border-radius': '5px'}
        )
    ], style={'width': '100%', 'text-align': 'center', 'margin-top': '20px'}),

    # Two graphs side by side
    html.Div([
        dcc.Graph(id='graph1', style={'display': 'inline-block', 'width': '48%', 'border-radius': '10px'}),
        dcc.Graph(id='graph2', style={'display': 'inline-block', 'width': '48%', 'border-radius': '10px'})
    ], style={'background-color': '#1c1e29', 'padding': '20px', 'border-radius': '10px', 'margin-top': '30px'}),

    # Data summary section
    html.Div(id='data-summary', style={'color': 'white', 'text-align': 'center', 'margin-top': '20px'}),

    # Report Download button
    html.Div([
        html.Button("Download PDF Report", id="download-btn", n_clicks=0, style={'margin-top': '20px'}),
        dcc.Download(id='download-pdf')
    ], style={'text-align': 'center'}),
], style={
    'background-image': 'url(https://www.nasa.gov/sites/default/files/thumbnails/image/1-bluemarble_west.jpg)',
    'background-size': 'cover',
    'height': '100vh',
    'padding': '20px'
})

# Callback to update graphs and show data summary
@app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure'),
     Output('data-summary', 'children'),
     Output('download-pdf', 'data')],
    [Input('planet-dropdown', 'value'),
     Input('download-btn', 'n_clicks')]
)
def update_graphs(selected_planet, n_clicks):
    # Choose the data based on the selected planet
    if selected_planet == 'moon':
        data = moon_data
        velocity_col = 'velocity(m/s)'
    else:
        data = mars_data
        velocity_col = 'velocity(c/s)'

    # Filter data
    filtered_data = functions.good_data(data, velocity_col)

    # Data summary
    data_summary = {
        'Mean Velocity': filtered_data[velocity_col].mean(),
        'Median Velocity': filtered_data[velocity_col].median()
    }
    summary_text = [html.P(f"{key}: {value:.2f}") for key, value in data_summary.items()]

    # Create the first scatter plot (Time vs Velocity)
    fig1 = px.scatter(data, x='time_rel(sec)', y=velocity_col, title=f'{selected_planet.title()} Time vs Velocity')
    fig1.update_layout(paper_bgcolor='#1c1e29', plot_bgcolor='#1c1e29')

    # Check if 'amplitude' column exists in the dataset
    if 'amplitude' in filtered_data.columns:
        # Create the second line plot (Time vs Amplitude)
        fig2 = px.line(filtered_data, x='time_rel(sec)', y='amplitude', title=f'{selected_planet.title()} Time vs Amplitude')
        fig2.update_layout(paper_bgcolor='#1c1e29', plot_bgcolor='#1c1e29')
    else:
        # If 'amplitude' does not exist, create an empty figure or plot something else
        fig2 = px.scatter(filtered_data, x='time_rel(sec)', y=velocity_col, title=f'{selected_planet.title()} Time vs Velocity (Duplicate)')
        fig2.update_layout(paper_bgcolor='#1c1e29', plot_bgcolor='#1c1e29')

    # Generate PDF Report if the button is clicked
    if n_clicks > 0:
        generate_pdf_report(data_summary, selected_planet, selected_planet)
        pdf_base64 = base64.b64encode(open("seismic_report.pdf", "rb").read()).decode('utf-8')
        return fig1, fig2, summary_text, {'content': pdf_base64, 'filename': 'seismic_report.pdf'}

    return fig1, fig2, summary_text, None

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
