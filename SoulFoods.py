import colorsys
from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def main():
    print("hey there")
    # open csv to read
    # open another csv to write
    # iterate over each row, filter pink morsel and combine the quantity and price
    # write each row after combining the fields
    
    df = pd.read_csv("C:\\Users\\Akshay bruh\\Desktop\\quantium-starter\\data\\all_csv_files.csv")
    print(df)

    #remove duplicates
    if len(df[df.duplicated()]):
        df.drop_duplicates(keep='first',inplace=True)
    df = df[df['product'] == "pink morsel"]
    print("----filtered df------")
    print(df)

    df = df.replace("[$]", "", regex=True)

    print("----dollar removed df------")
    print(df)

    df["sales"] = df["price"].astype(float) * df["quantity"].astype(float)
    df2 = df.drop(["quantity", "price"], axis=1)
    print("----final df------")
    print(df2)

    df2.to_csv("C:\\Users\\Akshay bruh\\Desktop\\quantium-starter\\data\\final_csv.csv", encoding='utf-8', index=False)
    df2 = df2.sort_values(by="date")
# #creating a dash layout
    app = Dash(__name__)

    colors = {
    "primary": "#FEDBFF",
    "secondary": "#D598EB",
    "font": "#522A61"
    }

# create the visualization
    def generate_figure(chart_data):
        line_chart = px.line(chart_data, x="date", y="sales", title="Pink Morsel Sales")
        line_chart.update_layout(
        plot_bgcolor=colors["secondary"],
        paper_bgcolor=colors["primary"],
        font_color=colors["font"]
        )
        return line_chart


    visualization = dcc.Graph(
        id="visualization",
        figure=generate_figure(df2)
        )

# create the header
    header = html.H1(
        "Pink Morsel Visualizer",
         id="header",
         style={
                "background-color": colors["secondary"],
                "color": colors["font"],
                "border-radius": "20px"
                }
            )

# region picker
    region_picker = dcc.RadioItems(
        ["north", "east", "south", "west", "all"],
        "north",
        id="region_picker",
        inline=True
        )
    region_picker_wrapper = html.Div(
        [
            region_picker
            ],
        style={
            "font-size": "150%"
            }
        ),
    
# define the region picker callback
    @app.callback(
            Output(visualization, "figure"),
            Input(region_picker, "value")
            )
    def update_graph(region):
    # filter the dataset
            if region == "all":
                trimmed_data = df2
            else:
                trimmed_data = df2[df2["region"] == region]

    # generate a new line chart with the filtered data
            figure = generate_figure(trimmed_data)
            return figure


# define the app layout
    app.layout = html.Div(
        [
        header,
        visualization,
        region_picker_wrapper
        ],
    style={
        "textAlign": "center",
        "background-color": colors["primary"],
        "border-radius": "20px"
    }
)
    

    app.run_server(debug=True)

if __name__ == "__main__":
    main()
    