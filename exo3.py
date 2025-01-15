from dash import Dash, html, dash_table,dcc
import pandas as pd
import dash
import plotly.express as px
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


# Création de l'application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Lire le fichier CSV en ignorant les lignes problématiques
df = pd.read_csv("https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv", on_bad_lines='skip')

# Filtrer le DataFrame pour ne conserver que les colonnes 'title' et 'num_pages'
df = df[['title', '  num_pages','authors']]

# Sélectionner les 10 premières lignes pour l'exemple

# Créer un graphique à barres avec Plotly Express


# Définir la mise en page de l'application
app.layout = dbc.Container([
    html.H1("Affichage d'un DataFrame avec Dash"),
    dbc.Row([
        dbc.Col(html.Div(dcc.Dropdown(
                            id='author-dropdown',
                            options=[{'label': author, 'value': author} for author in df['authors'].unique()],
                            placeholder="Sélectionnez un auteur"
                        )), width=8),
        dbc.Col(html.Div(dbc.Input(
                        type="number",
                        id="max-pages-input",
                        min=0,
                        max=10000,
                        value=500,
                        placeholder="Entrez une quantité",
                        className="form-control"
                        ),), width=4)    
    ])
    ,
    dcc.Graph(id='bar-chart')
])

@app.callback(
    Output('bar-chart', 'figure'),
    [Input('author-dropdown', 'value')],
    [Input('max-pages-input', 'value')]
)
def update_output(value, value2):

    filtered_df = df.loc[df['authors'] == value]
    filtered_df = filtered_df[filtered_df['  num_pages'] <= value2]

    fig = px.bar(filtered_df, x='title', y='  num_pages', title='Nombre de pages par livre')
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)