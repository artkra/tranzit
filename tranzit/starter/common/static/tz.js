function TZ(url, callbacks) {
    this.ws = new WebSocket(url);
    this.callbacks = callbacks;
    this.ws.onmessage = function(e) {
        console.log(e);
        this.parse(e.data);
    };
    this.parse = function(data) {
        var parsed = [],
            method = '',
            args = [];

        try {
            parsed = data.split('|');
            method = parsed[0];
            args = parsed[1].split(',');


        } catch(e) {
            console.error(e);
        }
    };
    this.send = function(method, args) {
        var msg = method + '|' + args.join(',');

        this.ws.send(msg);
    };
};

window.onload = function() {
    console.info('WINDOW LOADED');
}