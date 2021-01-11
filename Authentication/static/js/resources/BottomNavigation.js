//>>>Hide nav indicators
$(".nav-btn-profile-circle").hide();
$(".nav-btn-card-circle").hide();
$(".nav-btn-wallet-circle").hide();

//>>>Disable an element
$(".disabled").attr('disabled','disabled');
       
$("#nav-btn-home").on("click" , function (){
  $.ajax({
    url:"/havwis/home/",
    cache:false,
    dataType:"html",
    success: function (data){
      $("body").html(data);
    }
  });  
  $("#nav-btn-card img").removeClass("filter-default"); $("#nav-btn-wallet img").removeClass("filter-default");
  $("#nav-btn-home img").addClass("filter-default"); $("#nav-btn-home img").removeClass("filter-blue-2");
  $("#nav-btn-home-text").addClass("text-primary"); $("#nav-btn-home-text").removeClass("text-muted");
  $("#nav-btn-wallet-text").removeClass("text-primary");
  $(".nav-btn-home-circle").show();  $(".nav-btn-wallet-circle").hide();$(".nav-btn-card-circle").hide(); $("#nav-btn-card-text").addClass("text-muted");
});
$("#nav-btn-wallet").on("click" , function (){
  $.ajax({
    url:"/havwis/wallet/",
    cache:false,
    dataType:"html",
    success: function (data){
      $(".linearlayout").html(data);
    }
  });  
  $("#nav-btn-wallet img").addClass("filter-default");
  $("#nav-btn-home-text").removeClass("text-primary");
  $("#nav-btn-card img").removeClass("filter-default");
  $("#nav-btn-card-text").removeClass("text-primary");  
  $(".nav-btn-card-circle").hide(); 
  $("#nav-btn-home img").removeClass("filter-default");
  $("#nav-btn-home img").addClass("filter-blue-2");
  $("#nav-btn-home-text").removeClass("text-primary"); $("#nav-btn-home-text").addClass("text-muted");
  $("#nav-btn-wallet img").addClass("filter-default");
  $("#nav-btn-wallet-text").addClass("text-primary");
  $(".nav-btn-home-circle").hide(); 
  $(".nav-btn-wallet-circle").show();
});
$("#nav-btn-card").on("click" , function(){
  $(".linearlayout").load("/havwis/card/");
  $("#nav-btn-home img").removeClass("filter-default"); $("#nav-btn-home img").addClass("filter-blue-2");
  $("#nav-btn-wallet img"). removeClass("filter-default"); $("#nav-btn-home-text").removeClass("text-primary"); $("#nav-btn-home-text").addClass("text-muted");
  $("#nav-btn-wallet-text").removeClass("text-primary");     $("#nav-btn-card img"). addClass("filter-default"); $("#nav-btn-home-text").removeClass("text-primary"); $("#nav-btn-home-text").addClass("text-muted");
  $("#nav-btn-card-text").addClass("text-primary");  
  $(".nav-btn-card-circle").show(); 
  $(".nav-btn-home-circle").hide();  $(".nav-btn-wallet-circle").hide();
});
$("#add-money").on("click" , function (){
  $("body").load("/havwis/pay/");
});