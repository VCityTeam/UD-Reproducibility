/** @format */
const express = require('express');

export class SimpleServer {
  constructor() {}

  start(config) {
    const app = express();
    const cors = require('cors');

    //app.use(cors());
    //Cors
    /*app.use(function(req, res, next) {
      res.header("Access-Control-Allow-Origin", "*");
      res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization, Client-Security-Token, Accept-Encoding");
      res.header("Access-Control-Allow-Headers", "POST, GET, OPTIONS, DELETE, PUT");
      next();
    });*/
    app.use(express.static(config.folder, {
      setHeaders: function setHeaders(res, path, stat) {
        res.header('Access-Control-Allow-Origin', '*');
        res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
        res.header('Access-Control-Allow-Headers', 'Content-Type');
      }
    }))

    /*app.configure(function() {
      app.use(express.bodyParser());
      app.use(express.cookieParser());
      app.use(express.session({ secret: 'cool beans' }));
      app.use(express.methodOverride());
      app.use(allowCrossDomain);
      app.use(app.router);
      app.use(express.static(__dirname + '/public'));
  });*/

    //serve
    //app.use(express.static(config.folder)); //what folder is served

    //http server
    app.listen(config.port, function (err) {
      if (err) console.log('Error in server setup');
      console.log('Server listening on Port', config.port, ' folder ' + config.folder);
    });
  }
}
