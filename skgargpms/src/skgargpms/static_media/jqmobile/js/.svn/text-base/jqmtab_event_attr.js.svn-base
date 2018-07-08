//* JS elements required manage the Event based form.

function AttrForm(event_name,headerID){
	/*
	 * Accept attribute list of a event and generate the html form with these attributes as its fields. 
	*/
	
	attr_list = EventAttrMap[event_name];
	
	
	var flag = false;
	var attr_form = '<form action="" method="POST" id="id_attr_form">';
	attr_form += '<input type="hidden" name="headerID" id="id_headerID" value="'+ headerID +'" />';
	attr_form += '<input type="hidden" name="event_name" id="id_event_name" value="'+ event_name +'" />';
	
	var attr_row = '';
	for( index in attr_list ){
		
		flag = true;
		
		if(attr_list[index].mapID != undefined){
			
			//Main row div
			attr_row = "<div id='field" + attr_list[index].mapID + "' data-role='fieldcontain'>";
			
			//Check for this field is hidden or not.
			
			if(attr_list[index].hidden){

				//Put that Field here in hidden input format, and now we adding a dummy value.
				attr_row += "<input type='hidden' value='dummy' id='id_attr_name" + attr_list[index].mapID + "' name='attr_name" + attr_list[index].mapID + "'/>"
				
			}else{
				
				// Label the attr name
				attr_row += "<label  for='id_attr_name"+ attr_list[index].mapID +"'>" + attr_list[index].attr_name + "</label>";
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
	
	attr_form += "<input type='button' onClick='return CommitAttrForm(\"" + event_name + "\"," + headerID + ")' value='Save' />";
	
	attr_form += "</form>";
	//console.log("form constructed....");
	
	if(flag == true){
		return attr_form;
		
	}else{
		return false;
	}
	
}


function startEventForm(event_name,headerID){
	/*
	 * Handle the Button click on the event button,
	 * And also bind the event with 
	 */ 
	
	//Generating dynamic attribute form.
	var html_form = AttrForm(event_name,headerID)
	
	if (html_form != false){
		
		$('#id_attr_content').html('');
		$('#id_attr_content').html(html_form);

		//Refresh the added content by enhancing the page style using this stmt.
		$('#id_attr_form').trigger("create");
		
		//Change current page to show the event attr form.
		$.mobile.changePage($('#id_attr_page'),{ transition:"pop",changeHash: false,});
		
	}
	else{
		
		sendEvent(event_name,headerID);
	}
	
}

function hideEventForm(){
	
	//Flag reset.
	event_form_window = false;
	
	$('#event_form_base').fadeOut(100);
	$('#event_form_content').fadeOut(100);
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
		
		//Specific parameters for the jqmtab
		form_data += '&jqmtab=' + 'YES&event_name=' + event_name ;
		//console.log(form_data);
		
		
		//Show the loading image.
		$.mobile.showPageLoadingMsg();
		
		$.ajax({
			
			url: '/SubmitAttrForm/',
			data: form_data,
			datatype: 'json',
			type: 'GET',
			success: function(msg){
				//Successfully saved the attributes in the server.
				//Proceed with the sendEvent operation after hiding the attr form.
				
				//console.log(msg);
				//sendEvent(event_name,headerID);
				if( msg.status == 'OK'){
					//We send this url from backend to reduce the complexity.
					$.mobile.changePage(msg.clinic_url,{transition: "pop"});
				}
			}
			
		}); 
		
	}else{
		//Do nothing...
		//console.log('Validation faild...');
	}
	return false;
	
}