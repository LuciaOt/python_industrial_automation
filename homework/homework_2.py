import requests
import pandas as pd
import matplotlib.pyplot as plt
import json
import os

''' From NREL's official documentation I used these data https://developer.nrel.gov/docs/solar/pvwatts/v8/
and used  DEMO_KEY

I decided to fetch column ac_monthly (the usable electricity that comes out of your solar system) and 
capacity factor (how much energy you ACTUALLY get vs. how much you could get if the system ran at full power 24/7 all year)   
'''
class NRELSolarDataAnalyzer:
   
    def __init__(self, api_key='DEMO_KEY', lat=34.0522, lon=-118.2437):
        self.base_url = "https://developer.nrel.gov/api/pvwatts/v8.json"
        self.params = {
            'api_key': api_key,
            'lat': lat,
            'lon': lon,
            'system_capacity': 4,   # 4 kW system
            'azimuth': 180,         # South-facing
            'tilt': 20,             # Panel tilt angle
            'array_type': 1,        # Fixed - Roof Mounted
            'module_type': 1,       # Premium module
            'losses': 14            # System losses
        }
        self.data = None
        self.df = None
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        
    
    def fetch_data(self):
        print("Fetching data from NREL API...")
        try:
            response = requests.get(self.base_url, params=self.params)
            
            if response.status_code == 200:
                self.data = response.json()
                print("Data fetched successfully!")
                return True
            else:
                print(f"Error fetching data: {response.status_code}")
                print(response.text)
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return False
    
    def process_data(self):
        if self.data is None:
            print("No data available. Please fetch data first.")
            return None
        
        outputs = self.data['outputs']
        
        # Create a comprehensive pandas DataFrame with all monthly data
        self.df = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'AC_Output_kWh': outputs['ac_monthly'],
            'DC_Output_kWh': outputs['dc_monthly']
        })
        
       
        print("\nDataFrame with all fetched data:")
        print(self.df)
        
        return self.df
    
   
    def create_bar_chart(self, ax):
        if self.df is None:
            print("No dataframe available. Please process data first.")
            return
        
        ax.bar(self.df['Month'], self.df['AC_Output_kWh'], 
               color='skyblue', edgecolor='navy')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('AC Output (kWh)', fontsize=12)
        ax.set_title('Monthly Solar Energy Production - Los Angeles', 
                     fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        for i, v in enumerate(self.df['AC_Output_kWh']):
            ax.text(i, v + 10, f'{v:.0f}', ha='center', 
                    va='bottom', fontsize=9)
    
    def create_line_chart(self, ax):
        if self.df is None:
            print("No dataframe available. Please process data first.")
            return
        
        ax.plot(self.df['Month'], self.df['AC_Output_kWh'], 
                marker='o', linewidth=2, markersize=8, 
                color='orange', label='Monthly Output')
        ax.fill_between(range(len(self.df)), self.df['AC_Output_kWh'], 
                        alpha=0.3, color='orange')
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('AC Output (kWh)', fontsize=12)
        ax.set_title('Solar Energy Production Trend', 
                     fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()
    
    def visualize(self, save_image=False, save_path='nrel_solar_data.png'):
        if self.df is None:
            print("No dataframe available. Please process data first.")
            return
     
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        self.create_bar_chart(axes[0])
        self.create_line_chart(axes[1])
        plt.tight_layout()
        plt.show()
    
    def save_to_csv(self, file_path='nrel_solar_data.csv'):
        if self.df is None:
            print("No dataframe available. Please process data first.")
            return
        
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.script_dir, file_path)
        
        self.df.to_csv(file_path, index=False)
        print(f"Data saved to '{file_path}'")
    
    def run_analysis(self, save_csv=True, save_image=False):
        if not self.fetch_data():
            return False
        self.process_data()
        if save_csv:
            self.save_to_csv()
        self.visualize(save_image=save_image)
        return True


def main():
    # Create analyzer instance for Los Angeles
    analyzer = NRELSolarDataAnalyzer(
        api_key='DEMO_KEY',
        lat=34.0522,    # Los Angeles latitude
        lon=-118.2437   # Los Angeles longitude
    )
    
    analyzer.run_analysis(save_csv=True, save_image=False)
    

if __name__ == "__main__":
    main()