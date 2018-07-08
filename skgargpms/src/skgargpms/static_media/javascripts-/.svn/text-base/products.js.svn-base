function products_form_new(){
   $("#productName").val("");
   $("#productDate").val("");
   $("#productDescription").val("");
   products_form_expand(); 

}



function product_info_get(){
        info["product"] = new Array();
        info["product"]["commit"] = "Create";
        info["product"]["actionID"] = 0;
	info["product"]["count"] = 0; 
       products_form_contract();
        var fi = new Array();
        fi["company_id"] = companyID;
$.ajax({

   url: urlProcess("/products/find_by_company"),
   datatype: "xml",
      data: returnStringArray(fi),
      type: "GET",
   success: function(xml){
    var count = 0;
    $(xml).find(xmlStyle("product")).each(function(){
    var $marker = $(this);
    info["product"][count] = new Array();
    info["product"][count]["name"] = outputString($marker.find("name").text());
    info["product"][count]["date_launched"] = $marker.find("date-launched").text();
    info["product"][count]["description"] = $marker.find("description").text();
    info["product"][count]["id"] = $marker.find("id").text();

    info["product"][count]["count"] = count;
    count += 1;

    });
    info["product"]["count"] = count;

    product_info_update();

}
});
}


function product_form_update(count){
   var maker = info["product"][count];
   $("#productName").val(maker["name"]);
   $("#productDate").val(maker["date"]);
   $("#productDescription").val(maker["description"]);
   info["product"]["commit"]= "Update";
   info["product"]["actionID"] = maker["id"];
   products_form_expand();
}





function products_form_cancel(){
	products_form_contract();
}



function product_info_update(){
var outString = "<ul>";
var count = 0;
$(info["product"]).each(function(){
        var marker = info["product"][count];
        outString += "<li>Name: " + marker["name"]; 
        if (admin){

        outString += "<a href=\"javascript:product_form_delete("+count+");\"><img src=\"/images/icons/deleteitem.png\" /></a><a href=\"javascript:product_form_update("+count+");\"><img src=\"/images/icons/pencil.png\" /></a>";

        }
        outString +="<br>";
		outString += "Description: " + marker["description"] + "<br>";
        outString += "Date Launched: " + checkDate(dateNice(marker["date_launched"])) + "<br>";
        outString += "<br><br></li>";
        count += 1;

});
outString += "</ul>";

if (info["product"]["count"]==0){
outString = "No products have been entered for this company yet.";
}

$("#products_info").html(outString);
}

