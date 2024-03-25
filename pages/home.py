import dash
from dash import html
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
from dash import html, dcc,callback
import pandas as pd
from joblib import load
import numpy as np
import plotly.graph_objs as go
from plotly.graph_objs import Scatterpolar, Layout, Figure


#create_Scatterpolar 
def create_Scatterpolar(df1, player1, player2):
    # Création des traces pour le graphe radar pour df1 et df2
    trace1 = go.Scatterpolar(
        r=df1.loc[df1["Input_Player"]==player1, ["pac", "sho", "pas", "phy"]].values.flatten().tolist(),
        theta=["pac", "sho", "pas", "phy"],
        fill='toself',
        name=f"{player1}" ,
        line=dict(color='rgba(0, 0, 255, 0.5)'),
        fillcolor='rgba(0, 0, 255, 0.5)' 
    )
    
    trace2 = go.Scatterpolar(
        r=df1.loc[df1["Input_Player"]==player2, ["pac", "sho", "pas", "phy"]].values.flatten().tolist(),
        theta=["pac", "sho", "pas", "phy"],
        fill='toself',
        name=f"{player2}" ,
        line=dict(color='rgba(255, 0, 0, 0.5)'), 
        fillcolor='rgba(255, 0, 0, 0.5)'
    )

    # Configuration de la mise en page du graphe
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title=dict(
            text='Capacités du Joueur',
            x=0.5,
            xanchor='center',
            font=dict(
                size=24,
                color='lightblue'
            )
        ),
        showlegend=True,
        paper_bgcolor='rgba(34, 37, 47, 1)',
        plot_bgcolor='#2d3144',
    )
    # Création de la figure avec les traces et la mise en page
    fig = go.Figure(data=[trace1, trace2], layout=layout)
    return fig



# Notre Dataframe
df=pd.read_parquet('new_merge.parquet')
df["Input_Player"]=df.index+" ("+df.loc[:,"Club Actuelle"]+")"
df=df.copy().reset_index()

#                               Syteme de Recommendation

# Charger la matrice de similarité cosinus sauvegardée
cosine_sim = load('./pages/recommender_model.joblib')
def recommend_items(user_index, data, similarity_matrix, top_n):
    # Produire des scores pour les articles en fonction des similarités
    user_similarities = similarity_matrix[user_index].copy()

    # Explicitement mettre la similarité de l'utilisateur avec lui-même à 0
    user_similarities[user_index] = 0

    # Obtenir les indices des articles que l'utilisateur a déjà notés/évalués
    items_rated_by_user = data.iloc[user_index].to_numpy().nonzero()[0]

    # Mettre les similarités des articles déjà notés à 0
    user_similarities[items_rated_by_user] = 0

    # Trier les scores et obtenir les indices des articles
    item_indices = np.argsort(user_similarities)[::-1]

    # Récupérer les indices des top_n recommandations avec leurs scores
    recommended_items = [(item_index, user_similarities[item_index]) for item_index in item_indices[:top_n]]

    return recommended_items


dash.register_page(__name__, path="/",external_stylesheets=["/assets/style.css"])





def layout():
    return html.Div([
    html.H1('Outil de Recommendation pour les joueurs de Football',style={'text-align': 'center'}),
    html.P(style={'text-align':'center'},children=['Nos données proviennent des sites',html.A(" Foot Mercato",href="https://www.footmercato.net/",style={'color':'white','text-decoration': 'None'}),html.A(", Transfer Markt",href="https://www.transfermarkt.fr/",style={'color':'white','text-decoration': 'None'}),html.A(" et EA Sports FC 24 player ratings database",href="https://www.ea.com/games/ea-sports-fc/ratings",style={'color':'white','text-decoration': 'None'})]),
    
    html.Div([
        # html.H3('Tweak the parameters'),

        # html.Label('Player type'),
        # dcc.RadioItems(
        #     id='player-type',
        #     options=[
        #         {'label': 'Outfield players', 'value': 'OP'},
        #         {'label': 'Goal Keepers', 'value': 'GK'}
        #     ],
        #     value='OP'
        # ),
        
        html.Label('Nom du Joueur',style={"padding":"20px 0px 5px 0px"}),
        dcc.Dropdown(
            id='player-name',
            options=df["Input_Player"],
            value=None,style={"color":"black"}
        ),
        html.Label('Club',style={"padding":"20px 0px 5px 0px"}),
        dcc.Dropdown(
            id='club',
            options=df.loc[:,"Club Actuelle"].unique(),
            value=None ,style={"color":"black"}
        ),
        
        html.Label('Championnat',style={"padding":"20px 0px 5px 0px"}),
        dcc.Dropdown(
            id='championnat',
            options=[df.loc[:,"Championat"].unique()][0],
            value=None ,style={"color":"black"}
        ),
        html.Button('Générer du contenu', id='gen-button', n_clicks=0,style={'font-size':'20px',"margin":"20px 200px 5px 200px"}),
        
        
        # html.Label('Age bracket'),
        # dcc.RangeSlider(
        #     id='age-bracket',
        #     min=int(df.Age.min()),
        #     max=int(df.Age.max()),
        #     value=[int(df.Age.min()), int(df.Age.max())],
        #     marks={i: str(i) for i in range(int(df.Age.min()), int(df.Age.max()))}
        # ),
    html.Div(id='dynamic-content1'),  # L'endroit où le contenu sera généré
    html.Div(id='dynamic-content2')
    ],style={"display":"flex","flex-direction":'column','justify-content':'center','margin':'30px','padding':'20px'}),
    # html.Div(id='dynamic-content1'),  # L'endroit où le contenu sera généré
    # html.Div(id='dynamic-content2')
    # html.H3(f'Showing recommendations for {df["Input_Player"]}'),
    
    # html.Table([
    #     html.Thead(
    #         html.Tr([html.Th(col) for col in ['Player', 'Similarity', 'Position', 'League', 'Age', '90s', 'Foot']])
    #     ),
    #     html.Tbody([
    #         html.Tr([
    #             html.Td('Toni Kroos (Real Madrid)'),
    #             html.Td('94.58%'),
    #             html.Td('MF'),
    #             html.Td('La Liga'),
    #             html.Td('30'),
    #             html.Td('23.5'),
    #             html.Td('right')
    #         ]),
    #         # Repeat this pattern for other players
    #     ])
    # ])
])

@callback(
    Output('player-name', 'options'),
    [Input('championnat', 'value'),
     Input('club', 'value')]
)
def update_player_name_dropdown(championnat, club):
    # Filtre basé sur les inputs du championnat et du club
    if championnat and club:
        filtered_df = df[(df["Championat"] == championnat) & (df["Club Actuelle"] == club)]
    elif championnat:
        filtered_df = df[df["Championat"] == championnat]
    elif club:
        filtered_df = df[df["Club Actuelle"] == club]
    else:
        filtered_df = df

    # Mettre à jour les options du dropdown. Chaque option est un dictionnaire.
    return [{'label': player, 'value': player} for player in filtered_df["Input_Player"].unique()]


@callback(
    Output('championnat', 'options'),
    [Input('player-name', 'value'),
     Input('club', 'value')]
)
def update_player_name_dropdown(championnat, club):
    # Filtre basé sur les inputs du championnat et du club
    if championnat and club:
        filtered_df = df[(df["Input_Player"] == championnat) & (df["Club Actuelle"] == club)]
    elif championnat:
        filtered_df = df[df["Input_Player"] == championnat]
    elif club:
        filtered_df = df[df["Club Actuelle"] == club]
    else:
        filtered_df = df

    # Mettre à jour les options du dropdown. Chaque option est un dictionnaire.
    return [{'label': player, 'value': player} for player in filtered_df["Championat"].unique()]


@callback(
    Output('club', 'options'),
    [Input('player-name', 'value'),
     Input('championnat', 'value')]
)
def update_player_name_dropdown(championnat, club):
    # Filtre basé sur les inputs du championnat et du club
    if championnat and club:
        filtered_df = df[(df["Input_Player"] == championnat) & (df["Championat"] == club)]
    elif championnat:
        filtered_df = df[df["Input_Player"] == championnat]
    elif club:
        filtered_df = df[df["Championat"] == club]
    else:
        filtered_df = df

    # Mettre à jour les options du dropdown. Chaque option est un dictionnaire.
    return [{'label': player, 'value': player} for player in filtered_df["Club Actuelle"].unique()]

@callback(
    Output('dynamic-content1', 'children'),
    [Input('gen-button', 'n_clicks')],
    [State('player-name', 'value')]  # Utiliser State pour récupérer la valeur sans déclencher le callback
)
def update_output(n_clicks, name):
    if n_clicks > 0 and name is not None:
        # Convertir le nom du joueur en index numérique
        player_index = df[df['Input_Player'] == name].index[0]
        recommendations = recommend_items(player_index, df, cosine_sim, top_n=5)
        # Créer une liste de composants HTML pour afficher les recommandations
        option={}
        rows = []
        for idx, score in recommendations:
            # Récupérer les détails du joueur recommandé
            player_info = df.iloc[idx]
            player_name = player_info["Input_Player"].split(" (")[0].strip()  # Split string and remove whitespace
            option[player_info['Input_Player']]=player_info["Input_Player"]
            rows.append(html.Tr([
                html.Td(player_info['Input_Player']),
                html.Td(f"{score:.2f}%"),
                # html.Td(player_info['Position']),
                html.Td(player_info['Championat']),
                html.Td(player_info['Club Actuelle']),
                html.Td(player_info['Age']),
                html.Td(player_info['Age']),
                html.Td(dcc.Link("voir plus", href=f'/joueur/{player_name}',style={'color':'white'}))
            ]))

        return html.Div([
            html.H3(children=f'Afficher les recommandations pour {name}', style={"textAlign": "center"}),
            html.Table([
                html.Thead(
                    html.Tr([html.Th(col) for col in ['Player', 'Similarity', 'Championat', 'Club Actuelle', 'Age', 'Position', 'Lien']])
                ),
                html.Tbody(rows)
            ]),
            html.Div([html.Label(children=f"{name} comparer a"),dcc.Dropdown(id="comparer",options=option,style={"color":'black','width':'400px'})],style={'display':'flex','flex-direction':'row','justify-content':'space-between','margin':'20px 0px 10px 0px'}),
            html.Button('Générer la comparaison', id='Comparaisonbutton', n_clicks=0,style={'font-size':'20px',"margin":"20px 200px 5px 200px"}),

            
        ],style={'margin':'30px','background-color':'rgba(34, 37, 47, 1)','display':'flex','flex-direction':'column','justify-content':'center','padding':'20px 30px 20px 30px'})
    else:
           return html.P('Sélectionnez un joueur et cliquez sur le bouton pour générer des recommandations')
       

@callback(
    Output('dynamic-content2', 'children'),
    Input('Comparaisonbutton', 'n_clicks'),
    State('comparer', 'value'),
    State('player-name', 'value')
)
def update_outputs(n_clicks, name,player_name):
        if n_clicks > 0 and name is not None:
                player_info1 = df.loc[df["Input_Player"]==name]
                player_info2 = df.loc[df["Input_Player"]==player_name]
                return html.Div([
                            html.Div([
                                html.Div([
                                    html.H2([player_info1["Name"].values[0].replace("-"," "), html.Span(f" {player_info1['overallRating'].values[0]}", className='rating')]),
                                    html.Img(src=player_info1['avatarUrl'].values[0]),
                                    html.Div([
                                        html.Div('ST / LW / RW', className='positions'),
                                        html.Div([
                                            html.Div(['Pace: ', html.Span(player_info1["pac"].values[0], className='value')], className='attribute'),
                                            html.Div(['Shooting: ', html.Span(player_info1["sho"].values[0], className='value')], className='attribute'),
                                            html.Div(['Passing: ', html.Span(player_info1["pas"].values[0], className='value')], className='attribute'),
                                            html.Div(['Dribbling: ', html.Span(player_info1["Name"].values[0], className='value')], className='attribute'),
                                            html.Div(['Defending: ', html.Span(player_info1["Name"].values[0], className='value')], className='attribute'),
                                            html.Div(['Physical: ', html.Span(player_info1["phy"].values[0], className='value')], className='attribute')
                                        ], className='attributes'),
                                        html.Div([
                                            html.Div(['Club Actuelle: ', html.Span(children=[html.Span(player_info1["Club Actuelle"].values[0])], className='stars')], className='skill-moves'),
                                            html.Div(['Championnat: ', html.Span(children=[html.Span(player_info1["Championat"].values[0])], className='stars')], className='weak-foot')
                                        ], className='skills'),
                                        html.Div(f'Meilleur Pieds: {player_info1["Meilleur Pieds"].values[0]}', className='foot'),
                                        html.Div(f'Poids: {player_info1["Poids"].values[0]} Kg', className='work-rate'),
                                        html.Div(f'Taille: {player_info1["Taille"].values[0]} Cm', className='work-rate'),
                                        html.Div(f'Age: {player_info1["Age"].values[0]}', className='age')
                                    ], className='player-info')
                                ], className='player-card mbappe'),
                                dcc.Graph(figure=create_Scatterpolar(df, name, player_name)),
                                html.Div([
                                    html.H2([player_info2['Input_Player'].values[0].replace("-"," ").split("(")[0], html.Span(player_info2['overallRating'].values[0], className='rating')]),
                                    html.Img(src=player_info2['avatarUrl'].values[0]),
                                    html.Div([
                                        html.Div('RW / LW', className='positions'),
                                        html.Div([
                                            html.Div(['Pace: ', html.Span(player_info2['pac'].values[0], className='value')], className='attribute'),
                                            html.Div(['Shooting: ', html.Span(player_info2['sho'].values[0], className='value')], className='attribute'),
                                            html.Div(['Passing: ', html.Span(player_info2['pas'].values[0], className='value')], className='attribute'),
                                            html.Div(['Dribbling: ', html.Span(player_info2['Input_Player'].values[0], className='value')], className='attribute'),
                                            html.Div(['Defending: ', html.Span(player_info2['Input_Player'].values[0], className='value')], className='attribute'),
                                            html.Div(['Physical: ', html.Span(player_info2['phy'].values[0], className='value')], className='attribute')
                                        ], className='attributes'),
                                        html.Div([
                                            html.Div(['Club Actuelle: ', html.Span(children=[html.Span(player_info2["Club Actuelle"].values[0])], className='stars')], className='skill-moves'),
                                            html.Div(['Championnat: ', html.Span(children=[html.Span(player_info2["Championat"].values[0])], className='stars')], className='weak-foot')
                                        ], className='skills'),
                                        html.Div(f'Meilleur Pieds: {player_info2["Meilleur Pieds"].values[0]}', className='foot'),
                                        html.Div(f'Poids: {player_info2["Poids"].values[0]} Kg', className='work-rate'),
                                        html.Div(f'Taille: {player_info2["Taille"].values[0]} Cm', className='work-rate'),
                                        html.Div(f'Age: {player_info2["Age"].values[0]}', className='age')
                                    ], className='player-info')
                                ], className='player-card di-maria')
                            ], className='player-card-container')
                        ],className="containerComparaison")
