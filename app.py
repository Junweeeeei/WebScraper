import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import pyodbc
from dash.dependencies import Input, Output
import dash_table
import os
from dotenv import load_dotenv

# Setup Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load environment variables from .env file
load_dotenv()

# Access environment variables
db_server = os.getenv('DB_SERVER')
db_database = os.getenv('DB_DATABASE')
db_uid = os.getenv('DB_UID')
db_pwd = os.getenv('DB_PWD')


# Database connection
def get_data():
    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={db_server};'
        f'DATABASE={db_database};'
        f'UID={db_uid};'
        f'PWD={db_pwd};'
        'Encrypt=yes;'
        'TrustServerCertificate=no;'
        'Connection Timeout=30;'
    )
    query = "SELECT [Security Description], [Trades], [TTA], [Open], [High], [Low], [LTP], [LTY], [Timestamp] FROM RegularMarket ORDER BY Timestamp"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# Layout of the dashboard
app.layout = html.Div(
    children=[
        dbc.Row(
            dbc.Col(
                html.H1("Security Description Time Series and Data Table"),
                width={"size": 6, "offset": 1},
                style={'paddingTop': '100px', 'paddingBottom': '20px'},
            ),
            justify="center"
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id='security-dropdown',
                    options=[{'label': i, 'value': i} for i in get_data()['Security Description'].unique()],
                    placeholder="Select Security Description"
                    
                ),
                width={"size": 6},
                style={'paddingTop': '20px', 'paddingBottom': '20px'},  # Padding for top and bottom of dropdown
            ),
            justify="center"
        ),
        dbc.Row(
            dbc.Col(
                html.Div(  # Parent container for DataTable
                    children=[
                        dash_table.DataTable(
                            id='data-table',
                            columns=[{'name': col, 'id': col} for col in get_data().columns],
                            style_table={
                                'height': '400px',  # Set table height
                                'overflowY': 'auto',  # Scroll when table height exceeds 400px
                                'width': '100%',  # Set the width of the table to 60% of the screen width
                                'margin': '0 auto',  # Center the table horizontally
                            },
                            style_cell={'textAlign': 'center'},
                            page_size=10,
                            page_current=0,
                            page_count=0,
                            style_as_list_view=True,  # Optional, to remove the borders
                        ),
                    ],
                    style={
                        'width': '80%',  # Set the parent container width to 80% of the screen
                        'margin': '0 auto',  # Center the container horizontally
                        'border': '2px solid #737e8e',  # Optional border style
                        'padding': '20px',  # Padding around the DataTable
                        'borderRadius': '10px',  # Optional rounded corners
                        'backgroundColor': '#f8f9fa',  # Optional background color
                    }
                ),
                width={"size": 12},  # Use full width for the column
            ),
            justify="center"  # Center the entire row (including the table)
        ),
        dbc.Row(
            dbc.Col(
                html.Div(  # Parent container for DataTable
                    children=[
                        dcc.Graph(
                            id='security-chart',
                            style={
                                'width': '80%',  # Set the width of the plot (adjust as needed)
                                'height': '500px',  # Set the height of the plot (adjust as needed)
                                'margin': '0 auto',  # Center the plot horizontally
                            }
                        ),
                    ],
                    style={
                        'width': '80%',  # Set the parent container width to 80% of the screen
                        'margin': '0 auto',  # Center the container horizontally
                        'border': '2px solid #737e8e',  # Optional border style
                        'padding': '20px',  # Padding around the DataTable
                        'borderRadius': '10px',  # Optional rounded corners
                        'backgroundColor': '#f8f9fa',  # Optional background color
                    }
                ),
                width=12,
                style={'paddingTop': '50px', 'paddingBottom': '50px'},
            ),
        ),
    ]
)


# Update table and graph based on selected Security Description
@app.callback(
    [Output('data-table', 'data'),
     Output('security-chart', 'figure')],
    [Input('security-dropdown', 'value')]
)
def update_dashboard(selected_security):
    # Fetch the data
    df = get_data()

    # If no security is selected, display all rows in the table
    if not selected_security:
        table_data = df.to_dict('records')  # Show all data
        # Initialize an empty chart if no security is selected
        fig = {}
    else:
        # Filter data based on selected Security Description
        df_selected = df[df['Security Description'] == selected_security]
        table_data = df_selected.to_dict('records')

        # Create the chart
        fig = px.line(
            df_selected,
            x='Timestamp',
            y=['Trades', 'TTA'],
            title=f"Time Series of Trades and TTA for {selected_security}",
            labels={'value': 'Value'}
        )

    return table_data, fig



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8050)))
