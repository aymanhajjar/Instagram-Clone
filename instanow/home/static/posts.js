
const fetchPages = async (url) => {
    let headers = new Headers()
    headers.append("X-Requested-With", "XMLHttpRequest")
    return fetch(url, { headers })
}

document.addEventListener("DOMContentLoaded", () => {
    let sentinel = document.getElementById("sentinel");
    let scrollElement = document.getElementById("profileposts");
    let counter = 2;
    let endcounter = 0;
    let end = false;
    let username = document.getElementById("profileusername").value;
    console.log(`${username}`);
  
    
    let observer = new IntersectionObserver(async (entries) => {
      entry = entries[0];
      if (entry.intersectionRatio > 0) {
          let url = `/profile/${username}?page=${counter}`;
          let req = await fetchPages(url);
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
              console.log(`${endcounter}`)
              console.log(`${username}`);

              
          }
      }
    })
    observer.observe(sentinel);
  })