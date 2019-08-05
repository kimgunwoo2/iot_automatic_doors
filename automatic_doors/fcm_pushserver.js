var admin = require("firebase-admin");
var serviceAccount = require("/home/pi/Downloads/serviceAccountKey.json");
 
admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://pushpush-bc109.firebaseio.com"
});
 
var registrationToken = "fMp-wHR-PeQ:APA91bFgW2iYxBYLEQw1IEi-hKO8MhaapPFzPie9LHbgu_S7wR4ojEalUxs-bPBW4mb8J49IH5Rfv1n3SSZoGMxMTylXM2PUo2zoxRiawBWRJw4OKtvncDVitUvgGkt5vrc7Dj35jgun";
 
var state = 'none';
var hum = 'none';
cnt = 0;
process.argv.forEach(function (val, index, array) {
	if (index == 2) {
		if(val == 'h') cnt = 1;
		if(val == 'c') cnt = 2;
		if(val == 'r') cnt = 3;
	}
 
});
 
if(cnt == 1){
	var payload = {
	    notification: {
	        title: "Hum Alarm",
	        body: "The laundry is dry"
	    }
	};
}
if(cnt == 2){
	var payload = {
	    notification: {
	        title: "laundry Alarm",
	        body: "It's nice weather to do the laundry"
	    }
	};
}
if(cnt == 3){
	var payload = {
	    notification: {
	        title: "Weather Alarm",
	        body: "Rain"
	    }
	};
}
 
admin.messaging().sendToDevice(registrationToken, payload)
    .then(function(response) {
        console.log("Successfully sent message:", response);
	process.exit();
    })
    .catch(function(error) {
        console.log("Error sending message:", error);
	process.exit();
    });