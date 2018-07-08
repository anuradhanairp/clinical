/*
 * Special JS functions that intercept the JQM default URL and page change functions, via that
 * we can inject our own code snippets and hooks or bypass the page loading functions.
 */

$(document).ready(function(){
	
	// Some utility functions used with here.
	
	var destroy_stomp_client = function(){
		
		//clinet is an global variable
		if(client != undefined ){
			client.disconnect();
		}
		
		client = undefined;
		
		//console.log("stompp connection destroied by URL intercepter...");
			
	};
	
	
	
	$(document).bind("pagebeforechange",function(e , data){
		
		//When page change initiated, before changing the page controll will come here with new paeget url.
		
		//Check for the URL, where its an internal page or actual URL
		if(typeof data.toPage == "string"){
			//We are being asked to load a page by url, but we only want to intercept particular ,
			//set of urls.
			var url = $.mobile.path.parseUrl(data.toPage);
			//console.log(url);
			
			//Going to Main page of the app.
			if(url.pathname == '/jqmtab/'){
				destroy_stomp_client();
				//console.log("naviagting to the main page...");
				//update the url, to remove the hash url representations.
				//console.log(url);
			}
			
			
			//Going to Report page.
			if (url.pathname == '/jqmtab/reports/'){
				destroy_stomp_client();
				//console.log("naviagating to the report page");
			}
			
			//Going to Payment Page.
			if(url.pathname == '/jqmtab/payment/'){
				destroy_stomp_client();
				//console.log("navigating to the payment page..");
			}
			
			//Going to the Logout Page.
			if(url.pathname == '/jqmtab/logout/'){
				destroy_stomp_client();
				//console.log("navigating to the logout page..");
			}
			
			//Going to the Signin page.
			if(url.pathname == '/jqmtab/signin/'){
				destroy_stomp_client();
				//console.log("navigating to the singin page...");
			}
			
			/*
			if(client != undefined ){
				console.log('stompp client is now active: '+ client);
			}else{
				console.log("stompp client isn't active now");
			}
			*/
			
		}
		
		//console.log('testing..');
		
	});
});


