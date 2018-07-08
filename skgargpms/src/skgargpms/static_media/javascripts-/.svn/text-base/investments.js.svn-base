


function investment_info_get(){
        info["investment"] = new Array();
        info["investment"]["commit"] = "Create";
        info["investment"]["actionID"] = 0;
        info["investment"]["count"] = 0;
       people_form_contract();
        var fi = new Array();
        fi["companyID"] = companyID;
$.ajax({
   type: "GET",
   url: urlProcess("/investments/find_by_company/?company_id="+companyID),
   datatype: "xml",
   success: function(xml){
    var count = 0;
    
    var outputStr = "";
    
    var bTitled = false; 
    $(xml).find("angel").each(function(){
    var $marker = $(this);
    if (!bTitled){
	   bTitled = true; 	
	   outputStr += "Angel<br/>";
	} 
    info["investment"][count] = new Array();
    info["investment"][count]["funding_type"] = $marker.find("funding-type").text();
    info["investment"][count]["funding_date"] = $marker.find("funding-date").text();
    info["investment"][count]["agency"] = $marker.find("agency").text();
    info["investment"][count]["funding_amount"] = $marker.find("funding-amount").text();
    info["investment"][count]["id"] = $marker.find("id").text();

    info["investment"][count]["count"] = count;
    
	outputStr += stringOutput(info["investment"][count]);
	count += 1;
    });
 
	var bTitled = false; 
    $(xml).find("seed").each(function(){
    var $marker = $(this);
    if (!bTitled){
	   bTitled = true; 	
	   outputStr += "Seed<br/>";
	} 
    info["investment"][count] = new Array();
    info["investment"][count]["funding_type"] = $marker.find("funding-type").text();
    info["investment"][count]["funding_date"] = $marker.find("funding-date").text();
    info["investment"][count]["agency"] = $marker.find("agency").text();
    info["investment"][count]["funding_amount"] = $marker.find("funding-amount").text();
    info["investment"][count]["id"] = $marker.find("id").text();

    info["investment"][count]["count"] = count;
   
	outputStr += stringOutput(info["investment"][count]);
	count += 1;
    });

	var bTitled = false; 
    $(xml).find("seriesa").each(function(){
    var $marker = $(this);
    if (!bTitled){
	   bTitled = true; 	
	   outputStr += "Series A<br/>";
	} 
    info["investment"][count] = new Array();
    info["investment"][count]["funding_type"] = $marker.find("funding-type").text();
    info["investment"][count]["funding_date"] = $marker.find("funding-date").text();
    info["investment"][count]["agency"] = $marker.find("agency").text();
    info["investment"][count]["funding_amount"] = $marker.find("funding-amount").text();
    info["investment"][count]["id"] = $marker.find("id").text();

    info["investment"][count]["count"] = count;
   
	outputStr += stringOutput(info["investment"][count]);
	count += 1;
    });
    
 	var bTitled = false; 
    $(xml).find("seriesb").each(function(){
    var $marker = $(this);
    if (!bTitled){
	   bTitled = true; 	
	   outputStr += "Series B<br/>";
	} 
    info["investment"][count] = new Array();
    info["investment"][count]["funding_type"] = $marker.find("funding-type").text();
    info["investment"][count]["funding_date"] = $marker.find("funding-date").text();
    info["investment"][count]["agency"] = $marker.find("agency").text();
    info["investment"][count]["funding_amount"] = $marker.find("funding-amount").text();
    info["investment"][count]["id"] = $marker.find("id").text();

    info["investment"][count]["count"] = count;
   
	outputStr += stringOutput(info["investment"][count]);
	count += 1;
    });
    
    
	var bTitled = false; 
    $(xml).find("seriesc").each(function(){
    var $marker = $(this);
    if (!bTitled){
	   bTitled = true; 	
	   outputStr += "Series C<br/>";
	} 
    info["investment"][count] = new Array();
    info["investment"][count]["funding_type"] = $marker.find("funding-type").text();
    info["investment"][count]["funding_date"] = $marker.find("funding-date").text();
    info["investment"][count]["agency"] = $marker.find("agency").text();
    info["investment"][count]["funding_amount"] = $marker.find("funding-amount").text();
    info["investment"][count]["id"] = $marker.find("id").text();

    info["investment"][count]["count"] = count;
   
	outputStr += stringOutput(info["investment"][count]);
	count += 1;
    });
    
	var bTitled = false; 
    $(xml).find("seriesd").each(function(){
    var $marker = $(this);
    if (!bTitled){
	   bTitled = true; 	
	   outputStr += "Series D<br/>";
	} 
    info["investment"][count] = new Array();
    info["investment"][count]["funding_type"] = $marker.find("funding-type").text();
    info["investment"][count]["funding_date"] = $marker.find("funding-date").text();
    info["investment"][count]["agency"] = $marker.find("agency").text();
    info["investment"][count]["funding_amount"] = $marker.find("funding-amount").text();
    info["investment"][count]["id"] = $marker.find("id").text();

    info["investment"][count]["count"] = count;
   
	outputStr += stringOutput(info["investment"][count]);
	count += 1;
    });
    
	var bTitled = false; 
    $(xml).find("seriese").each(function(){
    var $marker = $(this);
    if (!bTitled){
	   bTitled = true; 	
	   outputStr += "Series E<br/>";
	} 
    info["investment"][count] = new Array();
    info["investment"][count]["funding_type"] = $marker.find("funding-type").text();
    info["investment"][count]["funding_date"] = $marker.find("funding-date").text();
    info["investment"][count]["agency"] = $marker.find("agency").text();
    info["investment"][count]["funding_amount"] = $marker.find("funding-amount").text();
    info["investment"][count]["id"] = $marker.find("id").text();

    info["investment"][count]["count"] = count;
   
	outputStr += stringOutput(info["investment"][count]);
	count += 1;
    });
    
	var bTitled = false; 
    $(xml).find("seriesf").each(function(){
    var $marker = $(this);
    if (!bTitled){
	   bTitled = true; 	
	   outputStr += "Series F<br/>";
	} 
    info["investment"][count] = new Array();
    info["investment"][count]["funding_type"] = $marker.find("funding-type").text();
    info["investment"][count]["funding_date"] = $marker.find("funding-date").text();
    info["investment"][count]["agency"] = $marker.find("agency").text();
    info["investment"][count]["funding_amount"] = $marker.find("funding-amount").text();
    info["investment"][count]["id"] = $marker.find("id").text();

    info["investment"][count]["count"] = count;
   
	outputStr += stringOutput(info["investment"][count]);
	count += 1;
    });

	var bTitled = false; 
    $(xml).find("seriesg").each(function(){
    var $marker = $(this);
    if (!bTitled){
	   bTitled = true; 	
	   outputStr += "Series G<br/>";
	} 
    info["investment"][count] = new Array();
    info["investment"][count]["funding_type"] = $marker.find("funding-type").text();
    info["investment"][count]["funding_date"] = $marker.find("funding-date").text();
    info["investment"][count]["agency"] = $marker.find("agency").text();
    info["investment"][count]["funding_amount"] = $marker.find("funding-amount").text();
    info["investment"][count]["id"] = $marker.find("id").text();

    info["investment"][count]["count"] = count;
   
	outputStr += stringOutput(info["investment"][count]);
	count += 1;
    });

	var bTitled = false; 
    $(xml).find("purchased").each(function(){
    var $marker = $(this);
    if (!bTitled){
	   bTitled = true; 	
	   outputStr += "Purchased<br/>";
	} 
    info["investment"][count] = new Array();
    info["investment"][count]["funding_type"] = $marker.find("funding-type").text();
    info["investment"][count]["funding_date"] = $marker.find("funding-date").text();
    info["investment"][count]["agency"] = $marker.find("agency").text();
    info["investment"][count]["funding_amount"] = $marker.find("funding-amount").text();
    info["investment"][count]["id"] = $marker.find("id").text();

    info["investment"][count]["count"] = count;
   
	outputStr += stringOutput(info["investment"][count]);
	count += 1;
    });
    
    	var bTitled = false; 
    $(xml).find("ipo").each(function(){
    var $marker = $(this);
    if (!bTitled){
	   bTitled = true; 	
	   outputStr += "IPO<br/>";
	} 
    info["investment"][count] = new Array();
    info["investment"][count]["funding_type"] = $marker.find("funding-type").text();
    info["investment"][count]["funding_date"] = $marker.find("funding-date").text();
    info["investment"][count]["agency"] = $marker.find("agency").text();
    info["investment"][count]["funding_amount"] = $marker.find("funding-amount").text();
    info["investment"][count]["id"] = $marker.find("id").text();

    info["investment"][count]["count"] = count;
   
	outputStr += stringOutput(info["investment"][count]);
	count += 1;
    });
    
    
    investment_info_update2(outputStr);
    
    
    info["investment"]["count"] = count;

 //   investment_info_update();

}
});


}


function stringOutput(inputArry){
	
//var inputArry = info["investement"][count];
outputStr = "";

	
outputStr += "<ul>";	
outputStr += "<li>Investors: " + inputArry["agency"] + "</li>";
var count = inputArry["count"];
if (admin){
  outputStr += "<a href=\"javascript:investment_form_delete("+count+");\"><img src=\"/images/icons/deleteitem.png\" /></a><a href=\"javascript:investment_form_update("+count+");\"><img src=\"/images/icons/pencil.png\" /></a>";
}
outputStr += "<li>Funding Date: " + checkDate(dateNice(inputArry["funding_date"])) + "</li>";
outputStr += "<li>Funding Amount: " + amountInput(inputArry["funding_amount"]) + "</li>";
outputStr += "</ul>";		
return outputStr; 
}

function investments_form_new(){
	
	
   $("#investmentAgency").val("");
   $("#investmentFundingAmount").val("");
   $("#investmentDate").val("");

   investments_form_expand(); 

}


function amountInput(input){
if (input.length < 4) input = "$"+input+" thousand"
else if (input.length < 7){ 
	var out = "$"+input.substring(0,input.length - 3);
	if(input.substring(input.length - 3, input.length - 2) != "0") out += "."+ input.substring(input.length - 3, input.length -2);
	out += " million";
	input = out;
}
else if (input.length < 10){

	var out = "$"+input.substring(0,input.length - 6);
	if(input.substring(input.length - 6, input.length - 5) != "0") out += "."+ input.substring(input.length - 6, input.length - 5);
	out += " billion";
	input = out;

}
else {
		var out = "$"+input.substring(0,input.length - 9);
	if(input.substring(input.length - 9, input.length - 8) != "0") out += "."+ input.substring(input.length - 9, input.length - 8);
	out += " trillion";
	input = out;

}

return input; 
}

function investment_info_update2(inputStr){
$("#investments_info").html(inputStr);	
	
}


function investment_info_update(){
var outString = "<ul>";
var count = 0;
$(info["investment"]).each(function(){
        var marker = info["investment"][count];
        outString += "<li>Agency: " + marker["agency"];
        if (admin){
        outString += "<a href=\"javascript:investment_form_delete("+count+");\"><img src=\"/images/icons/deleteitem.png\" /></a><a href=\"javascript:investment_form_update("+count+");\"><img src=\"/images/icons/pencil.png\" /></a>";
        }
        outString +="<br>";
        outString += "Funding Date: " + marker["funding_date"] + "<br>";
        outString += "Funding Amount: " + marker["funding_amount"] + "<br>";
        outString += "Funding Type: " + marker["funding_type"] + "<br>";
        outString += "<br><br></li>";
        count += 1;

});
outString += "</ul>";

if (info["investment"]["count"]==0){
outString = "No investments have been entered for this company yet.";
}

$("#investments_info").html(outString);
}

