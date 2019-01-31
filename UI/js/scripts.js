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

function register(){
  url = 'http://127.0.0.1:5000/api/v1/auth/signup'
  var data = {
    "user_name": "innocent",
    "email": "bisonlou@gmail.com",
    "first_name": "lou",
    "last_name": "lou",
    "phone_number": "0753669897",
    "password": "Pa$$word123",
    "other_names": "",
    "is_admin": false
  };

  fetch(url, {
    method: 'POST', // or 'PUT'
    body: JSON.stringify(data), // data can be `string` or {object}!
    headers:{
      'Content-Type': 'application/json'
    }
  }).then(res => res.json())
  .then(response => console.log('Success:', JSON.stringify(response)))
  .catch(error => console.error('Error:', error));

}
