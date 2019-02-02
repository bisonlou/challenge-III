function createNode(element) {
  return document.createElement(element);
}

function append(parent, el) {
return parent.appendChild(el);
}

function loadRedFlags(){
  const table = document.getElementById('redflag-table');
  const url = 'http://127.0.0.1:5000/api/v1/redflags';
  
  fetch(url)
  .then((resp) => resp.json())
  .then(function(data) {
    let redflag = data.results;
    return authors.map(function(author) {
      let tr = createNode('tr'),
          td = createNode('td')
  
      date = `${redflag.dteRegistered}`;
      title = `${redflag.title}`;
      location = `${redflag.location}`;
  
      append(table, tr);
      append(tr, td);
      append(td, title);
    })
  })
  .catch(function(error) {
      console.log(JSON.stringify(error));
    });   
}

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
    window.location.href = "http://localhost/iReporter/home.html";
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
  
  redflags_table = document.getElementById('redflag-table');

  for(i=0; i< (data['data'][0]).length; i++){
        var row = redflags_table.insertRow(i + 1);
        
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        cell1.innerHTML = data['data'][0][i]['createdon'];
        cell2.innerHTML =  data['data'][0][i]['title'];
        cell3.innerHTML =  data['data'][0][i]['status'];
        cell4.innerHTML =  '<a href="./redflag_edit.html">Edit</a> | <a href="./redflag_confirm_delete.html">Delete</a>';

  }
 
}).catch(err => {
  console.log(err);
});
}


function postRedflags(){
  url = 'http://127.0.0.1:5000/api/v1/incidents';

  title = document.getElementById('title').value
  comment = document.getElementById('comment').value

fetch(url,{
  method: 'post',
  body: JSON.stringify({
        'title': title,
        'comment': comment,
        'location': '(00.000000, 00.000000)',
        'type': 'red-flag',
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
    window.location.href = "http://localhost/iReporter/home.html";
  }
}).catch(err => {
  console.log(err);
});
}

