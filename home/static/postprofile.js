function postmodalprofile(i, username) {
    document.getElementById('homemodal').style.display='flex';
    token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    console.log(`${i}`);
    postid = i;
    var liked = 0;
    var saved = 0;

    console.log(`../p/${i}`)
    fetch(`../p/${i}`, {method:"GET"})
    .then( (response) => response.json() )
    .then( (post) => {
        console.log('parsed json', post);

        body =
        `<div class="postdetailscontainer">

            <div class="imagepost">
                <img src="${post.image}" class="postimage"> 
            </div>
            <div class="detailscontainer">
                <div class="postusernamemodal">
                    <img src="${post.profileimage}" class = "postppic modalpic">  
                    <a class="profilehref" href="../profile/${post.username}">${post.username}</a>
                </div>
                <div class="postbuttons">`;


        [post.liker].forEach((element) => {
            element.forEach((like) => {
                if ( `${username}` == like.liker){
                       
                    liked = 1;
                    console.log(`liked is ${liked}`);
                    
                }
                else{
                    console.log(`liked is ${liked}`);
                    
            }})

           
            
          });

        if (liked == 0)
        {
            body +=`
                        <button class="btn" class="actionbutton" id = "notlikedmodal${post.id}" onclick="likepostmodal('${post.id}', '${token}')"><span id="likebutton${post.id}"><i class="far fa-heart" style="pointer-events: none;"></i></span></button>
                        <button class="btn" class="actionbutton" id = "likedmodal${post.id}" style="display:none" onclick="unlikepostmodal('${post.id}', '${token}')"><span id="likebutton${post.id}"><i class="fas fa-heart redheart" style="pointer-events: none;"></i></span></button>`
                        ;
        }
        else{
            body +=`
            <button class="btn" class="actionbutton" id = "likedmodal${post.id}" onclick="unlikepostmodal('${post.id}', '${token}')"><span id="likebutton${post.id}"><i class="fas fa-heart redheart" style="pointer-events: none;"></i></span></button>
            <button class="btn" class="actionbutton" id = "notlikedmodal${post.id}" style="display: none" onclick="likepostmodal('${post.id}', '${token}')"><span id="likebutton${post.id}"><i class="far fa-heart" style="pointer-events: none;"></i></span></button>`
            ;
        }
        

        body += `<button class="btn" onclick="focuscommmodal('${post.id}')"><i class="far fa-comment"></i></button>`;



        [post.savedby].forEach((element) => {
            element.forEach((save) => {
                if ( `${username}` == save.saver){
                       
                    saved = 1;
                    
                }})

           
            
          });

        if (saved == 1)
        {
            body +=`
            <button class="btn savebutton" id = "savedmodal${post.id}" onclick="unsavepostmodal('${post.id}', '${token}')"><i class="fas fa-bookmark"></i></button>
            <button class="btn savebutton" id = "notsavedmodal${post.id}" onclick="savepostmodal('${post.id}', '${token}')" style="display:none"><i class="far fa-bookmark"></i></button>`
                                ;
        }
        else{
            body +=`
            <button class="btn savebutton" id = "notsavedmodal${post.id}" onclick="savepostmodal('${post.id}', '${token}')"><i class="far fa-bookmark"></i></button>
            <button class="btn savebutton" id = "savedmodal${post.id}" onclick="unsavepostmodal('${post.id}', '${token}')" style="display:none"><i class="fas fa-bookmark"></i></button>`
                    ;
        }
        
        body += `<div class="postdetails">
        <span class="likecount"><a href="javascript:void(0)" class = "profilehref" onclick="showlikers('${post.id}')"><span id="postlikesmodal${post.id}">${post.like_count} likes</a></span></span><br>
        <div class="postuserandcap">
        <span class="postuser"><a class="profilehref" href="../profile/${post.username}">${post.username}</a> </span>
        <span class="postcaptionmodal">${post.caption}</span><br>
        </div>
        <div class="commentsonpost" id="scrollcomments">`;

        [post.comments].forEach((element) => {
            element.forEach((comment) => {
                console.log(comment);
                console.log(comment.userpic[0]);
                console.log(`${comment.username}`);
    
                body += `<img class="commentpic" src="../media/${comment.userpic[0].ppic}">
                <span class="commentowner modalcomment"><a class="profilehref" href="../profile/${comment.username}">${comment.username}</a> </span>
                <span class="comment">${comment.text}</span><br>
                <div class="commenttime">
                ${comment.date}
                </div>
                `;
            })
            
        });
        body += `
                <span id="extracommentmodal${post.id}"></span>
                </div>
                </div>
                </div>
                <div class="addcomment">
                <form action="javascript:void(0);" name="comment" onsubmit="postcommentmodal('${post.id}')">
            <input class = "addcommentfield" type="text" id="commfieldmodal${post.id}" placeholder="Add a comment..." name="addcomment">
            <input class="submitcomment" type="submit" value="Post">
            </form>
            </div
                </div>
                </div>
                `;
                    
                
        document.querySelector('#details').innerHTML = body;
    })
}

window.onclick = function(event) {
    var modal = document.getElementById("homemodal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
    }

    function likepostmodal(i, token){
        console.log(`${token}`)
        $.ajax({
            url: `../p/${i}/like`,
            type: "POST",
            data: {
                csrfmiddlewaretoken: `${token}`
            }
        }).done(function(returned_data){
            console.log('parsed json', returned_data)
            document.querySelector(`#postlikesmodal${i}`).innerHTML = `${returned_data.likecount} likes`
            document.getElementById(`notlikedmodal${i}`).style.display='none';
            document.getElementById(`likedmodal${i}`).style.display='inline-block';
            
        });
    
        
    }
    
    function unlikepostmodal(i, token){
        console.log(`${token}`)
        $.ajax({
            url: `../p/${i}/unlike`,
            type: "POST",
            data: {
                csrfmiddlewaretoken: `${token}`
            }
        }).done(function(returned_data){
            console.log('parsed json', returned_data)
            document.querySelector(`#postlikesmodal${i}`).innerHTML = `${returned_data.likecount} likes`
            document.getElementById(`notlikedmodal${i}`).style.display='inline-block';
            document.getElementById(`likedmodal${i}`).style.display='none';
            
        });
    
        
    }

    function focuscommmodal(i) {
        document.getElementById(`commfieldmodal${i}`).focus();
    }

    function postcommentmodal(i) {
        if ( $(`#commfieldmodal${i}`).val() != ''){
        $.ajax({
            url: `../p/${i}/addcomment`,
            type: "POST",
            data: {
                'commenttext': $(`#commfieldmodal${i}`).val(),
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
            }
        }).done(function(returned_data){
            console.log('parsed json', returned_data);
            body = `<span class="commentowner"><a class="profilehref" href="profile/${returned_data.owner}">${returned_data.owner}</a> </span>
            <span class="comment">${returned_data.text}</span><br>`;
              document.getElementById(`extracommentmodal${i}`).innerHTML += body;
              document.getElementById(`commfieldmodal${i}`).value= '';
              document.getElementById(`commentcount${i}`).innerHTML = `View all ${returned_data.commentcount} comments`;
              $("#scrollcomments").scrollTop($("#scrollcomments")[0].scrollHeight);
              
        });
      }
    }

function savepostmodal(i, token){
    console.log(`${token}`)
    $.ajax({
        url: `../p/${i}/save`,
        type: "POST",
        data: {
            csrfmiddlewaretoken: `${token}`
        }
    }).done(function(returned_data){
        console.log('parsed json', returned_data)
        document.getElementById(`notsavedmodal${i}`).style.display='none';
        document.getElementById(`savedmodal${i}`).style.display='inline-block';
        
    });

    
}

function unsavepostmodal(i, token){
    console.log(`${token}`)
    $.ajax({
        url: `../p/${i}/unsave`,
        type: "POST",
        data: {
            csrfmiddlewaretoken: `${token}`
        }
    }).done(function(returned_data){
        console.log('parsed json', returned_data)
        document.getElementById(`notsavedmodal${i}`).style.display='inline-block';
        document.getElementById(`savedmodal${i}`).style.display='none';
    });

    
}


function follow(targetuser, thisuser){
    $.ajax({
        url: `../profile/${targetuser}/follow`,
        type: "POST",
        data: {
            'thisuser': `${thisuser}`,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        }
    }).done(function(returned_data){
        console.log('parsed json', returned_data)
        document.getElementById(`flwcount`).innerHTML = `<b>${returned_data.followercount}</b> followers`;
        document.getElementById(`flwingcount`).innerHTML = `<b>${returned_data.followingcount}</b> following`;
        document.getElementById(`followbtn`).style.display = 'none';
        document.getElementById(`unfollowbtn`).style.display = 'inline-block';

    });
}

function unfollow(targetuser, thisuser){
    $.ajax({
        url: `../profile/${targetuser}/unfollow`,
        type: "POST",
        data: {
            'thisuser': `${thisuser}`,
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
        }
    }).done(function(returned_data){
        console.log('parsed json', returned_data)
        document.getElementById(`flwcount`).innerHTML = `<b>${returned_data.followercount}</b> followers`;
        document.getElementById(`flwingcount`).innerHTML = `<b>${returned_data.followingcount}</b> following`;
        document.getElementById(`followbtn`).style.display = 'inline-block';
        document.getElementById(`unfollowbtn`).style.display = 'none';
    });
}