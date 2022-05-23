var Keypad = require("rpi-keypad");
 
var input = Keypad(
    [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
        ["*", "0", "#"],
    ],                // keypad layout
    [40, 38, 36, 32], // row GPIO pins
    [37, 35, 33]  // colum GPIO pins
);
    
setInterval(() => {
    var key = keypad.getKey();
    if (key != null){
        console.log("key pressed: " + key);
    } else {
        console.log("no key pressed");
    }
}, 100);
