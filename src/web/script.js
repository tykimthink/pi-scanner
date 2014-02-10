
/*
    This section contains all of the global variables for the page.
*/
var background_jobs = 0;
var image_refresh_handle;
/*
    Runs when the page is first loaded and sets up things like automatic request calls
    and status updates.
*/
function on_page_load()
{
    inc_busy();
    var manual_control_image = document.getElementById('manualCameraPicture');
    manual_control_image.src="/API/getLatestFrame";
    calibration_menu_load();
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
function save_latest_frame()
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
            dec_busy();
        }
    }
    xmlhttp.open("GET","/API/getLatestFrame",true);
    xmlhttp.send();
}

/*
 Asynchronously requests for the latest frame from the camera (stored server-side) be updated.
 If the request is successful then the manual camera control picture is updated.
*/
function grab_latest_frame()
{
    inc_busy();
    var manual_control_image = document.getElementById('manualCameraPicture');
    manual_control_image.src="/API/getLatestFrame";
    dec_busy();
}

/*

*/
function toggle_image_auto_refresh()
{
    var button = document.getElementById('manualToggleAutoRefresh');
    if(button.style.color=='red')
    {
        button.style.color='green';
        image_refresh_handle = window.setInterval("grab_latest_frame();",100);
    }
    else
    {
        window.clearInterval(image_refresh_handle);
        button.style.color='red';
    }
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

/*
    Performs a generic API callback and returns the response text to the caller.
*/
function callback_get(target)
{
    var xmlhttp;
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.open("GET",target,false);
    xmlhttp.send();
    return xmlhttp.responseText;
}

/*
    Fires whenever the calibration menu is loaded
*/
function calibration_menu_load()
{
    inc_busy();
    var selBox = document.getElementById("CalibrationFileList");
    var existingFiles = callback_get("/API/Calibration.getAll");
    selBox.innerHTML = "";
    var list = existingFiles.split("\n");
    for (var i = 0; i< list.length -1; i++)
    {
        filename = list[i].split(",")[0];
        title = list[i].split(",")[1];
        var option = document.createElement("option");
        option.text = title;
        option.value = filename;
        selBox.add(option,selBox[1]);
    }
    var o1 = document.createElement("option");
    o1.text = "-----------------------------";
    o1.value = "None";
    selBox.add(o1,selBox[0]);
    var o2 = document.createElement("option");
    o2.text = "Create New";
    o2.value = "Action_New";
    selBox.add(o2,selBox[0]);
    var o3 = document.createElement("option");
    o3.text = "Select A File To Load:";
    o3.value = "None";
    selBox.add(o3,selBox[0]);
    dec_busy();
}

/*
    Loads a calibration file whenever the current selection changes.
*/
function load_calibration_file()
{
    inc_busy();
    var selBox = document.getElementById("CalibrationFileList");
    fileName = selBox.options[selBox.selectedIndex].value;
    if(fileName == "None")
    {
        // Do Nothing!
    }
    else if(fileName == "Action_New")
    {
        newName = callback_get("/API/Calibration.newBlank");
        var option = document.createElement("option");
        option.text = "New Empty Calibration File";
        option.value = newName;
        selBox.add(option);
        selBox.selectedIndex = selBox.options.length-1;
    }
    else
    {
        var nameBox = document.getElementById("calibration_current_name");
        var notesBox = document.getElementById("calibration_current_description");
        var cameraBox = document.getElementById("calibration_current_camera");
        var laserAngleBox = document.getElementById("calibration_current_angle");
        var laserDistanceBox = document.getElementById("calibration_current_distance");

        nameBox.value = callback_get("/API/Calibration.LoadEl?file="+fileName+"&el=name");
        notesBox.value = callback_get("/API/Calibration.LoadEl?file="+fileName+"&el=notes");
        cameraBox.value = callback_get("/API/Calibration.LoadEl?file="+fileName+"&el=camera");
        laserAngleBox.value = callback_get("/API/Calibration.LoadEl?file="+fileName+"&el=laser-camera-angle");
        laserDistanceBox.value = callback_get("/API/Calibration.LoadEl?file="+fileName+"&el=laser-camera-distance");


        var pointsBox = document.getElementById("calibration_current_points");
        pointsBox.innerHTML="";
        var list = callback_get("/API/Calibration.LoadEl?file="+fileName+"&el=data").split("\n");
        
        for (var i = 0; i< list.length -1; i++)
        {
            X = list[i].split(",")[0];
            Z = list[i].split(",")[1];
            var point = document.createElement("option");
            point.text = X +"\t->\t"+Z;
            point.value = X+","+Z;
            pointsBox.add(point);
        }

    }
    dec_busy();
}