import cv2
import requests
import time

# Konfigurace
rtsp_url = "rtsp://admin:Asdf1234@192.168.0.206:8554/Streaming/Channels/101"  # PASTE YOUR RTSP URL HERE: rtsp://username:password@ipadress:port/stream1 
printer_uuid = "8d247544-f901-43dc-a2e0-7b1a90309c17"  # PASTE YOUR UUID OF YOUR PRINTER HERE
camera_token = "oPWRByCjm2hTYezNIn0N"  # PASTE YOUR CAMERA TOKEN HERE
camera_fingerprint = "your_device_fingerprint"  # DO NOT EDIT!
api_url = f"https://connect.prusa3d.com/c/snapshot"  # DO NOT EDIT!

# Function to get picture from camera
def capture_snapshot(rtsp_url):
    # Open rtsp stream
    cap = cv2.VideoCapture(rtsp_url)
    
    if not cap.isOpened():
        print("Nelze otevřít RTSP stream.")
        return None
    
    # wait for first 
    ret, frame = cap.read()
    if not ret:
        print("Chyba při načítání snímku z kamery.")
        return None
    
    # Zavřeme kameru
    cap.release()
    
    # Uložíme snímek jako JPG do dočasného souboru
    snapshot_path = "snapshot.jpg"
    cv2.imwrite(snapshot_path, frame)
    
    return snapshot_path

# Funkce pro odeslání snímku na API
def upload_snapshot(snapshot_path):
    headers = {
        'Token': camera_token,  # Token pro autentifikaci kamery
        'Fingerprint': camera_fingerprint,  # Fingerprint kamery
    }
    
    # Otevření souboru s obrázkem
    with open(snapshot_path, 'rb') as image_file:
        snapshot_data = image_file.read()

    # Odeslání PUT požadavku
    response = requests.put(api_url, data=snapshot_data, headers=headers)
    
    # Ladící výstupy
    print("Stavová odpověď API:", response.status_code)
    print("Tělo odpovědi:", response.text)
    
    if response.status_code == 204:
        print("Snímek byl úspěšně nahrán.")
    else:
        print(f"Chyba při nahrávání snímku: {response.status_code} - {response.text}")

# Hlavní část skriptu
if __name__ == "__main__":
    # Pořídíme snímek z RTSP kamery
    snapshot_path = capture_snapshot(rtsp_url)
    
    if snapshot_path:
        # Nahrajeme snímek na API
        upload_snapshot(snapshot_path)
    else:
        print("Nepodařilo se pořídit snímek.")
