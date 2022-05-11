# Kerberos

## What is Kerberos 
Kerberos is a computer-network authentication protocol that works on the basis of tickets to allow nodes communicating over a non-secure network to prove their identity to one another in a secure manner. Its designers aimed it primarily at a client–server model, and it provides mutual authentication—both the user and the server verify each other's identity. Kerberos protocol messages are protected against eavesdropping and replay attacks.

-- Wikipedia

## Architecture

<img src="https://github.com/rihemebh/Kerberos-project/blob/main/architecture.png" />


## What we will do ? 

You will find in this repo a flask endpoint that needs kerberos authentication 
In order to test it you need to configure 3 machines : KDC, Client and Server then generate token from the ticket produced by the KDC and everything will work properly 

### Prerequisite

- Docker 
- Ubuntu image 
- Python3 
- Flask and Flask-Kerberos

We need to configure 3 different machines : 
  - KDC
  - Server 
  - Client 
  
  --Note: in the rest of this document I will only use 2 machines one for the KDC and the other will work as server and client
1. Pull docker image  : ``docker pull ubuntu``
2. Create network bridge to create a private netwok between containers so they can communicate with each others  : ``docker network create --driver=bridge <network name>``
3. Create 3 containers from that image

Since the image doesn’t have any preinstalled dependencies you should first run : 

```cmd
apt update && apt upgrade 
```

then install whatever you need (for our case we will need: nano,  host, ntp, ntpdate, python3 python3-pip )

### Machines' Setup:

We will use ``insat.tn`` as domain name 
#### 1. In each machine match different ips to their sub domain name in ``/etc/hosts`` 
```cmd 
172.21.0.2      kdc.insat.tn kdc
172.21.0.3      server.insat.tn server
``` 

To test if everything is working properly try this command on each sub-domain: 
```
host kdc.insat.tn
```
#### 2. Synchronize date between machines with ntp and ntpdate :

##### Why ?

Kerberos is time sensitive. It uses timestamps mechanism to check the validity of a ticket.Thus, we will create our own time server and synchronize all the machines.

- On the Kdc machine edit the ``/etc/ntp.conf`` and add the lines below:
```cmd
restrict 127.0.0.1
restrict ::1
restrict 192.168.56.110 mask 255.255.255.0
nomodify notrap
server 127.127.1.0 stratum 10
listen on *
```

- On the server install ntp and ntpdate:
```cmd
apt install ntp
apt install ntpdate
```
- then edit the ``/etc/ntp.conf`` and add the lines below:
```cmd
pool ntp.ubuntu.com
server 192.168.56.110
server obelix
````
- Synchronize time by running the below command on the server machine:
```cmd
ntpdate -dv 192.168.56.110
```


#### 3. Configure KDC 
```
apt install krb5-kdc krb5-admin-server krb5-config 
```
When it's prompted : 
  - realm : INSAT.TN
  - kerberos server : kdc.insat.tn
  - Administrative Service:	kdc.insat.tn
- create the realm: A Kerberos realm is the domain over which a Kerberos authentication server has the authority to authenticate a user, host or service.
```
krb5_newrealm
```

- Create principals and generate keytab:
  - A Kerberos Principal represents a unique identity in a Kerberos system to which Kerberos can assign tickets to access Kerberos-aware services.
  - The Kerberos Keytab file contains mappings between Kerberos Principal names and DES-encrypted keys that are derived from the password used to log into the Kerberos Key Distribution Center (KDC).
```
kadmin.local                              
addprinc root/admin                       
addprinc -randkey host/kdc.example.tn     
ktadd host/kdc.example.tn                 
```

#### 4. Configure Server

```
apt install krb5-user libpam-krb5 libpam-ccreds
```

Then do the same thing for realm, kerberos service, administrative service 

- Add host : 
```
kadmin                                      
addprinc -randkey host/server.insat.tn     
ktadd host/server.insat.tn  
```
- Install Flask and Flask-Kerberos with pip 


 ### Now your machines are ready to use with the flask service 
 
#### What is next ?
 Since Kerberos is based on ticket granting and not passwords so we need first to grant a ticket for the user to access the service 
 
 We have 2 types of tickets : 
 TGT: ticket granting ticket, the ticket that will allow you to get tickets for services 
 TGS: ticket granting service, allow you to access a service secured by kerberos
 
- About Flask Kerberos: check this link (https://flask-kerberos.readthedocs.io/en/latest/)
 
 In order to test the endpoint you need to follow these steps: 
 
 - Generate a ticket : ``kinit``
 - List of ticket with some other details about it like expiration date : ``klist``  
 
 - Now, all you have to do is executing the requestHandler.py file, its role is to generate a negotiate token and add the header to the url
### References : 

- [https://ubuntu.com/server/docs/service-kerberos](https://ubuntu.com/server/docs/service-kerberos)
- [https://web.mit.edu/kerberos/krb5-1.12/doc/admin/admin_commands/kadmin_local.html](https://web.mit.edu/kerberos/krb51.12/doc/admin/admin_commands/kadmin_local.html)
- https://github.com/hamza-mahjoub/flask-kerberos-module
