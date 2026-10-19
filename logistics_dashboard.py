import streamlit as st 
import pandas as pd

st.set_page_config(page_title="Global Supply Chain Hub", page_icon="🌐", layout="wide")

#Logistics Architecture
if "logistics_network" not in st.session_state:
    st.session_state.logistics_network = {
        "depots": {
            "Chicago": {"capacity_tons": 500, "current_load": 320, "status": "Optimal"},
            "Houston": {"capacity_tons": 350, "current_load": 110, "status": "Open"},
            "New York": {"capacity_tons": 600, "current_load": 580, "status": "Overloaded"}, 
            "San Diego": {"capacity_tons": 160, "current_load": 100, "status": "Optimal"},
            "Seattle": {"capacity_tons": 450, "current_load": 300, "status": "Optimal"},
            "Atlanta": {"capacity_tons": 200, "current_load": 100, "status": "Open"}
        },
        #Dictionary
        "active_shipments": [
            {
                "shipment_id": "SHIP-101",
                "contents": "Server Racks",
                "destination": "Chicago",
                "weight": 14.5,
                "status": "In Transit",
                "delay_hours": 0
            },
            {
                "shipment_id": "SHIP-102",
                "contents": "Liquid Cooling Fluid",
                "destination": "New York",
                "weight": 12.3,
                "status": "In Transit"
            },
            {
                "shipment_id": "SHIP-103",
                "contents": "Server Rack Brackets",
                "destination": "Houston",
                "weight": 8.7,
                "status": "In Transit"
            },
            {
                "shipment_id": "SHIP-104",
                "contents": "Sonar Sensor Arrays",
                "destination": "San Diego",
                "weight": 5,
                "status": "In Transit"
            },
            {
                "shipment_id": "SHIP-105",
                "contents": "Titanium Fuselage Bolts",
                "destination": "Seattle",
                "weight": 7,
                "status": "In Transit"
            },
            {
                "shipment_id": "SHIP-106",
                "contents": "Lithium Batteries",
                "destination": "Atlanta",
                "weight": 10,
                "status": "In Transit"
            }            
        ]
    }
    
#Logistics Infrastructure

def process_fleet_diagnostics(network_data):
    total_transit_weight = 0.0
    network_alerts = []
    
    #Loop 1: Calculate total weight of all active shipments
    for shipment in network_data["active_shipments"]:
        total_transit_weight += shipment["weight"]
        
    #Loop 2: Checks depots for capacity overloads
    for depot_name, stats in network_data["depots"].items():
        max_capacity = stats["capacity_tons"]
        current_occupancy = stats["current_load"]
        
        #Calculates depot occupancy %
        occupancy_ratio = current_occupancy / max_capacity
        
        #Critical Risk Flag: depot capacity >=90%
        if occupancy_ratio >= 0.9:
            alert_message = f"🚨 Alert: {depot_name} hub is over 90% occupied."
            network_alerts.append(alert_message)
            
    return total_transit_weight, network_alerts

#Interface titles and CSS styling
st.title("🌐 Global Fleet Operations Control Hub")

st.markdown(
    """
    <style>
        div[data-testid="stMarkdownContainer"] p {
            font-size: 18px !important;
            color: #2c3e50 !important;
            font-weight: 700 !important;
        }
        table {
            width: 100% !important;
            border-collapse: collapse !important;
            margin-top: 15px !important;
        }
        th {
            background-color: #f1f3f5 !important;
            color: #111111 !important;
            font-size: 16px !important;
            font-weight: bold !important;
            padding: 12px 15px !important;
            border-bottom: 3px solid #dee2e6 !important;
            text-align: left !important;
        }
        td {
            padding: 14px 15px !important;
            font-size: 16px !important;
            color: #333333 !important;
            border-bottom: 1px solid #e9ecef !important;
            text-align: left !important;
        }
        tr:nth-child(even) {
            background-color: #f8f9fa !important;
        }
        div[data-testid="stMetricValue"] {
            font-size: 40px !important;
            font-weight: bold !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.write("Track Global Distribution Depots and Active Freight Capacity Loads.")
st.divider()

#Global Calculations    
transit_weight, active_alerts = process_fleet_diagnostics(st.session_state.logistics_network)

#Tracking KPI's
total_depots = len(st.session_state.logistics_network["depots"])
active_shipment_count = len(st.session_state.logistics_network["active_shipments"])

#UI rendering. 3 columns.
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(label="🚚 Total Freight Volume", value=f"{active_shipment_count:,} Cargo Streams")

with metric_col2:
    st.metric(label="📊 Total Transit Weight", value=f"{transit_weight:.2f} Tons")
    
with metric_col3:
    st.metric(label="🏭 Regional Depots", value=f"{total_depots} Hubs")
    
st.divider()

#Geographic Hub Map
st.subheader("🌐 Distribution Map")

#coordinate dictionary for each regional hub
map_coordinate_data = [
    {"City": "Chicago", "latitude": 41.8781, "longitude": -87.6298},
    {"City": "Houston", "latitude": 29.7604, "longitude": -95.3698},
    {"City": "New York", "latitude": 40.7128, "longitude": -74.0060},
    {"City": "San Diego", "latitude": 32.7157, "longitude": -117.1611},
    {"City": "Seattle", "latitude": 47.6062, "longitude": -122.3321},
    {"City": "Atlanta", "latitude": 33.7490, "longitude": -84.3880}
]

#Convert map coordinate data into pandas dataframe
df_map = pd.DataFrame(map_coordinate_data)


#Render map onto the canvas
import pydeck as pdk

st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=39.8283,
        longitude=-98.5795,
        zoom=3.3,
        min_zoom=3.0,
        max_zoom=10.0,
        pitch=0
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_map,
            get_position='[longitude, latitude]',
            get_color='[255,75,75,200]',
            get_radius=80000,
            pickable=True 
        )
    ]
))

st.divider()

#Lower Logistics Workspace
ui_col1, ui_col2 = st.columns(2, gap="large")

#Left Column - Active Shipment Manifest
with ui_col1:
    st.subheader("📋 Active Cargo Manifest")
    st.caption("List of all freight currently in transit.")
    
    if st.session_state.logistics_network["active_shipments"]:
        
        #Convert active shipments dictionary into dataframe
        df_shipments = pd.DataFrame(st.session_state.logistics_network["active_shipments"])
        
        df_shipments.columns = [
            "Shipment Tracking ID", "Cargo Contents",
            "Destination Depot", "Total Weight (Tons)",
            "Current Status", "Delay Log Hours"
        ]
        
        #Render table on left side
        st.table(df_shipments)
        
    else:
        st.info("No Active Freight Shipments.")
        
    
with ui_col2:
    st.subheader("🏭 Warehouse Capacity Ledger")
    st.caption("Track occupancy rates across regional depots.")
    
    #Convert depots dictionary into a dataframe
    df_depots = pd.DataFrame(st.session_state.logistics_network["depots"]).T
    
    #Rename index column keys for clean user presentation
    df_depots.index.name = "Depot Location"
    df_depots.columns = ["Max Capacity (Tons)", "Current Occupancy (Tons)", "System Status"]
    
    #Render data table
    st.table(df_depots)
    
if active_alerts:
    for alert in active_alerts:
        st.error(alert)
    st.write("")
    
st.divider()
st.subheader("➕ Dispatch New Freight Shipment")

form_col1, form_col2, form_col3 = st.columns(3)

with form_col1:
    new_contents = st.text_input("Cargo Contents:", value="Fiber Optic Cable", key="log_contents")
    
with form_col2:
    new_dest = st.selectbox(
        "Destination Depot Location:",
        list(st.session_state.logistics_network["depots"]),
        key="log_dest"
    )
    
with form_col3:
    new_weight = st.number_input("Total Cargo Volume (Tons):", min_value=1.0, value=15.0, step=0.5, key="log_weight")
    
#Render freight dispatch button
if st.button("Dispatch Freight", use_container_width=True):
    
    #Generate unique tracking ID string
    next_id_num = len(st.session_state.logistics_network["active_shipments"]) + 101
    generated_id = f"SHIP-{next_id_num}"
    
    new_cargo_package = {
        "shipment_id": generated_id,
        "contents": new_contents,
        "destination": new_dest,
        "weight": new_weight,
        "status": "In Transit",
        "delay_hours": 0.0
    }
    
    st.session_state.logistics_network["active_shipments"].append(new_cargo_package)
    
    #Automatically update warehouse inventory level
    target_city = new_cargo_package["destination"]
    st.session_state.logistics_network["depots"][target_city]["current_load"] += new_weight
    
    st.toast(f"Success: Container {generated_id} dispatched to {new_dest}")
    st.rerun()
    
    
    
    