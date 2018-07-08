function user_list_process(){
	//Get Users specific reports.
	//alert('processing user report');
	
	user = $('#id_user_list').val();
	//console.log(user);
	
	var data = {'user':user, 'clinicID':clinicID};
	$.ajax({
			url: "/getJsonReport/",
			data: data,
			dataType: 'json',
			type: "POST",
			success: function(data){
				//msg = data.patients[0]
				if( data.user == 'default'){
					//Cleqr the fdtable data's
					$('#fdtable > tbody > tr').remove();
					$('#id_report_user').hide();
					$('#id_report_default').show();
					
					for(i=0; i< data.patients.length; i++){
						msg = data.patients[i];
						//alert(msg.headerID + msg.patient.name +': ' + data.patients.length  );
						updateTable(msg,true);
												
					}
					//alert(data.clinicID + data.user + data.patient.name + data.patient.headerID);
					//alert(data.patients[0].events.signinTregistration + data.patients.length);
				}
				
				else{
					//alert("The user is not available.");
					
					//Cleqr the fdtable data's
					$('#fdtable_user > tbody > tr').remove();
					$('#id_report_default').hide();
					$('#id_report_user').show();
					
					//alert(data.patients[0].patient.name);
					for(i=0; i < data.patients.length; i++){
						msg = data.patients[i];
						//alert(msg.headerID);
						updateTableUser(msg,true);
					}
				}
			}
	});
	
}


//Function which specifically used to update the user specific report on the report page.
function updateTableUser(msg,new_row){

	if (new_row == false ){
		
		//Take the current row count from 
		row_number = $('#count_user'+ msg.headerID +' td:first').html();
	}
	else{
		
		//Adding new row to the frontdesk, thead will be an extra row count at any time.
		row_number = $('#fdtable_user tr').length;
		
	}
	
    var tableString = "";
    tableString += '<tr id="count_user'+ msg.headerID +'">';
    
    tableString += "<td align=center><b>"+ row_number +'</b></td> <td align=center>'+ msg.patient.name + "</td>";
    
    var length = event_map_user.length;
    
    for(var j=0; j<length; j++){
    	
    	tableString += "<td align=center>";
    	if(msg.patient[event_map_user[j]] != undefined){
    		tableString += msg.patient[event_map_user[j]];
    	}
    	else{
    		tableString += 'X';
    	}
    	tableString += "</td>";
    	
    }
    
   
    tableString += "</tr>";	
    
    
    if( new_row == true){
    	//Add new two at first of tbody. If empty tbody do first, or the else part.
    	if( row_number == 1 ){
    		
    		$('#fdtable_user > tbody').append(tableString);
    	}
    	else {
    		$('#fdtable_user > tbody > tr:first').before(tableString);
    	}
    	
    }
    else{
    	//Update the row of given 'id'.
    	$('#count_user'+ msg.headerID).replaceWith(tableString); 
    }
   
} 



function updateTable(msg,new_row){
	
	if (new_row == false){
		row_count = $('#count' + msg.headerID + ' td:first').html();
		//alert(row_count + msg.headerID);
	}
	else{
		row_count = $('#fdtable tr').length;
	}
	//alert("newRow: "+ new_row + '  Number of rowsL: '+ row_count);
	var tableString = "";
    tableString += "<tr id='count"+ msg.headerID +"'>";
    tableString += "<td align=center>"+ row_count +"</td><td align=center>"+ msg.patient.name +"</td>";
    var length = event_map_dflt.length;
 
    for(var j=0; j<length; j++){
    	tableString += "<td align=center>";
    	if(msg.patient[event_map_dflt[j]] != undefined){
    		tableString += msg.patient[event_map_dflt[j]];
    	}
    	else{
    		tableString += 'X';
    	}
    	tableString += "</td>";
    	
    	
    }
    
    tableString += "</tr>";	
    
    //alert(tableString);
    
    
    if( new_row == true){
    	
    	if (row_count == 1){
    		$('#fdtable > tbody').append(tableString);
    	}
    	else{
    		$('#fdtable > tbody > tr:first').before(tableString);
    	}
    }
    else{
    	$('#count'+ msg.headerID).replaceWith(tableString); 
    }
    
    
 
} 


function handle_new_signin(msg){
	
	if($('#id_report_user').is(":visible")){
		current_user = $('#id_user_list').val();
		if(current_user == msg.from){
			new_row = true;
			updateTableUser(msg,new_row);
		}
		
	}else if($('#id_report_default').is(":visible")){
		
		if(msg.response == 'OK'){
			new_row = true;
			updateTable(msg,new_row);
		}
	}
}

function handle_new_event(msg){
			
	if(msg.response != 'False'){
		
		if($('#id_report_user').is(":visible")){
			//In the user specific report case we never delete a row, just update the delete status.
			current_user = $('#id_user_list').val();
			
			if(current_user == msg.from){
				new_row = false;
				//alert("Updating user specific report: " + msg.username );
				updateTableUser(msg,new_row);
			}
			
		}
		else if ($('#id_report_default').is(":visible")){

			if(msg != undefined && msg.patient != undefined && msg.patient['delete'] != undefined){
				$('#count' + msg.headerID ).remove();
				total_rows = $('#fdtable > tbody tr').length;
				$('#fdtable > tbody tr').each(function(){
					this.cells[0].innerHTML = total_rows --;
				});
			}
			else{
				new_row = false;
				updateTable(msg,new_row);
			}
		}
	}
}

function handle_incomming_message(msg){
	//Process the message based on its type.
	switch(msg.type){

	case "signin":
		handle_new_signin(msg);
		break;
	case "eventlog":
		handle_new_event(msg);
		break;
	}
	
	
}


function generate_pdf(){
    var current_date = $('#id_header_tools_cal_value').val();
    var ifr = document.getElementById('id_download_iframe');
    try{
	if(!ifr){
	    $('body').append('<iframe id="id_download_iframe" width="1" height="1" frameborder="0" name="download_iframe"></iframe>');
	    ifr = document.getElementById('id_download_iframe');
	}
	// console.log(ifr);
	var url ="/pdf/?type=reports&date="+escape(current_date)+"&clinicID="+clinicID;
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




$(document).ready(function(){
	
	itemList = new Array();
	itemData = new Array();  

	$('#id_header_tools_pdf').click(generate_pdf);
	
	//Open Stomp clinet.
	client = new STOMPClient();
	
	client.onopen = function(){
		quit_handlers(client);
	};
	
	client.onclose = function(){
		//You where logged out from the system. alert the user.
		var cookie = $.cookie(SESSION_COOKIE_NAME);
		client.connect(HOST,STOMP_PORT,USERNAME,cookie);
	};
	
	client.onerror = function(error){
		alert("An Error Ocurrered" + error);
	};
	
	client.onerrorframe = function(frame){
		alert("Error Frame: "+ frame.body);
	};

	client.onconnectedframe = function(){
		//Subscribe to the STOMP Queue Channel.
		client.subscribe(CHANNEL_NAME);
	};
	
	client.onmessageframe = function(frame){
		//We get Messages here. Process it over here.
		
		var msg = JSON.parse(frame.body);
		handle_incomming_message(msg);
	};
	
	//Create Cookie from Jquery.
	var cookie = $.cookie(SESSION_COOKIE_NAME);
	client.connect(HOST,STOMP_PORT,USERNAME,cookie);
	
	//updateRoutine();
	// updateRoutine();
	//setInterval( updateRoutine, RESPONSE_REFRESH );
	
	
	//Settings required to manage the generalized clininc event management.
	//***Function to store the table event order and use it when new patient added to the table***.
	
	var head_length_user = $('#fdtable_user thead td').size() - 2 ;
	
	//var head_length_user = head_length_dflt; //Same as the above count
	
	//alert(head_length_user);
	var index = -2; //Skip two cells, serial No and Patient Name.
	
	$('#fdtable_user thead td').each(function(){
		//alert("test");
		if(index >= 0){
			//alert("test");
			event_map_user[index] =  $('b',this).html().toLowerCase();
			//alert($('b',this).html());
		}
		index ++;
	});
	
	//alert(event_map_dflt.length + "first element:" + event_map_dflt[0]);
	
	//Crete mapping array for the derault eventTevent structure.
	
	for(i=0; i < head_length_user; i++){
		
		if(i < (head_length_user -1) ){
			event_map_dflt[i] = event_map_user[i] + "T" + event_map_user[i+1];
		}
		else{
			event_map_dflt[i] = event_map_user[i];
		}
		
	}
	
	//for(i=0; i< head_length_user; i++){
		//alert(event_map_dflt[i]);
	//}
	
});

