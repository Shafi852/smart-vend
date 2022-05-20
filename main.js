const express = require('express');
const app = express();
const server = require('./Controller/WebServController')
const razorpay = require("razorpay");

const rzp= new razorpay({ key_id: 'rzp_test_1EfZWGKCb7w8pk', key_secret: 'o2gOV4kTWgcVeQlgkePv7BkZ' });
app.set('view engine' , 'ejs');
rzp.qrCode.fetchAllPayments('qr_JLeX7r9wc43R5N').then(data=>console.log(data))
server.postHandler(app);

app.listen(3000);
