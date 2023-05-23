const fetchPage = async (url) => {
    let headers = new Headers()
    headers.append("X-Requested-With", "XMLHttpRequest")
    return fetch(url, { headers })
}

document.addEventListener("DOMContentLoaded", () => {
    let sentinel = document.getElementById("sentinel");
    let scrollElement = document.getElementById("randompostsgird");
    let counter = 2;
    let endcounter = 0;
    let end = false;
  
    
    let observer = new IntersectionObserver(async (entries) => {
      entry = entries[0];
      if (entry.intersectionRatio > 0) {
          let url = `../../explore/?page=${counter}`;
          let req = await fetchPage(url);
          if (req.ok) {
              let body = await req.text();
              scrollElement.innerHTML += body;

              counter++;
          } else {
              // If it returns a 404, stop requesting new items
              end = true;
            if(endcounter == 0){
              body = "<div id='end'> You've reached the end!</div>";
              scrollElement.innerHTML += body;
            }

              endcounter++;

              
          }
      }
    })
    observer.observe(sentinel);
  })

  

  function makeAjaxRequest() {
    searchitem = $('#txtSearch').val();
    if (searchitem == ''){
        document.getElementById('srchdrp').style.display='none';
    }

    body = ''
      $.ajax({
        url: `../../../search/${searchitem}`,
        data: {name: searchitem},
        type: 'get',
      }).done(function(results){
          document.getElementById('srchdrp').style.display='block';
          console.log('parsed json', results)

          results.forEach(element => {
              body += `
                    <a href="../../../profile/${element.username}" class="searchhref">
                    <div class="searchcontainer">
                    <img id="ppic" src="media/${element.ppic}">
                    <span class="searchusername"> ${element.username} </span>
                    </div>
                    </a>`
          });
          document.getElementById('srchdrp').innerHTML = body;
          
      }) ;
  }