
import tkinter as tk
from tkinter import messagebox
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Load saved artifacts
model = joblib.load("C:/Users/Acer/gbr_best_model.pkl")
scaler = joblib.load("C:/Users/Acer/scaler.pkl")
features = joblib.load("C:/Users/Acer/feature_names.pkl")
fi_df = joblib.load("C:/Users/Acer/feature_importance.pkl")


# Main Window
root = tk.Tk()
root.title("Concrete Strength Predictor")
root.geometry("900x600")

# Frames
input_frame = tk.LabelFrame(root, text="Input Parameters", padx=10, pady=10)
input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

output_frame = tk.LabelFrame(root, text="Prediction Output", padx=10, pady=10)
output_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

plot_frame = tk.LabelFrame(root, text="Feature Importance", padx=10, pady=10)
plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)


# Input Fields
entries = {}

for i, feature in enumerate(features):
    label = tk.Label(input_frame, text=feature)
    label.grid(row=i, column=0, sticky="w", pady=2)

    entry = tk.Entry(input_frame, width=10)
    entry.insert(0, "0.0")
    entry.grid(row=i, column=1, pady=2)

    entries[feature] = entry


# Prediction Function
def predict_strength():
    try:
        values = [float(entries[f].get()) for f in features]
        x = np.array(values).reshape(1, -1)
        #x_scaled = scaler.transform(x)
        prediction = model.predict(x)[0]

        result_label.config(
            text=f"Predicted Compressive Strength: {prediction:.2f} MPa",
            fg="green"
        )

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values")


# Predict Button
predict_btn = tk.Button(
    output_frame,
    text="Predict Strength",
    command=predict_strength,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12)
)
predict_btn.pack(pady=10)

result_label = tk.Label(
    output_frame,
    text="Predicted Compressive Strength: -- MPa",
    font=("Arial", 14)
)
result_label.pack(pady=5)


# Feature Importance Plot
fig, ax = plt.subplots(figsize=(4, 5))
fi_sorted = fi_df.sort_values(by="Importance", ascending=True)

ax.barh(fi_sorted["Feature"], fi_sorted["Importance"])
ax.set_title("Feature Importance")
ax.set_xlabel("Importance Score")

canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# Run App
root.mainloop()

'''

import sklearn
import xgboost

print("sklearn:", sklearn.__version__)
print("xgboost:", xgboost.__version__)'''

