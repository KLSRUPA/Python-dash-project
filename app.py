import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# ---------------------------
# Load & Prepare Data
# ---------------------------
file_path =  r"C:\Users\Rupa\Downloads\dash project\New folder\swedish_population_by_year_and_sex_1860-2022.csv"

df = pd.read_csv(file_path)

# Convert from wide to long format
df_long = df.melt(
    id_vars=["age", "sex"],
    var_name="year",
    value_name="population"
)

df_long["year"] = df_long["year"].astype(int)

# ---------------------------
# Dash App
# ---------------------------
app = dash.Dash(__name__)
app.title = "Swedish Population Dashboard"

# ---------------------------
# Layout
# ---------------------------
app.layout = html.Div(
    style={"padding": "20px", "fontFamily": "Arial"},
    children=[
        html.H1("Swedish Population by Age & Sex", style={"textAlign": "center"}),

        html.Div(
            style={"display": "flex", "gap": "20px"},
            children=[
                html.Div([
                    html.Label("Select Year"),
                    dcc.Dropdown(
                        id="year-dropdown",
                        options=[
                            {"label": str(y), "value": y}
                            for y in sorted(df_long["year"].unique())
                        ],
                        value=2022
                    ),
                ], style={"width": "30%"}),

                html.Div([
                    html.Label("Select Sex"),
                    dcc.Dropdown(
                        id="sex-dropdown",
                        options=[
                            {"label": s.title(), "value": s}
                            for s in df_long["sex"].unique()
                        ],
                        value="men"
                    ),
                ], style={"width": "30%"}),
            ],
        ),

        dcc.Graph(id="population-bar-chart"),
    ],
)

# ---------------------------
# Callback
# ---------------------------
@app.callback(
    Output("population-bar-chart", "figure"),
    Input("year-dropdown", "value"),
    Input("sex-dropdown", "value"),
)
def update_chart(selected_year, selected_sex):
    filtered_df = df_long[
        (df_long["year"] == selected_year) &
        (df_long["sex"] == selected_sex)
    ]

    fig = px.bar(
        filtered_df,
        x="age",
        y="population",
        title=f"Population Distribution by Age ({selected_sex.title()}, {selected_year})",
        labels={"age": "Age", "population": "Population"},
    )

    # Reduce the number of ticks by selecting every 10th value for the x-axis
    tickvals = filtered_df['age'].unique()[::10]  # Select every 10th age value
    ticktext = [str(age) for age in tickvals]  # Convert ages to strings for tick labels

    fig.update_layout(
        xaxis_tickmode="array",
        xaxis_tickvals=tickvals,
        xaxis_ticktext=ticktext,
        xaxis_tickangle=45,  # Rotate the ticks more for better visibility
        plot_bgcolor="white",
        xaxis=dict(
            ticks="outside", 
            tickwidth=1, 
            ticklen=10, 
            showline=True,
            tickfont=dict(size=10),  # Reduce font size for the ticks
        ),
        width=1200,  # Increase figure width to give more space
    )

    return fig



# ---------------------------
# Run Server
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)



