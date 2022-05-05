var bodyParser = require('body-parser');
var lastJson = NaN

module.exports={ postHandler : function(app){
    // handle webhook json and display on website
    app.post('/', (req,res)=>{
        lastJson = req;
        
    })
},

lastJson : function(){
    lastJson;
}


}
lastJson.status