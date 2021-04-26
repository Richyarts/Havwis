<script>
  try{
    {% if info %}
      let info = eval("{{info|safe}}")
      const one_btc_one_usd = info[0]["lastPrice"]
    {% else %}
      const one_btc_one_usd = 50034.70
    {% endif %}
    let post_data = {"csrfmiddlewaretoken":"{{csrf_token}}", "amount":$("#btc-input").val() , "address":$("#address").val(), "network":"{{network}}"};
    $(".custom-control-input").on("click", ()=>{
      if($(".custom-control-input").prop("checked")){
         $("#process").prop("disabled", false);
       }else{
         $("#process").prop("disabled", true);
       }
     });
    $("#btc-input").on("keyup", function(){
       $("#usd-input").val(parseFloat((one_btc_one_usd * $("#btc-input").val()).toFixed(4)));
     });
     $("#usd-input").on("keyup", function(){
       $("#btc-input").val(parseFloat(($("#usd-input").val()/one_btc_one_usd)).toFixed(8));
     });
     $("#confirm").on("click", function(){
       $("#process").prop("disabled", false);
       $("#modal_tx_fee").modal("hide");
       $("#modal_tx_pin").modal("show");
     });
     $("#process").on("click", function(){
       $("#process").html("<span class='spinner-grow spinner-grow-sm text-white'></span>");
       $.post("/activity/wallet/send/?network={{network}}&next=fee", {"csrfmiddlewaretoken":"{{csrf_token}}", "amount":$("#btc-input").val() , "address":$("#address").val(), "network":"{{network}}"}, (data, status)=>{
         if(data.status){
           try{
           const usd_amount = parseFloat($("#usd-input").val());
           const crypto_amount = parseFloat($("#btc-input").val());
           const tx_fee = parseFloat(data.data.fee);
           const tx_fee_usd = parseFloat((one_btc_one_usd * tx_fee).toFixed(2));
           const tx_fee_percent = (tx_fee_usd/usd_amount).toFixed(4);
           const final_crypto_amount = parseFloat((crypto_amount - tx_fee).toFixed(8));
           const final_usd_amount = parseFloat((usd_amount - tx_fee_usd).toFixed(4));
           $(".tx-amount").html(`${final_crypto_amount} BTC ~ <span class="text-success">$${final_usd_amount}</span>`);
           $(".tx-fee").html(`${tx_fee} BTC ~ $${tx_fee_usd}`);
           $("#modal_tx_fee").modal("show");
           }catch(e){ alert(e); }
         }else{
           alert(JSON.stringify(data))
         }
       }).success(function(){
         $("#process").html("Proceed");
       }).error(function(){
         alert("error")
       });
     });
  }catch(e){
    alert(e)
  }
</script>