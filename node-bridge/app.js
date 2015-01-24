var mqtt = require('mqtt');
var http = require('http');

var config = JSON.parse(require('fs').readFileSync(__dirname + '/../config/config.json'));

function pingServer(){ 
  http.get(config.server_url, function(res){ 
    console.log('got motion!');
  }).on('error', function(e){ 
    console.log(' ERR ! ' + e.message);
  });
}

var settings = {
  keepalive: 1000,
  protocolId: 'MQIsdp',
  protocolVersion: 3,
  clientId: 'MQTT_'+config.board_id, // should be unique (randomizes it)
  username: config.api_id,
  password: config.api_secret,
  rejectUnauthorized: false
}

// Start new MQTT client istance.
var client = mqtt.connect('mqtts://cloud.smartables.io:8883', settings);

// Catch errors.
client.on('error', function(err) {
  console.log('error!', err);
  });

// When connection established
client.on('connect', function() { 
  console.log('connected to mqtt server');

  // Sample code for subscribe a specific topic.
  client.subscribe(config.api_id+'/'+config.board_id+'/SENSE/1');

  // Attach a function when a new message is received.
  client.on('message', function(topic, message) {
    var dig_in = JSON.parse(message).dig;
    if (dig_in == 1){ 
      console.log('pinging server');
      pingServer();
    }
  });

});
