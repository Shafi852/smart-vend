const express = require('express');
const app = express();
const server = require('./Controller/WebServController')



app.set('view engine' , 'ejs');

server.postHandler(app);

app.listen(3000);
