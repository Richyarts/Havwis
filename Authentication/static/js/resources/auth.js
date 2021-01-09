$(function (){
  $('.phone_layout').hide();
  $('.password_layout').hide();
});

$('.username_layout_button').on('click' , function (){
  $('.phone_layout').show();
  $('.username_layout').hide();
  $('.email-remove').hide();
});

var phone_visbile = 0;
$('.phone_layout_button').on('click' , function (){
  if(phone_visbile == 1){
    $('.password_layout').show();
    $('.phone_layout').hide();
  }
  if(phone_visbile == 0){
    $('.phone-tab').removeClass('active');
    $('.email-tab').addClass('active');
    $('.phone-remove').hide();
    $('.email-remove').show();
  }
  phone_visbile++;
});

$('.phone-layout-tab').on('click' , function (){
    $('.email-tab').removeClass('active');
    $('.phone-tab').addClass('active');
    $('.email-remove').hide();
    $('.phone-remove').show();
    if(phone_visbile != 0){
      phone_visbile = 0;
    }
});

$('.email-layout-tab').on('click' , function (){
    $('.phone-tab').removeClass('active');
    $('.email-tab').addClass('active');
    $('.phone-remove').hide();
    $('.email-remove').show();
    if(phone_visbile != 1){
      phone_visbile = 1;
    }
});
$('alert').hide();

var visibility = 0;
$('button').click(function (){
  visibility++;
 });
 
if(visibility == 0){
  var back = true;
}

$(function (){
  $('#auth-back').on("click" , function(){
    if(visibility == 2){
      $('.email-tab').removeClass('active');
      $('.phone-tab').addClass('active');
      $('.phone-remove').show();
      $('.username_layout').hide();
      $('.password_layout').hide();
    }
    if(visibility == 1){
      $('.password_layout').hide();
      $('.username_layout').show();
      $('.phone_layout').hide();
      alert(visibility);
    }
    if(visibility == 0){
      $('.password_layout').hide();
      $('.username_layout').show();
      $('.phone_layout').hide(); alert(visibility)
    }
    if(back){
      alert(back);
      $("body").load("/auth/login/");
    }
    visibility--;
  });
});