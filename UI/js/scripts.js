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
