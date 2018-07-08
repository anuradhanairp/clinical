var current_date = null;
function updateContent(date){
    try{
	
     $.ajax(
	{
	    url:'/ajax/payment/',
	    data:{clinicID:clinicID,date:date},
	    type:"POST",
	    success:function(text){
		$('#id_payment_content').html(text);
	    },
	    error:function(rq, error,text){
		// alert(error);
	    }
	    
	}
    );
    } catch (x) {
	// akert(x);
    }
}

function generate_pdf(){
    var current_date = $('#id_header_tools_cal_value').val();
    var ifr = document.getElementById('id_download_iframe');
    try{
	if(!ifr){
	    $('body').append('<iframe id="id_download_iframe" width="1" height="1" frameborder="0" name="download_iframe"></iframe>');
	    ifr = document.getElementById('id_download_iframe');
	}
	// console.log(ifr);
	var url ="/pdf/?type=payments&date="+escape(current_date)+"&clinicID="+clinicID;
	window.open(url);
	// alert(current_date);
    } catch (x) {
	console.log(x);
    }
}


$(document).ready(
    function(){
	$('#id_header_tools_pdf').click(generate_pdf);
    }
);

