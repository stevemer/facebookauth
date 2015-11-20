import requests
from requests_kerberos import HTTPKerberosAuth
#authenticate = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
authenticate = HTTPKerberosAuth()
r = requests.get("https://vienna.eecs.umich.edu/api/W/2014/scores", auth=authenticate)
print r.text

