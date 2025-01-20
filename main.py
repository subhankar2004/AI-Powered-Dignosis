import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from dotenv import load_dotenv

class PatientAnalyzer:
    def __init__(self):
        try:
            # Load data
            self.df = pd.read_csv("hospital_patient_data.csv")
            # Convert birth date to datetime
            self.df['Birth Date'] = pd.to_datetime(self.df['Birth Date'])
        except FileNotFoundError:
            st.error("Could not find hospital_patient_data.csv in the current directory.")
            st.stop()

        # Initialize LLM
        self.setup_llm()

    def setup_llm(self):
        """Setup the Groq LLM."""
        try:
            load_dotenv()
            groq_api_key = os.getenv('GROQ_API_KEY')

            if not groq_api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables.")

            self.llm = ChatGroq(
                temperature=0.2,
                groq_api_key=groq_api_key,
                model_name="mixtral-8x7b-32768"
            )
        except Exception as e:
            st.error(f"Error initializing Groq LLM: {str(e)}")
            st.stop()

    def get_available_patients(self):
        """Get list of available patient IDs."""
        return [f"{pid} ({name})" for pid, name in zip(self.df['Patient ID'], self.df['Patient Name'])]

    def get_patient_metrics(self, patient_id):
        """Calculate patient health metrics and statistics."""
        # Extract actual patient_id from the display string
        actual_patient_id = patient_id.split(" (")[0]

        # Filter data
        patient = self.df[self.df['Patient ID'] == actual_patient_id]

        if patient.empty:
            return None, None, None

        patient = patient.iloc[0]

        # Calculate metrics for vital signs
        vital_stats = {
            'heart_rate': self.df['Heart Rate (bpm)'].agg(['mean', 'median', 'min', 'max']).to_dict(),
            'blood_oxygen': self.df['Blood Oxygen Level (%)'].agg(['mean', 'median', 'min', 'max']).to_dict(),
            'sugar_level': self.df['Sugar Level (mg/dL)'].agg(['mean', 'median', 'min', 'max']).to_dict()
        }

        # Calculate performance vs average
        performance = {
            'heart_rate_vs_avg': round((patient['Heart Rate (bpm)'] / vital_stats['heart_rate']['mean'] - 1) * 100, 2),
            'blood_oxygen_vs_avg': round((patient['Blood Oxygen Level (%)'] / vital_stats['blood_oxygen']['mean'] - 1) * 100, 2),
            'sugar_level_vs_avg': round((patient['Sugar Level (mg/dL)'] / vital_stats['sugar_level']['mean'] - 1) * 100, 2)
        }

        return patient, vital_stats, performance

    def create_vitals_chart(self, performance_data):
        """Create vitals visualization."""
        metrics = list(performance_data.keys())
        values = list(performance_data.values())

        # Clean metric names
        display_metrics = [m.replace('_vs_avg', '').replace('_', ' ').title() for m in metrics]

        # Create color scale based on medical ranges
        colors = ['#e74c3c' if abs(v) > 15 else '#f39c12' if abs(v) > 10 else '#2ecc71' for v in values]

        fig = go.Figure(data=[
            go.Bar(
                x=display_metrics,
                y=values,
                marker_color=colors,
                text=[f"{v:+.1f}%" for v in values],
                textposition='auto',
            )
        ])

        fig.update_layout(
            title={
                'text': "Vital Signs vs Population Average",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Vital Signs",
            yaxis_title="% Difference from Average",
            template="plotly_white",
            height=400,
            margin=dict(t=50, l=0, r=0, b=0),
            yaxis=dict(
                gridcolor='rgba(0,0,0,0.1)',
                zerolinecolor='rgba(0,0,0,0.2)'
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    def create_bmi_chart(self, height, weight):
        """Create BMI visualization."""
        bmi = weight / ((height/100) ** 2)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=bmi,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 40]},
                'steps': [
                    {'range': [0, 18.5], 'color': "#3498db"},
                    {'range': [18.5, 24.9], 'color': "#2ecc71"},
                    {'range': [24.9, 29.9], 'color': "#f1c40f"},
                    {'range': [29.9, 40], 'color': "#e74c3c"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': bmi
                }
            },
            title={'text': "BMI Index"}
        ))

        st.plotly_chart(fig, use_container_width=True)

    def generate_analysis(self, patient, stats, performance):
        """Generate AI analysis of the patient's health status."""
        analysis_data = {
            'patient_details': patient.to_dict(),
            'vital_statistics': stats,
            'performance': performance
        }

        prompt = PromptTemplate.from_template("""
            ### PATIENT DATA:
            {data}

            ### INSTRUCTION:
            Analyze the patient's health status based on all available metrics.
            Structure your analysis as follows:

            1. OVERALL HEALTH STATUS:
            - Analyze vital signs compared to normal ranges
            - Highlight any concerning metrics
            - Consider age and gender factors

            2. SYMPTOMS ANALYSIS:
            - Evaluate reported symptoms
            - Identify potential correlations
            - Assess severity

            3. PRESCRIPTION:
            - Recommend generic medications based on symptoms
            - Specify dosage and duration
            - List potential side effects

            4. LIFESTYLE RECOMMENDATIONS:
            - Suggest dietary modifications
            - Recommend exercise routines if applicable
            - Propose lifestyle changes

            5. PRECAUTIONS & FOLLOW-UP:
            - List necessary precautions
            - Recommend follow-up timeline
            - Suggest additional tests if needed

            Format the analysis using clear markdown headings and bullet points.

            ### ANALYSIS:
        """)

        try:
            chain = prompt | self.llm
            return chain.invoke({"data": str(analysis_data)}).content
        except Exception as e:
            st.error(f"Error generating analysis: {str(e)}")
            return None

def main():
    # Page config
    st.set_page_config(
        page_title="Hospital Patient Analyzer",
        page_icon="🏥",
        layout="wide"
    )

    # Styling
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton > button {
            width: 100%;
            background-color: #2ecc71 !important;
        }
        div[data-testid="stMarkdownContainer"] > h3 {
            padding-top: 1rem;
            padding-bottom: 0.5rem;
            color: #2c3e50;
        }
        .stAlert {
            background-color: #f8f9fa;
            border: none;
            border-radius: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

    # Navigation bar
    menu = st.sidebar.radio("Navigation", ["Home", "Patient Analysis"])

    if menu == "Home":
        # Landing Page
        st.image("hospital_logo.png", width=200)  # Replace with hospital logo
        st.title("Welcome to Dhanvantari")
        st.markdown(
            """
            Explore our AI-powered tool for comprehensive patient health analysis.
            Use the navigation bar to access the Patient Analysis tool.
            """
        )

    elif menu == "Patient Analysis":
        # Main Analysis Page
        st.title("🏥 Patient Health Analyzer")
        st.markdown("Comprehensive health analysis and recommendations powered by AI")
        st.markdown("---")

        # Initialize analyzer
        analyzer = PatientAnalyzer()

        # Patient selection
        available_patients = analyzer.get_available_patients()
        patient_id = st.selectbox(
            "Select Patient",
            options=available_patients,
            help="Choose a patient to analyze"
        )

        # Analysis button
        if st.button("🔍 Generate Analysis"):
            if patient_id:
                with st.spinner("🤖 Analyzing patient data..."):
                    # Get patient metrics
                    patient, stats, performance = analyzer.get_patient_metrics(patient_id)

                    if patient is not None:
                        # Create tabs
                        tab1, tab2, tab3 = st.tabs(["📊 Analysis", "💊 Prescription", "📑 Raw Data"])

                        with tab1:
                            # Patient details
                            st.markdown("### 👤 Patient Information")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Name", patient['Patient Name'])
                                st.metric("Age", patient['Age'])
                            with col2:
                                st.metric("Gender", patient['Gender'])
                                st.metric("Blood Group", patient['Blood Group'])
                            with col3:
                                st.metric("Insurance Provider", patient['Insurance Provider'])

                            # Vital signs
                            st.markdown("### 📈 Vital Signs")
                            analyzer.create_vitals_chart(performance)
                            
                            # BMI Chart
                            st.markdown("### 📊 BMI Analysis")
                            analyzer.create_bmi_chart(patient['Height (cm)'], patient['Weight (kg)'])

                            # Symptoms
                            st.markdown("### 🤒 Reported Symptoms")
                            symptoms = patient['Symptoms'].split(', ')
                            for symptom in symptoms:
                                st.markdown(f"- {symptom}")

                        with tab2:
                            # AI Analysis and Prescription
                            st.markdown("### 🤖 AI Analysis & Recommendations")
                            analysis = analyzer.generate_analysis(patient, stats, performance)
                            if analysis:
                                st.markdown(analysis)

                        with tab3:
                            st.markdown("### 📊 Raw Patient Data")
                            st.dataframe(
                                analyzer.df[analyzer.df['Patient ID'] == patient_id.split(" (")[0]],
                                use_container_width=True
                            )
                    else:
                        st.error("Could not find patient data.")

        # Footer
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col2:
            st.markdown("Built with ❤️ by Subhanakr Patra and Team Dhanvantari")

if __name__ == "__main__":
    main()