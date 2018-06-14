$(function(){
    $('#search').keyup(function(){
        $.ajax({
            type: 'POST',
            url: 'events/serach',
            data: {
                'search_events' : $('#search').val,
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: searchSuccess,
            datatype: 'html'
        })
    })
});

function searchSuccess(data, textStatus, jqXHR){
    $('#search_results').html(data);
}