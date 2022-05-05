const express = require('express');
const app = express();
const server = require('./Controller/WebServController')

app.set('veiw engine ' , 'ejs');

server(app);

app.listen(3000);
