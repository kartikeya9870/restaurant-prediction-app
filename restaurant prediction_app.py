import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor
from tkinter import *
import time

df = pd.read_csv('restaurant_data.xlsx.csv')


columns_to_drop = [
    'Restaurant ID', 'Restaurant Name', 'Address', 'Country Code',
    'Latitude', 'Longitude', 'Currency', 'Is delivering now',
    'Switch to order menu', 'Rating color', 'Rating text', 'Locality', 'Locality Verbose', 'Price range'
]
df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])


label_encoders = {}
for col in df.select_dtypes(include='object').columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

X = df.drop('Aggregate rating', axis=1)
y = df['Aggregate rating']

model = DecisionTreeRegressor()
model.fit(X, y)

app = Tk()
app.title("🍽️ Restaurant Rating Predictor")
app.geometry("480x540")
app.configure(bg="#ffffff")
app.resizable(False, False)
app.attributes('-alpha', 0.0)

def fade_in(alpha=0.0):
    if alpha < 1.0:
        alpha += 0.05
        app.attributes('-alpha', alpha)
        app.after(30, fade_in, alpha)

fade_in()

bg_color = "#ffffff"
fg_color = "#222222"
accent_color = "#4CAF50"
hover_color = "#388E3C"
entry_bg = "#f5f5f5"

Label(app, text="Restaurant Rating Predictor", bg=bg_color, fg=fg_color,
      font=("Segoe UI", 20, "bold")).pack(pady=20)

form_frame = Frame(app, bg=bg_color)
form_frame.pack(pady=10)

fields = {}

def add_field(label_text, row, is_dropdown=False, options=None):
    Label(form_frame, text=label_text, bg=bg_color, fg=fg_color,
          font=("Segoe UI", 11)).grid(row=row, column=0, padx=10, pady=8, sticky='w')
    if is_dropdown:
        var = StringVar()
        var.set(options[0])
        dropdown = OptionMenu(form_frame, var, *options)
        dropdown.config(bg=entry_bg, font=("Segoe UI", 10), width=22)
        dropdown.grid(row=row, column=1, padx=10)
        fields[label_text] = var
    else:
        entry = Entry(form_frame, bg=entry_bg, font=("Segoe UI", 10), width=25)
        entry.grid(row=row, column=1, padx=10)
        fields[label_text] = entry

add_field("City", 0, True, list(label_encoders['City'].classes_))
add_field("Cuisines", 1, True, list(label_encoders['Cuisines'].classes_))
add_field("Average Cost for two", 2)
add_field("Has Online delivery", 3, True, list(label_encoders['Has Online delivery'].classes_))
add_field("Has Table booking", 4, True, list(label_encoders['Has Table booking'].classes_))
add_field("Votes", 5)

result_var = StringVar()
result_label = Label(app, textvariable=result_var, font=("Segoe UI", 12, "bold"),
                     fg="#333", bg=bg_color)
result_label.pack(pady=15)

def predict():
    try:
        result_var.set("⏳ Predicting...")
        app.update()
        time.sleep(1)

        input_data = {
            'City': label_encoders['City'].transform([fields['City'].get()])[0],
            'Cuisines': label_encoders['Cuisines'].transform([fields['Cuisines'].get()])[0],
            'Average Cost for two': float(fields['Average Cost for two'].get()),
            'Has Online delivery': label_encoders['Has Online delivery'].transform([fields['Has Online delivery'].get()])[0],
            'Has Table booking': label_encoders['Has Table booking'].transform([fields['Has Table booking'].get()])[0],
            'Votes': int(fields['Votes'].get())
        }

        input_df = pd.DataFrame([input_data])
        input_df = input_df[X.columns] 

        predicted_rating = model.predict(input_df)[0]
        result_var.set(f"⭐ Predicted Rating: {predicted_rating:.2f}")

    except Exception as e:
        result_var.set(f"⚠️ Error: {e}")

def on_enter(e):
    predict_btn.config(bg=hover_color)

def on_leave(e):
    predict_btn.config(bg=accent_color)

predict_btn = Button(app, text="🔍 Predict Rating", font=("Segoe UI", 11, "bold"),
                     bg=accent_color, fg="white", width=22, height=2, command=predict, relief=FLAT)
predict_btn.pack(pady=10)

predict_btn.bind("<Enter>", on_enter)
predict_btn.bind("<Leave>", on_leave)

Label(app, text="Made with 💚 in Python", bg=bg_color, fg="#777", font=("Segoe UI", 9)).pack(side="bottom", pady=10)

app.mainloop()
