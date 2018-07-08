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
    
	windowOpen=true;
	//$('#id_print_payment_receipt').unbind('click').bind('click', print_payment_receipt(header));
	//Initialize the tab system.
	$( "#tabs" ).tabs(
			
			{
				select: function(event,ui){
			    			//alert("tab selected" + ui.index + ui.tab);
			    			//Fetch the interrupt list or Refresh the list only when clicking the 5th tab.
			    			if (ui.index == 5){ //Payment-Procedure tab.
			    				do_pendinginterrupts();
			    			}
			    			else if(ui.index == 3){ //Proceducer tab.
			    				
			    				//*** Some TAB specific settins. ***//

			    			    $('#tabs-4 input').each(function(){
			    			    	//We dynamically add the onClick event. This is the only way to get the patient header info.
			    			    	var value = $(this).attr('name');
			    			    	
			    			    	//$(this).attr('onClick','process_interrupts('+ header + ',"' + value +'")');
			    			    	//document.getElementById(value).setAttribute('onClick','adfasdf()');
			    			    	
			    			    	//Bind Click events to all start and stop buttons.We will remove this binding before exiting the tab.
			    			    	$(this).unbind('click').bind('click', function(){
			    			    		
			    			    		
			    			    		process_interrupts(header,value);
			    			    	});
			    			    	
			    			    	//** USED FOR IE BUG 
			    			    	//alert("binding..." + value);
			    			    	
			    			    	
			    			    });
			    			    
			    			}
			    			
			    						    				
			    			
			    			/*else if(ui.index == 6)
			    			{
			    				$('#tab-7 input').each(function(){
			    					     $(this).unbind('click').bind('click',function(){
                                         //$("#appointment_no").attr("checked","checked");
			    					     //document.getElementById("appointment_no").checked=true;
			    					    	 document.getElementById("demo1").style.visibility="hidden";
			    					    	// $("#demo1").hide();
                                         });
			    				});
			    				}*/
			    				/*$("input[name='shadowappointment']").each(function() {
			    					if($(this).val() == 'no') {
			    					$(this).attr('checked','checked');
			    					}
			    					});*/
			    			
						}
			}
			
			
	);
	
    $('#id_cc_info').val("");
    $('#id_payment_amount').val("");
    $('#id_payment_type').val("cash");
    $('li.cc_info').hide();
    $('#id_paymentprocedure_cc_info').val("");
    $("#id_paymentprocedure_payment_amount").val("");
    $("#id_paymentprocedure_payment_type").val("cash");
    $('li.paymentprocedure_cc_info').hide();
    
    $('.shadow-remove').unbind('click').click(function(){
	    if(confirm('Do you really want to delete patient?')){
	    	
	    	sendEvent('delete',header);
	    	
	    	
	    	$('.shadow-wrap').hide();
	    	$('.shadow-content').hide();
	    	}
	    return false;
	});
    
    $('#id_print_payment_receipt').unbind('click').click(function(){
    	
    	
    	//alert('text...' + header);
    	
    	var current_date = $('#id_header_tools_cal_value').val();
    	
    	url = '/printReceipt/?headerID=' + header + '&date=' + current_date 
    	
    	$('#print_receipt_iframe').attr('src',url);
    	    	    	
    });
    
    $('#id_edit_button').unbind('click').click(function(){
		//Change the Clinic id of the patient. For that we 
		//1. Delete the current patientLog 
		//2. Then update newclicic info to the patientLog
		
		//alert("Processing edit_tab");
		
		new_clinic = $("#clinic_list").val();
		
		//Subscribe the stomp client with new clinic channel.
		new_clinic_channel = "/topic/frontdesk" + new_clinic;
		client.subscribe(new_clinic_channel);
		
		//First delete the correponding client from the front desk.
		sendEvent("delete",header);
		
		//Then update the desitination clinic with this new patient.
		msg = {'type':'move','headerID': header,'new_clinic':new_clinic };
		msg = JSON.stringify(msg);
		client.send(msg,new_clinic_channel);
		
		//After sending the update, clean the subscribe link. and Avoid the mixing up of ***frontdesk channels***.
		if ( new_clinic_channel != CHANNEL_NAME ){
			//To remove the chance of get unsbuscribed from original channel.
			client.unsubscribe(new_clinic_channel);
		}
		$('.shadow-wrap').click();
		
		
		return false;
		
	
    });
    

   
    $('#id_add_payment_button').unbind("click").click(do_submit_payment);
    $('.payment_form_close').unbind("click").click(hideDisplayDialog);
    $('#id_add_provider_button').unbind("click").click(do_submit_provider);
    
    
    $('#id_add_paymentprocedure_button').unbind("click").click(do_submit_paymentprocedure);
    $('#next_apt_date').unbind("click").click(submitappointment);
    
    //Interrupt list building.
    //$('#id_tab6').click(do_pendinginterrupts);
    
    
    //$('#id_interrupt_type').unbind("click");
    
    $('.shadow-wrap').fadeIn(250);
    $('.shadow-content').fadeIn(250);
    
    
    function submitappointment()
	   {    
		   var seldate=$("#datepicker").val();
		   var dateBits =seldate.split('/');
		   //var dateBits = this.form.date.value.split('/');
        //alert(dateBits[2] + '-' + dateBits[0]
       // + '-' + dateBits[1] + ' 00:00:00');
		   var newdatebits=dateBits[2] + '-' + dateBits[0]+ '-' + dateBits[1] ;
		   var year = dateBits[2];
		   var month = dateBits[0];
		   var date = dateBits[1];
		   //alert(year+month+date);
		   //alert(typeof(year)+typeof(month)+typeof(date));
		   //alert(newdatebits);
		  $.ajax(
				   {
					   url:"/saveappointment/",
					   data:{header:header,newdate:newdatebits,user:USERNAME},
					   type:"POST",
					   success:function(text){
						               //alert(text);
						             if(text=="1") 
						            	{
						            	 alert("successfully submitted");
						            	 document.getElementById("demo1").style.visibility="hidden";
						            	} 
					                }
				   }
				   );
        
        
	   }
  //this function create an interrupt list for each patient 
    function do_pendinginterrupts()
    {
    	
    	//alert("updating list");
       	$.ajax(
    			{
    				url:"/patientinterrupts/",
    				data:{header:header},
    				dataType: 'json',
    				type:"POST",
    				success: function(data){
    					//msg=simplejson.loads(msg);
    					   					
    					a = data.paymentprocedureinterrupts;
    					b = data.interruptid;
    					
    					//alert(a.length + "    " +  b.length);
    					if(a.length > 0 && b.length > 0){
    						showinterrupts(a,b);
    					}
    					else{
    						$('#id_interrupt_type').html("");
    						$("<option value='others'>others</option>").appendTo('#id_interrupt_type');
    					}
    					
    					
    				}
    			}
    		); 
    }
    
   function showinterrupts(a,b)
    {
    	$('#id_interrupt_type').html("");
    	
    	
    	for(var i in a)    	
    	{
    		//alert(a[i]+b[i]);
    		   		
    		$("<option value='"+b[i]+"'> "+a[i]+" </option>").appendTo('#id_interrupt_type');
    	}
    	
    	$("<option value='others'>others</option>").appendTo('#id_interrupt_type');
    	
    }
    
    function do_submit_provider(form){
    	//Send ajax post request to server with the provider information.
    	
    	var provider = $('#id_provider').val();
    	
    	//alert(provider +":" +  header);
    	
    	$.ajax(
    			{
    				url: "/addProvider/",
    				data: { header:header, provider_id:provider, user:USERNAME },
    				type: "POST",
    				success: function(text){
    					//alert(text);
    					if(text == 1){
    					$('.shadow-wrap').click();
    					}
    				}
    				
    			}
    		);
    	
    	return false;
    	
    }
    
    
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
    		data: {type:payment_type,amount:amount,cc_info:cc_info,header:header,user:USERNAME},
    		type: "POST",
    		success: function(text){
    			
    			//alert(text);
    			
    			//alert(text.header + text.user + text.amount +text.event);
    			
    		    if(text=="1"){
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
    //function to provide payment facility to interrupts
    function do_submit_paymentprocedure(form){
    	var inp_cc_info=$('#id_paymentprocedure_cc_info');
    	var inp_amount = $('#id_paymentprocedure_payment_amount');
    	var payment_type = $('#id_paymentprocedure_payment_type').val();
    	var interrupt_type  =   $('#id_interrupt_type').val();
    	var amount = parseFloat(inp_amount.val());
    	var cc_info = parseInt(inp_cc_info.val(),10);
    	//alert(interrupt_type);
    	if(interrupt_type=="others")
    	{
    		msg={type:payment_type,amount:amount,cc_info:cc_info,header:header,user:USERNAME}
    	}
    	else
    	{
    		msg={type:payment_type,amount:amount,cc_info:cc_info,interrupt:interrupt_type, header:header,user:USERNAME}
    	}	

    	if((!amount) ||(isNaN(amount))){
    	    _error(inp_amount);
    	    return false;
    	}
    	if(payment_type == 'cc'){
    	    if((!cc_info) ||(isNaN(cc_info)) || (inp_cc_info.val().length != 4)){
    		_error(inp_cc_info);
    		return false;
    	    }
    	}
    	$.ajax(
    	    {
    		url: "/addPayment/",
    		//data: {type:payment_type,amount:amount,cc_info:cc_info,interrupt:interrupt_type, header:header,user:USERNAME},
    		data:msg,
    		type: "POST",
    		success: function(text){
    			//alert(text);
    			
    		    if(text=="1"){
    		    	
    		    	//refresh the interrupt list.
    		    	do_pendinginterrupts();
    		    	
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
    
    
    

    
    //Default selcted tab is always first one.
    $( "#tabs" ).tabs( "option", "selected", 0 );
    
     
}//end of displaydialog function



function initDisplayDialog(){
    
	$('#id_payment_type').change(function(e){
    	
	    if(this.value == 'cc'){
	    	$('li.cc_info').show(200);
	    }
	    else{
	    	$('li.cc_info').hide(200);
	    }
	});
  $('#id_paymentprocedure_payment_type').change(function(e){
    	
	    if(this.value == 'cc'){
	    	$('li.paymentprocedure_cc_info').show(200);
	    }
	    else{
	    	$('li.paymentprocedure_cc_info').hide(200);
	    }
	});
	
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
	
	var msg = {'header':header,'status':status,'int_id':int_id,'username':USERNAME };
	
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

$(document).ready(function(){
	initDisplayDialog();
    });

