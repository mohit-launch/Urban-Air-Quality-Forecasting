import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Function to calculate so2 individual pollutant index
def cal_SOi(so2):
    si=0
    if (so2<=40):
     si= so2*(50/40)
    elif (so2>40 and so2<=80):
     si= 50+(so2-40)*(50/40)
    elif (so2>80 and so2<=380):
     si= 100+(so2-80)*(100/300)
    elif (so2>380 and so2<=800):
     si= 200+(so2-380)*(100/420)
    elif (so2>800 and so2<=1600):
     si= 300+(so2-800)*(100/800)
    elif (so2>1600):
     si= 400+(so2-1600)*(100/800)
    return si

# Function to calculate no2 individual pollutant index
def cal_Noi(no2):
    ni=0
    if(no2<=40):
     ni= no2*50/40
    elif(no2>40 and no2<=80):
     ni= 50+(no2-40)*(50/40)
    elif(no2>80 and no2<=180):
     ni= 100+(no2-80)*(100/100)
    elif(no2>180 and no2<=280):
     ni= 200+(no2-180)*(100/100)
    elif(no2>280 and no2<=400):
     ni= 300+(no2-280)*(100/120)
    else:
     ni= 400+(no2-400)*(100/120)
    return ni

# Function to calculate rspm individual pollutant index
def cal_RSPMI(rspm):
    rpi=0
    if(rspm<=30):
     rpi=rspm*50/30
    elif(rspm>30 and rspm<=60):
     rpi=50+(rspm-30)*50/30
    elif(rspm>60 and rspm<=90):
     rpi=100+(rspm-60)*100/30
    elif(rspm>90 and rspm<=120):
     rpi=200+(rspm-90)*100/30
    elif(rspm>120 and rspm<=250):
     rpi=300+(rspm-120)*(100/130)
    else:
     rpi=400+(rspm-250)*(100/130)
    return rpi

# Function to calculate spm individual pollutant index
def cal_SPMi(spm):
    spi=0
    if(spm<=50):
     spi=spm*50/50
    elif(spm>50 and spm<=100):
     spi=50+(spm-50)*(50/50)
    elif(spm>100 and spm<=250):
     spi= 100+(spm-100)*(100/150)
    elif(spm>250 and spm<=350):
     spi=200+(spm-250)*(100/100)
    elif(spm>350 and spm<=430):
     spi=300+(spm-350)*(100/80)
    else:
     spi=400+(spm-430)*(100/430)
    return spi

def get_aqi_category(x):
    if x<=50:
        return "Good"
    elif x>50 and x<=100:
        return "Moderate"
    elif x>100 and x<=200:
        return "Poor"
    elif x>200 and x<=300:
        return "Unhealthy"
    elif x>300 and x<=400:
        return "Very unhealthy"
    elif x>400:
        return "Hazardous"
    return "Unknown"

# Load the model
@st.cache_resource
def load_model():
    try:
        with open('aqi_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("Model file 'aqi_model.pkl' not found. Please make sure it is in the same directory.")
        return None

model = load_model()

st.title("Air Quality Index (AQI) Predictor")
st.write("Enter the pollutant values to predict the AQI and its category.")

# Input form
with st.form("aqi_form"):
    col1, col2 = st.columns(2)
    with col1:
        so2 = st.number_input("SO2 (Sulphur Dioxide)", min_value=0.0, format="%.2f")
        rspm = st.number_input("RSPM (Respirable Suspended Particulate Matter)", min_value=0.0, format="%.2f")
    with col2:
        no2 = st.number_input("NO2 (Nitrogen Dioxide)", min_value=0.0, format="%.2f")
        spm = st.number_input("SPM (Suspended Particulate Matter)", min_value=0.0, format="%.2f")
    
    submitted = st.form_submit_button("Predict AQI")

if submitted:
    if model:
        # Calculate individual indices
        SOi = cal_SOi(so2)
        Noi = cal_Noi(no2)
        Rpi = cal_RSPMI(rspm)
        SPMi = cal_SPMi(spm)

        # Prepare input for model
        # The model expects ['SOi', 'Noi', 'Rpi', 'SPMi']
        input_data = pd.DataFrame([[SOi, Noi, Rpi, SPMi]], columns=['SOi', 'Noi', 'Rpi', 'SPMi'])
        
        try:
            prediction = model.predict(input_data)
            predicted_result = prediction[0]
            
            aqi_category = ""
            # Check if prediction is numeric or string (Classifier vs Regressor)
            if isinstance(predicted_result, (str, np.str_)):
                aqi_category = predicted_result
                st.success(f"Predicted AQI Category: {predicted_result}")
            else:
                # If regressor, we get a number, so we categorize it
                st.success(f"Predicted AQI: {predicted_result:.2f}")
                aqi_category = get_aqi_category(predicted_result)
            
            # Display category with styling
            if aqi_category in ["Unhealthy", "Very unhealthy", "Hazardous"]:
                st.markdown(f"""
                    <div style="padding: 20px; background-color: #ff4b4b; color: white; border-radius: 10px; text-align: center;">
                        <h2 style="margin:0;">{aqi_category}</h2>
                        <p style="margin:0;">Air quality is considered {aqi_category.lower()}.</p>
                    </div>
                """, unsafe_allow_html=True)
            elif aqi_category == "Poor":
                 st.markdown(f"""
                    <div style="padding: 20px; background-color: #ffa500; color: white; border-radius: 10px; text-align: center;">
                        <h2 style="margin:0;">{aqi_category}</h2>
                        <p style="margin:0;">Air quality is considered {aqi_category.lower()}.</p>
                    </div>
                """, unsafe_allow_html=True)
            elif aqi_category == "Moderate":
                 st.markdown(f"""
                    <div style="padding: 20px; background-color: #ffd700; color: black; border-radius: 10px; text-align: center;">
                        <h2 style="margin:0;">{aqi_category}</h2>
                        <p style="margin:0;">Air quality is considered {aqi_category.lower()}.</p>
                    </div>
                """, unsafe_allow_html=True)
            elif aqi_category == "Good":
                 st.markdown(f"""
                    <div style="padding: 20px; background-color: #28a745; color: white; border-radius: 10px; text-align: center;">
                        <h2 style="margin:0;">{aqi_category}</h2>
                        <p style="margin:0;">Air quality is considered {aqi_category.lower()}.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.info(f"AQI Category: {aqi_category}")

            
            with st.expander("See Calculation Details"):
                st.write(f"Calculated Indices:")
                st.write(f"- SOi: {SOi:.2f}")
                st.write(f"- Noi: {Noi:.2f}")
                st.write(f"- Rpi: {Rpi:.2f}")
                st.write(f"- SPMi: {SPMi:.2f}")

        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
    else:
        st.error("Model could not be loaded. Please check the model file.")
