# dashboard_page_1.py
import streamlit as st
 
def about():
    st.title("About Our Project")
 
    st.write(
        "Welcome to our electricity demand prediction system! In today's rapidly evolving world, the need for accurate electricity demand forecasting has become paramount for sustainable development. Our system integrates advanced machine learning models – linear regression, KNN, XGBoost, and SVM – to predict electricity demand with precision.\n\n"
        "**Key Features:**\n\n"
        "- **Diverse Model Ensemble:** We employ a blend of machine learning algorithms for robust predictions.\n"
        "- **Data Quality Assurance:** Our system ensures high-quality data through effective pre-processing techniques, including cubic spline interpolation and outlier removal.\n"
        "- **Performance Metrics:** The system is evaluated using metrics such as Mean Square Error (MSE), Root Mean Square Error (RMSE), and r2 score, providing insights into its accuracy and reliability.\n"
        "- **Decision XGBoost:** After thorough comparison, XGBoost emerges as the optimal algorithm, boasting impressive MSE, RMSE, and R2 score values of 0.03, 0.17, and 0.95, respectively.\n\n"
        "**User-Friendly Interface:**\n\n"
        "Our interface is designed with you in mind, making it easy for individuals and businesses to make informed decisions, reduce energy costs, and contribute to a sustainable future.\n\n"
        "Explore the power of accurate electricity demand prediction with our user-friendly system!"
    )
 
def main():
    # Add your main content here
    st.title("Electricity Demand Prediction Dashboard")
 
    # Create a sidebar with navigation links
    st.sidebar.title("Navigation")
    pages = ["Home", "About"]  # Add more pages if needed
    choice = st.sidebar.radio("Go to", pages)
 
    # Based on the user's choice, display the appropriate page
    if choice == "Home":
        st.header("Home Page")
        # Add content for the home page here
    elif choice == "About":
        about()  # Call the about function