import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# Define the file paths
file_path_data = r"C:\Users\tcarlisle\Documents\Python\Plotting Data\run02.csv"  # Data file path
file_path_control = r"C:\Users\tcarlisle\Documents\Python\Plotting Data\cuttercycling.csv"  # Control data file path

# Read the CSV files
df_data = pd.read_csv(file_path_data, index_col = 'Time')
df_control = pd.read_csv(file_path_control, index_col = 'Time')

print(df_data.dtypes)

# Ensure the length of the two dataframes match by aligning them
min_len = min(len(df_data), len(df_control))
df_data = df_data[:min_len]
df_control = df_control[:min_len]

# Check if the CSV contains the required columns for both data and control
required_columns = ["Fx", "Fy", "Fz", "Tx", "Ty", "Tz"]
for col in required_columns:
    if col not in df_data.columns:
        raise ValueError(f"Missing column: {col} in data CSV file")
    if col not in df_control.columns:
        raise ValueError(f"Missing column: {col} in control CSV file")

# Convert Forces from N to lb (for data and control)
df_data["Fx_lb"] = df_data["Fx"] * 0.224809 + 14 
df_data["Fy_lb"] = df_data["Fy"] * 0.224809 - 3 
df_data["Fz_lb"] = df_data["Fz"] * 0.224809 - 46.1

df_control["Fx_lb"] = df_control["Fx"] * 0.224809 + 14 - 5.4
df_control["Fy_lb"] = df_control["Fy"] * 0.224809 - 3 + 6.6
df_control["Fz_lb"] = df_control["Fz"] * 0.224809 - 46.1 + 41.8

# Convert Moments from Nm to lb*in (for data and control)
df_data["Tx_lb_in"] = df_data["Tx"] * 8.8507 
df_data["Ty_lb_in"] = df_data["Ty"] * 8.8507 + 200
df_data["Tz_lb_in"] = df_data["Tz"] * 8.8507 

print(df_data.describe())

df_control["Tx_lb_in"] = df_control["Tx"] * 8.8507 
df_control["Ty_lb_in"] = df_control["Ty"] * 8.8507 
df_control["Tz_lb_in"] = df_control["Tz"] * 8.8507 

print(df_control.describe())

# Set up the plot with extra space between the two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# Plot Forces in lb (Fx, Fy, Fz)
line_fx_data, = ax1.plot(df_data.index, df_data["Fx_lb"], label="Fx (Data, lb)", linestyle="-")
line_fy_data, = ax1.plot(df_data.index, df_data["Fy_lb"], label="Fy (Data, lb)", linestyle="--")
line_fz_data, = ax1.plot(df_data.index, df_data["Fz_lb"], label="Fz (Data, lb)", linestyle=":")

line_fx_control, = ax1.plot(df_control.index, df_control["Fx_lb"], label="Fx (Control, lb)", linestyle="-", color='orange')
line_fy_control, = ax1.plot(df_control.index, df_control["Fy_lb"], label="Fy (Control, lb)", linestyle="--", color='orange')
line_fz_control, = ax1.plot(df_control.index, df_control["Fz_lb"], label="Fz (Control, lb)", linestyle=":", color='orange')

ax1.set_xlabel("Time (Index)")
ax1.set_ylabel("Force (lb)")
ax1.set_title("Forces over Time (in lb)")
ax1.legend()
ax1.grid(True)

# Plot Moments in lb*in (Tx, Ty, Tz)
line_tx_data, = ax2.plot(df_data.index, df_data["Tx_lb_in"], label="Tx (Data, lb·in)", linestyle="-")
line_ty_data, = ax2.plot(df_data.index, df_data["Ty_lb_in"], label="Ty (Data, lb·in)", linestyle="--")
line_tz_data, = ax2.plot(df_data.index, df_data["Tz_lb_in"], label="Tz (Data, lb·in)", linestyle=":")

line_tx_control, = ax2.plot(df_control.index, df_control["Tx_lb_in"], label="Tx (Control, lb·in)", linestyle="-", color='orange')
line_ty_control, = ax2.plot(df_control.index, df_control["Ty_lb_in"], label="Ty (Control, lb·in)", linestyle="--", color='orange')
line_tz_control, = ax2.plot(df_control.index, df_control["Tz_lb_in"], label="Tz (Control, lb·in)", linestyle=":", color='orange')

ax2.set_xlabel("Time (Index)")
ax2.set_ylabel("Moment (lb·in)")
ax2.set_title("Moments over Time (in lb·in)")
ax2.legend()
ax2.grid(True)

# Adjust subplot parameters to provide more space between the graphs
plt.subplots_adjust(bottom=0.2, hspace=0.35)  # Increase hspace for more space between graphs

# Sliders for adjusting the start and end index
ax_slider_start = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_start = Slider(ax_slider_start, 'Start Index', 0, min_len-1, valinit=0, valstep=.1)

ax_slider_end = plt.axes([0.2, 0.06, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_end = Slider(ax_slider_end, 'End Index', 0, min_len-1, valinit=min_len-1, valstep=.1)

# Button functions to toggle visibility of each component (force and moment)
def toggle_fx_data(event):
    line_fx_data.set_visible(not line_fx_data.get_visible())
    update_button_color(button_fx_data, line_fx_data.get_visible())
    fig.canvas.draw()

def toggle_fy_data(event):
    line_fy_data.set_visible(not line_fy_data.get_visible())
    update_button_color(button_fy_data, line_fy_data.get_visible())
    fig.canvas.draw()

def toggle_fz_data(event):
    line_fz_data.set_visible(not line_fz_data.get_visible())
    update_button_color(button_fz_data, line_fz_data.get_visible())
    fig.canvas.draw()

def toggle_tx_data(event):
    line_tx_data.set_visible(not line_tx_data.get_visible())
    update_button_color(button_tx_data, line_tx_data.get_visible())
    fig.canvas.draw()

def toggle_ty_data(event):
    line_ty_data.set_visible(not line_ty_data.get_visible())
    update_button_color(button_ty_data, line_ty_data.get_visible())
    fig.canvas.draw()

def toggle_tz_data(event):
    line_tz_data.set_visible(not line_tz_data.get_visible())
    update_button_color(button_tz_data, line_tz_data.get_visible())
    fig.canvas.draw()

def toggle_fx_control(event):
    line_fx_control.set_visible(not line_fx_control.get_visible())
    update_button_color(button_fx_control, line_fx_control.get_visible())
    fig.canvas.draw()

def toggle_fy_control(event):
    line_fy_control.set_visible(not line_fy_control.get_visible())
    update_button_color(button_fy_control, line_fy_control.get_visible())
    fig.canvas.draw()

def toggle_fz_control(event):
    line_fz_control.set_visible(not line_fz_control.get_visible())
    update_button_color(button_fz_control, line_fz_control.get_visible())
    fig.canvas.draw()

def toggle_tx_control(event):
    line_tx_control.set_visible(not line_tx_control.get_visible())
    update_button_color(button_tx_control, line_tx_control.get_visible())
    fig.canvas.draw()

def toggle_ty_control(event):
    line_ty_control.set_visible(not line_ty_control.get_visible())
    update_button_color(button_ty_control, line_ty_control.get_visible())
    fig.canvas.draw()

def toggle_tz_control(event):
    line_tz_control.set_visible(not line_tz_control.get_visible())
    update_button_color(button_tz_control, line_tz_control.get_visible())
    fig.canvas.draw()

# Function to update button color based on visibility
def update_button_color(button, is_visible):
    if is_visible:
        button.color = 'lightblue'  # Visible color
    else:
        button.color = 'lightgray'  # Hidden color
    button.label.set_color('black')  # Set button label color
    button.canvas.draw()

# Create buttons for the force and moment components (Data and Control)
ax_button_fx_data = plt.axes([0.02, 0.93, 0.05, 0.05])
button_fx_data = Button(ax_button_fx_data, 'Fx (Data)', color='lightblue')
button_fx_data.on_clicked(toggle_fx_data)

ax_button_fy_data = plt.axes([0.02, 0.87, 0.05, 0.05])
button_fy_data = Button(ax_button_fy_data, 'Fy (Data)', color='lightblue')
button_fy_data.on_clicked(toggle_fy_data)

ax_button_fz_data = plt.axes([0.02, 0.81, 0.05, 0.05])
button_fz_data = Button(ax_button_fz_data, 'Fz (Data)', color='lightblue')
button_fz_data.on_clicked(toggle_fz_data)

ax_button_tx_data = plt.axes([0.02, 0.75, 0.05, 0.05])
button_tx_data = Button(ax_button_tx_data, 'Tx (Data)', color='lightblue')
button_tx_data.on_clicked(toggle_tx_data)

ax_button_ty_data = plt.axes([0.02, 0.69, 0.05, 0.05])
button_ty_data = Button(ax_button_ty_data, 'Ty (Data)', color='lightblue')
button_ty_data.on_clicked(toggle_ty_data)

ax_button_tz_data = plt.axes([0.02, 0.63, 0.05, 0.05])
button_tz_data = Button(ax_button_tz_data, 'Tz (Data)', color='lightblue')
button_tz_data.on_clicked(toggle_tz_data)

ax_button_fx_control = plt.axes([0.02, 0.57, 0.05, 0.05])
button_fx_control = Button(ax_button_fx_control, 'Fx (Control)', color='lightblue')
button_fx_control.on_clicked(toggle_fx_control)

ax_button_fy_control = plt.axes([0.02, 0.51, 0.05, 0.05])
button_fy_control = Button(ax_button_fy_control, 'Fy (Control)', color='lightblue')
button_fy_control.on_clicked(toggle_fy_control)

ax_button_fz_control = plt.axes([0.02, 0.45, 0.05, 0.05])
button_fz_control = Button(ax_button_fz_control, 'Fz (Control)', color='lightblue')
button_fz_control.on_clicked(toggle_fz_control)

ax_button_tx_control = plt.axes([0.02, 0.39, 0.05, 0.05])
button_tx_control = Button(ax_button_tx_control, 'Tx (Control)', color='lightblue')
button_tx_control.on_clicked(toggle_tx_control)

ax_button_ty_control = plt.axes([0.02, 0.33, 0.05, 0.05])
button_ty_control = Button(ax_button_ty_control, 'Ty (Control)', color='lightblue')
button_ty_control.on_clicked(toggle_ty_control)

ax_button_tz_control = plt.axes([0.02, 0.27, 0.05, 0.05])
button_tz_control = Button(ax_button_tz_control, 'Tz (Control)', color='lightblue')
button_tz_control.on_clicked(toggle_tz_control)

# Define update function for sliders and adjust the axis limits based on the sliders
def update(val):
    start_index = int(slider_start.val)
    end_index = int(slider_end.val)
    
    # Use .iloc to slice the DataFrame based on positional index
    line_fx_data.set_data(df_data.index[start_index:end_index], df_data["Fx_lb"].iloc[start_index:end_index])
    line_fy_data.set_data(df_data.index[start_index:end_index], df_data["Fy_lb"].iloc[start_index:end_index])
    line_fz_data.set_data(df_data.index[start_index:end_index], df_data["Fz_lb"].iloc[start_index:end_index])
    
    line_fx_control.set_data(df_control.index[start_index:end_index], df_control["Fx_lb"].iloc[start_index:end_index])
    line_fy_control.set_data(df_control.index[start_index:end_index], df_control["Fy_lb"].iloc[start_index:end_index])
    line_fz_control.set_data(df_control.index[start_index:end_index], df_control["Fz_lb"].iloc[start_index:end_index])
    
    line_tx_data.set_data(df_data.index[start_index:end_index], df_data["Tx_lb_in"].iloc[start_index:end_index])
    line_ty_data.set_data(df_data.index[start_index:end_index], df_data["Ty_lb_in"].iloc[start_index:end_index])
    line_tz_data.set_data(df_data.index[start_index:end_index], df_data["Tz_lb_in"].iloc[start_index:end_index])
    
    line_tx_control.set_data(df_control.index[start_index:end_index], df_control["Tx_lb_in"].iloc[start_index:end_index])
    line_ty_control.set_data(df_control.index[start_index:end_index], df_control["Ty_lb_in"].iloc[start_index:end_index])
    line_tz_control.set_data(df_control.index[start_index:end_index], df_control["Tz_lb_in"].iloc[start_index:end_index])

    # Update x-axis limits to match the visible range of the data
    ax1.set_xlim(df_data.index[start_index], df_data.index[end_index])
    ax2.set_xlim(df_data.index[start_index], df_data.index[end_index])
    
    fig.canvas.draw_idle()


# Attach update function to sliders
slider_start.on_changed(update)
slider_end.on_changed(update)

# Show the plot
plt.show()
