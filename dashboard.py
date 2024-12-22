import pandas as pd
import streamlit as st
import plotly.express as px

# Load the dataset
st.title("Music Popularity Dataset Dashboard")

# File uploader to load the dataset dynamically
uploaded_file = st.file_uploader("Upload your preprocessed dataset (CSV)", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Sidebar for user input
    st.sidebar.header("Filter Options")
    selected_genre = st.sidebar.multiselect("Select Genre(s):", 
                                            options=[col for col in df.columns if 'Genre_' in col], 
                                            default=[])

    # Filter data based on selection
    if selected_genre:
        genre_filter = df[selected_genre].sum(axis=1) > 0
        filtered_df = df[genre_filter]
    else:
        filtered_df = df

    # Top features to visualize
    st.header("Feature Distributions")
    selected_feature = st.selectbox("Select a Feature to Visualize:", options=df.columns)

    # Display histogram for selected feature
    fig = px.histogram(filtered_df, x=selected_feature, title=f"Distribution of {selected_feature}")
    st.plotly_chart(fig)

    # Correlation heatmap
    st.header("Correlation Heatmap")
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    correlation_matrix = df[numeric_cols].corr()
    fig_corr = px.imshow(correlation_matrix, text_auto=True, title="Feature Correlation Heatmap")
    st.plotly_chart(fig_corr)

    # Scatter Plot
    st.header("Scatter Plot")
    x_axis = st.selectbox("X-Axis:", options=df.columns, index=0)
    y_axis = st.selectbox("Y-Axis:", options=df.columns, index=1)
    scatter_fig = px.scatter(filtered_df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
    st.plotly_chart(scatter_fig)

    # Data Table
    st.header("Filtered Data Table")
    st.dataframe(filtered_df)

else:
    st.write("Please upload a dataset to begin.")
