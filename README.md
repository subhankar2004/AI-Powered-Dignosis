# Dhanwantari - AI-Powered Patient Health Analyzer 🏥

## Overview
Dhanwantari is a comprehensive healthcare analytics platform that combines medical data analysis with AI-powered insights. The system provides detailed patient health analysis, generates prescriptions, and offers personalized health recommendations using advanced visualization and machine learning techniques.

## Features
- 📊 Interactive health metrics visualization
- 🤖 AI-powered health analysis and recommendations
- 💊 Automated prescription generation
- 📈 BMI and vital signs analysis
- 📋 Comprehensive patient data management
- 🔍 Symptom analysis and correlation
- 💡 Lifestyle recommendations
- 🏷️ Follow-up scheduling suggestions

## Prerequisites
- Python 3.8 or higher
- Groq API key (for AI analysis)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dhanwantari.git
cd dhanwantari
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # For Unix/macOS
venv\Scripts\activate     # For Windows
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Required Libraries
Create a `requirements.txt` file with the following dependencies:
```
streamlit
langchain-groq
pandas
plotly
python-dotenv
```

## Configuration

1. Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

2. Prepare your data:
- Ensure `hospital_patient_data.csv` is in the project root
- Add your hospital logo as `hospital_logo.png` (optional)

## Data Format
The `hospital_patient_data.csv` should contain the following columns:
```
Patient ID, Patient Name, Email, Gender, Weight (kg), Age, Birth Date, 
Occupation, Address, Insurance Provider, Insurance Policy Number, 
Allergies, Current Medication, Past Medical History, Identification Type, 
Symptoms, Blood Group, Heart Rate (bpm), Blood Oxygen Level (%), 
Height (cm), Sugar Level (mg/dL), Blood Pressure Level
```

## Running the Application

1. Start the Streamlit server:
```bash
streamlit run app.py
```

2. Access the application:
- Open your web browser
- Navigate to `http://localhost:8501`

## Usage Guide

### Home Page
- View welcome message
- Access navigation menu

### Patient Analysis
1. Select a patient from the dropdown menu
2. Click "Generate Analysis" button
3. View results in three tabs:
   - Analysis: View vital signs and health metrics
   - Prescription: View AI-generated recommendations
   - Raw Data: Access complete patient data

## Features in Detail

### Health Metrics Visualization
- Vital signs comparison with population averages
- BMI analysis with color-coded ranges
- Interactive charts and graphs

### AI Analysis
- Comprehensive health status evaluation
- Symptom correlation analysis
- Personalized health recommendations

### Prescription Generation
- Generic medication recommendations
- Dosage and duration specifications
- Side effects information

### Patient Data Management
- Secure patient information storage
- Easy access to medical history
- Insurance information tracking

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support, please contact:
- Email: subhankarpatra2118@gmail.com
- Issue Tracker: GitHub Issues

## Acknowledgments
- Developed by Subhankar Patra and Team Dhanvantari
- Powered by Groq AI
- Built with Streamlit

## Version History
- v1.0.0: Initial release
  - Basic patient analysis
  - AI recommendations
  - Health metrics visualization

---

Built with ❤️ by Team Dhanvantari