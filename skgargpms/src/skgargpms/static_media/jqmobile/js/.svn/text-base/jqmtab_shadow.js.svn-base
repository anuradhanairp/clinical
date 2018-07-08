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

function printIframe(id)
{
    var iframe = document.frames ? document.frames[id] : document.getElementById(id);
    var ifWin = iframe.contentWindow || iframe;
    iframe.focus();
    ifWin.printPage();
    return false;
}

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
    	
    	$.mobile.showPageLoadingMsg();//this function is used to show a loading image until the response comes from server 	

    	var inp_cc_info=$('#id_cc_info');
    	var inp_amount = $('#id_payment_amount');
    	var payment_type = $('#id_payment_type').val();
    	var amount = parseFloat(inp_amount.val());
    	var cc_info = parseInt(inp_cc_info.val(),10);
 
    	if((!amount) ||(isNaN(amount))){
    	    _error(inp_amount);
    	    //alert("t1");
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
    		data: {type:payment_type,amount:amount,cc_info:cc_info,header:header},
    		type: "POST",
    		success: function(text){
    			
    		    if(text=="1"){
    		    	$.mobile.hidePageLoadingMsg();	

    		    	$('#id_cc_info').val();
    		    	
    		    	$('#id_payment_amount').val();
    		    	
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
     
    	
	    var current_date; 
    	
		if( $.cookie('current_date')!= undefined )
		{
			current_date =  $.cookie('current_date')
		}	
		else
		{
			var current_time = new Date();
    
			var y = current_time.getFullYear();
			var m = current_time.getMonth()+1;//in javascript january is taken as 0.So to get the correct month add 1 to the javascript value
			var d = current_time.getDate();
			current_date= y+"-"+m+"-"+d;
    
		}
    	//console.log(current_date);
    	
    	url = '/printReceipt/?headerID=' + header + '&date=' + current_date 
    	
    	$('#print_receipt_iframe').attr('src',url);
    	    	    	
    });

});


$('#id_provider_page').live('pageshow', function(event){
	
	var header = $("#header_id").val();
	
	/*
	var home_url = $("#url_id").val();
	
	if ($.cookie('current_date')!= undefined)
	{	
	
		home_url = home_url +'&date='+ $.cookie('current_date');
	}
	
	$('a.ui-shadow').attr("data-rel","");
	$('a.ui-shadow').attr("href", home_url);
	*/

	$('#id_add_provider_button').unbind("click").click(do_submit_provider);
	
	function do_submit_provider(form){
		
		$.mobile.showPageLoadingMsg();	
    	//Send ajax post request to server with the provider information.
    	var provider = $('#id_provider').val();
    	$.ajax(
    			{
    				url: "/addProvider/",
    				data: { header:header, provider_id:provider},
    				type: "POST",
    				success: function(text){
    					//alert(text);
    					if(text == 1){
    					
    					$.mobile.hidePageLoadingMsg();		
    					
    					alert("successfully assigned");	
    					
    					$('.shadow-wrap').click();
    					}
    				}
    				
    			}
    		);
    	
    	return false;
    	
    }
	
});

$('#id_edit_page').live('pageshow', function(event){
	
	var headerid = $("#header_id").val();

	$('#id_edit_button').unbind('click').click(function(){
		//Change the Clinic id of the patient. For that we 
		//1. Delete the current patientLog 
		//2. Then update newclicic info to the patientLog
		
		//alert("Processing edit_tab");
		$.mobile.showPageLoadingMsg();	
		
		new_clinic = $("#clinic_list").val();
		//console.log(new_clinic);
	
		
		//Subscribe the stomp client with new clinic channel.
		new_clinic_channel = "/topic/frontdesk" + new_clinic;
		
		msg = {'headerID': headerid, 'new_clinic_id': new_clinic, 'user': 'suresh' }
		
		$.post('/jqmtab/move_patient/', msg, function(data){
			
			if(data.status == 'OK'){
				
				$.mobile.hidePageLoadingMsg();
				alert('Patient Successfully moved to new clinic..');
			
			}else{
    			
    			var msg = data.msg;
    			
    			for(index in data.interrupts){
    				msg += "\n" + index + 1 + ". " + data.interrupts[index][1];
    			}
    			
    			alert(msg);
			}
		});
		return false;
    });
});


$('#id_procedure_page').live('pageshow', function(event){
	
	var headerid = $("#header_id").val();
	
	var handle_procedure = function(interrupt_id,header_id,value){
		
		//console.log("test..");
		var status;
		//console.log("interid"+" "+interrupt_id);
		if (value == "off")
		{
			 status = "started";
			
		}	
		if (value == "on")
		{
			status = "stopped";
		}
		var data = 'header_id='+header_id+"&interrupt_id="+ interrupt_id+"&status="+status ;
		//console.log(data);
		//ajax call to save the status of interrupts corresponding to particular patient
		$.post('/jqmobile/jqmobile_handle_procedure/',data, function(data){
		    
			//console.log(data);
			if(data.status == "started")
			{
				$("#interrupt_"+data.interrupt_id).html('<option value="off">stop</option>'+ '<option value="on">start</option>');
				
			}
			if(data.status == "stopped")
			{
				$("#li_interrupt_"+data.interrupt_id).html(
						
						'<label for="interrupt">'+data.interrupt_name+" "+'complete'+'</label>'
						
				
				);
				
				
			}
		});
			
	}

	//this function is used to handle the slider(used to start or stop the interrupt) in procedure tab 
	//The attribue 'aria-valuenow' of 'a' tag hold the current value of slider 
	$(".ui-slider").bind("mouseup, vmouseup", function() {
        // lunch action here
        var  header_id = $("#header_id").val();
        $(this).find('a').attr('href',"");
        value = $(this).find('a').attr('aria-valuenow');
        var id = $(this).find('a').attr('aria-labelledby'); //eg: sprinkles_1-label,here 1 is the id of interrupt
        var selid = id.split("-");//sprinkles_1-label is split into sprinkles_1 and label
	    var intrid = selid[0].split("_");//sprinkles_1 is split into sprinkles and 1
        var interruptid = intrid[1];
        handle_procedure(interruptid,header_id,value);
        
    });
});




$('#id_remove_page').live('pagebeforeshow', function(event){
	
	var headerid = $("#header_id").val();
	
	$('.shadow-remove').unbind('click').click(function(){
		//$.mobile.showPageLoadingMsg();	
	   
		if(confirm('Do you really want to delete patient?')){
	    	
			$.mobile.showPageLoadingMsg();	
	    	
			var msg = {'user': 'suresh', 'headerID': headerid}
	    	
	    	$.post('/jqmtab/remove_patient/',msg, function(data){
	    		
	    		if(data.status == 'OK'){
	    			
	    			$.mobile.hidePageLoadingMsg();
	    			
	    			alert('Patient succesfully delted..');
	    			
	    		}else{
	    				    			
	    			var msg = data.msg;
	    			
	    			for(index in data.interrupts){
	    				msg += "\n" + index + 1 + ". " + data.interrupts[index][1];
	    			}
	    			alert(msg);
   			
	    		}
	    	});
	    	
	    }
	    return false;
	});
	
});



$('#id_payment_procedure_page').live('pagebeforeshow', function(event){
	
	var headerid = $("#header_id").val();
	
	$('#id_paymentprocedure_cc_info').val("");
    $("#id_paymentprocedure_payment_amount").val("");
    $("#id_paymentprocedure_payment_type").val("cash");
    $('li.paymentprocedure_cc_info').hide();
    initDisplayDialog();
    
    do_pendinginterrupts();
    //console.log(headerid);
    
    //$('#id_interrupt_type').selectmenu('refresh',true);
    //$(".payment_procedure_form").listview('refresh');
    
    $('#id_interrupt_type').bind('change',function(){
    	console.log($('#id_interrupt_type').val());
    	console.log($("#id_interrupt_type option:selected").text());
       //$("#id_interrupt_type option:selected").text();
    	//$("#id_interrupt_type").text(txt);
    	//$('#id_interrupt_type').selectmenu('refresh');
   
    });
    
    function do_pendinginterrupts()
    {
    	
    	//alert("updating list");
       	$.ajax(
    			{
    				url:"/patientinterrupts/",
    				data:{header:headerid},
    				dataType: 'json',
    				type:"POST",
    				success: function(data){
    					//msg=simplejson.loads(msg);
    					//console.log(data);   					
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
       	
       	//$(".payment_procedure_form").listview('refresh');
       	//$('#id_interrupt_type').selectmenu('refresh',true);
       	
    }
    
    function showinterrupts(a,b)
    {
    	//console.log(a+" "+b);
    	$('#id_interrupt_type').html("");
    	//$('#id_interrupt_type').change(console.log($("#id_interrupt_type").val()););
   		
		//$("<option data-placeholder='true'>choose </option>").appendTo('#id_interrupt_type');
    	
    	for(var i in a)    	
    	{
    		//alert(a[i]+b[i]);
    		   		
    		$("<option value='"+b[i]+"' > "+a[i]+" </option>").appendTo('#id_interrupt_type');
    		$('#id_interrupt_type').selectmenu('refresh');
    	}
    	
    	$("<option value='others' >others</option>").appendTo('#id_interrupt_type');
    	
    	$('#id_interrupt_type').selectmenu('refresh');
    	$(".payment_procedure_form").listview('refresh');
    	
    }
    
    $('#id_add_paymentprocedure_button').unbind("click").click(do_submit_paymentprocedure);
    
    function do_submit_paymentprocedure(form){
    	
    	$.mobile.showPageLoadingMsg();
    	var inp_cc_info=$('#id_paymentprocedure_cc_info');
    	var inp_amount = $('#id_paymentprocedure_payment_amount');
    	var payment_type = $('#id_paymentprocedure_payment_type').val();
    	var interrupt_type  =   $('#id_interrupt_type').val();
    	var amount = parseFloat(inp_amount.val());
    	var cc_info = parseInt(inp_cc_info.val(),10);
    	//alert(interrupt_type);
    	if(interrupt_type=="others")
    	{
    		msg={type:payment_type,amount:amount,cc_info:cc_info,header:headerid}
    	}
    	else
    	{
    		msg={type:payment_type,amount:amount,cc_info:cc_info,interrupt:interrupt_type, header:headerid}
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
    		    	
    		    	$.mobile.hidePageLoadingMsg();
    		    	//console.log($('#id_paymentprocedure_cc_info'));
    		    	$('#id_paymentprocedure_cc_info').val("");
    		        $("#id_paymentprocedure_payment_amount").val("");
    		    	
    		    	//refresh the interrupt list.
    		    	do_pendinginterrupts();
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
    
    
    
});


$('#id_appointment_page').live('pagebeforeshow', function(event){
	
	var headerid = $("#header_id").val();
		
	$('#next_apt_date').unbind("click").click(submitappointment);
	$('#appointment_no').change(get_radio_value);
	$('#appointment_yes').change(get_radio_value);
	$("#ui-datepicker-div").html("");
	   
	function submitappointment()
	   {    
		
		   $.mobile.showPageLoadingMsg();
		   var seldate=$("#datepicker").val();
		   var dateBits =seldate.split('/');
		   var newdatebits=dateBits[2] + '-' + dateBits[0]+ '-' + dateBits[1] ;
		   var year = dateBits[2];
		   var month = dateBits[0];
		   var date = dateBits[1];
		   
		   $.ajax(
				   {
					   url:"/saveappointment/",
					   data:{header:headerid,newdate:newdatebits,user:null},
					   type:"POST",
					   success:function(text){
						               //alert(text);
						             if(text=="1") 
						            	{
						            	 $.mobile.hidePageLoadingMsg();
						            	 alert("successfully submitted");
						            	 document.getElementById("demo1").style.visibility="hidden";
						            	 //$("#demo1").hide();
						            	 $('#appointment_yes').attr("checked", false);


						            	} 
					                }
				   }
				   );
     
     
	   }
	
	function get_radio_value()
	{
		  
		   var var_name = $("input[name='shadowappointment']:checked").val();
		  
		   if(var_name=="yes")
		   {
			   document.getElementById("demo1").style.visibility="visible";
		   }
		   if(var_name=="no")
		   {
			   document.getElementById("demo1").style.visibility="hidden";

		   }

	}
	
});


$('#id_payment_page').live('pagebeforeshow', function(event){
	
	//console.log("paymentpage");
	var clinic_id = $("#clinic_id").val();
	
	
	var payment_back = $("#payment_back").attr('href');
	
	if ($.cookie('current_date')!= undefined)
	{	
	
		payment_back = payment_back + '&date=' + $.cookie('current_date');
		
	}
	else
	{
		payment_back = payment_back;
	}	
	
	$("#payment_back").attr("href",payment_back);
	$('#id_header_tools_pdf').click(generate_pdf);
	
	
	$(".ui-shadow").click(function(){      
        $('.ui-dialog').dialog('close');
    });
	
	
	
	function generate_pdf(){
	    /*var current_time = new Date();
	    
	    var y = current_time.getFullYear();
	    var m = current_time.getMonth()+1;//in javascript january is taken as 0.So to get the correct month add 1 to the javascript value
	    var d = current_time.getDate();
	    var current_date= y+"-"+m+"-"+d;*/
	    	
		if( $.cookie('current_date')!= undefined )
		{
			current_date =  $.cookie('current_date')
		}	
		else
		{
			var current_time = new Date();
	    
	    	var y = current_time.getFullYear();
	    	var m = current_time.getMonth()+1;//in javascript january is taken as 0.So to get the correct month add 1 to the javascript value
	    	var d = current_time.getDate();
	    	current_date= y+"-"+m+"-"+d;
	    
		}
	    try{
		
		var url ="/pdf/?type=payments&date="+escape(current_date)+"&clinicID="+clinic_id;
		window.open(url);
		// alert(current_date);
	    } catch (x) {
		console.log(x);
	    }
	}

	
});
