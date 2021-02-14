
$(document).ready(
    function(){
        // Establish a connection to the socket
        var socket = io.connect('http://' + document.domain + ':' + location.port + '/eqnio');

        // Process an update to the list of equations. They are received pre-pretty-ified.
        socket.on('eqn_update',
            function(payload) {
                eqn_list = payload.eqn_list;
                var eqn_html = '';
                for (var i = 0; i < eqn_list.length; i++) {
                    eqn_html = eqn_html + '<p>' + eqn_list[i] + '</p>';
                }
                $('#eqn_list').html(eqn_html);
            }
        );
    }
);
