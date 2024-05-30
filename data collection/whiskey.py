from bs4 import BeautifulSoup
import requests
from http.cookiejar import CookieJar
import pandas as pd

login = "https://www.whiskybase.com/account/login?p=%2F"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://www.whiskybase.com',  # Replace with the actual URL of the website
}
session = requests.Session()
login_page=session.get(login, headers=headers)
soup = BeautifulSoup(login_page.content, 'html.parser')
login_form = soup.find('form', {'method':'POST'})
csrf_token = login_form.find('input', {'name': '_token'}).get('value')  # Extract CSRF token

username_field = login_form.find('input', {'class':'form-control', 'name':'username'})
password_field = login_form.find('input', {'class':'form-control','name': 'password'})
print(username_field)
print(password_field)
login_data = {
    '_token': csrf_token,
    'username': 'hossman',
    'password': 'khalehZari2268'
}
login_action = "https://www.whiskybase.com/account/login"  # This is typically specified in the form's 'action' attribute
response = session.post(login_action, data=login_data, headers=headers)
print(response.cookies)
if response.status_code == 200:
    print('login success')
    # You are now logged in. You can access protected pages using the 'session' object.
else:
    print('Login failed.')
    print(response)


brands = session.get('https://www.whiskybase.com/whiskies/bottlers', headers=headers)

brands_html=BeautifulSoup(brands.content, 'html.parser')

f = open("demofile2.html", "a")
f.write(str(brands_html))
f.close()


data = []
for row in brands_html.find_all('tr'):
    cols = row.find_all(['td', 'th'])
    cols = [col.text.strip() for col in cols]
    data.append(cols)

# Create a DataFrame
columns = data[0]
df = pd.DataFrame(data, columns=columns)
df=df.drop(0).reset_index()
# Display the DataFrame
print(df)

df.to_csv('bottlers.csv',sep=',')

df.plot()