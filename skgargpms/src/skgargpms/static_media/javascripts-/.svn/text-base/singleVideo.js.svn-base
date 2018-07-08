info["single_video"] = new Array();
info["single_video"]["code"] = "nothing";
info["video"] = new Array();
function singleVideos_form_save(){
       	singleVideos_form_contract();

        var fi = new Array();
        fi["video[swf]"] = $('#videoSWF').val().replace(/&/g,",,,,,").replace("=",",,,,,,,,,,");
	fi["video[company_id]"]=companyID;
	fi["video[height]"]= $('#videoHeight').val();
	fi["video[width]"] = $('#videoWidth').val();
	fi["video[type]"] = $("input[name='vtype']:checked").val();
        var commit = info["video"]["commit"];
        fi["commit"]=commit;
        if(commit == "Update"){
             fi["id"] = info["video"]["actionID"];
        }

        $.ajax({
        type: "POST",
        url: "video.php",
        data: returnStringArray(fi),
        datatype: "xml",
        success: function(xml){

        singleVideo_info_get();
        }});
        info["video"]["commit"] = "Create";
        info["video"]["actionID"] = 0;
}

function singleVideo_info_get(){
        info["video"] = new Array();
        info["video"]["commit"] = "Create";
        info["video"]["actionID"] = 0;
        singleVideos_form_contract();
        var fi = new Array();
        fi["companyID"] = companyID;
$.ajax({
   type: "GET",
   url: "videoInfo.php",
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    var count = 0;
    
    $(xml).find("video").each(function(){
    var $marker = $(this);
    var videoID = $marker.find("videoID").text();
    var videoIDNormal = videoID;
    videoID = videoID.toLowerCase();
    //alert(videoID);
    info["video"][videoID] = new Array();
    info["video"][videoID]["swf"] = $marker.find("swf").text();
    info["video"][videoID]["thumbnail"] = $marker.find("thumbnail").text();
    info["video"][videoID]["height"] = $marker.find("height").text();
    info["video"][videoID]["width"] = $marker.find("width").text();
    info["video"][videoID]["videoID"] = videoID;
    info["video"][videoID]["id"] = $marker.find("id").text();
    info["video"][videoID]["type"] = $marker.find("type").text();

    if (info["video"][videoID]["thumbnail"] < 5) info["video"][videoID]["thumbnail"] = "http://www.health2con.com/logos/h20tv200.gif";    


    count += 1;

    });
    //alert(count);
    //alert(info["video"].length);
    singleVideo_info_update();

}
});
}


function singleVideo_form_update(videoID){
   var maker = info["video"][videoID];
   $("#videoSWF").val(maker["swf"]);
   $('#videoHeight').val(maker["height"]);
   $('#videoWidth').val(maker["width"]);
   $('#vtype').val(maker["type"]);

   info["video"]["commit"]= "Update";
   info["video"]["actionID"] = maker["id"];



   singleVideos_form_expand();
}


function singleVideo_form_delete(videoID){
   fi = new Array();
   fi["id"] =  info["video"][videoID]["id"];
$.ajax({
   type: "GET",
   url: "videoDelete.php",
   data: returnStringArray(fi),
   datatype: "xml",
   success: function(xml){
    var count = 0;
    singleVideo_info_get();

}
});
}




function HtmlDecode(text) {
 return $('<div/>').html(text).text();
}


function singleVideos_form_cancel(){
	singleVideos_form_contract();
}





function singleVideo_info_update(){
var outString = "";
var count = 0;
for(k in info["video"]){
	outString += "<span id='"+k+"_info'><a href='http://"+k+"'><img width=90 src='"+info["video"][k]["thumbnail"]+"'/></a></span>&nbsp;";	
	if(admin){
	if((k != "commit") && (k != "actionID")){ 
        outString += "<a href=\"javascript:singleVideo_form_delete('"+k+"');\"><img src=\"css/blueprint/plugins/buttons/icons/deleteitem.png\" /></a>";
//	outString += "<a href=\"javascript:singleVideo_form_update('"+k+"');\"><img src=\"css/blueprint/plugins/buttons/icons/pencil.png\" /></a>";

	}
	}

	count += 1;
}
$("#singleVideo_info").html(outString);
for(k in info["video"]){
        if((k != "commit") && (k != "actionID")){
		$('#'+k+"_info a").nyroModal();
}
}
}


