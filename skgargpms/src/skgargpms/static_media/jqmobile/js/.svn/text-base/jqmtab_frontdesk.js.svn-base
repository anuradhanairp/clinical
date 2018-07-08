
function get_cell_order(msg){
	/*
	 *This function construct the all <td> </td> of a one <tr> based on the generalized ordering of event map. 
	 *Function which helps to print the Event times based on the table Event order changes.
	 */

	//alert(event_map[0]);
	//alert(msg.patient[event_map[0]]);
	var imgurl="/static/index_htm_files/loader.white.gif";
	var length = event_map.length; 
	
	var tableString = '';
	
	for(i = 0; i < length; i++){
		
		tableString += "<td align=center>";
		   
	    if( msg.patient[event_map[i]] != undefined){
	    	tableString += msg.patient[event_map[i]]; 
	    }
	    else{
	    	
	    	//According to the Theme of the jquery mobile we can update the class properties here.
	    	
	    	tableString +=  '<div data-theme="c" class="ui-btn ui-btn-corner-all ui-shadow ui-btn-up-c" aria-disabled="false"><span class="ui-btn-inner ui-btn-corner-all"><span class="ui-btn-text"> X</span></span>';
	    	
	    	tableString += 	"<button id='button_" + msg.headerID + "_" + event_map[i] + "' class=\"ui-btn-hidden\" aria-disabled=\"false\" onclick=\"startEventForm('"+ event_map[i]  +"','"+msg.headerID+"');\">X</button>";
	    	
	    	tableString += "</div>"; 
	       		
	    }
	    tableString += "</td>";
	}
	
	
	//console.log(tableString);
	
	return tableString;
    
}

// We can use this same table construction for the comet based implementation also.
function updateTable(msg,new_row){
	
	if (new_row == false ){
		
		//Take the current row count from 
		row_number = $('#count'+ msg.headerID +' td:first').html();
		
		//console.log("row number: "+ row_number);
		
	}
	else{
		
		//Adding new row to the frontdesk, thead will be an extra row count at any time.
		row_number = $('#fdtable tr').length;
		
	}
	
    var tableString = "";
    tableString += '<tr id="count'+ msg.headerID +'">';
    
    tableString += "<td align=center><b>"+ row_number +'</b></td> <td align="center"><a href="/jqmtab/patient/' + msg.headerID + '/" class="ui-link">'+  msg.patient.name +"</a></td>";
    
    //Get the ordered table string from this function.
    dynamic_td_content = get_cell_order(msg);
    
    tableString += dynamic_td_content;
    
    tableString += "</tr>";	
    
    
    if( new_row == true){
    	//Add new two at first of tbody. If empty tbody do first, or the else part.
    	if( row_number == 1 ){
    		
    		$('#fdtable > tbody').append(tableString);
    	}
    	else {
    		$('#fdtable > tbody > tr:first').before(tableString);
    	}
    	
    }
    else{
    	//Update the row of given 'id'.
    	$('#count'+ msg.headerID).replaceWith(tableString); 
    }
} 


//Send the Updated patient Event From the Frontdesk.
function sendEvent(event, headerID){
	
	//console.log("seding evens to sever");
	msg = {'type':'eventlog','headerID':headerID,'event':event};
	msg = JSON.stringify(msg);
	client.send(msg,CHANNEL_NAME);
	
	//To display the loading image.
	$.mobile.showPageLoadingMsg();
	
}

function handle_event_update(message){
	//Update patient table when an operator click on the frontdesk button. message is a json data from server.
	//alert(message.patient.signin);
	//console.log(message);
	
	if (message.response == 'False'){
		
		if(message.from == USERNAME){
			//Only sent the warning to event originator.
			//alert("Warnning: First assign Provider to this Patient..");
			alert(message.reason);
			//console.log(message.event);
			
			var alert_msg = message.reason;
			//alert(a);
			//alert(message.headerID);
			//alert(message.event);
			//alert(a.indexOf('Interrupts'))
			var new_url = "/jqmtab/shadow_procedures/"+ message.headerID+ '/';
			if (alert_msg.indexOf('Interrupts') > -1)
			{
				//console.log("testing interrupts")
			   //displayDialog(message.headerID);
			   //$( "#tabs" ).tabs( "option", "selected", 3);
				//var new_url = "/jqmtab/shadow_procedures/"+ message.headerID+ '/';
				//$("#button_"+message.headerID+"_"+message.event).attr("href",new_url);
				$.mobile.changePage(new_url);//This method is used to redirect to a newpage.If any interrupt is pending we have to stop that interrupt.So we redirect to procedure page
				//console.log($("#id_procedure_page"));
				
				//$("#id_procedure_page").show(); 
				
			}  
			else if(message.event == "provider")
			{	
			   //displayDialog(message.headerID);
			   var procedure_url = "/jqmtab/shadow_procedures/"+ message.headerID+ '/';
			   var provider_url = "/jqmtab/shadow_provider/"+ message.headerID+ '/';
			   //$.mobile.changePage(provider_url);
			   if (alert_msg.indexOf('Interrupts') > -1)
				{
				  // displayDialog(message.headerID);
				   //$( "#tabs" ).tabs( "option", "selected", 3);
				   $.mobile.changePage(procedure_url);
				}
			   else{
				  // console.log("test provider");
				  // $( "#tabs" ).tabs( "option", "selected", 1);
				   $.mobile.changePage(provider_url);
			   }
				
			 //document.getElementById("tabs-1").style.visibility="hidden";
			 //$("#tabs-1").hide();$("#tab1").hide();
			}
			
			
			
			//Special reactivation of button at the table cell when the transaction was faild.
			var loading_id = 'loading_' + message.headerID + '_' +message.event;
			var button_id='button_'+message.headerID+'_'+message.event;
			// hide the div tag after the alert message is displayed 
			$("#" + loading_id).hide();
			//document.getElementById(loading_id).style.visibility='hidden';
			//display the button for the next transaction
			$("#"+button_id).show();
			//document.getElementById(button_id).style.visibility='visible';
		}
	}
	
	/*
	 * To make the nested key checking of javascript object by IE we changed the code to more correct form.
	 * Firefox skip some errors and it help coders but IE need exact rules.
	 */
	//else if(message.patient.delete != undefined ){
	else if(message != undefined && message.patient != undefined &&  message.patient['delete'] != undefined ){
		//Delete the corresponding row from the frontdesk. 
		$("#count"+ message.headerID).remove();
		
		//Reorder the table serial numbers.
		total_rows = $('#fdtable > tbody tr').length
		$('#fdtable > tbody tr').each(function(){
			this.cells[0].innerHTML = "<b>" + total_rows -- + "</b>";
		});
	}
	else{
		new_row = false;
		updateTable(message,new_row);
		$.mobile.hidePageLoadingMsg();
	}
	
}

function handle_new_signin(msg){
	//Update the new patient login at frontdesk.
	if (msg.response == 'OK') {
		new_row = true;
		//alert("got new update.");
		
		/*
		var datepickdate = $('#id_header_tools_cal_value').val()
		
		var currentTime = new Date()
		var month = currentTime.getMonth()  + 1
		month = month.toString();
		month = month.length == 1 ? '0'+ month : month;
		
		var day = currentTime.getDate()
		day = day.toString();
		day = day.length == 1 ? '0' + day : day;
		
        var year = currentTime.getFullYear()
        
        currentdate = year + "-" + month + "-" + day
        
        //alert('current date: ' + currentdate + '  frontdesk date: ' + datepickdate);
		
        if(currentdate == datepickdate)
        	{
        	  alert('updating tabel..');
              updateTable(msg,new_row);
        	}
        */
		
		updateTable(msg,new_row);
	}

}

//Function which accept message frame from the Stomp queue and do corresponding actions.
function handle_incomming_message(message){
	
	//alert(message.type);
	switch(message.type){
		case "eventlog":
			handle_event_update(message);
			break;
			
		case "signin":
			handle_new_signin(message);
			break;
			
		default:
			break;
	}
	
	
}
/*$( "#id_frontdesk_page" ).live( "pagecreate", function(){   
		console.log("pagecreation");
	    $( "input[type='date'], input[data-type='date']" ).each(function(){
	    	console.log($(this).hasClass("hasDatepicker"));
	        if ($(this).hasClass("hasDatepicker") == true) {
	            $(this).after( $( "<div />" ).datepicker({ altField: "#" + $(this).attr( "id" ), showOtherMonths: true }) );
	            $(this).addClass("hasDatepicker");
	        }
	    }); 
	});*/


$('#id_frontdesk_page').live("pagecreate", function(event,ui){
	
	//console.log('Creating the frontdesk page....');
	
});

$("#id_frontdesk_page").live("pagebeforeshow",function(event,ui){
	//Here we add codes that need to be run before we show this page every time.

	
	var current_time = new Date();
    
    var y = current_time.getFullYear();
    var m = current_time.getMonth()+1;//in javascript january is taken as 0.So to get the correct month add 1 to the javascript value
    var d = current_time.getDate();
    var current_date= y+"-"+m+"-"+d;
    
    $("#change_date").val(current_date);	
   
	  function  get_calender_date(new_date){
		 
		// console.log("cookiee setting...");
		 
		 $.cookie('current_date',new_date,{ path: '/jqmtab' });
		 		 		 
		 $('a').each(function(){
		
			var current_href = $(this).attr('href')
	
			if(current_href != undefined ){
			
				
					current_href = current_href.split('&date=')[0];
	
					//var current_date = escape($('#id_header_tools_cal_value').val());
			
					var new_href = current_href + '&date=' + new_date;
			
					if(current_href.indexOf('clinicID') > -1)
					{
						//change only when clinicID is there and &date= is not in the date string.
			    		//alert($(this).attr('href') + " : " + $(this).html());
						
						//console.log('changing urls: ' + this );
						$(this).attr('href', new_href);
				
					}
				
			
					}//end-if
		
		//alert(current_href);
	
	});
	
	return false;
	}
	   
	   
	var cookie_date = $.cookie('current_date');

	if(cookie_date != undefined )
	{
		
        get_calender_date(cookie_date);
		
		var date_field = cookie_date.split("-");
		
		$("#change_date").val(date_field[1]+"/"+date_field[2]+"/"+date_field[0]);
		
		//$('#id_header_tools_cal_value').attr('value',cookie_date);
		//$('#id_header_tools_cal_alt').attr('value',cookie_date_gui);
		
		
	}
	
	
});


/*
 * Pasted from the jquery mobile development section. Above section actually directly from the old frontdesk.js file.
 * 
 */


$('#id_frontdesk_page').live('pageshow',function(event, ui){
	
	/*
	 * This event will execute when we create this page.
	 */
	
	//Reset the col width of the hidden frontdesk table header.
	$('#id_frontdesk_page').bind("orientationchange pageshow",function(){
		
		//console.log("Re-sorting the td widths ...");
		//$("#id_hidden_header").width($("#fdtable").width())
		
		header = $('#fdtable thead tr td');
		hidden_header = $('#id_hidden_header thead tr td');
		col_length = header.length;
				
		for(i = 0; i < col_length; i++){
			//Update hidden_header col width by taking values from current active col. 
			$(hidden_header[i]).width($(header[i]).width());
		}
		
	});
	
	
	/*
	 * Get the List of event_to_attribute list, via ajax, this will be used 
	 * when we click each event, the form will popup with correspondng attributes,
	 * as its form fields.
	 */
	
	if(client == undefined){
		//Open Stomp clinet. global scope.
		client = new STOMPClient();
		
		client.onopen = function(){
				//quit_handlers(client);
		};
		
		client.onclose = function(c){
			//Alert User about the connection intteruption
			//alert("You are logged out from the server...");
			//Try to reconect when the connection is failed.This might happen when there is any network or
			// communication problems.
			//var cookie = $.cookie(SESSION_COOKIE_NAME);
			//client.connect(HOST,STOMP_PORT,USERNAME,cookie);
		};
		
		client.onerror = function(error){
			//Alert the Problem while establishing connection with stomp server.
			alert('An Error ocurred' + error);
		};
		
		client.onerrorframe = function(frame){
			//Alert the error frame details.
			//alert("Frame Error:"+ frame.body);
		};
		
		client.onconnectedframe = function(){
			//Here we subscribe the stomp queue channel.
			client.subscribe(CHANNEL_NAME);
			
		};
		
		client.onmessageframe = function(frame){
			//We got a updated frame from queue.
			//Check frame header and body to decide what to do with this frame.
			var msg = JSON.parse(frame.body);
			
			//console.log(msg);
			
			handle_incomming_message(msg);
		};
		
		//Using jQuery cookie as the passcode to stomp server.
		
		var cookie = $.cookie(SESSION_COOKIE_NAME);
		client.connect(HOST,STOMP_PORT,USERNAME,cookie);
	}
	
	

	
	//***Function to store the table event order and use it when new patient added to the table***.
	var head_length = $('#fdtable thead td').size() - 2 ;
	//alert(head_length);
	var index = -2; //Skip two cells, serial No and Patient Name.
	
	$($.mobile.activePage).find('div[data-role="content"] thead td').each(function(){
		
		//console.log(this);
		
		if(index >= 0){
			event_map[index] =  $('b',this).html().toLowerCase();
		}
		
		index ++;
	});
	
	//console.log(event_map);
	/*
	 * When we show frontdesk page, we adjusting the view by rebinding the table layout fixing.
	 */
	
	//console.log('Pageshow: Adjusting... frontdesk UI');
	
	
	var table_body_scroll = function(div){
		
		/*
		 * Function which helps to maintain the table header in constant position when we scroll. 
		 * Here we using the onscroll event to implement this logic.
		 */
		
		//console.log("scrolling..." + div);
		//console.log("Horizontal: " + div.srcElement.scrollLeft + "Vertical: " + div.srcElement.scrollTop);
		
		//console.log(div);
		var width = $('#id_hidden_header').width();
		
		if(div.srcElement.scrollTop > 0){
			
			$('#id_hidden_header').width(width);
			$('#id_hidden_header').show();
						
		}
		else{
			$('#id_hidden_header').hide();
	
		}
	}
	
	//console.log($("div[data-role='content']:visible"));
	$("div[data-role='content']:visible").bind('scrollstart',table_body_scroll);
		
	/*
	 * Event attribute related configurations are given here.
	 */
	var map_url = '/GetFullEventAttrMap/';
	var data = {'clinicID': clinicID};
	
	$.ajax({
		
		url : map_url,
		type : 'GET',
		datatype: 'json',
		data: data,
		success: function(msg){
			
			//alert("Got full attr list of this clinic..." + msg);
			
			//Set All attribute-to-event map here.
			EventAttrMap = msg;
		}
		
	});
	
	//console.log('Page show event..');

});

$('#id_frontdesk_page').live('pagebeforehide',function(event,ui){
	//This event will be triggered justbefore we navigate away from current page.
	$('.hasDatepicker').hide();
	//console.log("testing...");
});


/*
//When we navigate to another page we close the connection with server.
$('#id_frontdesk_page').live('pagehide',function(event,ui){
	
	//console.log("Pagehide: Closing the stomp connection..");
	
	if(client != undefined){
		console.log("Disconnecting the stomp connection");
		client.disconnect();
		
		//re-assigning the client object to 'undefined' object.
		client = undefined;
	}
	
	//Removing the Oriantation binding.
	//$(window).unbind("orientationchange resize pageshow");
	
});

*/

