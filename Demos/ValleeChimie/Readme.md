A kludgy and temporary attempt at packaging the IFC demo.

Try running with
```
docker build -t vallee-chimie ud-viz-context
```

Retrieve your Fully Qualified Domain Name (FQDN). For example
 * on OSX using dhcp (and with a misconfigured/hardwired
   hostname) one can first use `ifconfig | grep -i inet` to
   retrieve the host IP number and then `host <host_IP_number>`
   to retrieve the FQDN.

Then run the container with
```
docker run -d -h <FQDN> -p 8080:80/tcp -t vallee-chimie
```
and open a web browser on URL http://localhost:8080/

