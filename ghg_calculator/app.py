from flask import Flask, render_template, request

app = Flask(__name__)

# Emission Factors (kg CO2e per unit)
TRANSPORT_EMISSIONS = {
    "car_petrol": 0.251,  # kg CO2e per km
    "car_diesel": 0.269,
    "bus": 0.103,
    "train": 0.041,
    "bicycle": 0.0,
    "electric_car": 0.05
}

DIET_EMISSIONS = {
    "vegan": 1.5,  # Metric tons CO2e per year
    "vegetarian": 1.7,
    "pescatarian": 2.0,
    "omnivore": 3.3,
    "heavy_meat": 5.0
}

ELECTRICITY_FACTOR = 0.4  # kg CO2e per kWh


def calculate_emissions(vehicle, distance, electricity, diet):
    transport_emissions = TRANSPORT_EMISSIONS.get(vehicle, 0) * distance
    electricity_emissions = electricity * ELECTRICITY_FACTOR
    diet_emissions = DIET_EMISSIONS.get(diet, 0) * 1000  # Convert to kg CO2e per year
    total_emissions = transport_emissions + electricity_emissions + diet_emissions
    return transport_emissions, electricity_emissions, diet_emissions, total_emissions


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        vehicle = request.form["vehicle"]
        distance = float(request.form["distance"])
        electricity = float(request.form["electricity"])
        diet = request.form["diet"]

        transport, electricity, diet, total = calculate_emissions(vehicle, distance, electricity, diet)
        return render_template("result.html", transport=transport, electricity=electricity, diet=diet, total=total)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
