import requests

headers = '''
Request URL:
https://www.spesaonline.unes.it/onboarding/services?cap=20121&latitude=45.4720482&longitude=9.1920381&city=Milan
Request Method:
GET
Status Code:
200 OK
Remote Address:
20.67.109.193:443
Referrer Policy:
strict-origin-when-cross-origin
cache-control:
no-cache, no-store, max-age=0, must-revalidate
connection:
Keep-Alive
content-encoding:
gzip
content-security-policy:
frame-ancestors
content-type:
application/json;charset=UTF-8
date:
Tue, 03 Dec 2024 11:31:04 GMT
expires:
0
keep-alive:
timeout=5, max=100
pragma:
no-cache
server:
*
set-cookie:
anonymous-consents=%5B%5D; Max-Age=31536000; Expires=Wed, 03 Dec 2025 11:31:04 GMT; Path=/; Secure; HttpOnly
strict-transport-security:
max-age=31536000 ; includeSubDomains
transfer-encoding:
chunked
vary:
Accept-Encoding,User-Agent
x-content-type-options:
nosniff
x-frame-options:
SAMEORIGIN
x-sap-pad:
89613
x-xss-protection:
1; mode=block
accept:
*/*
accept-encoding:
gzip, deflate, br, zstd
accept-language:
en-US,en;q=0.9,my-ZG;q=0.8,my;q=0.7,ar-EG;q=0.6,ar;q=0.5,en-GB;q=0.4
connection:
keep-alive
content-type:
application/json
cookie:
_gcl_au=1.1.613904187.1733222479; _ga_MJ4D3HWMTL=GS1.1.1733222480.1.0.1733222480.60.0.876357978; _ga=GA1.1.1689684607.1733222480; anonymous-consents=%5B%5D; cookie-notification=NOT_ACCEPTED; JSESSIONID=Y9-3aad4925-555d-4416-9b0c-0fddf3eef44c.accstorefront-7cc9965994-l9xm4; ROUTE=.accstorefront-7cc9965994-l9xm4; CookieConsent={stamp:%272J6bfQGCB9XjfV1HIzA/XNpzl9BFaeJRUMjZEZ//mGirfWe9PyMXqA==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cmethod:%27explicit%27%2Cver:1%2Cutc:1733222946759%2Cregion:%27ng%27}; _ga_55CY4YM2Q2=GS1.1.1733225463.2.0.1733225463.60.0.0
csrftoken:
e3775920-5801-4ab2-8d27-75e77d3fd836
host:
www.spesaonline.unes.it
referer:
https://www.spesaonline.unes.it/
sec-ch-ua:
"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"
sec-ch-ua-mobile:
?0
sec-ch-ua-platform:
"macOS"
sec-fetch-dest:
empty
sec-fetch-mode:
cors
sec-fetch-site:
same-origin
user-agent:
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36

'''

# Endpoint for scraping stores
# response = requests.get('https://www.spesaonline.unes.it/onboarding/services?cap=20121&latitude=45.4720482&longitude=9.1920381&city=Milan')
# with open('response.json', 'w') as file:
#     file.write(response.text)

# Possible endpoint API for scraping products
response = requests.get('https://www.spesaonline.unes.it/search?query=&production_0064-index%5Bpage%5D=1')
with open('products.json', 'w') as file:
    file.write(response.text)