var btn = $(".MainBtn");

$(btn).click(function(){
  $(this).addClass("active");
  $("h2").text("Listen...");
  eel.listen()();
});

eel.expose(end_listen);
function end_listen(text) {
  $(".MainBtn").removeClass("active");
  $("h2").text(text);
}
