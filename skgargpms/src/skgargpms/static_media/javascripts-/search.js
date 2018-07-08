
var host = ""; 
var info = new Array();
info["company"] = new Array(); 
var searchFile = "";



function search_info_get(cID){

        //        showCompanyView();
        var fi = new Array();
        
$.ajax({
   type: "GET",
   url: "/companies/"+cID+".xml",
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    var index = info["company"].push(new Array) - 1; 
    info["company"][index]["name"] =  $("name",xml).text();
    info["company"][index]["description"] =  $("description",xml).text();
    info["company"][index]["employee-number"] =  $("employee-number",xml).text();
    info["company"][index]["enabled"] =  $("enabled",xml).text();
    info["company"][index]["founded"] =  $("founded",xml).text();
    info["company"][index]["private-notes"] =  $("private-notes",xml).text();
    info["company"][index]["url"] =  $("url",xml).text();
    info["company"][index]["id"] = $("id",xml).text();
    search_info_update();
   }
});


}



var activeCats = new Array();
var availCats = new Array(); 
var catName = new Array(); 
var companyList = new Array();


function searchCategory_info_get(){
   $("#updatingResults").hide();

	catName = new Array();
        var fi = new Array();
$.ajax({
   type: "GET",
   url: "/categories.xml",
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    var count = 0;
    $(xml).find("category").each(function(){
    var $marker = $(this);
    catName[String($marker.find("id").text())] = String($marker.find("name").text());
    count += 1;

    });

}
});
}


function updateSelectedCats(){

      var reqStr = "";
      var count = 0;
      $.each(activeCats,function(item,item2){
      
                if(item2 != undefined){
                    			if(activeCats[item2] != undefined){
                	if (count != 0){
                    	    reqStr += ", ";
                	}
               // availCats.splice(availCats.indexOf(item2,1));
                	reqStr += "<span><a href=# onclick=\"javascript:removeActiveCat('"+item2+"')\">"+catName[item2]+"</a></span>";
                	count += 1;
                }
                }
});


	if(reqStr.length == 0){
	
		reqStr = "<p class=\"nobottommargin\" align=\"center\"><br><br>No Selected Categories</p>";
	
	}
	else reqStr += "<br><br><p class=\"nobottommargin\" align=\"center\">(Click tags to remove filters)</p>";
     
    reqStr = "<fieldset><legend>Selected Categories</legend>" + reqStr;
    
    reqStr += "</fieldset>"; 




  	$("#activeCats").html(reqStr);



}

function updateAvailableCats(){
     
      var reqStr = "";
      var count = 0;
      $.each(availCats,function(item,item2){
      		if(item2 != undefined){
      			if(activeCats[item2] == undefined){
      		
                if (count != 0){
                        reqStr += ", ";
                }
                reqStr += "<span><a href=# onclick=\"javascript:addActiveCat('"+item2+"')\">"+catName[item2]+"</a></span>";
                count += 1;
             
             }
            }
		});


	if(reqStr.length == 0){
	
		reqStr = "<p class=\"nobottommargin\" align=\"center\" >No Available Categories</p>";
	
	}
	else reqStr += "<br><br><p class=\"nobottommargin\" align=\"center\">(Click tags to filter results)</p>";
     
    reqStr = "<fieldset><legend>Available Categories</legend>" + reqStr;
    
    reqStr += "</fieldset>"; 
  	$("#availCats").html(reqStr);



}




function addActiveCat(id){
   activeCats[id] = id;
   updateSelectedCats();
   updateAvailableCats();
 //  availCats.splice(availCats.indexOf(id,1));
	dosearch();
}


function removeActiveCat(id){
    activeCats[id] = undefined; 
    updateSelectedCats();
    
   updateAvailableCats();
	dosearch();
}




function returnStringArray(arr){
        var sOutput = "";
        for(var i in arr) {
                var value = arr[i];
                sOutput += i + "="+value+"&";
        }
        return sOutput.replace(/%5B%5D/g, '[]');
}


function searchPress(){
	activeCats = new Array();
	dosearch();
		
}

var searchResults = ""; 


            function unique(arrayName)
            {
                var newArray=new Array();
                label:for(var i=0; i<arrayName.length;i++ )
                {  
                    for(var j=0; j<newArray.length;j++ )
                    {
                        if(newArray[j]==arrayName[i]) 
                            continue label;
                        if(arrayName[i] == undefined)
                        	continue label; 
                    }
                    newArray[newArray.length] = arrayName[i];
                }
                return newArray;
            }


	info["company"] = new Array();

var compCatTracker = new Array();
var boolSetCCT = false; 

function setCCT(){
	if(!boolSetCCT){
		boolSetCCT = true; 
		compCatTracker = new Array();
	}
}


function hideResults(){
 $("#resultsInfo").hide();
    $("#catSec").hide();
   $("#updatingResults").show();


}

function showResults(){
   $("#updatingResults").hide();
 $("#resultsInfo").show();
    $("#catSec").show();


}

var searchUrl = "";

function dosearch(){
      hideResults(); 
	 
      var reqStr = "";
      var count = 0;
      $.each(activeCats,function(i,item){
      if(item != undefined){
		if (count != 0){
			reqStr += ",";
		}
		reqStr += item; 
		count += 1;
		}
});

        var fi = new Array();

	searchResults = "";
        //        showCompanyView();
        var fi = new Array();
        fi["q"] = $("#search").val();
        	fi["categoryList"] = reqStr;
            var reqStr = "";
      var count = 0;
      $.each(companyList,function(i,item){
      if(item != undefined){
		if (count != 0){
			reqStr += ",";
		}
		reqStr += item; 
		count += 1;
		}
});
        	
        	fi["companyList"] =  reqStr;
$.ajax({
   type: "GET",
   url: searchUrl,
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
   companyList = new Array();
   availCats = new Array();
   var foundResults = false;
    $(xml).find("company").each(function(){
    setCCT();
   	foundResults = true;
	var marker = $(this);
   	var id = marker.find("id").text();
   	//alert(id);
   	var index = info["company"][id] = new Array();
   
	info["company"][id]["name"] =  marker.find("name").text();
    info["company"][id]["description"] =  marker.find("description").text();
    info["company"][id]["employee-number"] =  marker.find("employee-number").text();
    info["company"][id]["enabled"] =  marker.find("enabled").text();
    info["company"][id]["founded"] =  marker.find("founded").text();
    info["company"][id]["private-notes"] =  marker.find("private-notes").text();
    info["company"][id]["url"] =  marker.find("url").text();
    info["company"][id]["id"] = marker.find("id").text();
  	companyList[id] = id;
  	compCatTracker[id] = new Array();

   });
 

   if(foundResults){
   		  $(xml).find("company-category").each(function(){
	var marker = $(this);
	var companyID = marker.find("company-id").text();
	var categoryID = marker.find("category-id").text();
	if (companyID in companyCategories){
	}
	else {
		companyCategories[companyID] = new Array(); 
		}
	
	companyCategories[String(companyID)][(String(categoryID))]=String(categoryID);
   });	                  
   }
   
  $(xml).find("company-category").each(function(){
  	 var marker = $(this);
  	 var categoryID = marker.find("category-id").text();
  	 var companyID = marker.find("company-id").text();
  	 compCatTracker[companyID][categoryID] = categoryID; 
  
  });
  
  
  $(xml).find("category-id").each(function(){
	var marker = $(this);
	if (activeCats[marker.text()] == undefined){
	if (availCats[marker.text()] == undefined){
	  availCats[(marker.text())]=marker.text();

	}
	}
   });
  if(!foundResults){	
      companyList = new Array();
	  $(xml).find("company-id").each(function(){
	var marker = $(this);
	var allCatsMatch = true; 
	$.each(activeCats, function(i, key){
	if (key != undefined){
		 if (activeCats[key] != undefined){
			if (compCatTracker[marker.text()][key] == undefined){
				allCatsMatch = false; 
			}
		 }
		}
	});
	if (allCatsMatch){
	companyList[marker.text()]=marker.text();
	}
	$.each(companyCategories[String(marker.text())], function(i, item){
	    if(item != undefined){
	    availCats[(String(item))]=String(item);
	
		}
	});


        });  

	
	$.each(companyList,function(i3,item3){
		var okaySearchInfo = true; 
		if(item3 == undefined){
			okaySearchInfo = false; 
		}
		else{
	    $.each(activeCats,function(i4,item4){
	    	//alert(i4);
	    	//alert(companyCategories[item]);
	    	if((item4 == undefined)){
	    	   // alert("here3");
	    		//okaySearchInfo = false; 
	    	}
	    	else{
	         	if(companyCategories[item3] == undefined){
	         		//okaySearchInfo = false; 
	         	//	alert("here2");
	        	}
	        	else{	
	         	 	if(companyCategories[item3][item4] == undefined){
	     	    //	  alert("here");
	     	    // condition i really want to checkn --skg
	        	      okaySearchInfo = false;
	          	   }
	        	}
	        }
	    });
	   }
		if (okaySearchInfo){
	
		 	foundResults = true;
	    }
	
	});
	
        
    }

search_info_update();
availCats = unique(availCats); 
updateSelectedCats();
updateAvailableCats();

  if(!foundResults){
	$("#resultsInfo").html("<p align='center'>No results found.</p>");
}
  showResults();
  
}
});
        
}

var companyCategories = new Array();


function search_info_update(){
var outString = ""; 
 $(companyList).each(function(i,value){ 
if(companyList[value] != undefined){
if(companyList[value]["id"] == undefined){
 //alert(value);
 //alert(companyList[value]);
}
//printArray(info["company"][i]);
outString += "<div class=\" span-13\"><span class=\"largeTop\"><a href=\"/companies/";
outString +=info["company"][value]["id"]+"\">";

outString +=info["company"][value]["name"];
outString += "</a></span><br><label>Description: </label>"+ info["company"][value]["description"]+"<br><br></div>";
//alert(outString);
// $("#companyUrlI").text(info["company"]["url"]);
}
});
//alert(outString);
$("#resultsInfo").html(outString);
}


