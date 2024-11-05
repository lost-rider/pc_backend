import requests

url = "https://api.mouser.com/api/v1/search/keyword"
headers = {
    "Content-Type": "application/json",
    "apiKey": "f5058d4b-a63d-4314-ac9f-09e0418624fc"  ,
    "version":"1"
}

payload = {
    "SearchByKeywordRequest": {
        "keyword": "string",
        "records": 50,
        "startingRecord": 0,
        "searchOptions": "",
        "searchWithYourSignUpLanguage": "en"
    }
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    parts = data.get("SearchResults", {}).get("Parts", [])
    for part in parts:
        print(f"Manufacturer: {part['Manufacturer']}")
        print(f"Part Number: {part['ManufacturerPartNumber']}")
        print(f"Description: {part['Description']}")
        print(f"Availability: {part['Availability']}")
        print(f"DataSheetUrl: {part['DataSheetUrl']}")
        print("-" * 20)
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

