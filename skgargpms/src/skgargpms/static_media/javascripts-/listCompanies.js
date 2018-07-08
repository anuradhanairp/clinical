function products_form_new(){
   $("#productName").val("");
   $("#productDate").val("");
   products_form_expand(); 

}


function product_info_get(){
        info["product"] = new Array();
        info["product"]["commit"] = "Create";
        info["product"]["actionID"] = 0;
	info["product"]["count"] = 0; 
       products_form_contract();
        var fi = new Array();
        fi["companyID"] = companyID;
$.ajax({
   type: "GET",
   url: "/companies/listCompanies.xml",
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    var count = 0;
    $(xml).find("product").each(function(){
    var $marker = $(this);
    info["product"][count] = new Array();
    info["product"][count]["name"] = outputString($marker.find("name").text());
    info["product"][count]["date_launched"] = $marker.find("date-launched").text();
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
   info["product"]["commit"]= "Update";
   info["product"]["actionID"] = maker["id"];
   products_form_expand();
}


function product_form_delete(count){
   fi = new Array();
   fi["id"] =  info["product"][count]["id"];
$.ajax({
   type: "GET",
   url: "productDelete.php",
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    var count = 0;
    product_info_get();

}
});
}


function products_form_save(){
	products_form_contract();
	
	var fi = new Array(); 
	fi["product[date_launched]"] = $('#productDate').val();
	fi["product[name]"] = $('#productName').val();
	fi["commit"]="Create";
	printArray(fi);

        fi["personnel[company_id]"]=companyID;
        fi["commit"]=commit;
        if(commit == "Update"){
             fi["id"] = id;
        }

        $.ajax({
        type: "POST",
        url: "people.php",
        data: returnStringArray(fi),
        datatype: "xml",
        success: function(xml){
        alert(xml);

        people_info_get();
        }});

	
	
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

        outString += "<a href=\"javascript:product_form_delete("+count+");\"><img src=\"css/blueprint/plugins/buttons/icons/deleteitem.png\" /></a><a href=\"javascript:product_form_update("+count+");\"><img src=\"css/blueprint/plugins/buttons/icons/pencil.png\" /></a>";

        }
        outString +="<br>";
        outString += "Date Launched: " + marker["date_launched"] + "<br>";
        outString += "<br><br></li>";
        count += 1;

});
outString += "</ul>";

if (info["product"]["count"]==0){
outString = "No products have been entered for this company yet.";
}

$("#products_info").html(outString);
}

