function CodeBrowserEditBlock(runtime, element) {
  var generateHandlerUrl = runtime.handlerUrl(element, 'generate');
  function jsCallback(response) {
        if (response.result == true) {
            window.location.reload(true);
        } else {
            $('.error-message', element).html('Error: ' + response.message);
        }
    }
    
  $('#generate_btn', element).click(function(eventObject) {
        params = {
            "lab": $("#lab", element).val()
        };
        $.ajax({
            type: "POST",
            url: generateHandlerUrl,
            data: JSON.stringify(params),
            success: jsCallback
        });
        $('.error-message', element).html();
    });
}
