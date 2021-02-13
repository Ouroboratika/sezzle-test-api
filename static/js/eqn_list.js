
$(document).ready(
    function(){
        //connect to the socket server.
        var socket = io.connect('http://' + document.domain + ':' + location.port + '/eqnio');

        //receive details from server
        socket.on('eqn_update',
            function(eqn_list) {
                console.log(eqn_list)
                $('#eqn_list').html(eqn_list);
            }
        );
    }
);
