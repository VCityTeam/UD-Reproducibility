A demo of 3DTiles based buildings accross [Lyon's chemistry valley](https://fr.wikipedia.org/wiki/Vall%C3%A9e_de_la_chimie).

## 1. Compute correct data for your demo


## 2. Build ud-viz context

### 1. Configure your demo
- Go on the generaldemoConfig.json file in the ud-viz-contest folder
- Change value of your extend position to visualize the correct map of your data, here:
 ```
   "extents": {
    "vallee_chimie": {
      "min_x": "1832891.32",
      "max_x": "1846735.29",
      "min_y": "5150253.55",
      "max_y": "5174952.52"
    }
  ```

### 2. Build your demo
 - Run this command line to build your context
```
docker build -t vallee-chimie ud-viz-context
```

- Retrieve your Fully Qualified Domain Name (FQDN):
   1. First retrieve your deploying host IP address. If ifconfig is
    available for you (Ubun tu, OSX) try using `ifconfig | grep -i inet`
   2. Then out of this IP adress retrieve the FQDN of your host with
    the `host <host_IP_number>` command.

- Then run the container with
```
docker run -d -h <FQDN> -p 8282:80/tcp -t vallee-chimie
```
- and open a web browser on URL http://localhost:8282/

