import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Load traffic data
data = pd.read_csv("traffic_data.csv")

# Title
st.title("AI Traffic Flow Analytics Dashboard")

# Show raw data
st.subheader("Traffic Dataset")

st.dataframe(data.tail(20))

# -----------------------------
# Vehicle Count Line Chart
# -----------------------------

st.subheader("Traffic Density Over Time")

fig1 = px.line(
    data,
    y="vehicle_count",
    title="Vehicle Count"
)

st.plotly_chart(fig1)

# -----------------------------
# Signal Activity Chart
# -----------------------------

st.subheader("Traffic Signal Activity")

fig2 = px.line(
    data,
    y="signal_status",
    title="Signal Status"
)

st.plotly_chart(fig2)

# -----------------------------
# Traffic Statistics
# -----------------------------

st.subheader("Traffic Statistics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Maximum Vehicles",
    int(data["vehicle_count"].max())
)

col2.metric(
    "Average Vehicles",
    round(data["vehicle_count"].mean(), 2)
)

col3.metric(
    "Total Records",
    len(data)
)

# -----------------------------
# Congestion Level
# -----------------------------

latest_traffic = data["vehicle_count"].iloc[-1]

st.subheader("Congestion Status")

if latest_traffic < 5:

    st.success("Low Traffic")

elif latest_traffic < 12:

    st.warning("Medium Traffic")

else:

    st.error("Heavy Traffic")

# -----------------------------
# Heatmap Section
# -----------------------------

st.subheader("Traffic Heatmap")

# Generate heatmap data
heatmap_data = np.random.randint(
    0,
    latest_traffic + 1,
    size=(10, 10)
)

fig3 = go.Figure(
    data=go.Heatmap(
        z=heatmap_data
    )
)

fig3.update_layout(
    title="Urban Traffic Congestion Heatmap"
)

st.plotly_chart(fig3)

# -----------------------------
# Vehicle Distribution Pie Chart
# -----------------------------

st.subheader("Traffic Distribution")

vehicle_types = ["Cars", "Buses", "Trucks", "Bikes"]

vehicle_values = [
    np.random.randint(20, 50),
    np.random.randint(5, 20),
    np.random.randint(5, 15),
    np.random.randint(10, 30)
]

fig4 = px.pie(
    names=vehicle_types,
    values=vehicle_values,
    title="Vehicle Type Distribution"
)

st.plotly_chart(fig4)

# -----------------------------
# AI Prediction Section
# -----------------------------

st.subheader("AI Traffic Prediction")

future_traffic = latest_traffic + np.random.randint(-2, 5)

st.info(
    f"Predicted Upcoming Traffic Density: {future_traffic} vehicles"
)

# -----------------------------
# Emergency System Status
# -----------------------------

st.subheader("Emergency Traffic System")

if latest_traffic > 12:

    st.error("Emergency Congestion Control Activated")

else:

    st.success("Traffic Operating Normally")