function returnStringArray(arr){
	var sOutput = "";
	var i = '';
	for(i in arr) {
        	var value = arr[i];
        	sOutput += i + "="+value+"&";
	}	
	return sOutput.replace(/%5B%5D/g, '[]');
}

function _error(element){
    element.focus();
    element.css('background-color','#ff9999');
    window.setTimeout(
	function(){
	    element.css('background-color','');
	},
	500
    );
}

function display_paymenthistory(header){
	
    $.ajax(
	{
	    url:'/paymenthistory/',
	    data:{header:header,date:current_date},
	    type:"POST",
	    success:function(text){
		$('.shadow-body-inner').html(text);
		$('.shadow-wrap').fadeIn(100);
		$('.shadow-body').fadeIn(100);
	    }
	    
	}
    );
    // alert(header);
}


function hideDisplayDialog(){
    $('.shadow-wrap').fadeOut(100);
    $('.shadow-content').fadeOut(100);
    $('.shadow-body').fadeOut(100);
    windowOpen=false;
    
    //$('#id_print_payment_receipt').unbind('click');
    
    /*
     * Also unbind the click events from the Interrupt tabs buttons.
     * This is done to avoid the accumulation of click events.
     */
    
    $('#tabs-4 input').each(function(){
    	
    	//** USED FOR IE BUG 
    	//alert("unbinding the events" + $(this).attr('value'));
    	
    	$(this).unbind('click');
    });
}



function displayDialog(header){
    
	console.log(header);
	//windowOpen=true;
	//$('#id_print_payment_receipt').unbind('click').bind('click', print_payment_receipt(header));
	//Initialize the tab system.
	
	
    $('#id_cc_info').val("");
    $('#id_payment_amount').val("");
    $('#id_payment_type').val("cash");
    $('li.cc_info').hide();
	
    $('#id_paymentprocedure_cc_info').val("");
    $("#id_paymentprocedure_payment_amount").val("");
    $("#id_paymentprocedure_payment_type").val("cash");
    $('li.paymentprocedure_cc_info').hide();
    
    
    
     
}



function initDisplayDialog(){
	//console.log("init");
	$('#id_payment_type').change(function(e){
    	
		//console.log("test..");
	    if(this.value == 'cc'){
	    	$('li.cc_info').show(200);
	    }
	    else{
	    	$('li.cc_info').hide(200);
	    }
	});
 /* $('#id_paymentprocedure_payment_type').change(function(e){
    	
	    if(this.value == 'cc'){
	    	$('li.paymentprocedure_cc_info').show(200);
	    }
	    else{
	    	$('li.paymentprocedure_cc_info').hide(200);
	    }
	});*/
	
	//$('.provider-form').change(function(e){})
	
	//$('.provider-form').hide();
	//$('.payment-form').hide();
	
    $('.shadow-wrap').unbind('click').click(hideDisplayDialog);
    //$('.shadow-content').click(hideDisplayDialog);
    $('.shadow-body').click(hideDisplayDialog);

    
    //$('.shadow-payment').unbind('click').click(function(){
	//    return false;
	//});
    
    //$('.shadow-provider').unbind('click').click(function(){
	//    return false;
	//});
    
}


function process_interrupts(header,value){
	//This function will be called from the shadow window, and it process the start and ending of particular interrupts.
	//value is the corresponding button id.
	
	//** USED FOR IE BUG 
	//alert("header: " + header + "Value: " + value);
	
	var split = value.split("_");
	
	var status = split[0];
	var int_id = split[1];
	
	//alert("header: " + header +" Status: " + status +" INT_ID: " + int_id );
	
	var msg = {'header':header,'status':status,'int_id':int_id,'username':USERNAME};
	
	$.ajax({
			
		url: '/handleInterrupt/',
		dataType : 'json',
		type     : 'POST',
		data	 : msg,
		success  : function(msg){
			
			//alert("successfully updated the interrupts.." + msg.header + msg.status + msg.int_id + msg.username);
			//Unbind that click event after processing the button.
			//$('#'+ value).unbind('click');
			
		}
		
	});
	
	
}

function print_payment_receipt(header){
	//Process printing the patient amounts.
	alert('pringing receipt..'+ header);
	//window.print();
}

function printIframe(id)
{
    var iframe = document.frames ? document.frames[id] : document.getElementById(id);
    var ifWin = iframe.contentWindow || iframe;
    iframe.focus();
    ifWin.printPage();
    return false;
}

$('#id_shadow_page').live('pageshow', function(event){
	var header = $("#header_id").val();
	//console.log(header);
	$('#id_payment_type').val("cash");
	$('#id_cc_info').val("");
	 $('#id_payment_amount').val("");
	 
	 $('li.cc_info').hide();
	
	initDisplayDialog();
	$('#id_add_payment_button').unbind("click").click(do_submit_payment);
	
	//function to provide payment facility to events
    function do_submit_payment(form){
    	var inp_cc_info=$('#id_cc_info');
    	var inp_amount = $('#id_payment_amount');
    	var payment_type = $('#id_payment_type').val();
    	var amount = parseFloat(inp_amount.val());
    	var cc_info = parseInt(inp_cc_info.val(),10);
       // alert(amount);
        //alert(cc_info);
        //alert(payment_type);
    	if((!amount) ||(isNaN(amount))){
    	    _error(inp_amount);
    	    //alert("t1");
    	    return false;
    	}
    	//alert("t");
    	if(payment_type == 'cc'){
    	    if((!cc_info) ||(isNaN(cc_info)) || (inp_cc_info.val().length != 4)){
    		_error(inp_cc_info);
    		//alert("t2");
    		return false;
    	    }
    	}
    	
    	$.ajax(
    	    {
    	    	
    		url: "/addPayment/",
    		data: {type:payment_type,amount:amount,cc_info:cc_info,header:header},
    		type: "POST",
    		success: function(text){
    			
    			//alert(text);
    			
    			//alert(text.header + text.user + text.amount +text.event);
    			
    		    if(text=="1"){
    		    	alert("successfully paid");
    		    	try{
    		    		after_payment_add(header);
    		    	} 
    		    	catch (x) {
    		    	}
    		    	

    			$('.shadow-wrap').click();
    		    }
    		}
    	  });
    	return false;
    }
$('#id_print_payment_receipt').unbind('click').click(function(){
    	
    	
    	//alert('text...' + header);
    	
    	var current_date = $('#id_header_tools_cal_value').val();
    	//console.log(current_date);
    	
    	url = '/printReceipt/?headerID=' + header + '&date=' + current_date 
    	
    	$('#print_receipt_iframe').attr('src',url);
    	    	    	
    });
	
		
	
	//console.log("ready..");
    });


$('#id_provider_page').live('pageshow', function(event){
	
	var header = $("#header_id").val();
	
	$('#id_add_provider_button').unbind("click").click(do_submit_provider);
	
	function do_submit_provider(form){
    	//Send ajax post request to server with the provider information.
    	
    	var provider = $('#id_provider').val();
    	
    	//alert(provider +":" +  header);
    	
    	$.ajax(
    			{
    				url: "/addProvider/",
    				data: { header:header, provider_id:provider},
    				type: "POST",
    				success: function(text){
    					//alert(text);
    					if(text == 1){
    					alert("successfully assigned");	
    					$('.shadow-wrap').click();
    					}
    				}
    				
    			}
    		);
    	
    	return false;
    	
    }
	
});

