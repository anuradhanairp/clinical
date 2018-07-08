




function CBrowse_updateSelectedCats(){

      var reqStr = "";
      var count = 0;
      $.each(activeCats,function(item,item2){
      
                if(item2 != undefined){
                    			if(activeCats[item2] != undefined){
                	if (count != 0){
                    	    reqStr += ", ";
                	}
               // availCats.splice(availCats.indexOf(item2,1));
                	reqStr += "<span><a href=# onclick=\"javascript:CBrowse_removeActiveCat('"+item2+"')\">"+catName[item2]+"</a></span>";
                	count += 1;
                }
                }
});


	if(reqStr.length == 0){
	
		reqStr = "<p class=\"nobottommargin\" align=\"center\"><br><br>No Selected Segments</p>";
	
	}
	else reqStr += "<br><br><p class=\"nobottommargin\" align=\"center\">(Click tags to remove filters)</p>";
     
    reqStr = "<fieldset><legend>Selected Segments</legend>" + reqStr;
    
    reqStr += "</fieldset>"; 




  	$("#activeCats").html(reqStr);



}

function CBrowse_updateAvailableCats(){
     
      var reqStr = "";
      var count = 0;
      $.each(availCats,function(item,item2){
      		if(item2 != undefined){
      			if(activeCats[item2] == undefined){
      		
                if (count != 0){
                        reqStr += ", ";
                }
                reqStr += "<span><a href=# onclick=\"javascript:CBrowse_addActiveCat('"+item2+"')\">"+catName[item2]+"</a></span>";
                count += 1;
             
             }
            }
		});


	if(reqStr.length == 0){
	
		reqStr = "<p class=\"nobottommargin\" align=\"center\" >No Available Segments</p>";
	
	}
	else reqStr += "<br><br><p class=\"nobottommargin\" align=\"center\">(Click tags to filter results)</p>";
     
    reqStr = "<fieldset><legend>Available Segments</legend>" + reqStr;
    
    reqStr += "</fieldset>"; 
  	$("#availCats").html(reqStr);



}




function CBrowse_addActiveCat(id){
   activeCats[id] = id;
   CBrowse=updateSelectedCats();
   CBrowse=updateAvailableCats();
 //  availCats.splice(availCats.indexOf(id,1))
   getPart2();
}


function CBrowse_removeActiveCat(id){
    activeCats[id] = undefined; 
    CBrowse_updateSelectedCats();
    
   CBrowse_updateAvailableCats()
   getPart2();
}



var part = "";
var partOp = false; 

function getPart(part2){
	activeCats = new Array();
	part = part2;
	partOp = true; 
	getPart2();
		
}




function getPart2(){
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
	if (count == 0) partOp = true; 
	if(partOp == true){
        fi["part"] = part;
	fi["val"] = "true";
	partOp = false; 
	}
	else{
	fi["val"] = "false";
	fi["part"] = part;
	}
        fi["categoryList"] = reqStr; 
    count = 0;    
    reqStr = "";
      $.each(companyList,function(i,item){
      if(item != undefined){
		if (count != 0){
			reqStr += ",";
		}
		reqStr += item; 
		count += 1;
		}	
	});        
    fi["companyList"] = reqStr;     
        
        
        
$.ajax({
   type: "GET",
   url: "/companies/find_by_start_part",
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
   	

  	info["company"][id] = new Array();  
   
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

CBrowse_info_update();
availCats = unique(availCats); 
CBrowse_updateSelectedCats();
CBrowse_updateAvailableCats();

  if(!foundResults){
	$("#resultsInfo").html("<p align='center'>No results found.</p>");
}
 //alert("hello");
 showResults(); 

}
});
        
}

var companyCategories = new Array();

function CBrowse_delete(cID){
   fi = new Array();
   fi["id"] =  cID;
$.ajax({
   type: "GET",
   url: "/companies/destroy_item",
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    getPart2();

}
});
}



function CBrowse_info_update(){
var outString = ""; 

var nameInfo = new Array(); 
var idInfo = new Array();
var alpha = new Array();

 $(companyList).each(function(i,value){ 
if(companyList[value] != undefined){

nameInfo[info["company"][value]["name"].toLowerCase()] = value;
alpha.push(info["company"][value]["name"].toLowerCase());

}
});

alpha.sort();

$(alpha).each(function(i,value){ 


idInfo.push(nameInfo[value]);

});



 $(idInfo).each(function(i,value){ 

if(companyList[value] != undefined){
if(companyList[value]["id"] == undefined){
 //alert(value);
 //alert(companyList[value]);
}
//printArray(info["company"][i]);

var enabled = info["company"][value]["enabled"];
var continueUpdate = true; 

if (enabled == "false") continueUpdate = false; 
if (admin) continueUpdate = true; 

if(continueUpdate){
outString += "<div class=\" span-4\"><span><a href=\"/companies/";
outString +=info["company"][value]["id"]+"\">";

outString +=outputString(info["company"][value]["name"]);
outString += "</a></span>";

if (admin){
	var cID = info["company"][value]["id"];

        outString += "<a href=\"javascript:CBrowse_delete("+cID+")\"><img src=\"/images/icons/deleteitem.png\" /></a>";
       


}

//</span><br><label>Description: </label>"+ info["company"][value]["description"]+"<br><br></div>";

outString += "</div>";
//alert(outString);
// $("#companyUrlI").text(info["company"]["url"]);
}
}

});
//alert(outString);
$("#resultsInfo").html(outString);
}


