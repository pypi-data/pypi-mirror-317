Please read more about this algorithm in: https://doi.org/10.1016/j.cie.2024.110812
At the moment, we are working diligently to improve and update SPINEX. Please share your thoughts and suggestions with us.

# Example of using this algorithm
import numpy as np
from spinex_timeseries import SPINEX_Timeseries
 
# Generate sample data
time = np.linspace(0, 20, 100)
data = np.sin(time) + np.random.normal(0, 0.1, 100)
 
# Initialize the model
model = SPINEX_Timeseries(data, forecast_horizon=5)
 
# Make predictions
predictions = model.predict()
print("Predicted Values:", predictions)
 
# Detect anomalies
anomalies, threshold = model.detect_anomalies()
print("Anomalies Detected:", anomalies)
 
# Plot predictions
model.plot_prediction()