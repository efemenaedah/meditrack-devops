from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store (preloaded with 3 patients)
patients = [
    {
        "id": 1,
        "name": "John Doe",
        "age": 45,
        "gender": "Male",
        "diagnosis": "Hypertension",
        "ward": "Cardiology",
        "admitted_on": "2026-03-20"
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "age": 37,
        "gender": "Female",
        "diagnosis": "Diabetes",
        "ward": "Endocrinology",
        "admitted_on": "2026-03-22"
    },
    {
        "id": 3,
        "name": "Michael Brown",
        "age": 60,
        "gender": "Male",
        "diagnosis": "Asthma",
        "ward": "Respiratory",
        "admitted_on": "2026-03-25"
    }
]

# Next ID counter
next_id = 4


# ---------------------------
# Health Check
# ---------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "meditrack-api"
    }), 200


# ---------------------------
# Get all patients
# ---------------------------
@app.route("/patients", methods=["GET"])
def get_patients():
    return jsonify(patients), 200


# ---------------------------
# Create a new patient
# ---------------------------
@app.route("/patients", methods=["POST"])
def create_patient():
    global next_id

    data = request.get_json()

    required_fields = ["name", "age", "gender", "diagnosis", "ward", "admitted_on"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_patient = {
        "id": next_id,
        "name": data["name"],
        "age": data["age"],
        "gender": data["gender"],
        "diagnosis": data["diagnosis"],
        "ward": data["ward"],
        "admitted_on": data["admitted_on"]
    }

    patients.append(new_patient)
    next_id += 1

    return jsonify(new_patient), 201


# ---------------------------
# Get patient by ID
# ---------------------------
@app.route("/patients/<int:patient_id>", methods=["GET"])
def get_patient(patient_id):
    for patient in patients:
        if patient["id"] == patient_id:
            return jsonify(patient), 200

    return jsonify({"error": "Patient not found"}), 404


# ---------------------------
# Update patient
# ---------------------------
@app.route("/patients/<int:patient_id>", methods=["PUT"])
def update_patient(patient_id):
    data = request.get_json()

    for patient in patients:
        if patient["id"] == patient_id:
            patient.update(data)
            return jsonify(patient), 200

    return jsonify({"error": "Patient not found"}), 404


# ---------------------------
# Delete patient
# ---------------------------
@app.route("/patients/<int:patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    for patient in patients:
        if patient["id"] == patient_id:
            patients.remove(patient)
            return jsonify({"message": "Patient deleted successfully"}), 200

    return jsonify({"error": "Patient not found"}), 404


# Run the app locally (optional)
if __name__ == "__main__":
    app.run(debug=True)
