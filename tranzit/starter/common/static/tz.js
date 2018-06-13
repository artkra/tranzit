function TZ(url, callbacks) {
// Basic example.
// <callbacks> is an object with your callbacks for WS views. Example below.
//
// You can use this template for handling websocket messaging
// if you follow this template
// for your response:
//     '<function_name>|arg1, arg2, arg3'
    var me = this;

    this.ws = new WebSocket(url);
    this.callbacks = callbacks;
    this.ws.onmessage = function(e) {
        console.log('[Incoming message from ' + e.origin + ']: ' + e.data);
        me.parse(e.data);
    };
    this.parse = function(msg) {
        var parsed = [],
            method = '',
            args = [];

        try {
            parsed = msg.split('|');
            method = parsed[0];
            args = parsed[1].split(',');

            me.callbacks[method].apply(this, args);

        } catch(e) {
            console.error('Callback error for message: ' + msg);
        }
    };
    this.send = function(method, args) {
        var msg = method + '|' + args.join(',');

        this.ws.send(msg);
    };

};

window.onload = function() {
    window.mainTZ = new TZ(
        'ws://0.0.0.0:19719',
        {
            get_hello: function(data) {console.log(data);}
        }
    );

    window.reconnect = function() {
        setTimeout(function() {
            if (window.mainTZ.ws.readyState != 1) {
                console.error('LOST WS CONNECTION. RECONNECTING ...');
                window.mainTZ = new TZ(
                    'ws://0.0.0.0:19719',
                    {
                        get_hello: function(data) {console.log(data);}
                    }
                );
            }
            window.reconnect();
        }, 15000);
    };

    window.reconnect();
}