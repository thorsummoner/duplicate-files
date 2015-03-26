/* General Javascript Configuration */

$(document).ready(function(){
	$("ul.sf-menu").supersubs({ 
		minWidth:    12,
		maxWidth:    27,
		extraWidth:  1     
	}).superfish();
});


function validate(form)
{
	if( form.cfname.value == "" || form.cfemail.value == "" || form.cfmessage.value == "" ) 
   { 
	  document.getElementById('message').innerHTML = ' Fill out all fields!';
	  document.getElementById('message').style.display = 'inline';
	  return false; 
   }
}

