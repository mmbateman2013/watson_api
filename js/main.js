$(document).ready(function(){
    $('#submit').click(function(){
        show_vars();
    });
});

function show_vars(){
    var query = $('#query-text').val();
    var collection = $('#collection-text').val();
    $('#collection-ans').text(collection);
    $('#query-ans').text(query);
}
