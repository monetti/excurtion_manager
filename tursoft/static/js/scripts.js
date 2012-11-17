function pjax(){
    event.preventDefault();
    container = $(this).attr('rel'),
    target = $(this).attr('href');
    $.get(
        target,
        function(data){
            $(container).empty();
            $(container).append(data);
        }
    
    );
}

$(function(){
    $('body').on('click', '.control',function(){
        target = $(this).attr('href');
        $(this).toggleClass('active');
        $(target).toggle('fade', 300);
        return false;
        
    });
    $('form input[type="text"]:first').focus()
 
    $('body').on('click.pjax', '.pjax', pjax)
    
    

});
