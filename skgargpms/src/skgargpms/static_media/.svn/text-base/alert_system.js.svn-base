//Javascript functions required to manage the alert system GUI and ajax operations.
/*
 * We are taking jquery plugin from django admin module, so we need on change here to
 * get the usual jQuery funcality.
 */

$ = django.jQuery

$(document).ready(function(){
	
	$('#id_location_list').change(location_changed);
	$('#id_clinic_list').change(clinic_changed);
});



function location_changed(){
	
	var location_id = $('#id_location_list').val()
	
	
	//alert('Hello'  + location_id);
	
	$.ajax({
				url: '/fetchClinics/',
				method: 'POST',
				dataType: 'json',
				data: {'location_id': location_id},
				success: function(clinic_list){
					
					//alert("clinic list received.." + clinic_list);
					
					$('#id_clinic_list').html('');//Clear the list.
					
					$('#id_event_list').html('');//Clear event list also.
					$('<option value="">---------</option>').appendTo('#id_clinic_list');
					
					//console.log(clinic_list);
					for(var i = 0; i < clinic_list.length; i++){

						//alert(clinic_list[i]);
						$('<option value="' + clinic_list[i][0] + '">' + clinic_list[i][1] + " : " + clinic_list[i][2] +  '</option>' ).appendTo('#id_clinic_list');
						
					}
							
				}
		
	});
}

function clinic_changed(){
	
	var clinic_id = $('#id_clinic_list').val();
	
	//alert(clinic_id);
	$.ajax({
			
		url: '/fetchEventMap/',
		method: 'POST',
		dataType: 'json',
		data: {'clinic_id':clinic_id},
		success: function(eventMap){
			
			//alert(eventMap);
			
			$('#id_event_list').html('');
			
			var new_html = '';
			
			for(var i =0; i < eventMap.length ; i++){
				
				var html =  "<input type='checkbox' name='event_names' value='" + eventMap[i] + "'> " + capitaliseFirstLetter(eventMap[i]) + "&nbsp&nbsp&nbsp"  ;
				
				new_html += html;
						
			}
			
			$('#id_event_list').html(new_html);
			
		}
		
	});
	
}

function capitaliseFirstLetter(string)
{
    return string.charAt(0).toUpperCase() + string.slice(1);
}


function save_alert_conf(){
	
	
	var email_regx=/^([0-9a-zA-Z]+([_.-]?[0-9a-zA-Z]+)*@[0-9a-zA-Z]+[0-9,a-z,A-Z,.,-]*\.[a-zA-Z]{2,4},)*?[0-9a-zA-Z]+([_.-]?[0-9a-zA-Z]+)*@[0-9a-zA-Z]+[0-9,a-z,A-Z,.,-]*\.[a-zA-Z]{2,4}$/;
	
	var clinic_id  = $('#id_clinic_list').val();
	
	//alert('clinic_id' + clinic_id);
	
	var location_id = $('#id_location_list').val();
	//alert('location_id' + location_id);
	var name = $('#id_name').val();
	
	if(name == ''){
		alert("Name is required Field ..");
		return false;
	}
	
	//alert('name' + name );
	
	var enabled = $('#id_enabled').val();
	
	//alert('enabled'+ enabled);
			
	
	var from_addr = $('#id_from_addr').val();
	
	var flag = email_regx.exec(from_addr);
	
	if ( !flag ){
	
		alert('From: Email address isn\'t valid ..');
		return false;
	}
	
		
	
	//alert('fromadd'+ from_addr);
	
	var to_addr = $('#id_to_addr').val();
	
	
	var flag = email_regx.exec(to_addr);
	
	if ( !flag ){
		
		alert('To: Email address isn\'t valid ..');
		return false;
	}
	
	
	
	//alert('to_addr: '+ to_addr);
	
	
	var eventMap = new Array();
	
	var flag = 0;
	
	$('#id_event_list :checkbox:checked').each(function(){
		
		eventMap.push($(this).val());
		flag ++;
		//alert($(this).val());
		
	});
	
	
	if(flag == 0){
		alert('Select Minimum One Event ...');
		return false;
	}
	
	var waiting_time = $('#id_waiting_time').val();
	
	if(isNaN(parseInt(waiting_time)) ){
		alert('Please input Integer to Waiting Time Field ... ');
		return false;
	}
	
	var alert_retry = $('#id_alert_retry').val();
	
	if(isNaN(parseInt(alert_retry))){
		alert('Please input an Integer to the Alert retry box');
		return false;
	}
	//alert(eventMap);
	
	var alert_interv = $('#id_alert_interv').val();
	
	if(isNaN(parseInt(alert_interv))){
		alert('Please input an Integer to the Alert retry box');
		return false;
	}
	
	return true;
	
}


function save_user()
{
	var uname = $('#id_username').val();
	var password = $('#id_password1').val();
	var staff_status = $('#id_is_staff:checked').val();
	var super_status = $('#id_is_superuser:checked').val();
	
	if(staff_status == "on")
	{
		var staff = "True";
	}	
	if(staff_status == undefined) 
	{
		var staff = "False";
			
	}
	if(super_status == "on")
	{
		var superstat = "True";
	}	
	if(super_status == undefined) 
	{
		var superstat = "False";
			
	}
	
	
	$.ajax({
		url: '/save_new_user/',
		method: 'POST',
		data: {'uname':uname,'password':password,'staff':staff,'superstat':superstat},
		success: function(data){
						
                     
		}
	});
}
