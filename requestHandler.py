#!/usr/bin/python3

import requests
import kerberos


try:
	_, krb_context = kerberos.authGSSClientInit("host@server.example.tn")
	print("step : "+str(kerberos.authGSSClientStep(krb_context, "")))

	print("Creating auth header......")
	negotiate_details = kerberos.authGSSClientResponse(krb_context)
	headers = {"Authorization": "Negotiate "+ negotiate_details, 'Content-Type':'application/json'}

	r = requests.get("http://127.0.0.1:8080/predict", headers=headers)

	print("Status : "+str(r.status_code))
	print("Results : ")
	print(r)

except Exception as err:
	print(type(err))
	print(err)