


function partnership_info_get(){
        info["partnership"] = new Array();
        info["partnership"]["commit"] = "Create";
        info["partnership"]["actionID"] = 0;
        info["partnership"]["count"] = 0;
       partnerships_form_contract();
        var fi = new Array();
        fi["company_id"] = companyID;
$.ajax({

   url: urlProcess("/partnerships/find_by_company"),
   data: returnStringArray(fi),
      type: "GET",
   datatype: "xml",
   success: function(xml){
    var count = 0;
    $(xml).find(xmlStyle("partnership")).each(function(){
    var $marker = $(this);
    info["partnership"][count] = new Array();
    info["partnership"][count]["description"] = outputString($marker.find("description").text());
    info["partnership"][count]["date"] = $marker.find("date").text();
    info["partnership"][count]["id"] = $marker.find("id").text();

    info["partnership"][count]["count"] = count;
    count += 1;

    });
    info["partnership"]["count"] = count;

    partnership_info_update();

}
});
}

function partnership_info_update(){
var outString = "<ul>";
var count = 0;
$(info["partnership"]).each(function(){
        var marker = info["partnership"][count];
        outString += "<li>" +marker["description"] + " ("+ checkDate(dateNice(marker["date"]))+")" ;
        if (admin){

        outString += "<a href=\"javascript:partnership_form_delete("+count+");\"><img src=\"/images/icons/deleteitem.png\" /></a><a href=\"javascript:partnership_form_update("+count+");\"><img src=\"/images/icons/pencil.png\" /></a>";

        }
        outString += "<br><br></li>";
        count += 1;

});
outString += "</ul>";

if (info["partnership"]["count"]==0){
outString = "No partnerships have been entered for this company yet.";
}

$("#partnerships_info").html(outString);
}

