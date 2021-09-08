var startColumn = '';

var dragstartHandler = function(event, data){
    event.dataTransfer.setData("text/plain", JSON.stringify(data));
    event.dataTransfer.effectAllowed = "move";
    startColumn = data.Status;
};

var dragoverHandler = function(event){
    event.preventDefault();
    var columnEls = event.target.getElementsByClassName('column');
    if(columnEls.length>0)
    {
        $(columnEls[0]).css('background-color','#F00');
    }
};

var dragleaveHandler = function(event){
    event.preventDefault();
    var columnEls = event.target.getElementsByClassName('column');
    if(columnEls.length>0)
    {
        $(columnEls[0]).css('background-color','grey');
    }
};

var dragendHandler = function(event){
    event.preventDefault();
    var columns = document.getElementsByClassName('column');
    [...columns].forEach(col => 
        {
            $(col).css('background-color','grey')
        }
    );
};

var dropHandler = function(event){
    event.preventDefault();
    var columnEls = event.target.getElementsByClassName('column');
    if(columnEls.length>0)
    {
        var targetColumn = columnEls[0].id.replaceAll("_", " ");

        if(targetColumn!=startColumn)
        {
            var ticket = JSON.parse(event.dataTransfer.getData("text/plain"));
            var moveticketpayload = {ticketId:ticket['Ticket #'], targetColumn:targetColumn};

            $.ajax({
                type : "PUT",
                url : '/data',
                dataType: "json",
                data: JSON.stringify(moveticketpayload),
                contentType: 'application/json;charset=UTF-8',
                success: function () {
                    console.log('Status updated');
                    location.reload(true);
                }
            });
        }
    }
};