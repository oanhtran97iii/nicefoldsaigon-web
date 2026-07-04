import urllib.request
import urllib.parse

url = "https://docs.google.com/forms/d/e/1FAIpQLSfMTQAoppyHdDGNcGGiDWDI3Gonl6t1WkcbdlMQseX7ORg31g/formResponse"

payload = {
    "entry.978937613": "Antigravity Test Customer",
    "entry.1507224408": "+84999999999",
    "entry.564072479": "antigravity.test@gmail.com",
    "entry.1411190461": "Same-day Wash & Fold (8h-12h) — 250,000 VND (Includes 4kg & 2-way Delivery, extra: 50,000 VND/kg)",
    "entry.1151563479": "Pickup at my hotel / location"
}

data = urllib.parse.urlencode(payload).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        print("Status Code:", response.getcode())
        if response.getcode() == 200:
            print("Success! Custom form submission works with this URL.")
        else:
            print("Response:", response.read()[:200])
except Exception as e:
    print("Error:", e)
