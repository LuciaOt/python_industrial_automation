import requests
import pandas as pd
import matplotlib.pyplot as plt
import json

''' From NREL's official documentation I used these data https://developer.nrel.gov/docs/solar/pvwatts/v8/
and used  DEMO_KEY
'''

base_url = "https://developer.nrel.gov/api/pvwatts/v8.json"

# parameters chosen based on documentation - LA
params = {
    'api_key': 'DEMO_KEY',  
    'lat': 34.0522,        
    'lon': -118.2437,      
    'system_capacity': 4,   
    'azimuth': 180,         
    'tilt': 20,             
    'array_type': 1,        
    'module_type': 1,       
    'losses': 14            
}

'''Fetch data from API:
    I decided to fetch column ac_monthly (the usable electricity that comes out of your solar system) and 
    capacity factor (how much energy you ACTUALLY get vs. how much you could get if the system ran at full power 24/7 all year)'''
print("Fetching data from NREL API...")
response = requests.get(base_url, params=params)
if response.status_code == 200:
    data = response.json()
    print("Data fetched successfully!")
    
    ac_monthly = data['outputs']['ac_monthly']
    
    # Create a pandas DataFrame
    df = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'AC_Output_kWh': ac_monthly
    })
    
    print("\nDataFrame:")
    print(df)
    
    annual_output = data['outputs']['ac_annual']
    capacity_factor = data['outputs']['capacity_factor']
    

    
    # Create visualizations
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # Bar chart of monthly output
    axes[0].bar(df['Month'], df['AC_Output_kWh'], color='skyblue', edgecolor='navy')
    axes[0].set_xlabel('Month', fontsize=12)
    axes[0].set_ylabel('AC Output (kWh)', fontsize=12)
    axes[0].set_title('Monthly Solar Energy Production - Los Angeles', fontsize=14, fontweight='bold')
    axes[0].grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, v in enumerate(df['AC_Output_kWh']):
        axes[0].text(i, v + 10, f'{v:.0f}', ha='center', va='bottom', fontsize=9)
    
    # Line chart showing trend
    axes[1].plot(df['Month'], df['AC_Output_kWh'], marker='o', linewidth=2, 
                 markersize=8, color='orange', label='Monthly Output')
    axes[1].fill_between(range(len(df)), df['AC_Output_kWh'], alpha=0.3, color='orange')
    axes[1].set_xlabel('Month', fontsize=12)
    axes[1].set_ylabel('AC Output (kWh)', fontsize=12)
    axes[1].set_title('Solar Energy Production Trend', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig('nrel_solar_data.png', dpi=300, bbox_inches='tight')
    print("\nVisualization saved as 'nrel_solar_data.png'")
    plt.show()
    
    
else:
    print(f"Error fetching data: {response.status_code}")
    print(response.text)