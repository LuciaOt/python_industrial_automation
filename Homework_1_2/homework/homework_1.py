import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

data_path = r'C:\Users\lucia.otiepkova\robotdreams\rd-python-industrial-automation\datasets\steel_copper_welding\V1.csv'
df = pd.read_csv(data_path)
rename_columns = {
    'power (W)': 'Power',
    'welding speed (m/min)': 'WeldingSpeed',
    'gas flow rate (l/min)': 'GasFlowRate',
    'focal position (mm)': 'FocalPosition',
    'angular position (°)': 'AngularPosition',
    'material thickness (mm)': 'MaterialThickness',
    'weld number': 'WeldNumber',
    'cross section positon in the weld (mm)': 'CrossSectionPosition',
    'cracking in the weld metal': 'Cracking',
    'weld seam width steel (µm)': 'WeldWidthSteel',
    'weld seam width copper (µm)': 'WeldWidthCopper',
    'weld depth copper (µm)': 'WeldDepthCopper',
    'gap': 'Gap'
}

df.rename(columns=rename_columns, inplace=True)

factors = ['Power', 'WeldingSpeed', 'AngularPosition', 'FocalPosition', 'GasFlowRate', 'MaterialThickness']

# scatter plot 
fig = px.scatter(
    df,
    x='WeldNumber',
    y='WeldDepthCopper',
    color='Cracking',
    facet_col='CrossSectionPosition',
    title='Weld Depth Over Weld Numbers (Faceted by Cross-Section Position)'
)

fig.update_layout(
    xaxis_title='Weld Number',
    yaxis_title='Weld Depth (Copper)',
    legend_title='Cracking',
    margin=dict(t=50, l=50, r=50, b=50)
)

fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))  # Simplify facet labels
fig.show()


# Violin plot for each factor's influence on weld depth
# for factor in factors:
#     sns.violinplot(data=df, x=factor, y='WeldDepthCopper', hue='Cracking', split=True, palette={'yes': 'red', 'no': 'blue'})
#     plt.title(f'Violin Plot of Weld Depth by {factor}')
#     plt.xlabel(factor)
#     plt.ylabel('Weld Depth (Copper)')
#     plt.legend(title='Cracking', loc='upper right', fontsize=8, title_fontsize=10)
#     plt.show()



# Pairplot 
# pairplot = sns.pairplot(df, vars=factors + ['WeldDepthCopper'], hue='Cracking', palette={'yes': 'red', 'no': 'blue'})
# pairplot.fig.suptitle('Pairplot of Factors and Weld Depth', y=1.02)

# # Adjust font sizes for axis labels and legend
# for ax in pairplot.axes.flat:
#     ax.set_xlabel(ax.get_xlabel(), fontsize=8)
#     ax.set_ylabel(ax.get_ylabel(), fontsize=8)

# # Ensure the legend is visible and properly formatted
# pairplot._legend.set_title('Cracking')
# pairplot._legend.set_bbox_to_anchor((1.05, 0.5))
# pairplot._legend.get_title().set_fontsize(8)
# for text in pairplot._legend.texts:
#     text.set_fontsize(8)

# plt.show()

