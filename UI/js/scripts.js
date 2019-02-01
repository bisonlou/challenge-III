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
  console.log(data);
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
  console.log(data)
}).catch(err => {
  console.log(err);
});
}

function postRedflags(){
  url = 'http://127.0.0.1:5000/api/v1/redflags';

fetch(url,{
  method: 'post',
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
  console.log(data)
}).catch(err => {
  console.log(err);
});
}

