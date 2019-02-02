
function welcome(){
  url = 'http://127.0.0.1:5000/';

  fetch(url)
  .then(response => {
    return response.json();
  }).then(data => {
    console.log(data);
  }).catch(err => {
    console.log(err);
  });
}

function register(){
  url = 'http://127.0.0.1:5000/api/v1/auth/signup';

  email = document.getElementById('email').value
  username = document.getElementById('username').value
  firstname = document.getElementById('firstname').value
  lastname = document.getElementById('lastname').value
  othernames = document.getElementById('othernames').value
  phonenumber = document.getElementById('phonenumber').value
  password = document.getElementById('password').value
  

  fetch(url,{
    method: 'post',
    headers: {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json'
    },
    body: JSON.stringify({
          'user_name': username,
          'email': email,
          'first_name': firstname,
          'last_name': lastname,
          'phone_number': phonenumber,
          'password': password,
          'other_names': othernames,
          'is_admin': true
      })
    })

  .then(response => {
    return response.json();
  }).then(data => {
    if (data['status'] == 201){
      window.location.href = "http://localhost/iReporter/login.html";
    }
  }).catch(err => {
    console.log(err);
  });
}

function login(){
  url = 'http://127.0.0.1:5000/api/v1/auth/login';

  email = document.getElementById('login_email').value
  password = document.getElementById('login_password').value

  fetch(url,{
    method: 'post',
    headers: {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json'},
    body: JSON.stringify({
          'email': email,
          'password': password
      })
    })

  .then(response => {
    return response.json();
  }).then(data => {
    token = data['data'][0]['access_token'];
    bearer_token = "Bearer " + token + ";";
    document.cookie = "token=" + bearer_token;

    if (data['status'] == 200){
      window.location.href = "http://localhost/iReporter/index.html";
    }
  }).catch(err => {
    console.log(err);
  });
}


function getRedflags(){
  url = 'http://127.0.0.1:5000/api/v1/redflags';

  fetch(url,{
    headers: {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json'},
    headers: {
          'Authorization': document.cookie
      }
    })

  .then(response => {
    return response.json();
  }).then(data => {

    if (data['status'] == 401){
      window.location.href = "http://localhost/iReporter/login.html";
    }
    
    redflags_table = document.getElementById('redflag-table');

    for(i=0; i< (data['data'][0]).length; i++){
          var row = redflags_table.insertRow(i + 1);
          
          var cell1 = row.insertCell(0);
          var cell2 = row.insertCell(1);
          var cell3 = row.insertCell(2);
          var cell4 = row.insertCell(3);

    incidentId = data['data'][0][i]['id'];
	  long_date_time = new Date(data['data'][0][i]['createdon']);
		
	  var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	  var days = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"];


	    month = months[long_date_time.getMonth()];
	    day = days[long_date_time.getDay()];
	    year = long_date_time.getFullYear();
      date = long_date_time.getDate();
        if(date < 10){
          date = "0" + date;
        }

      display_date = day + " " + date + " " + month + " " + year;
      
	
          cell1.innerHTML = display_date;
          cell2.innerHTML =  data['data'][0][i]['title'];
          cell3.innerHTML =  data['data'][0][i]['status'];
          cell4.innerHTML =  '<a href="./incident_edit.html?type=red-flag&id=' + incidentId +
                             '">Edit</a> | <a href="./incident_confirm_delete.html?type=red-flag&id=' + incidentId +
                             '">Delete</a>';

    }
  
  }).catch(err => {
    console.log(err);
  });
}

function getInterventions(){
  url = 'http://127.0.0.1:5000/api/v1/interventions';

  fetch(url,{
    headers: {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json'},
    headers: {
          'Authorization': document.cookie
      }
    })

  .then(response => {
    return response.json();
  }).then(data => {

    if (data['status'] == 401){
      window.location.href = "http://localhost/iReporter/login.html";
    }
    
    redflags_table = document.getElementById('intervention-table');

    for(i=0; i< (data['data'][0]).length; i++){
          var row = redflags_table.insertRow(i + 1);
          
          var cell1 = row.insertCell(0);
          var cell2 = row.insertCell(1);
          var cell3 = row.insertCell(2);
          var cell4 = row.insertCell(3);

	  incidentId = data['data'][0][i]['id'];
	  long_date_time = new Date(data['data'][0][i]['createdon']);
		
	  var months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	  var days = ["Sun", "Mon", "Tue", "Wed", "Thur", "Fri", "Sat"];


	    month = months[long_date_time.getMonth()];
	    day = days[long_date_time.getDay()];
	    year = long_date_time.getFullYear();
      date = long_date_time.getDate();
        if(date < 10){
          date = "0" + date;
        }

      display_date = day + " " + date + " " + month + " " + year;
      	
          cell1.innerHTML = display_date;
          cell2.innerHTML =  data['data'][0][i]['title'];
          cell3.innerHTML =  data['data'][0][i]['status'];
          cell4.innerHTML =  '<a href="./incident_edit.html?type=intervention&id=' + incidentId +
                             '">Edit</a> | <a href="./incident_confirm_delete.html?type=intervention&id=' + incidentId +
                             '">Delete</a>';

    }
  
  }).catch(err => {
    console.log(err);
  });
}



function postIncident(incidentType){
  url = 'http://127.0.0.1:5000/api/v1/incidents';

  title = document.getElementById('title').value
  comment = document.getElementById('comment').value

  fetch(url,{
    method: 'post',
    body: JSON.stringify({
          'title': title,
          'comment': comment,
          'location': '(00.000000, 00.000000)',
          'type': incidentType,
          'status': 'pending',
          'images': ['image_001.jpg'],
          'videos': ['video_001.mp4']
        }),
    headers: {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json'},
    headers: {
          'Authorization': document.cookie,
          'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/json'
      }
    })

  .then(response => {
    return response.json();
  }).then(data => {
    if (data['status'] == 201){
      window.location.href = "http://localhost/iReporter/index.html";
    }
  }).catch(err => {
    console.log(err);
  });
}

function getIncident(){
  var url = window.location.href;
  var incidentType = /type=([^&]+)/.exec(url)[1];
  var incidentId = /id=([^&]+)/.exec(url)[1];
  incidentId = parseInt(incidentId, 10)

  title = document.getElementById('title')
  comment = document.getElementById('comment')

  url = 'http://127.0.0.1:5000/api/v1/incidents/' + incidentId;

  fetch(url,{
    method: 'get',
    headers: {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json'},
    headers: {
          'Authorization': document.cookie,
          'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/json'
      }
    })

  .then(response => {
    return response.json();
  }).then(data => {
    if (data['status'] == 201){
      window.location.href = "http://localhost/iReporter/index.html";
    }

    title.innerHTML = data['data'][0]['title']
    comment.innerHTML = data['data'][0]['comment']

  }).catch(err => {
    console.log(err);
  });

}
