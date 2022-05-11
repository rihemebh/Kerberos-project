

import requests
import kerberos


try:
	_, krb_context = kerberos.authGSSClientInit("host@server.insat.tn")
	negotiate_details = kerberos.authGSSClientResponse(krb_context)
	headers = {"Authorization": "Negotiate "+ negotiate_details, 'Content-Type':'application/json'}
	r = requests.get("http://127.0.0.1:8080/predict", headers=headers)

	print("Status : "+str(r.status_code))
	print("Results : ")
	print(r.text)

except Exception as err:
	print(type(err))
	print(err)