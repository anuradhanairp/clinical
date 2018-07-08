

function table_body_scroll(div){
	
	/*
	 * Function which helps to maintain the table header in constant position when we scroll. 
	 * Here we using the onscroll event to implement this logic.
	 */
	
	//console.log("scrolling..." + div);
	
	//console.log("Horizontal: " + div.scrollLeft + "Vertical: " + div.scrollTop);
	
	if(div.scrollTop > 0){
		$('#table_head').show();
		//console.log("show...");
	}
	else{
		$('#table_head').hide();
	}
}


function get_cell_order(msg){
	//Function which helps to print the Event times based on the table Event order changes.

	//alert(event_map[0]);
	//alert(msg.patient[event_map[0]]);
	var imgurl="/static/index_htm_files/loader.white.gif";
	var length = event_map.length; 
	
	var tableString = '';
	
	for(i = 0; i < length; i++){
		
		tableString += "<td align=center width=150px height:50px>";
		   
	    if( msg.patient[event_map[i]] != undefined){
	    	tableString += msg.patient[event_map[i]]; 
	    }
	    else{
	    	tableString += 	"<div id='loading_" + msg.headerID + "_" + event_map[i] + "' align='center' style='display:none;width:25px;height:25px'><img src='"+imgurl+"' alt='loading..' style='width: 20px; height: 10px;' /></div> <button id='button_" + msg.headerID + "_" + event_map[i] + "' style='width:25px;height:25px' onClick='wait(\""+ event_map[i] +"\",\""+ msg.headerID +"\");'>X</button>";
	    	//tableString += 	"<div id='loading_" + msg.headerID + "_" + event_map[i] + "' class=\'loading\'>loading</div> <button id='button_" + msg.headerID + "_" + event_map[i] + "' onClick='wait(\""+ event_map[i] +"\",\""+ msg.headerID +"\");'>X</button>";
	    }
	    tableString += "</td>";
	}
	
	//alert(tableString);
	
	return tableString;
	
	
    
}

// We can use this same table construction for the comet based implementation also.
function updateTable(msg,new_row){
	
	if (new_row == false ){
		
		//Take the current row count from .'new_row' is false when we update a particular row in frontdesk table.'new_row' is true when we add a new row to the frontdesk table as part of signin process
		row_number = $('#count'+ msg.headerID +' td:first').html();
	}
	else{
		
		//Adding new row to the frontdesk, thead will be an extra row count at any time.
		row_number = $('#fdtable tr').length;
		
	}
	
    var tableString = "";
    tableString += '<tr id="count'+ msg.headerID +'">';
    
    tableString += "<td align=center><b>"+ row_number +'</b></td> <td align=center><a href="javascript:void(0)" onclick="displayDialog(\''+msg.headerID+'\')">'+  msg.patient.name +"</a></td>";
    
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
	
	//alert("seding evens to sever");
	msg = {'type':'eventlog','headerID':headerID,'event':event};
	msg = JSON.stringify(msg);
	client.send(msg,CHANNEL_NAME);
    
	
}



function generate_pdf(){
    var current_date = $('#id_header_tools_cal_value').val();
    
    
    //alert(current_date);
    
    var ifr = document.getElementById('id_download_iframe');
    try{
	if(!ifr){
	    $('body').append('<iframe id="id_download_iframe" width="1" height="1" frameborder="0" name="download_iframe"></iframe>');
	    ifr = document.getElementById('id_download_iframe');
	}
	
	//console.log(ifr);
	var url ="/pdf/?type=frontdesk&date="+escape(current_date)+"&clinicID="+clinicID;
	window.open(url);
	// alert(current_date);
    } catch (x) {
	console.log(x);
    }
}




function quit_handlers(client){
	
	window.onbeforeunload = function(){
		//Properly disconnect the stomp server connection.
		client.disconnect();
		//Check the logout part for the tage "id" value.
		//$("#logout").animate({opacity:1.0},1000);
	};
	
	$(window).unload(function(){
		//do some thing when unloading.
		
		
	});
}


function handle_event_update(message){
	//Update patient table when an operator click on the frontdesk button. message is a json data from server.
	//alert(message.patient.signin);
	
	if (message.response == 'False'){
		
		if(message.from == USERNAME){
			//Only sent the warning to event originator.
			//alert("Warnning: First assign Provider to this Patient..");
			alert(message.reason);
			
			
			var alert_msg = message.reason;
			//alert(a);
			//alert(message.headerID);
			//alert(message.event);
			//alert(a.indexOf('Interrupts'))
			
			if (alert_msg.indexOf('Interrupts') > -1)
			{
			   displayDialog(message.headerID);
			   $( "#tabs" ).tabs( "option", "selected", 3);
			}  
			else if(message.event == "provider")
			{	
			   displayDialog(message.headerID);
			   if (alert_msg.indexOf('Interrupts') > -1)
				{
				   displayDialog(message.headerID);
				   $( "#tabs" ).tabs( "option", "selected", 3);
				}
			   else{
				   $( "#tabs" ).tabs( "option", "selected", 1);
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
	}
	
}

function handle_new_signin(msg){
	//Update the new patient login at frontdesk.
	if (msg.response == 'OK') {
		new_row = true;
		//alert("got new update.");
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
        	  //alert('updating tabel..');
              updateTable(msg,new_row);
        	}
	}

}

//Function which accept message frame from the Stomp queue and do corresponding actions.
function handle_incomming_message(message){
	
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

//Javascript start here.
$(document).ready(function(){
	
				/*
				 * Get the List of event_to_attribute list, via ajax, this will be used 
				 * when we click each event, the form will popup with correspondng attributes,
				 * as its form fields.
				 */

	
    			itemList = new Array();
    			itemData = new Array();  
	
    			initDisplayDialog();
    			
    			//Open Stomp clinet.
    			client = new STOMPClient();
    			
    			client.onopen = function(){
    				quit_handlers(client);
    			};
    			
    			client.onclose = function(c){
    				//Alert User about the connection intteruption
    				//alert("You are logged out from the server...");
    				
    				//Try to reconect when the connection is failed.This might happen when there is any network or
    				// communication problems.
    				var cookie = $.cookie(SESSION_COOKIE_NAME);
        			client.connect(HOST,STOMP_PORT,USERNAME,cookie);
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
    				//console.log(frame);
    				var msg = JSON.parse(frame.body);
    				//alert(frame.body);
    				
    				handle_incomming_message(msg);
    			};
    			
    			//Using jQuery cookie as the passcode to stomp server.
    			
    			var cookie = $.cookie(SESSION_COOKIE_NAME);
    			client.connect(HOST,STOMP_PORT,USERNAME,cookie);
    			
    			
    			$('#id_header_tools_pdf').click(generate_pdf);
    			
    			//Disabled the Ajax pulling for comet based implementations.
    			//updateRoutine();
    			//setInterval( updateRoutine, RESPONSE_REFRESH );
    			
    			
    			//***Function to store the table event order and use it when new patient added to the table***.
    			var head_length = $('#fdtable thead td').size() - 2 ;
    			//alert(head_length);
    			var index = -2; //Skip two cells, serial No and Patient Name.
    			
    			$('#fdtable thead td').each(function(){
    				//alert("test");
    				
    				if(index >= 0){
    					//alert("test");
    					event_map[index] =  $('b',this).html().toLowerCase();
    					//alert($('b',this).html().toLowerCase());
    				}
    				index ++;
    			});
    			//alert(event_map.length + "first element:" + event_map[0]);
    			
    			//Bind the calender 
    			
    			//$('#id_header_tools_cal').unbind('click').click(get_calender_date());
    			//get_calender_date(dateText);
    			
    			
    		  }

);


