import os
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Flash messages ke liye zaroori hai

# Sample rate estimation function (Aap ke pehle wale logic ke mutabiq)
def calculate_rate(weight, volume, origin, destination):
    base_rate = 100
    weight_cost = float(weight) * 2.5
    volume_cost = float(volume) * 1.5
    
    # Distance/Location multiplier
    if origin.lower() != destination.lower():
        location_multiplier = 1.2
    else:
        location_multiplier = 1.0
        
    total = (base_rate + weight_cost + volume_cost) * location_multiplier
    return round(total, 2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quote', methods=['POST'])
def quote():
    if request.method == 'POST':
        try:
            weight = request.form.get('weight', 0)
            volume = request.form.get('volume', 0)
            origin = request.form.get('origin', '')
            destination = request.form.get('destination', '')
            
            estimated_cost = calculate_rate(weight, volume, origin, destination)
            flash(f"Estimated Freight Cost: ${estimated_cost}", "success")
        except Exception as e:
            flash("Invalid input. Please check your numbers.", "danger")
            
        return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
