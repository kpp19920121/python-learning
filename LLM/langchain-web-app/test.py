import requests



response=requests.get("http://192.168.233.133:8080/");



print(f"response{response}")
print(f"response.status_code:{response.status_code}")
#print(f"{response.text}")
print(f"response.encoding:{response.encoding}")
print(f"response.headers:{response.headers}")





