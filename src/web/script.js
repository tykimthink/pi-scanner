
/*
    This section contains all of the global variables for the page.
*/
var background_jobs = 0;

/*
    Runs when the page is first loaded and sets up things like automatic request calls
    and status updates.
*/
function on_page_load()
{
    inc_busy();
    var manual_control_image = document.getElementById('manualCameraPicture');
    manual_control_image.src="/web/cam_latest.jpg";
    dec_busy();
}

/*
	Changes the current main display window on the home page.
*/
function sideMenuItem_Click(target)
{
    inc_busy();
	for (var i = 0; i <= 5; i++) 
	{
		if(i == target)
		{
			document.getElementById('contentContainer'+i).style.display = 'block';
		}
		else
		{
			document.getElementById('contentContainer'+i).style.display = 'none';
		}
	}
    dec_busy();
}

/*
 Asynchronously requests for the latest frame from the camera (stored server-side) be updated.
 If the request is successful then the manual camera control picture is updated.
*/
function grab_latest_frame()
{
    inc_busy();
    var xmlhttp;
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function()
    {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
            var manual_control_image = document.getElementById('manualCameraPicture');
            manual_control_image.src="/web/cam_latest.jpg";
            dec_busy();
        }
    }
    xmlhttp.open("GET","/API/getLatestFrame",true);
    xmlhttp.send();
}

/*
    Adds one to the number of background jobs running.
*/
function inc_busy()
{
    background_jobs++;
    update_busy_indicator();
}

/*
    subtracts one to the number of background jobs running.
*/
function dec_busy()
{
    background_jobs--;
    if(background_jobs<0)
    {
        background_jobs = 0;
    }
    update_busy_indicator();
}

/*
    Should be called by anything that alters the number of jobs running in the back ground.
    Simply updates the visibility of the icon in the top right.
*/
function update_busy_indicator()
{
    var icon = document.getElementById('busyIcon');
    var textBox = document.getElementById('statusBox');
    textBox.innerHTML=String(background_jobs);
    if(background_jobs > 0)
    {
        icon.style.display='inline';
    }
    else
    {
        icon.style.display='none';
    }
}