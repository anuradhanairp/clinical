//Extra Admin javascript.

$(document).ready(function(){
	
	//alert("from the extra javascript at admin header...");
	
	//Admin Event Design page binding..
	$('#id_delete_button').click(delete_row);
	
	$('#id_add_button').click(add_new_row);
	
	$('#id_submit_button').click(submit_clinic_map);
	
});

function delete_row(){
	//alert("from delete function");
	
	//From this we get the selected row from the table.
	$('#id_event_table tbody tr').filter(':has(:checkbox:checked)').each(function(){
		
		//Get value from the checkbox input tag.
		//alert($('input',this.cells[0]).val());
		
		row_id = $('input',this.cells[0]).val();
		$("#"+row_id).remove();
		//alert(row_id);
			
	});
	
	//Reorder the tables to avoid the same id field for rows and give unique number.
	
	var total_rows = $('#id_event_table > tbody tr').length;
	var rows = 0;
	var old_td_fields = new Array();
	
	
	$('#id_event_table > tbody tr ').each(function(){
		
		if(rows < total_rows){
	
			//Get exact option tag from the select tag.
			old_td_fields[rows ++] = $(this).find("select").html();
			//this.cells[1].innerHTML = "<b>" + rows ++ + "</b>";
			//alert(this.innerHTML);
		}
	});
	
	//alert(old_td_fields[0]);
	
	//Remove all rows from table body.
	$('#id_event_table tbody tr').remove();
	
	for(rows=0; rows<total_rows; rows++){
		//alert(old_td_fields[rows]);
		newRow = '<tr id=event' + (rows + 1) + '>';
		
		newRow += '<td> <input type="checkbox" name="event' + (rows + 1) + '"  value="event' + (rows + 1) + '"/>';
		
		newRow += '<td><b>' + (rows +1) + '</b></td>';
		newRow += '<td><select id="id_event'+ ( rows +1 ) + '_name" name="id_event'+ ( rows +1 ) + '_name">';
		newRow += old_td_fields[rows];
		newRow += '</select></tr>';
		//alert(newRow);
		//Add Fresh row.
		$('#id_event_table tbody').append(newRow);
	}
}

function add_new_row(){
	//alert("from Add new row function...");
	total_rows = $('#id_event_table tbody tr').size();

	if(total_rows > 0 ){
		
		total_rows ++;
		
		create_new_row(total_rows);
		//alert(total_rows);
		//alert(newRow);
		//event_name_list.replace("selected","");
		//alert(event_name_list);
		//alert(total_rows);
	}
	

}

function create_new_row(row_count){
	//General function where it will create row with proper id for row.It manage intermediate delete operation.
	newRow = '<tr id=event' + total_rows + '>';
	newRow += '<td> <input type="checkbox" value="event' + total_rows + '" name="event' + total_rows + '"  />';
	newRow += '<td><b>' + total_rows + '</b></td>';
	newRow += '<td><select id="id_event'+ total_rows + '_name" name="id_event'+ total_rows + '_name" >';
	
	
	$('#id_event' + (total_rows -1) + '_name option').each(function(){
		
		newRow += '<option value="' + this.value + '">' + this.value + '</option>' 
		//alert(this.value);
		
	});
	
	newRow += '</select></tr>'
	$('#id_event_table tbody').append(newRow);
	
}

function submit_clinic_map(){
	//alert("Submit function");
	
	if( $('#id_event_table tbody tr').size() == 0 ){
		alert("You can't submit without any mapping please refresh.");
		return false;
	
	}
	
	else{
		//Collect all the required parameters and pass it to server via ajax and json.(Our faviourate one here.)
		
		//alert("Processing form data.");
		clinicID = $('#clinicID').val();
		//row_length = $('#id_event_table tbody tr').size();
		
		var form_data = $('#id_event_form').serialize();
		//events = new Array();
		
		//alert("form_data: "+form_data);
		
		//for(i=0; i < row_length; i++){
			//events[i] = $('#id_event' + (i+1) + '_name').val();
			//alert($('#id_event' + (i+1) + '_name').val());
		//}
		
		//alert(events[4]);
		//var new_events = events.join('%')
		//var data = {'clinicID':clinicID,'events':form_data};
		//data = JSON.stringify(data);
		
		var url =  '/admin/design_clinics/' + clinicID + '/update/'
		
		$.ajax({
			url  : url,
			data : form_data,
			datatype : 'json',
			type : 'POST',
			success : function(msg){
				
				$('#id_status').hide().html("<span style=\"color:green\"><b>Successfully changed the event mapping..</b> </span>").fadeIn();
				
				//alert("successfully updated the server: " + msg.status);
				
			} 
			
		});

	}
		
	
	return false ;
}