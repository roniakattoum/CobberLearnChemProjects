import matplotlib.pyplot as plt
from pathlib import Path


# Number of carbon atoms in the first 10 linear alkanes (methane to decane)
number_of_carbons = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Corresponding normal boiling points in degrees Celsius
boiling_points_celsius = [
    -161.5,
    -88.6,
    -42.1,
    -0.5,
    36.1,
    68.7,
    98.4,
    125.6,
    150.8,
    174.1,
]

# Create the scatterplot
plt.scatter(number_of_carbons, boiling_points_celsius)
plt.title("Boiling Points of the First 10 Linear Alkanes")
plt.xlabel("Number of Carbon Atoms")
plt.ylabel("Boiling Point (°C)")
plt.xticks(number_of_carbons)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Create the output directory if it does not already exist, then save the plot
output_directory = Path("AlkaneBoilingPoints")
output_directory.mkdir(parents=True, exist_ok=True)
output_file = output_directory / "alkane_boiling_points.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")

print(f"Plot saved to: {output_file.resolve()}")
plt.show()