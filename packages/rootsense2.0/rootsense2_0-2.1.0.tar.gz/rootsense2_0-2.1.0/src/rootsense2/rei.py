import pymongo
import logging
import os
from datetime import datetime

# MongoDB Setup
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["rootsense"]

# Correct collection names based on your description
tickets_collection = db["tickets"]
root_cause_collection = db["rootsense"]
predictive_analysis_collection = db["predictions"]
rei_collection = db["rei"]  # The collection to store REI data

# Log File Setup
log_file_path = "../logs/system_logs.log"

# Check if log file exists; if not, create it and log a message
if not os.path.exists(log_file_path):
    with open(log_file_path, "w") as f:
        pass  # Create the file
    print(f"Log file '{log_file_path}' created.")

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def fetch_tickets():
    """
    Fetch all ticket data from the 'tickets' collection.
    """
    try:
        tickets = tickets_collection.find()  # Fetch all tickets
        return list(tickets)  # Return as a list
    except Exception as e:
        logging.error(f"Error fetching tickets data: {e}")
        return []

def fetch_root_cause_analysis():
    """
    Fetch all root cause analysis data from the 'root_cause_analysis' collection.
    """
    try:
        rca_data = root_cause_collection.find()  # Fetch all RCA data
        return list(rca_data)  # Return as a list
    except Exception as e:
        logging.error(f"Error fetching root cause analysis data: {e}")
        return []

def fetch_predictive_analysis():
    """
    Fetch all predictive analysis data from the 'predictive_analysis' collection.
    """
    try:
        predictive_data = predictive_analysis_collection.find()  # Fetch all predictive data
        return list(predictive_data)  # Return as a list
    except Exception as e:
        logging.error(f"Error fetching predictive analysis data: {e}")
        return []

def calculate_rei(actual_usage, predicted_usage):
    """
    Calculate the Resource Efficiency Index (REI) for a given metric.
    """
    try:
        if predicted_usage > 0:
            rei = (actual_usage / predicted_usage) * 100
            return round(rei, 2)
        else:
            return None  # Avoid division by zero if predicted usage is 0
    except Exception as e:
        logging.error(f"Error calculating REI: {e}")
        return None

def get_rei_insights(rei):
    """
    Generate collective insights based on overall REI value.
    """
    if rei > 100:
        return "The system is highly efficient. Resources are under-utilized."
    elif 80 <= rei <= 100:
        return "The system is operating efficiently. Resources are being used optimally."
    elif 50 <= rei < 80:
        return "The system is somewhat inefficient. There is room for improvement in resource utilization."
    else:
        return "The system is inefficient. Consider optimizing resource usage and processes."

def save_rei_to_db(collective_rei, insights):
    """
    Save the calculated collective REI and insights to the 'rei' collection in MongoDB.
    """
    try:
        rei_data = {
            "timestamp": datetime.utcnow(),
            "collective_rei": collective_rei,
            "insights": insights
        }
        rei_collection.insert_one(rei_data)
        logging.info("Successfully saved the collective REI and insights to the database.")
    except Exception as e:
        logging.error(f"Error saving REI data to the database: {e}")

def display_collective_outcome():
    """
    Display the collective REI and insights for CPU, Memory, and Disk resources.
    """
    tickets = fetch_tickets()
    rca_data = fetch_root_cause_analysis()
    predictive_data = fetch_predictive_analysis()

    # Initialize variables for calculating the overall REI
    total_rei = 0
    count = 0

    # Process each metric and calculate the REI
    for ticket in tickets:
        metric = ticket.get('metric')
        if metric not in ["CPU", "Memory", "Disk"]:
            continue  # Skip irrelevant metrics

        # Get actual usage from the ticket
        actual_usage = ticket.get('value')
        
        # Get predicted usage from RCA or predictive analysis
        predicted_usage = None
        for rca in rca_data:
            if metric == "CPU":
                predicted_usage = rca.get('cpu_usage_predictions')
            elif metric == "Memory":
                predicted_usage = rca.get('memory_percent_predictions')
            elif metric == "Disk":
                predicted_usage = rca.get('disk_percent_predictions')

        # If no prediction is found in RCA data, try predictive analysis data
        if predicted_usage is None and predictive_data:
            for prediction in predictive_data:
                if prediction.get('metric') == metric:
                    predicted_usage = prediction.get('predictions')  # Assuming predictions is a dictionary
                    if isinstance(predicted_usage, dict):
                        # Take the average of all predicted values for simplicity
                        predicted_usage = sum(predicted_usage.values()) / len(predicted_usage)

        if predicted_usage is not None:
            rei = calculate_rei(actual_usage, predicted_usage)
            if rei is not None:
                total_rei += rei
                count += 1
                print(f"{metric} Resource Efficiency Index (REI): {rei}%")
            else:
                print(f"Error calculating REI for {metric}.")
        else:
            print(f"No prediction data found for {metric}.")

    # Calculate overall REI
    if count > 0:
        collective_rei = total_rei / count
        print(f"\nOverall Resource Efficiency Index (REI): {collective_rei}%")
        insights = get_rei_insights(collective_rei)
        print(insights)
        
        # Save the result to MongoDB
        save_rei_to_db(collective_rei, insights)
    else:
        print("No valid metrics found to calculate the collective REI.")

if __name__ == "__main__":
    """
    Main function to execute the collective REI calculation and insights generation.
    """
    print("Starting the Collective Resource Efficiency Index (REI) Calculation:")
    logging.info("Collective REI Calculation initiated.")
    
    try:
        display_collective_outcome()
        logging.info("Collective REI Calculation completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during the Collective REI Calculation: {e}")
        print(f"An error occurred: {e}")
