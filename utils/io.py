# save json output and print it
import json
def saveto_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    # Example usage
    data = {
        "asset": "Gold in Mumbai",
        "value": 5000,
        "note": "Current market value based on recent trends."
    }
    filename = 'asset_value.json'
    saveto_json(data, filename)
    print(f"Data saved to {filename}")