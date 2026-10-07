import tkinter as tk
from tkinter import messagebox
import numpy as np
import joblib

# ================= LOAD MODELS =================
try:
    gbrt = joblib.load("gbrt.pkl")
    lgbm = joblib.load("lgbm.pkl")
    xgb = joblib.load("xgb.pkl")
    meta_model = joblib.load("meta_model.pkl")
except:
    print("❌ Model files not found!")
    exit()

# ================= PREDICTION FUNCTION =================
def predict():
    try:
        # Get input values
        values = [
            float(entry_cement.get()),
            float(entry_slag.get()),
            float(entry_flyash.get()),
            float(entry_water.get()),
            float(entry_sp.get()),
            float(entry_coarse.get()),
            float(entry_fine.get()),
            float(entry_age.get())
        ]

        X = np.array([values])

        # Base predictions
        pred_gbrt = gbrt.predict(X)[0]
        pred_lgbm = lgbm.predict(X)[0]
        pred_xgb  = xgb.predict(X)[0]

        # Stacking
        stack_input = np.array([[pred_gbrt, pred_lgbm, pred_xgb]])
        final_pred = meta_model.predict(stack_input)[0]

        result_var.set(f"{round(final_pred, 2)} MPa")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ================= UI =================
root = tk.Tk()
root.title("Concrete Strength Predictor")
root.geometry("400x500")

title = tk.Label(root, text="Concrete Strength Predictor", font=("Arial", 16))
title.pack(pady=10)

# Input fields
def create_input(label_text):
    frame = tk.Frame(root)
    frame.pack(pady=5)

    label = tk.Label(frame, text=label_text, width=25, anchor="w")
    label.pack(side="left")

    entry = tk.Entry(frame)
    entry.pack(side="right")

    return entry

entry_cement = create_input("Cement (kg/m³)")
entry_slag = create_input("Slag (kg/m³)")
entry_flyash = create_input("Fly Ash (kg/m³)")
entry_water = create_input("Water (kg/m³)")
entry_sp = create_input("Superplasticizer (kg/m³)")
entry_coarse = create_input("Coarse Aggregate (kg/m³)")
entry_fine = create_input("Fine Aggregate (kg/m³)")
entry_age = create_input("Age (days)")

# Predict button
predict_btn = tk.Button(root, text="Predict Strength", command=predict, bg="blue", fg="white")
predict_btn.pack(pady=20)

# Result
result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, font=("Arial", 14))
result_label.pack()

root.mainloop()
