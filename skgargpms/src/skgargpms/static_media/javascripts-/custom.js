var admin = false; 
var host = ""; 
var info = new Array();
var companyID = 0;
info["company"] = new Array(); 
info["people"] = new Array();
info["partnership"] = new Array();
info["product"] = new Array();
info["keyword"] = new Array();
info["investment"] = new Array();
info["partnership"]["commit"] = "Create";
info["partnership"]["actionID"] = 0;
info["product"]["actionID"] = 0;
info["product"]["commit"] = "Create";
info["investment"]["commit"] = "Create";
info["investment"]["actionID"] = 0;
info["people"]["commit"] = "Create";
info["people"]["actionID"] = 0;


function inputString(item){
if(item != undefined){
    item = item.replace("=",",,,,,,,,,,");
    item = item.replace("'","......");
    item = item.replace('"',".....");
	return item.replace("&",",,,,,");
}
}

function outputString(item){
if (item != undefined){
    item = item.replace(",,,,,,,,,,","=");
    item = item.replace("......","'");
    item = item.replace(".....",'"');
	return item.replace(",,,,,","&");

}
}

 function urlStyle(item){
if(item != undefined){
    item = item.toLowerCase(); 
 	item = item.replace("http://","");
 	item = item.replace("https://","");
 	return item;
 }
}

function xmlStyle(item){
	if(!notUrlKey)  item = "draft-"+item; 
	return item
}

function checkDate(item){
	if(item == undefined) return "";
	else return item; 
}


function printArray(arr){
for(var i in arr) {
	var value = arr[i];
	alert("("+i +") "+ value);
}
}

function dateNice(input){
	var inputArry = input.split("-");
	return monthConvert(inputArry[1]) + " " + inputArry[0];
}


function monthConvert(input){

	if(input == "01") input = "January";
	else if(input == "02") input = "February";
	else if(input == "03") input = "March";
	else if(input == "04") input = "April";
	else if(input == "05") input = "May";
	else if(input == "06") input = "June";
	else if(input == "07") input = "July";
	else if(input == "08") input = "August";
	else if(input == "09") input = "Semptember";
	else if(input == "10") input = "October";
	else if(input == "11") input = "November";
	else if(input == "12") input = "December";
	return input;
}


var notUrlKey = true; 
function urlProcess(input){
	if(!notUrlKey) input = "/draft_" + input.substr(1); 
	return input 
}


function createCompanyView(){
$('#products_div').hide();
$('#partnerships_div').hide();
$('#investments_div').hide();
$('#people_div').hide();
$('#keywords_div').hide();
$('#internal_div').hide();
$('#basic_info').hide();
$('#control_div').hide();
}

function showCompanyView(){

$('#products_div').show();
$('#partnerships_div').show();
$('#investments_div').show();
$('#people_div').show();
$('#keywords_div').show();
$('#internal_div').show();
$('#basic_info').show();
$('#control_div').show();

$('#products_form').hide();
$('#partnerships_form').hide();
$('#investments_form').hide();
$('#people_form').hide();
$('#keywords_form').hide();
$('#internal_form').hide();
$('#singleVideo_form').hide();
$('#basic_form').hide()

$('#products_div').show();
$('#partnerships_div').show();
$('#investments_div').show();
$('#people_div').show();
$('#keywords_div').show();
$('#internal_div').show();
$('#basic_info').show();
$('#control_div').show();

$('#products_info').show();
$('#partnerships_info').show();
$('#investments_info').show();
$('#people_info').show();
$('#keywords_info').show();
$('#internal_info').show();
$('#basic_info').show()

people_info_get();
product_info_get();
partnership_info_get();
investment_info_get();
companyCategory_info_get();
}

info["categoryNames"] = new Array();










