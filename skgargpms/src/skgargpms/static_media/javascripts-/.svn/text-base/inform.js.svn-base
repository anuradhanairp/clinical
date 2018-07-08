function product_form_save(){
        products_form_contract();
	 var urlStr = "/products/create";
        var fi = new Array();
        fi["product[name]"] = inputString($('#productName').val());
        fi["product[date_launched]"] = $('#productDate').val();
		fi["product[description]"] = $('#productDescription').val();
	fi["product[company_id]"]=companyID;
        var commit = info["product"]["commit"];
        //fi["commit"]=commit;
        if(commit == "Update"){
			fi["_method"] = "put";
			fi["id"] = info["product"]["actionID"];
			urlStr="/products/update";
//             fi["product[id]"] = info["product"]["actionID"];
        }
       
       
        $.ajax({
        type: "POST",
        url: urlProcess(urlStr),
        data: returnStringArray(fi),
        datatype: "xml",
        success: function(xml){

        product_info_get();
        }});
        info["product"]["commit"] = "Create";
        info["product"]["actionID"] = 0;
}

function people_form_save(){
	people_form_contract();
	var urlStr = "/personnels/create";
	var fi = new Array(); 
	fi["personnel[first_name]"] = $('#personnelFirstName').val();
	fi["personnel[last_name]"] = $('#personnelLastName').val();
	fi["personnel[email]"] = $('#personnelEmail').val();
	fi["personnel[current_title]"]=$('#personnelCurrentTitle').val();
	fi["personnel[previous_title]"]=$('#personnelPreviousTitle').val();
	fi["personnel[grad_edu]"] = $('#personnelGradEdu').val();
	fi["personnel[undergrad_edu]"] = $('#personnelUndergraduateEdu').val();
	fi["personnel[other_edu]"]=$('#personnelOtherEdu').val();
	fi["personnel[founder]"]=$("input[name='ftype']:checked").val();
	fi["personnel[company_id]"]=companyID;
	var commit = info["people"]["commit"];

        if(commit == "Update"){
			 fi["_method"] = "put";
			 	    urlStr = "/personnels/update";
             fi["id"] = info["people"]["actionID"];
        }  

	$.ajax({
   	type: "POST",
   	url: urlProcess(urlStr),
   	data: returnStringArray(fi),
   	datatype: "xml",
   	success: function(xml){
	
    	people_info_get();
        }});
	info["people"]["commit"] = "Create";
	info["people"]["actionID"] = 0;
}

function people_form_delete(count){
   fi = new Array();
   fi["id"] =  info["people"][count]["id"];
$.ajax({
   type: "GET",
   url: urlProcess("/personnels/destroy_item"),
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    var count = 0;
    people_info_get();

}
});
}


function categories_form_save(){
        categories_form_contract();
		var urlStr = "/categories/create";
        var fi = new Array();
        fi["category[name]"] = $('#categoryName').val();
        
        fi["commit"]=commit;
        if(commit == "Update"){
			 var urlStr = "/categories/update";
             fi["id"] = info["category"]["actionID"];
        }

        $.ajax({
        type: "POST",
        url: urlProcess(urlStr),
        data: returnStringArray(fi),
        datatype: "xml",
        success: function(xml){
	
        categories_info_get();
        }});
        info["category"]["commit"] = "Create";
        info["category"]["actionID"] = 0;
}

function categories_form_delete(count){
   fi = new Array();
   fi["id"] =  info["category"][count]["id"];
$.ajax({
   type: "GET",
   url: urlProcess("/categories/destroy_item"),
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    var count = 0;
    categories_info_get();

}
});
}

function categories_form_expand(){
   $("#categoryName").val("");

	$('#categories_form').slideDown('slow');
	$('#categories_info').slideUp('fast');
}


function categories_form_update(count){
   var maker = info["category"][count];
   $("#categoryName").val(maker["name"]);
   info["category"]["commit"]= "Update";
   info["category"]["actionID"] = maker["id"];
   categories_form_expand();
}


function basic_form_save(){
	
	basic_form_contract();
	showCompanyView();
	var fi = new Array(); 
	var urlStr = "/companies/create";
	fi["format"] = "xml";
	fi["company[name]"] = inputString($('#companyName').val());
	fi["company[employee_number]"] = $('#companyEmployeeNumber').val();
	fi["company[description]"]=inputString($('#companyDescription').val());
	fi["company[founded]"]=$('#companyFoundeddate').val();
	fi["company[enabled]"]=$("input[name='pdisplay']:checked").val();
	fi["company[url]"]=$('#companyURL').val();
	fi["company[private_notes]"] = inputString($('#companyPrivateNotes').val());
	if (info["company"]["commit"] == "Create"){
	fi["commit"]="Create";
	}
	else{
	var urlStr = "/companies/update";
	fi["_method"]="put";
	fi["id"] = companyID;
	}

$.ajax({
   type: "POST",
   url: urlProcess(urlStr),
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
     if (info["company"]["commit"] == "Create"){
     companyID = $("id",xml).text();
}
     info["company"]["commit"] = "Update";
    showCompanyView();
    basic_info_get();
	}});
}



function basic_form_cancel(){
	basic_form_contract();
}



function internal_form_save(){
	basic_form_save();
	internal_form_contract();

}

function internal_form_cancel(){
	internal_form_contract();
}





function companyCategoryCreate(categoryID){
        keywords_form_contract();

        var fi = new Array();
        fi["company_category[company_id"] = companyID;
        fi["company_category[category_id"] = categoryID;

        var commit = "Create";
        

        $.ajax({
        type: "POST",
        url: urlProcess("/company_categories/create"),
        data: returnStringArray(fi),
        datatype: "xml",
        success: function(xml){

        companyCategory_info_get();
        }});
}

function companyCategoryDelete(id){

        var fi = new Array();
        fi["id"] = id;

        $.ajax({
        type: "GET",
        url: urlProcess("/company_categories/destroy_item"),
        data: returnStringArray(fi),
        datatype: "xml",
        success: function(xml){
	companyCategory_info_get();

        }});
}

function keywords_form_save(){
var fi = new Array();
fi["checked"] = "";
fi["unchecked"] = "";
fi["companyID"] = companyID;
var count = 0;
var sCount = 0;
$(info["category"]).each(function(){
	 

     var marker = info["category"][count];
  
    if($("#cc"+marker["id"]).is(':checked')){
	 fi["checked"] += marker["id"] + ",";
	companyCategoryCreate(marker["id"]);
	sCount += 1;
      }
      else{
	 fi["unchecked"] += marker["id"] + ",";
	 if(idChecked[marker["id"]] == "exists") companyCategoryDelete(idInfo[marker["id"]]);

      	// companyCategoryDelete(marker["id"]);
      }
	count += 1;	
});
    if(sCount == 0){
        $("#keywords_info").text("No categories have been entered for this company yet.");
         }



	keywords_form_contract();
}

function keywords_form_cancel(){
	keywords_form_contract();
}

function investments_form_save(){
	investments_form_contract();
	
	var fi = new Array(); 
	fi["investment[agency]"] = $('#investmentAgency').val();
	fi["investment[funding_date]"] = $('#investmentDate').val();
	fi["investment[funding_type]"]=$("input[name='itype']:checked").val();
	fi["investment[funding_amount]"]=$('#investmentFundingAmount').val();
	
}

function investments_form_cancel(){
	investments_form_contract();
}



function investment_form_save(){
        investments_form_contract();
		var urlStr = "/investments/create";
        var fi = new Array();
        fi["investment[agency]"] = $('#investmentAgency').val();
        fi["investment[funding_date]"] = $('#investmentDate').val();
        fi["investment[funding_type]"]=$("input[name='itype']:checked").val();
        fi["investment[funding_amount]"]=$('#investmentFundingAmount').val();
	fi["investment[company_id]"] = companyID;
	var commit = info["investment"]["commit"];
        fi["commit"]=commit;
        if(commit == "Update"){
			 
             fi["id"] = info["investment"]["actionID"];
             urlStr = "/investments/update/"+fi["id"];
        }

        $.ajax({
        type: "POST",
        url: urlProcess(urlStr),
        data: returnStringArray(fi),
        datatype: "xml",
        success: function(xml){

        investment_info_get();
        }});
        info["investment"]["commit"] = "Create";
        info["investment"]["actionID"] = 0;
}


function investment_form_update(count){
   var maker = info["investment"][count];
   $("#itype").val(maker["funding_type"]);
   $("#investmentDate").val(maker["funding_date"]);
   $("#investmentAgency").val(maker["agency"]);
   $("#investmentFundingAmount").val(maker["funding_amount"]);


   info["investment"]["commit"]= "Update";
   info["investment"]["actionID"] = maker["id"];
   investments_form_expand();
}



function partnership_form_update(count){
   var maker = info["partnership"][count];
   $("#partnershipDescription").val(maker["name"]);
   $("#partnershipDate").val(maker["date"]);
   info["partnership"]["commit"]= "Update";
   info["partnership"]["actionID"] = maker["id"];
   partnerships_form_expand();
}





function partnerships_form_cancel(){
	partnerships_form_contract();
}



function partnerships_form_save(){
        partnerships_form_contract();
		var urlStr = "/partnerships/create";
        var fi = new Array();
        fi["partnership[description]"] = $('#partnershipDescription').val();
        fi["partnership[date]"] = $('#partnershipDate').val();
        fi["partnership[company_id]"]=companyID;
        var commit = info["partnership"]["commit"];
        //fi["commit"]=commit;
        if(commit == "Update"){
			 urlStr = "/partnerships/update";
             fi["id"] = info["partnership"]["actionID"];
             fi["_method"] = "put";
        }

        $.ajax({
        type: "POST",
        url: urlProcess(urlStr),
        data: returnStringArray(fi),
        datatype: "xml",
        success: function(xml){

        partnership_info_get();
        }});
        info["partnership"]["commit"] = "Create";
        info["partnership"]["actionID"] = 0;
}

function product_form_delete(count){
   fi = new Array();
   fi["id"] =  info["product"][count]["id"];
$.ajax({
   type: "GET",
   url: urlProcess("/products/destroy_item"),
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    
    product_info_get();

}
});
}

function partnership_form_delete(count){
   fi = new Array();
   fi["id"] =  info["partnership"][count]["id"];
$.ajax({
   type: "GET",
   url: urlProcess("/partnerships/destroy_item"),
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    
    partnership_info_get();

}
});
}


function partnerships_form_new(){
	
   $("#partnershipDescription").val("");
   $("#partnershipDate").val("");
	partnerships_form_expand(); 

}




function investment_form_delete(count){
   fi = new Array();
   fi["id"] =  info["investment"][count]["id"];
$.ajax({
   type: "GET",
   url: urlProcess("/investments/destroy_item"),
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    var count = 0;
    investment_info_get();

}
});
}
