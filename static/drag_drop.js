var startColumn = '';

var dragstartHandler = function(event, data){
    event.dataTransfer.setData("text/plain", data);
    event.dataTransfer.effectAllowed = "move";
    startColumn = data.Status;
};

var dragoverHandler = function(event){
    event.preventDefault();
    if(event.target.classList.contains('column'))
    {
        $(event.target).css('background-color','#F00');
    }
};

var dragleaveHandler = function(event){
    event.preventDefault();
    if(event.target.classList.contains('column'))
    {
        $(event.target).css('background-color','grey');
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
    if(event.target.classList.contains('column'))
    {
        if((event.target.id.replace("_", " "))!=startColumn)
        {
            console.log('moved an item');
        }
    }
};