const bodyParser = require('body-parser');
const res = require('express/lib/response');
var lastJson = { "entity": "event", "account_id": "acc_CJoeHMNpi0nC7k", "event": "qr_code.credited", "contains": ["payment", "qr_code"], "payload": { "payment": { "entity": { "id": "pay_HO2fEpc9JeOQU5", "entity": "payment", "amount": 200, "currency": "INR", "status": "captured", "order_id": null, "invoice_id": null, "international": false, "method": "upi", "amount_refunded": 0, "refund_status": null, "captured": true, "description": "QRv2 Payment", "card_id": null, "bank": null, "wallet": null, "vpa": "gauri.kumar@okhdfcbank", "email": "gauri.kumari@example.com", "contact": "+919999999999", "customer_id": "cust_HKsR5se84c5LTO", "notes": { "Branch": "Bangalore - Rajaji Nagar" }, "fee": 0, "tax": 0, "error_code": null, "error_description": null, "error_source": null, "error_step": null, "error_reason": null, "acquirer_data": { "rrn": "116812981837" }, "created_at": 1623914419 } }, "qr_code": { "entity": { "id": "qr_HO2e0813YlchUn", "entity": "qr_code", "created_at": 1623914349, "name": "Acme Groceries", "usage": "multiple_use", "type": "upi_qr", "image_url": "https://rzp.io/i/X6QM7LL", "payment_amount": null, "status": "active", "description": "Buy fresh groceries", "fixed_amount": false, "payments_amount_received": 0, "payments_count_received": 0, "notes": { "Branch": "Bangalore - Rajaji Nagar" }, "customer_id": "cust_HKsR5se84c5LTO", "close_by": 1625077799, "closed_at": null, "close_reason": null } } }, "created_at": 1623914419 }
var jsonfile= null
var lastreq= null
var currentreq = null

module.exports = {
    postHandler: function (app) {
        // handle webhook json and 

        app.post('/', bodyParser, (req, res) => {
            res.setHeader('Content-Type', 'application/json')
            
            if ((lastJson.payload.payment.entity.amount != jsonfile.payload.payment.entity.amount)&(lastJson.payload.payment.created_at != jsonfile.payload.payment.created_at) ) {
                    
                lastJson = jsonfile
                res.send(200);
            }else
            {
                res.send(404);
            }
            res.render()
        })
          
            app.post('/webhook', bodyParser, (req2, res2) => {


                jsonfile = req2.body;
                console.log(lastJson.payload.amount)
                res.send(200)

               
            })
       


    },
    JsonFile: function () { return (lastJson) }
}
