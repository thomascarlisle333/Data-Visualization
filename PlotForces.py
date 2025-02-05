import pandas as pd
import matplotlib.pyplot as plt

# Define the file path
file_path = r"C:\Users\tcarlisle\Documents\Python\Plotting Data\run02.csv"  # Update with your file path

# Read the CSV file
df = pd.read_csv(file_path)

# Check if the CSV contains the required columns
required_columns = ["Fx", "Fy", "Fz", "Tx", "Ty", "Tz"]
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing column: {col} in CSV file")

# Convert Forces from N to lb
df["Fx_lb"] = df["Fx"] * 0.224809 + 14
df["Fy_lb"] = df["Fy"] * 0.224809 - 3
df["Fz_lb"] = df["Fz"] * 0.224809 - 46.1

# Convert Moments from Nm to lb*in
df["Tx_lb_in"] = df["Tx"] * 0.224809 * 12 - 8
df["Ty_lb_in"] = df["Ty"] * 0.224809 * 12 + 78
df["Tz_lb_in"] = df["Tz"] * 0.224809 * 12 - 25

# Prompt user for time range
start_index = int(input("Enter the start index: "))
end_index = int(input("Enter the end index: "))

# Slice the DataFrame based on the user input range
df_range = df.iloc[start_index:end_index]

# Plot Forces in lb (Fx, Fy, Fz) for the specified range
plt.figure(figsize=(10, 5))
plt.plot(df_range.index, df_range["Fx_lb"], label="Fx (lb)", linestyle="-")
plt.plot(df_range.index, df_range["Fy_lb"], label="Fy (lb)", linestyle="--")
plt.plot(df_range.index, df_range["Fz_lb"], label="Fz (lb)", linestyle=":")
plt.xlabel("Time (Index)")
plt.ylabel("Force (lb)")
plt.title(f"Forces from Index {start_index} to {end_index} (in lb)")
plt.legend()
plt.grid(True)

# Plot Moments in lb*in (Tx, Ty, Tz) for the specified range
plt.figure(figsize=(10, 5))
plt.plot(df_range.index, df_range["Tx_lb_in"], label="Tx (lb·in)", linestyle="-")
plt.plot(df_range.index, df_range["Ty_lb_in"], label="Ty (lb·in)", linestyle="--")
plt.plot(df_range.index, df_range["Tz_lb_in"], label="Tz (lb·in)", linestyle=":")
plt.xlabel("Time (Index)")
plt.ylabel("Moment (lb·in)")
plt.title(f"Moments from Index {start_index} to {end_index} (in lb·in)")
plt.legend()
plt.grid(True)

# Show plots
plt.show()
