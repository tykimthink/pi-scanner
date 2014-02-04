
/*
	Changes the current main display window on the home page.
*/
function sideMenuItem_Click(target)
{
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
}