import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torchaudio
import os
import random
from sklearn.datasets import load_iris, load_digits

def render_dataset_selection_section():
    """Renders the dataset selection UI for the neural network creator."""
    
    st.header("Neural Network Creator")
    st.subheader("Dataset Selection")

    # Initialize session state variables if they do not exist
    if "dataset_selected" not in st.session_state:
        st.session_state["dataset_selected"] = False
    if "success_message" not in st.session_state:
        st.session_state["success_message"] = ""

    st.markdown("#### Choose Your Dataset")

    # Use tabs to separate dataset upload and predefined datasets
    tab1, tab2 = st.tabs(["Upload Dataset", "Use Premade Dataset"])

    with tab1:
        # Allow users to upload a dataset in CSV, Excel, or JSON format
        uploaded_file = st.file_uploader("Upload Your Dataset", type=["csv", "xlsx", "json"])
        
        if uploaded_file:
            st.session_state["dataset_selected"] = True
            st.session_state["success_message"] = f"Loaded {uploaded_file.name} dataset successfully!"
            st.write("Dataset preview:")

            # Attempt to read and display the uploaded dataset
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)  # Read CSV file
                elif uploaded_file.name.endswith(".xlsx"):
                    df = pd.read_excel(uploaded_file)  # Read Excel file
                elif uploaded_file.name.endswith(".json"):
                    df = pd.read_json(uploaded_file)  # Read JSON file

                st.write(df.head())  # Show the first few rows of the dataset
                st.session_state["dataset"] = df  # Store dataset in session state
            except Exception as e:
                st.error(f"Error reading dataset: {e}")

    with tab2:
        # Provide a selection box for predefined datasets
        st.subheader("Use a Predefined Dataset")
        predefined_datasets = ["Iris", "MNIST Handwriting", "SpeechCommands"]
        selected_dataset = st.selectbox("Select a Predefined Dataset", predefined_datasets)

        # Load the selected predefined dataset when the button is clicked
        if st.button("Load Predefined Dataset"):
            st.session_state["dataset_selected"] = True
            st.success(f"Loaded {selected_dataset} dataset successfully!")
            st.session_state["success_message"] = f"Loaded {selected_dataset} dataset successfully!"

            if selected_dataset == "Iris":
                # Load the Iris dataset and create a DataFrame
                data = load_iris()
                df = pd.DataFrame(data.data, columns=data.feature_names)
                df['target'] = data.target

                # Show 5 random examples from the Iris dataset
                st.write("Examples from this dataset:")
                random_indices = np.random.choice(len(df), size=5, replace=False)
                st.write(df.iloc[random_indices])

            elif selected_dataset == "MNIST Handwriting":
                # Load the MNIST (digits) dataset and create a DataFrame
                data = load_digits()
                df = pd.DataFrame(data.data)
                df['target'] = data.target

                # Display example images from the dataset
                st.write("Examples from this dataset:")
                random_indices = np.random.choice(len(data.images), size=5, replace=False)
                fig, axes = plt.subplots(1, 5, figsize=(10, 3))
                for ax, idx in zip(axes, random_indices):
                    ax.set_axis_off()
                    ax.imshow(data.images[idx], cmap=plt.cm.gray_r, interpolation='nearest')
                    ax.set_title(f'Label: {data.target[idx]}')
                st.pyplot(fig)

            # Store the selected dataset in session state
            st.session_state["dataset"] = df

    # Display a success or warning message depending on dataset selection
    if st.session_state["success_message"]:
        st.markdown(
            f'<div style="text-align: center; color: #00bb0b;">{ "A dataset is selected, build your model!" }</div>',
            unsafe_allow_html=True
        )

    if not st.session_state["dataset_selected"]:
        st.markdown(
            f'<div style="text-align: center; color: #f39c12;">{ "Please select a dataset to proceed." }</div>',
            unsafe_allow_html=True
        )

def selected_dataset():
    """Checks if a dataset has been selected and returns it; otherwise, shows an error message."""
    
    if not st.session_state.get("dataset_selected", False):
        st.error("No dataset selected. Please select a dataset before creating a model.")
        return None
