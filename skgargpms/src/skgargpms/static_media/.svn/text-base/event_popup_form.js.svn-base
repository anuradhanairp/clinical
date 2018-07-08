/*
 * JS elements required manage the Event based form.
 * That include the components required to manage the shadow window 
 * as well as the ajax calls and all gui related operations.
 * 
 * Initialise the Global JS object which store the Event-to-Attribute map of a Clinic.
 * EventAttrMap = { 'clinicId':id, 'signin': [{'mapId':id, 'attr_name': name, 'required': true, 'hidden': false,'error_message': msg}, {},...], etc.. }
 *
 *Algorithm:-
 * 
 * 1. When we enter in to a clinic, we fetch full event-to-attribut map in JS object via ajax.
 * 2. When clicking on a  event, we first do the attribute form thing, then Event sending process.
 * 3. Attribute form will list the attributes only to clicked event, if all attributes are hidden it skip this process.
 * 4. If required and non-hidden fields are there then user need to input non-empty value and need to save it, before going to SendEvent process.
 * 5. If everything related to attribute form has been completed then we go for sendEvent process, as usual way.
 * 
 */


var EventAttrMap = {};

$(document).ready(function(){
	//initialize the popup div and its values.
	
	
	//Get the complete  EventAttributeMap from the server via ajax.
	
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

});


function startEventForm(event_name,headerID){
	
	//Close button addition..
	$('.event_form_close').bind('click',hideEventForm);
	
	//console.log(event_name + headerId);
	
	//Generating dynamic attribute form.
	var html_form = AttrForm(event_name,headerID)
	
	if (html_form != false){
		
		//flag variable..set.
		event_form_window = true;
		$('#event_form_base').fadeIn(100);
		$('#event_form_content').fadeIn(100);
		
		$('#id_attr_form_div').html(html_form);
		//sendEvent(event_name,headerId);
	}
	else{
		//No attribute is there to list for this event, so we proceed with normal processing.
		hideEventForm();
		
		//Show loading gif image.
		var loading_id = 'loading_' + headerID + '_' +event_name;
		var button_id='button_'+headerID+'_'+event_name;
		show(loading_id,button_id);
		
		
		sendEvent(event_name,headerID);
	}
	
}



function hideEventForm(){
	
	//Flag reset.
	event_form_window = false;
	
	$('#event_form_base').fadeOut(100);
	$('#event_form_content').fadeOut(100);
}



function AttrForm(event_name,headerID){
	/*
	 * Accept attribute list of a event and generate the html form with these attributes as its fields. 
	*/
	
	attr_list = EventAttrMap[event_name];
	
	
	var flag = false;
	attr_form = "<form action='' method='POST' id='id_attr_form'>";
	
	for( index in attr_list ){
		
		flag = true;
		
		if(attr_list[index].mapID != undefined){
			
			//Main row div
			attr_row = "<div id='field" + attr_list[index].mapID + "' >";
			
			//Check for this field is hidden or not.
			
			if(attr_list[index].hidden){

				//Put that Field here in hidden input format, and now we adding a dummy value.
				attr_row += "<input type='hidden' value='dummy' id='id_attr_name" + attr_list[index].mapID + "' name='attr_name" + attr_list[index].mapID + "'/>"
				
			}else{
				
				// Label the attr name
				attr_row += "<label for='id_attr_name"+ attr_list[index].mapID +"'>" + attr_list[index].attr_name + "</label>";
				attr_row += "<input type='text' id='id_attr_name" + attr_list[index].mapID + "' name='attr_name" + attr_list[index].mapID + "'/>"
				//Error msg field
				attr_row += "<div id='id_error" + attr_list[index].mapID + "'> </div>";
				
				
			}
			
			//One Complete field
			attr_row += "</div>  <br />";

			//Append this row to form.
			attr_form += attr_row;
			
		}
	}
	
	//submitt and clear button.
	//CommitAttrForm(event_name,headerID)
	
	attr_form += "<input type='submit' onClick='return CommitAttrForm(\"" + event_name + "\"," + headerID + ")' value='Save' />";
	
	//Close the form tag.
	attr_form +=  "</form>";
	
	//Submit message div.
	attr_form += "<div id='submit_message'> </div>";
	
	
	if(flag == true){
		return attr_form;
	}else{
		return false;
	}
	
}


function AttrFormValidate(event_name){
	//Validate required fields of a event-to-attribute form.
	
	//console.log('validating the form...');
	
	var valid = true;
	var attr_list = EventAttrMap[event_name];
	
	for(index in attr_list){
		if(attr_list[index].required == true){
			
			//console.log('checking .... ' + '#id_attr_name' + attr_list[index].mapID);
			
			var attr_val = $('#id_attr_name' + attr_list[index].mapID).val();
			
			if(attr_val == ''){
				//No value with this field.
				valid = false;
				var err_msg = attr_list[index].error_msg;
				$('#id_error'+ attr_list[index].mapID).html(err_msg);
			}
		}
	}
	
	return valid;
}

function CommitAttrForm(event_name,headerID){
	//After validation, submit the attribute values in to server via ajax.
	
	//console.log(event_name + headerID);
	
	var form_data = $('#id_attr_form').serialize();
	
	var valid = AttrFormValidate(event_name);
	
	if(valid == true){
		//Proceed with Form submittion ...
		//console.log('Validation completed successfully...');
		
		form_data += '&headerID=' + headerID;
		
		//console.log(form_data);
		
		
		$.ajax({
			
			url: '/SubmitAttrForm/',
			data: form_data,
			datatype: 'json',
			type: 'GET',
			success: function(msg){
				//Successfully saved the attributes in the server.
				//Proceed with the sendEvent operation after hiding the attr form.
				hideEventForm();
				
				//Show loading gif image.
				var loading_id = 'loading_' + headerID + '_' + event_name;
				var button_id='button_'+headerID+'_' + event_name;
				show(loading_id,button_id);
				
				sendEvent(event_name,headerID);
			
			}
			
		}); 
		
	}else{
		//Do nothing...
		//console.log('Validation faild...');
	}

	return false;
	
}