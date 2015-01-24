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

var API_ID     = config.API_ID,
    API_SECRET = config.API_SECRET,
    BOARD_ID   = 'J5ZXPIWO7S';

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
  client.subscribe(API_ID+'/'+BOARD_ID+'/SENSE/1');

  // Attach a function when a new message is received.
  client.on('message', function(topic, message) {
    console.log(message.toString());
    if (message.dig == 1){ 
      pingServer();
    }
  });

});
