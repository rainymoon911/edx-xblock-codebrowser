function CodeBrowserBlock(runtime, element) {
  $(element).find('#generate_btn').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'generate');
    var data = {
      lab: $("#lab", element).val()
    };
    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      window.location.reload(true);
    });
  });
  
  $(element).find('#edit_btn').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'edit');
    var data = {
      src: $("#codeview", element).attr("src")
    };
    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
    });
  });
}
