
$(document).ready(
    function(){
        //connect to the socket server.
        var socket = io.connect('http://' + document.domain + ':' + location.port + '/eqnio');

        //receive details from server
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
