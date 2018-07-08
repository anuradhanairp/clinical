
/*
 * JS file, which hold the required js functions to manage the event attribute allocation table.
 */
$(document).ready(function(){
	
	//alert('testing');
	$('#id_event_selected').change(fetch_event_attr_map);
	$('#id_add_attr').click(add_attr_row);
	$('#id_delete_attr').click(delete_attr_row);
	$('#id_save_attr').click(save_attrs);
	
	//$('#id_save_attr').click(testfun);
	
	
})

function test_opt_args(arg1){
	
	/*var optarg = augment({
		opt1: 'Test',
		opt2:  'test22.'
	},optarg); */
	
	
	console.log("keyvalue"+arg1['v']);
	var args = {b:2, c:3 };
	for (var n in arguments[0]) { args[n] = arguments[0][n]; console.log(n); }
	
	console.log(args);
	console.log(arguments);
		
}

function testfun(){
	test_opt_args({'a':44,'b':4,'c':66});
}

function new_attr_row(args){
	//console.log(args);
	//Construct new row for the attribute table and returns it to caller.
	
	//optional arguments with default value...
	var opt_args = {'hidden':false, 'required':false};
	for (var n in arguments[0]) { opt_args[n] = arguments[0][n]; }
	
	id = opt_args['id'];
	attr_list = opt_args['attr_list'];
	hidden = opt_args['hidden'];
	required = opt_args['required'];
		
	var new_row = ' <tr id="row' + id + '">';
	new_row += '<td> <input type="checkbox" id="id_row'+ id + '" value="row'+ id +'">' + (id +1) + '</td>';
	new_row += '<td> <select id="id_attr'+ id +'" name="attr'+ id +'"> ' + attr_list + '</select></td>';
	
	if(required){
		new_row += '<td> <input type="checkbox" id="id_attr_required'+ id +'" name="attr_required'+ id +'" checked="checked"> </td>';
	}else{
		
		new_row += '<td> <input type="checkbox" id="id_attr_required'+ id +'" name="attr_required'+ id +'"> </td>';
	}
	
	if(hidden){
		new_row += '<td> <input type="checkbox" id="id_attr_hidden'+ id +'" name="attr_hidden'+ id +'" checked="checked"> </td>';
	}else{
		new_row += '<td> <input type="checkbox" id="id_attr_hidden'+ id +'" name="attr_hidden'+ id +'"> </td>';
	}
	
	new_row += '</tr>';
	
	return new_row;
}


function add_attr_row(){
	//Add new row to the table, with appending status also.
	//alert('adding attribute row...');
	
	var next_row = $('#id_attr_table tbody tr').size();
	
	if(next_row > 0 ){
		//The table is not empty, so we can reuse the previous rows event list..
		
		var attr_list = $('#id_attr' + (next_row - 1)).html().replace('selected="selected"','')
		
		var new_row = new_attr_row({'id':next_row,'attr_list':attr_list});
		
		$('#id_attr_table tbody').append(new_row);
	}
	else{
		//Table is empty, so we need to get the attribute list from the server via ajax, then update the table.
		$.ajax({
			
			url: '/fetchAttributes/',
			method: 'POST',
			dataType: 'json',
			data: {},
			success: function(attr_list){
			
				//Got new list of events...
				//alert(attr_list + attr_list.length);
				
				var attr_opt_list = '';
				for(attr in attr_list){
					attr_opt_list += '<option value="'+ attr_list[attr][1]  +'">' + attr_list[attr][0] +'</option>';
					
				}
				//console.log(attr_opt_list);
				var new_row = new_attr_row({'id':0,'attr_list':attr_opt_list});
				
				$('#id_attr_table tbody').append(new_row);
		
			}
		});
	}
	
}

function delete_attr_row(){
	//Delete selected row from the attribute table, and resort the attribute list.
	//alert('Deleteing selected row...');
	
	//delete the selected rows.
	$('#id_attr_table tbody tr').find('td:eq(0)').filter(':has(:checkbox:checked)').each(function(){
		var row_id = $('input',this).val();
		$('#' + row_id ).remove();
	});
	
	//resort the existing row..
	var total_rows = $('#id_attr_table tbody tr').size();
	
	//alert(total_rows);
	
	var updated_rows = '';
	
	row_id = 0;
	
	$('#id_attr_table tbody tr').each(function(){
		//Traverse through each current rows and build new row according to the new value.
		//console.log(this.cells[0].val() + this.cells[1].val() + this.cells[2].val() + this.cells[3].val() )
		
		
		var id = row_id++;
		var attr_list = $(this).find('td:eq(1)').find('select').html()
		
		var required  = $(this).find('td:eq(2)').filter(':has(:checkbox:checked)');
		required = ($('input',required).val() == 'on')? true: false;
		//console.log(required);

		var hidden = $(this).find('td:eq(3)').filter(':has(:checkbox:checked)');
		hidden = ($('input',hidden).val() == 'on')? true:false;
		//console.log(hidden);
		
		updated_rows += new_attr_row({'id':id,'attr_list':attr_list,'hidden':hidden, 'required':required});
	
	})
	
	//console.log(updated_rows);
	//Update the table with new rows.
	
	$('#id_attr_table tbody tr').remove();
	$('#id_attr_table tbody').append(updated_rows);

}



function save_attrs(){
	//Save Attributes of an event.
	
	var total_rows = $('#id_attr_table tbody tr').size();
	
	//if( total_rows == 0){
	//	alert('No Attribute is added ...!');
	//}
	//else{
		
		var form_data = $('#id_attr_form').serialize();
		
		form_data += '&length=' + total_rows;
		
		//alert(form_data);
		
		
		var clinic_id = $('#clinicID').val();
		post_url = '/admin/assign_attributes/' + clinic_id + '/update/';
		
		$.ajax({
				url: post_url,
				data: form_data,
				datatype: 'json',
				type: "POST",
				success: function(msg){
				    
					alert('Successfully updated the attribute list...');
			}
			
		});
	//}

}

function fetch_event_attr_map(){
	//Fetch Attribute list of correponding event under current clinic via ajax.
	//alert('Fetchin the attribute lists from the server...');
	
	var event_name = $('#id_event_selected').val();
	var clinicID = $('#clinicID').val();
	
	//console.log(event_name + clinicID);id
	
	var url = '/fetchEventAttributeMap/';
	var data = {'event_name': event_name, 'clinicID':clinicID}; 
	
	$.ajax({
			
			url : url,
			type : 'GET',
			datatype : 'json',
			data: data,
			success: function(event_attr){
				
				//update table.
				//alert(msg.length);
				
				//Initialize the attribute list.
			
				
				//Table is empty, so we need to get the attribute list from the server via ajax, then update the table.
				$.ajax({
					
					url: '/fetchAttributes/',
					method: 'POST',
					dataType: 'json',
					data: {},
					success: function(attr_list){
						
						var attr_opt_list = '';
						var new_row_set = '';
						var rows = 0;
						for(ev in event_attr){
							
							//console.log( event_attr[ev][0] + event_attr[ev][1] + event_attr[ev][2]  );
							for(attr in attr_list){
								
								if( event_attr[ev][0][0] == attr_list[attr][0] ){
									attr_opt_list += '<option value="'+ attr_list[attr][1]  +'" selected="selected">' + attr_list[attr][0] +'</option>';
								}else{
									attr_opt_list += '<option value="'+ attr_list[attr][1]  +'">' + attr_list[attr][0] +'</option>';
								}
							}
							
							new_row_set += new_attr_row({'id': rows ++, 'attr_list':attr_opt_list, 'required': event_attr[ev][1], 'hidden':event_attr[ev][2]});
							
							//reset option tag list.
							attr_opt_list = '';
						}
						
						//console.log(new_row_set);
						
						$('#id_attr_table tbody tr').remove();
						$('#id_attr_table tbody').append(new_row_set);
					}
	
				});
			}
	});
	
	
}

