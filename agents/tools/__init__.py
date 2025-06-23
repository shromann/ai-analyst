import duckdb
import markdown
import yaml
import os 
import glob


import seaborn as sns

sns.set_style('whitegrid')

import pandas as pd

import matplotlib.pyplot as plt

from .visualisation import _save_plot
from .simulation import _forecast

from google.adk.tools import ToolContext

class DataToolset:
    def __init__(self, path: str):
        self.table_name = path.split('/')[-1]
        self.agent_name = self.table_name + '_agent'
        self.csv_path = f"{path}/data.csv"      
        self.confs = {}

        with open(f"{path}/description.md", "r", encoding="utf-8") as f:
            self.description = markdown.markdown(f.read())


        yaml_files = glob.glob(os.path.join(path, "*.yaml")) + glob.glob(os.path.join(path, "*.yml"))
        for yaml_file in yaml_files:
            name = yaml_file.split('/')[-1]
            with open(yaml_file, "r", encoding="utf-8") as f:
                self.confs[name] = yaml.safe_load(f)
        

        self.instruction = (f"""<purpose>
            Use this tool to get data or metrics from
            <table_name>{self.table_name}</table_name>,
            which is about
            <data_description>{self.description}</data_description>
            </purpose>
            <query_requirements>
            - Use DuckDB-compliant SQL syntax, especially for dates:
                - Example: `WHERE date_column = DATE '2023-01-01'`
                - Example: `WHERE date_column >= CURRENT_DATE - INTERVAL '7 days'`
            - Use `CAST()` to explicitly convert data types when needed:
                - Example: `CAST('2023-01-01' AS DATE)`
            - String literals should use single quotes ('value').
            - Enclose identifiers in double quotes if necessary (e.g., "column name").
            </query_requirements>
            Your responses always follow the following format:
            <response_format>
                1. query data and make an appropriate visualisation of the data
                2. present an analysis of the queried data, break your response down to explain it clearly.
                3. present a the visualisation.
                4. if asked, present a forecast of the data, use the forecast tool.
            </response_format>
            <response_guide>
            <never_do>Never ask the user to do what you can do.</never_do>
            <can_do>Add emojis through out the reponse to make it look pretty</can_do>
            <can_do>When comparing in visualisation for categorical values, plot them in one plot</can_do>
            <can_do>Use hue, col then row in that order to compare categorical features.</can_do>
            <can_do>Always respond only in English</can_do>
            <response_guide>
            """
        )


    def query_tool(self, sql_query: str):
        """
        Execute a one-off SQL query on a CSV file using DuckDB, returning the results as a dictionary.

        This function leverages DuckDB's built-in support for querying CSV files using SQL. 
        It is intended for single-use queries where performance, simplicity, and compatibility 
        with local data files are important.

        Parameters:
        -----------
        sql_query : str
            The SQL query to execute. The query must follow DuckDB SQL syntax. You might need to add explicit type casts.

        Returns:
        --------
        dict
            Query result formatted as a dictionary, where keys are column names and values are lists 
            of column data.

        Notes:
        ------

        - For date filters and comparisons, DuckDB uses SQL-compliant date syntax:
            - `WHERE date_column = DATE '2023-01-01'`
            - `WHERE date_column >= CURRENT_DATE - INTERVAL '7 days'`

        - Use `CAST` to ensure proper typing when filtering or transforming values:
            - `CAST('2023-01-01' AS DATE)`
        
        - String literals should be enclosed in single quotes ('example'), and 
          identifiers (column/file names) may be quoted with double quotes if needed.
        """

        sql_query = sql_query.replace('`', '')

        with duckdb.connect(database=":memory:") as con:
            # Load data as a temporary in-memory table
            con.execute(f"""
                CREATE TABLE {self.table_name} AS 
                SELECT * FROM read_csv_auto('{self.csv_path}', HEADER=TRUE);
            """)
            
            result = con.execute(sql_query).df().to_dict('list')
        return result

    async def plot_tool(self, sql_query: str, title: str, x: str, y: str, hue: str, col: str, row: str, kind: str, plot_type: str, tool_context: ToolContext):
        """
        Executes a DuckDB SQL query, extracts specified columns, and generates a plot.

        Parameters
        ----------
        sql_query : str
            A DuckDB-compatible SQL query used to retrieve data. You might need to add explicit type casts.
        title : str
            The title for the resulting plot.
        x : str
            Column name to be used for the x-axis.
        y : str
            Column name to be used for the y-axis.
        hue : str
            Column name for color grouping (categorical hue).
        col : str
            Column name to create separate subplots across columns.
        row : str
            Column name to create separate subplots across rows.
        kind : str
            Type of plot to generate (e.g., 'scatter', 'line').
        plot_type : str
            Type of plot to generate, one of 'relation', 'categorical', 'distribution').
        tool_context : ToolContext
            Context object for saving and managing the generated plot.

        Returns
        -------
        dict
            A dictionary containing metadata or references to the saved visualization.

        Notes
        -----
        - Use DuckDB-compliant SQL syntax, especially for dates:
            - Example: `WHERE date_column = DATE '2023-01-01'`
            - Example: `WHERE date_column >= CURRENT_DATE - INTERVAL '7 days'`
        - Use `CAST()` to explicitly convert data types when needed:
            - Example: `CAST('2023-01-01' AS DATE)`
        - String literals should use single quotes ('value').
        - Enclose identifiers in double quotes if necessary (e.g., "column name").
        """
        

        data = self.query_tool(sql_query)

        data_df = pd.DataFrame(data)
        num_points = len(data_df)

        # Base dimensions
        base_height = 5
        max_height = 10
        min_aspect = 2.5
        max_aspect = 4.5

        # Adjust height modestly based on the number of rows (up to a point)
        height = min(base_height + num_points / 500, max_height)

        # Compute aspect ratio based on data spread, but clamp it
        aspect = min(max((num_points / 100), min_aspect), max_aspect)

        SNS_PLOTS = {
            'relation': sns.relplot,
            'categorical': sns.catplot,
            'distribution': sns.displot
        }

        sns_plot = SNS_PLOTS[plot_type](data=data, x=x, y=y, hue=hue, col=col, row=row, kind=kind, height=height, aspect=aspect)

        sns_plot.fig.suptitle(title, fontsize=13, y=1.03)  # adjust `y` as needed

        
        return await _save_plot(title, sns_plot, tool_context)


    def forecast_tool(self, sql_query: str, value_column: str, date_column: str, forecast_horizon: int, freq: str):
        """
        Executes a DuckDB SQL query, extracts specified columns, and generates a plot.

        Parameters
        ----------
        sql_query : str
            A DuckDB-compatible SQL query used to retrieve data. You might need to add explicit type casts.
        forecast_horizon : int
            Number of future periods to forecast.
        freq : str
            Frequency of the data (e.g., 'M' for monthly, 'D' for daily).

        Returns
        -------
        dict
            A dictionary containing the forecasted values.

        Notes
        -----
        - Use DuckDB-compliant SQL syntax, especially for dates:
            - Example: `WHERE date_column = DATE '2023-01-01'`
            - Example: `WHERE date_column >= CURRENT_DATE - INTERVAL '7 days'`
        - Use `CAST()` to explicitly convert data types when needed:
            - Example: `CAST('2023-01-01' AS DATE)`
        - String literals should use single quotes ('value').
        - Enclose identifiers in double quotes if necessary (e.g., "column name").
        """
        
        data = self.query_tool(sql_query)
        data_df = pd.DataFrame(data)

        data_df[date_column] = pd.to_datetime(data_df[date_column])
        data_df = data_df.set_index(date_column)
        
        preds = _forecast(data_df[value_column], forecast_horizon, freq)

        forecasts = preds\
            .reset_index()\
            .rename(
                columns={
                    'ds': date_column, 
                    'yhat': f'{value_column} (Forecasts)'
                }
            )\
            .to_dict('list')
        
        return forecasts
