# Kerberos-project

## What is Kerberos 
Kerberos is a network authentication protocol. It is designed to provide strong authentication for client/server applications by using secret-key cryptography.

-- Reference (https://web.mit.edu/kerberos/)
## Kerberos Architecture 

<img src="https://github.com/rihemebh/Kerberos-project/blob/main/architecture.png" />
## What we will do ? 

You will find in this repo a flask end point that needs kerberos authentication 
in order to test it you need to configure 3 machines : KDC, Client, Server as it's mentioned in the architecture 
then generate token from the ticket produced by the KDC and everything will work properly 

### Prerequisite

- Docker 

- Ubuntu image 

- Python3 

- Flask and Flask-Kerberos

We need to configure 3 different machines : 
  - KDC
  - Server 
  - Client 
  
1. Pull docker image  : ``docker pull ubuntu``
2. Create network bridge between the containers to create a private netwok between so they can communicate with each others  
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
#### 2. Synchronize date between machines with ntp and ntpdate :

- on the Kdc machine edit the ``/etc/ntp.conf`` and add the lines below:
```cmd
restrict 127.0.0.1
restrict ::1
restrict 192.168.56.110 mask 255.255.255.0
nomodify notrap
server 127.127.1.0 stratum 10
listen on *
```

- on the server install ntp and ntpdate:
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

##### Why ?

Kerberos is time sensitive. It uses timestamps mechanism to check the validity of a ticket.Thus, we will create our own time server and synchronize all the machines.

#### 3. Configure KDC 
```
apt install krb5-kdc krb5-admin-server krb5-config 
```
When it's prompt : 
  - realm : INSAT.TN
  - kerberos server : kdc.insat.tn
  - Administrative Service:	kdc.insat.tn
```
krb5_newrealm
```

- Create principals and geneate keytab:
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

Then do the same thing when it is prompt

- Add host : 
```
kadmin                                      
addprinc -randkey host/server.insat.tn     
ktadd host/server.insat.tn  
```
- Install Flask and Flask-Kerberos with pip 


 ### Now your machines are ready to use with the flask service 

### References : 
- https://github.com/hamza-mahjoub/flask-kerberos-module
- [https://ubuntu.com/server/docs/service-kerberos](https://ubuntu.com/server/docs/service-kerberos)
- [https://web.mit.edu/kerberos/krb5-1.12/doc/admin/admin_commands/kadmin_local.html](https://web.mit.edu/kerberos/krb51.12/doc/admin/admin_commands/kadmin_local.html)
