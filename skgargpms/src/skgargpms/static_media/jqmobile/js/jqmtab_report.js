/*
 * Global variables for the report related things.
 */

//To save the event order, it will used when an updated come from the server.
var event_map_dflt = new Array();
var event_map_user = new Array();



/*
 * Other utility functions for the report page.
 */

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


function updateTableDflt(msg,new_row){
	
	if (new_row == false){
		row_count = $('#count_dflt' + msg.headerID + ' td:first').html();
		//alert(row_count + msg.headerID);
	}
	else{
		row_count = $('#fdtable_dflt tr').length;
	}
	//alert("newRow: "+ new_row + '  Number of rowsL: '+ row_count);
	var tableString = "";
    tableString += "<tr id='count_dflt"+ msg.headerID +"'>";
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
    		$('#fdtable_dflt > tbody').append(tableString);
    	}
    	else{
    		$('#fdtable_dflt > tbody > tr:first').before(tableString);
    	}
    }
    else{
    	$('#count_dflt'+ msg.headerID).replaceWith(tableString); 
    }
       
 
} 






$('#id_report_page').live('pageshow',function(event){
	/*
	 * Initialize the report page by fetching datas from server.
	 */
	
	//Settings required to manage the generalized clininc event management.
	//***Function to store the table event order and use it when new patient added to the table***.
	
	//var current_date = $('#id_header_tools_cal_value').val();	
	//console.log(current_date);
	//console.log("reportpage");
	
	var url_back = $("#url_back").attr('href');
	
	if ($.cookie('current_date')!= undefined)
	{	
	
		url_back = url_back + '&date=' + $.cookie('current_date');
	}
	else
	{
		url_back = url_back ;
	}	
	
	
	$("#url_back").attr("href",url_back);
	/*$("#url_back").click(function(){
		window.location.href = url_back;
		
	});*/
	
	
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
	
	
	
	/*
	 * Bind the User selection with ajax call.
	 */
	
	var clinic_id = $("#clinic_id").val();
	$('#id_user_list').change(user_list_process);
	function user_list_process(){
		//Get Users specific reports.
		//console.log('processing user report');
		
		var user = $('#id_user_list').val();
		//console.log(user);
		
		var data = {'user':user, 'clinicID':clinic_id};
		
		//loading gif image.
		
		$.mobile.showPageLoadingMsg();
		
		$.ajax({
				url: "/getJsonReport/",
				data: data,
				dataType: 'json',
				type: "POST",
				success: function(data){
					
					//console.log(data);
					//msg = data.patients[0]
					if( data.user == 'default'){
						//Cleqr the fdtable data's
						$('#fdtable_dflt > tbody > tr').remove();
						$('#id_report_user').hide();
						$('#id_report_default').show();
						
						for(i=0; i< data.patients.length; i++){
							msg = data.patients[i];
							//alert(msg.headerID + msg.patient.name +': ' + data.patients.length  );
							updateTableDflt(msg,true);
													
						}
						//console.log(data.clinicID + data.user + data.patient.name + data.patient.headerID);
						//alert(data.patients[0].events.signinTregistration + data.patients.length);
					}
					
					else{
						//console.log("The user is not available.");
						
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
					
					$.mobile.hidePageLoadingMsg();
				}
		
		
		
		});
		
	}
	
    $("#id_header_tools_report_pdf").click(generate_pdf);
	function generate_pdf(){
		var clinic_id = $("#clinic_id").val();
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
	    try{
		
		var url ="/pdf/?type=reports&date="+escape(current_date)+"&clinicID="+clinic_id;
		window.open(url);
		// alert(current_date);
	    } catch (x) {
		console.log(x);
	    }
	}
	
});
