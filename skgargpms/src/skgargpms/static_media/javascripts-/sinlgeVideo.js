info["single_video"] = new Array();
info["single_video"]["code"] = "nothing";

function singleVideo_form_save(){
       	singleVideos_form_contract();

        var fi = new Array();
        fi["single_video[code]"] = $('#productName').val();
	fi["single_video[company_id]"]=companyID;
        var commit = info["single_video"]["commit"];
        fi["commit"]=commit;
        if(commit == "Update"){
             fi["id"] = info["single_video"]["actionID"];
        }

        $.ajax({
        type: "POST",
        url: "singleVideo.php",
        data: returnStringArray(fi),
        datatype: "xml",
        success: function(xml){

        singleVideo_info_get();
        }});
        info["single_video"]["commit"] = "Create";
        info["single_video"]["actionID"] = 0;
}

function singleVideo_info_get(){
        info["single_video"] = new Array();
        info["single_video"]["commit"] = "Create";
        info["single_video"]["actionID"] = 0;
        singleVideos_form_contract();
        var fi = new Array();
        fi["companyID"] = companyID;
$.ajax({
   type: "GET",
   url: "singleVideoInfo.php",
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    var count = 0;
    $(xml).find("single-video").each(function(){
    var $marker = $(this);
    info["single_video"] = new Array();
    info["single_video"]["code"] = $marker.find("code").text();
    info["single_video"]["id"] = $marker.find("id").text();

    count += 1;

    });

    singleVideo_info_update();

}
});
}


function singleVideo_form_update(){
   var maker = info["singleVideo"];
   $("#singleVideoCode").val(maker["code"]);
   info["singleVideoCode"]["commit"]= "Update";
   info["singleVideoCode"]["actionID"] = maker["id"];
   singleVideo_form_expand();
}


function singleVideo_form_delete(count){
   fi = new Array();
   fi["id"] =  info["singleVideo"]["id"];
$.ajax({
   type: "GET",
   url: "singleVideoDelete.php",
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    var count = 0;
    singleVideo_info_get();

}
});
}


function singleVideos_form_save(){
	singleVideos_form_contract();
	
	var fi = new Array(); 
	fi["single_video[code]"] = $('#singleVideoCode').val();
	var commit = info["single_video"]["commit"];
	printArray(fi);

        fi["single_video[company_id]"]=companyID;
   
        if(commit == "Update"){
             fi["id"] = id;
        }

        $.ajax({
        type: "POST",
        url: "singleVideo.php",
        data: returnStringArray(fi),
        datatype: "xml",
        success: function(xml){
        alert(xml);

        singleVideo_info_get();
        }});

	
	
}

function singleVideos_form_cancel(){
	singleVideos_form_contract();
}





function singleVideo_info_update(){
var outString = "<ul>";
var count = 0;

if (info["single_video"]["code"]=="nothing"){
#("#singleVideo_div").hide();

}

$("#singleVideo_info").html(info["single_video"]["code"]);
}:



