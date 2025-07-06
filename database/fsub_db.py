import json
import os

FILENAME = "fsub_data.json"

def load_fsub_data():
    if not os.path.exists(FILENAME):
        return {"channels": [], "mode": "on"}
    with open(FILENAME, "r") as f:
        return json.load(f)

def save_fsub_data(data):
    with open(FILENAME, "w") as f:
        json.dump(data, f, indent=2)

def add_fsub_channel(channel_id):
    data = load_fsub_data()
    if channel_id not in data["channels"]:
        data["channels"].append(channel_id)
        save_fsub_data(data)
        return True
    return False

def remove_fsub_channel(channel_id):
    data = load_fsub_data()
    if channel_id in data["channels"]:
        data["channels"].remove(channel_id)
        save_fsub_data(data)
        return True
    return False

def get_fsub_channels():
    return load_fsub_data().get("channels", [])

def toggle_fsub_mode():
    data = load_fsub_data()
    current = data.get("mode", "on")
    data["mode"] = "off" if current == "on" else "on"
    save_fsub_data(data)
    return data["mode"]

def get_fsub_mode():
    return load_fsub_data().get("mode", "on")
