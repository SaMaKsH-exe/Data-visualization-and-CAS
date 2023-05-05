import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as pl
import altair as alt

#reads an excel file 
#df = pd.read_excel(r'C:\Users\samak\Downloads\supermarkt_sales.xlsx')
df=pd.DataFrame()

#page layout 
st.set_page_config(page_title = "Visulesering af Data ",
                   layout = "wide")
st.title('Data Visualisation')

#drag and drop file uploader 
uploaded_file = st.file_uploader("Choose an data file")

#if excel file is not empty df is new drag and dropped excel file
if uploaded_file is not None:
    df= pd.read_excel(uploaded_file)

st.sidebar.header("Plese Filter here")

#select function
chart_type = st.sidebar.selectbox('Select chart type:', ['line', 'area', 'bar', 'scatter'])
agg_func = st.sidebar.selectbox('Select aggregation function:', ['sum', 'mean', 'median'])

if not df.empty:
    #x and y axis columns

    x_axis = st.sidebar.selectbox('Select x-axis column', df.columns)
    y_axis = st.sidebar.multiselect('Select y-axis columns', df.select_dtypes(include='number').columns.unique())

    # Apply the aggregation function to the y-axis columns
    if agg_func == 'sum':
        y_data = df[y_axis].sum()
    elif agg_func == 'mean':
        y_data = df[y_axis].mean()
    elif agg_func == 'median':
        y_data = df[y_axis].median()

    #Find average of columns that include numbers 
    columns_to_mean_value=st.sidebar.multiselect("Select the columns to do average",
                                options = df.select_dtypes(include='number').columns.unique()
                                )

    submit = st.sidebar.button('Submit')

#change the dataframe so it treats x and y axis as sperate 
def display_scattered_chart(df,chart_type,x_axis,y_axis):
    new_df = df[[x_axis] + y_axis]
    melted_df = new_df.melt(id_vars=[x_axis], var_name='y_axis', value_name='value')


    # Draw the chart based on the user's selection
    if chart_type == 'line':
        st.line_chart(melted_df,x=x_axis)
    elif chart_type == 'area':
        st.area_chart(melted_df,x=x_axis)
    elif chart_type == 'bar':
        st.bar_chart(melted_df,x=x_axis)
    elif chart_type == 'scatter':
        st.scatter_chart(df[[x_axis] + y_axis])
       
     


        chart = alt.Chart(melted_df).mark_line().encode(
            x=x_axis,
            y='value',
            color='y_axis'
        )
        # Display the chart using streamlit
        st.altair_chart(chart, use_container_width=True)

def display_Avg(columns_to_mean_value):
    # Create a list to hold column values
    column_values = []

    # Loop through each column and get its mean/average value
    for column_name in columns_to_mean_value:
        column_value = df[column_name].mean()
        column_values.append(column_value)

    num_columns = 3
    num_rows = (len(column_values) + num_columns - 1) // num_columns
    
    for row in range(num_rows):
        columns = st.columns(num_columns)
        for col in range(num_columns):
            index = row * num_columns + col
            if index < len(column_values):
                columns[col].metric(label=columns_to_mean_value[index], value=column_values[index])

  


if submit: #run te function
    display_Avg(columns_to_mean_value)

    display_scattered_chart(df,chart_type,x_axis,y_axis)


#show 
st.dataframe(df)

#summary of dataframe using describe method from panda
stats = df.describe()
st.header("Summary of Dataset")
st.write(stats)

