




function basic_info_get(){

        basic_form_contract();
	//        showCompanyView();
        var fi = new Array();
       
$.ajax({
   type: "GET",
   url: urlProcess("/companies/"+companyID+".xml"),
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    //alert(xml);
    info["company"]["name"] =  outputString($("name",xml).text());
    info["company"]["description"] =  outputString($("description",xml).text());
    info["company"]["employee-number"] =  $("employee-number",xml).text();
    info["company"]["enabled"] =  $("enabled",xml).text();
    info["company"]["founded"] =  $("founded",xml).text();
    info["company"]["private-notes"] =  outputString($("private-notes",xml).text());
    info["company"]["url"] =  urlStyle(outputString($("url",xml).text()));
    basic_info_update();
    if (admin) basic_form_update(); 
        }
   });


}

function basic_info_update(){
 $("#companyNameI").text(info["company"]["name"]);
 $("#companyDescriptionI").text(info["company"]["description"]);
 $("#companyEmployeeNumberI").text(info["company"]["employee-number"]);
 // radio button
 if (info["company"]["enabled"] == "true") $('#companyEnabledI').text("Enabled"); 
 else $('#companyEnabledI').text("Disabled");
 $("#companyFoundedI").text(checkDate(dateNice(info["company"]["founded"])));
 $("#companyURLI").html('<a href=http://'+info["company"]["url"]+'>'+info["company"]["url"]+'</a>');
 $("#companyPrivateNotesI").text(info["company"]["private-notes"]);
// $("#companyUrlI").text(info["company"]["url"]);
 
}

function basic_form_update(){
 $("#companyName").val(info["company"]["name"]);
 $("#companyDescription").val(info["company"]["description"]);
 $("#companyEmployeeNumber").val(info["company"]["employee-number"]);
 $("#companyEnabled").val(info["company"]["enabled"]);
 $("#companyFounded").val(info["company"]["founded"]);
 $("#companyPrivateNotes").val(info["company"]["private-notes"]);
  $("#companyURL").val(info["company"]["url"]);
// $("#companyUrl").text(info[["company"]"description"]);


}
