
const https = require("https")
var count=0;
const data = JSON.stringify({
  "test": "event",
  'count':count
})

const options = {
  hostname: "eoev19ctpl8p7i5.m.pipedream.net",
  port: 443,
  path: "/",
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Content-Length": data.length,
  },
}

var polling = true;
var stacode= null;
//count check to turn off polling
var intervel=setInterval(() => {
    
   
const req = https.request(options,(response)=>{
    response.setEncoding('utf8');
    stacode= response.statusCode
    
        response.on('data', function (chunk) {
            if (stacode==200){
                clearInterval(intervel);
            } 
          console.log("body: " + chunk);
        });
})

count++
req.write(data);
req.end();

  
    
    
}, 6000);
   

