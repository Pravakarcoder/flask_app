 
# from flask import Flask, render_template, jsonify
# import subprocess
# import json

# app = Flask(__name__)

# def get_wifi_passwords():
#     # Run the command to get a list of saved Wi-Fi profiles
#     result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True)
#     profiles = result.stdout

#     # Find all profile names
#     profile_names = [line.split(":")[1].strip() for line in profiles.split('\n') if "All User Profile" in line]

#     wifi_details = []

#     for profile in profile_names:
#         # Run command to get the password for each profile
#         profile_info = subprocess.run(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'], capture_output=True, text=True)
#         profile_info_output = profile_info.stdout

#         # Extract the password from the output
#         password_line = [line.split(":")[1].strip() for line in profile_info_output.split('\n') if "Key Content" in line]
#         password = password_line[0] if password_line else None

#         wifi_details.append({
#             'SSID': profile,
#             'Password': password
#         })

#     return wifi_details

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get_wifi_details', methods=['GET'])
# def get_wifi_details():
#     # Fetch Wi-Fi details and log them (or print them)
#     wifi_details = get_wifi_passwords()
    
#     # Log the details in JSON format
#     wifi_details_json = json.dumps(wifi_details, indent=4)
#     print("Wi-Fi Details (Server-Side):")
#     print(wifi_details_json)
    
#     # Return a message indicating that the details were logged
#     return jsonify({"message": "Wi-Fi details have been retrieved and logged on the server."})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, jsonify
import subprocess
import json

app = Flask(__name__)

def get_wifi_passwords():
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

@app.route('/')
def index():
    # Fetch Wi-Fi details
    wifi_details = get_wifi_passwords()
    
    # Print Wi-Fi details on the server side
    print("Wi-Fi Details (Server-Side):")
    print(json.dumps(wifi_details, indent=4))
    
    # Return a generic message to the client, not the actual details
    return jsonify({"message": "Wi-Fi details have been retrieved and logged on the server."})

if __name__ == '__main__':
    app.run(debug=True)
