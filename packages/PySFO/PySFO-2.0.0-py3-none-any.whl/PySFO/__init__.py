import requests

class SFO:
    def Get(self, path):
        return requests.get(f"https://sfoapi.vercel.app/{path}").json()
    
    def GetSFO(self, sfo):
        return requests.get(f"https://sfoapi.vercel.app/objects/{sfo}").json()