from dash import Dash, html
import plotly.graph_objs as go
import dash_core_components as dcc
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import html, callback
from plotly.graph_objs import Scatterpolar, Layout, Figure
import pandas as pd
import dash


df=pd.read_parquet('new_merge.parquet')



dash.register_page(__name__,external_stylesheets=["/assets/style.css"],path_template="/joueur/<joueur_id>",title='joueur',name='joueur')



def create_attribute_bar(title, value, max_value=100, color='green'):
    # Calculate the width of the inner bar based on value
    width_percentage = (value / max_value) * 100

    # Return a Dash HTML component for the attribute
    return html.Div(
        children=[
            html.Div(f"{title}: {value}", style={'font-weight': 'bold'}),
            html.Div(
                children=html.Div(style={'width': f'{width_percentage}%', 'background-color': color, 'height': '10px'}),
                style={'width': '100%', 'background-color': '#ddd', 'height': '10px'}
            )
        ],
        style={'margin': '5px 0'}
    )



# Données pour le graphe radar
categories = ['ATT', 'TEC', 'STA', 'DEF', 'POW', 'SPD']
values = [80, 70, 90, 75, 85, 90]  # Vous pouvez remplacer ces valeurs par des données réelles
def create_Scatterpolar(df,player):
    # Création de la trace pour le graphe radar
    trace = Scatterpolar(
        r=list(df.loc[:,["pac","sho","pas","phy"]].values[0]),
        theta=["pac","sho","pas","phy"],
        fill='toself',
        name=player  # Vous pouvez remplacer ce nom par celui d'un joueur réel
    )

    # Configuration de la mise en page du graphe
    layouts =  Layout(
                polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            ),
            angularaxis=dict(  
                color='lightblue'  
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
        showlegend=False,
        paper_bgcolor='rgba(34, 37, 47, 255)',  
        plot_bgcolor='#2d3144',
        
    )
    # Création de la figure avec la trace et la mise en page
    fig = Figure(data=[trace], layout=layouts)
    return fig




def layout(joueur_id=None):
    if joueur_id is not None:
        # Logique pour quand joueur_id est fourni
        joueur_info = joueur_id
        df1=df.loc[joueur_id,:].to_frame().transpose()
    else:
        # Logique pour quand aucun joueur_id n'est fourni
        joueur_info = "Aucun ID de joueur fourni."
    return html.Div([
    # App Header
    # html.Div(className='Header', children=[
    #     html.Div(className='HeaderLeft', children=[html.Img(src='/assets/player-image.png', style={'height': '50px'})]),
    #     html.Div(className='Headerright', children=[
    #         html.Div(className='Headerright1', children=[html.Img(src='/assets/player-image.png', style={'height': '50px'}),html.Div(className='Headerright11',children=[html.P("Lionel"),html.P("Messi")])]),
    #         html.Div(className='Headerright2', children=[
                
    #         ])
    #         ]),
    #     ]),
        html.Div([
            html.Div([
                html.Img(src='https://images.ctfassets.net/rs6bgs1g8dbr/2nGfUPDFsqlwy414FHqI0z/6c8c6d524d4d550b758beb8767b7967c/112893.png', alt='FC Barcea', className='club-logo')
                ],className="container1"),
            html.Div([
                html.Img(src=df1.loc[:,'avatarUrl'][0], alt=joueur_info, className='player-photo'),
                html.Div([
                    html.Span(joueur_info.split("-")[-1], className='label'),
                    html.Span(joueur_info.split("-")[0]),
                    
                ],className="container311"),
                ],className="container31"),
            html.Div([
                html.Div([
                    html.Span(df1.loc[:,'Age']),
                    html.Span('AGE', className='label')
                ],className="container32"),
                html.Div([
                    html.Span(df1.loc[:,'Taille']),
                    html.Span('CM', className='label')
                ],className="container32"),
                html.Div([
                    html.Span(df1.loc[:,'Poids']),
                    html.Span('KG', className='label')
                ],className="container32"),
                html.Img(src='https://images.ctfassets.net/rs6bgs1g8dbr/2WDsnQSFUeeDtN5E5VaRtQ/fd880af45fc99e56aac677d6bf583d77/f_52.png', alt='Argentine', className='flag-icon'),
            ],className="container3")

        ], className='player-stats'),
    # Body of the app
    html.Div(className='body', children=[
        # Left side (empty in your layout)
        html.Div(className='left',children=[
            html.Div(className='PlayerAndFlag',children=[
                html.H1(className="title",children=joueur_info.replace("-"," ")),
                html.Img(className='pays',src="https://images.ctfassets.net/rs6bgs1g8dbr/2WDsnQSFUeeDtN5E5VaRtQ/fd880af45fc99e56aac677d6bf583d77/f_52.png")
            ]),
            html.H2("Poste",className="poste"),
            html.Img(className='left11',src="https://media.contentapi.ea.com/content/dam/ea/easfc/fc-24/ratings/common/full/player-shields/en/158023.png.adapt.265w.png"),
            # html.Img(className='left2',src="/assets/image/image-removebg-preview.png"),
            html.Div([
                html.Div([
                    html.Div([
                        html.Label('Nom Complet'),
                        html.Span(joueur_info.replace("-"," "), className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Nationalité 1'),
                        html.Span(df1.loc[:,'Nationalite1'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Nationalité 2'),
                        html.Span(df1.loc[:,'Nationalite2'], className='value')
                    ], className='detail'),                    
                    html.Div([
                        html.Label('Club Actuelle'),
                        html.Span(df1.loc[:,'Club Actuelle'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Debut du Contrat'),
                        html.Span(df1.loc[:,'Debut du Contrat'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Fin du contrat'),
                        html.Span(df1.loc[:,'Fin du contrat'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Championnat'),
                        html.Span(df1.loc[:,'Championat'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Pays du championnat'),
                        html.Span(df1.loc[:,'Pays du championat'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Position'),
                        html.Span(df1.loc[:,'Club Actuelle'], className='badge')
                    ], className='detail'),
                    html.Div([
                        html.Label('Age'),
                        html.Span(df1.loc[:,'Age'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Meilleur Pieds'),
                        html.Span(df1.loc[:,'Meilleur Pieds'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Taille (cm)'),
                        html.Span(df1.loc[:,'Taille'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Poids (Kg)'),
                        html.Span(df1.loc[:,'Poids'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Face'),
                        html.Span(df1.loc[:,'Club Actuelle'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Nombre total de Trophées'),
                        html.Span(df1.loc[:,'Nombre total de trophees'], className='badge badge-green')
                    ], className='detail'),
                    html.Div([
                        html.Label('Price'),
                        html.Span(df1.loc[:,'Prix'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Equipementier'),
                        html.Span(df1.loc[:,'equipmentier'], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('ID'),
                        html.Span(joueur_info, className='value value-id')
                    ], className='detail'),
                ], className='profile-card')
            ]),
            ]),

        # Right side with four sections
        # Right section 1 with LaLiga Statistics
        html.Div(className="right1", children=[
                html.Div(
                    children=[
                        html.H1(f"VITESSE: {df1.loc[:,'pac'].values[0]}"),
                        create_attribute_bar('Accélération', df1.loc[:,'acceleration'].values[0]),
                        create_attribute_bar('Vitesse de Sprint', df1.loc[:,'sprintSpeed'].values[0]),
                    ],
                    className="stat1",style={'color': '#fff', 'padding': '20px', 'font':'10px cruyffsansmono,monospace'}
                ),
                html.Div(
                    children=[
                        html.H1(f"TIR: {df1.loc[:,'sho'].values[0]}"),
                        create_attribute_bar('Placement', df1.loc[:,'positioning'].values[0]),
                        create_attribute_bar('Finition', df1.loc[:,'finishing'].values[0]),
                        create_attribute_bar('Puissance de Tir', df1.loc[:,'shotPower'].values[0]),
                        create_attribute_bar('Tirs de Loin', df1.loc[:,'longShots'].values[0]),
                        create_attribute_bar('Volées', df1.loc[:,'volleys'].values[0]),
                        create_attribute_bar('Penalties', df1.loc[:,'penalties'].values[0]),
                    ],
                    className="stat1",style={'color': '#fff', 'padding': '20px', 'font':'10px cruyffsansmono,monospace'}
                ),
                html.Div(
                    children=[
                        html.H1(f"Passe:{df1.loc[:,'pas'].values[0]}"),
                        create_attribute_bar('Vision', df1.loc[:,'vision'].values[0]),
                        create_attribute_bar('Centres', df1.loc[:,'crossing'].values[0]),
                        create_attribute_bar('Précision des Coups Francs', df1.loc[:,'freeKickAccuracy'].values[0]),
                        create_attribute_bar('Passes Courtes', df1.loc[:,'shortPassing'].values[0]),
                        create_attribute_bar('Passes Longues', df1.loc[:,'longPassing'].values[0]),
                        create_attribute_bar('Courbe', df1.loc[:,'curve'].values[0]),
                    ],
                    className="stat1",style={'color': '#fff', 'padding': '20px', 'font':'10px cruyffsansmono,monospace'}
                ),
                html.Div(
                    children=[
                        html.H1(f"DRIBBLE:"),
                        create_attribute_bar('Agilité', df1.loc[:,'agility'].values[0]),
                        create_attribute_bar('Équilibre', df1.loc[:,'balance'].values[0]),
                        create_attribute_bar('Réactions', df1.loc[:,'reactions'].values[0]),
                        create_attribute_bar('Contrôle de Balle', df1.loc[:,'ballControl'].values[0]),
                        create_attribute_bar('Dribble', df1.loc[:,'dribbling'].values[0]),
                        create_attribute_bar('Sang-froid', df1.loc[:,'composure'].values[0]),
                    ],
                    className="stat1",style={'color': '#fff',  'padding': '20px', 'font':'10px cruyffsansmono,monospace'}
                ),
                html.Div(
                    children=[
                        html.H1(f"DÉFENSE:"),
                        create_attribute_bar('Interceptions', df1.loc[:,'interceptions'].values[0]),
                        create_attribute_bar('Précision de la Tête', df1.loc[:,'headingAccuracy'].values[0]),
                        create_attribute_bar('Conscience Défensive', df1.loc[:,'defensiveAwareness'].values[0]),
                        create_attribute_bar('Tacle Debout', df1.loc[:,'standingTackle'].values[0]),
                        create_attribute_bar('Tacle Glissé', df1.loc[:,'slidingTackle'].values[0]),
                        
                    ],
                    className="stat1",style={'color': '#fff',  'padding': '20px', 'font':'10px cruyffsansmono,monospace'}
                ),
                html.Div(
                    children=[
                html.H1(f"PHYSICALITÉ: {df1.loc[:,'phy'].values[0]}"),
                        create_attribute_bar('Saut', df1.loc[:,'jumping'].values[0]),
                        create_attribute_bar('Endurance', df1.loc[:,'stamina'].values[0]),
                        create_attribute_bar('Force', df1.loc[:,'strength'].values[0]),
                        create_attribute_bar('Agressivité', df1.loc[:,'aggression'].values[0]),

                    ],
                    className="stat1",style={'color': '#fff',  'padding': '20px', 'font':'10px cruyffsansmono,monospace'}
                ),
        ]),
        # Right section 2 with LaLiga Statistics
        html.Div(className="right2", children=[
                dcc.Graph(figure=create_Scatterpolar(df1,joueur_info))
        ]),
        # Right section 3 with LaLiga Statistics
        html.Div(className="right3", children=[
            dcc.Dropdown(options=[
                {'label': 'But du Pied Gauche', 'value': df1.loc[:,'But du Pied Gauche'].values[0]},
                {'label': 'But du Pied Droit', 'value': df1.loc[:,'But du Pied Droit'].values[0]},
                {'label': "But de l'Interieur de la surface", 'value': df1.loc[:,'But Interieur surface'].values[0]},
                {'label': "But l'Exterieur de la Surface", 'value': df1.loc[:,'But Exterieur Surface'].values[0]},
                {'label': 'But de la Tete', 'value': df1.loc[:,'But de Tete'].values[0]},
                {'label': 'But Coup Franc', 'value': df1.loc[:,'But Coup Franc'].values[0]},
                {'label': 'Matchs Globals jouées', 'value': df1.loc[:,'Matchs Globals jouees'].values[0]},
                {'label': 'Titularisations globales', 'value': df1.loc[:,'Titularisations globals'].values[0]},
                {'label': 'Entrées globales', 'value': df1.loc[:,'Entrees globals'].values[0]},
                {'label': 'Remplacements globals', 'value': df1.loc[:,'Remplacements globals'].values[0]},
                {'label': 'Buts globals', 'value': df1.loc[:,'Buts globals'].values[0]},
                {'label': 'Passes decisives globals', 'value': df1.loc[:,'Passes decisives globals'].values[0]},
                {'label': 'Nombre de cartons jaunes globals', 'value': df1.loc[:,'Nombre de cartons jaunes globals'].values[0]},
                {'label': 'Nombre de cartons rouges globals', 'value': df1.loc[:,'Nombre de cartons rouges globals'].values[0]},
                ],
                value=df1.loc[:,'Matchs Globals jouees'].values[0], id='dropdown',optionHeight=70,style={'margin-bottom': '15px','color': 'black',"width":"100%"}),
                dcc.Graph(id='grid-output'),
                dcc.Dropdown(options=[{'label': 'Matchs Globals jouées', 'value': df1.loc[:,'Matchs Globals jouees'].values[0]}],value=df1.loc[:,'Matchs Globals jouees'].values[0], id='dropdown1',style={'display':'none'})
        ],style={'display':'flex','flex-direction':'column'}),
        # Right section 4 with Current Season Statistics
        html.Div(className="right4", children=[
            html.Div([
                html.Div([
                    html.Div([
                        html.Label('Matchs Globals jouées'),
                        html.Span(df1.loc[:,'Matchs Globals jouees'].values[0], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Buts globals'),
                        html.Span(df1.loc[:,'Buts globals'].values[0], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('But du Pied Gauche'),
                        html.Span(df1.loc[:,'But du Pied Gauche'].values[0], className='value')
                    ], className='detail'),                    
                    html.Div([
                        html.Label('But du Pied Droit'),
                        html.Span(df1.loc[:,'But du Pied Droit'].values[0], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label("But de l'Interieur de la surface"),
                        html.Span(df1.loc[:,'But Interieur surface'].values[0], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label("But l'Exterieur de la Surface"),
                        html.Span(df1.loc[:,'But Exterieur Surface'].values[0], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('But de la Tete'),
                        html.Span(df1.loc[:,'But de Tete'].values[0], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Titularisations globales'),
                        html.Span(df1.loc[:,'Titularisations globals'].values[0], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Entrées globales'),
                        html.Span(df1.loc[:,'Entrees globals'].values[0], className='badge')
                    ], className='detail'),
                    html.Div([
                        html.Label('Remplacements globals'),
                        html.Span(df1.loc[:,'Remplacements globals'].values[0], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Passes decisives globals'),
                        html.Span(df1.loc[:,'Passes decisives globals'].values[0], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Nombre de cartons jaunes globals'),
                        html.Span(df1.loc[:,'Nombre de cartons rouges globals'].values[0], className='value')
                    ], className='detail'),
                    html.Div([
                        html.Label('Nombre de cartons rouges globals'),
                        html.Span(df1.loc[:,'Poids'], className='value')
                    ], className='detail'),
                ], className='profile-card')
            ]),
        ]),
        ]),

])
    
@callback(
    Output(component_id='grid-output', component_property='figure'),
    Input(component_id='dropdown', component_property='value'),
    Input(component_id='dropdown1', component_property='value'),
)
def update_output_div(input_value,input_value1):
    # Nombre de buts marqués et nombre de matchs joués
    buts_marqués = input_value
    matchs_joués = input_value1
    figure2 = go.Figure(
        go.Indicator(
            mode='gauge+number',
            value=buts_marqués,
            domain={'x': [0, 1], 'y': [0, 1]},
            # Le delta montre la différence entre les buts marqués et le nombre de matchs joués
            delta={'reference': matchs_joués},
            gauge={
                'axis': {'range': [None, matchs_joués]},
                'bar': {'color': 'darkblue'},
                'bgcolor': 'darkblue',
                # Les étapes montrent le ratio buts/matchs sous forme de couleur
                'steps': [
                    {'range': [0, buts_marqués], 'color': 'blue'},
                    {'range': [buts_marqués, matchs_joués], 'color': 'white'}
                ],
                # # Seuil représentant le nombre de matchs joués
                # 'threshold': {
                #     'line': {'color': 'red', 'width': 4},
                #     'thickness': 0,
                #     'value': matchs_joués
                # }
            }
        ),
        
    )
    figure2.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",  # Fond transparent
    font={'color': "white", 'family': "Arial"},  # Police blanche, à ajuster si nécessaire
    title=dict(
        text='Diagramme de Gauge',
        x=0.5,
        y=0.95,
        xanchor='center',
        yanchor='bottom',
        font=dict(
            family="Arial",
            size=20,
            color="lightblue"
        )
    ),

    )

    return figure2

