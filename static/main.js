//document.addEventListener('DOMContentLoaded', to_expand);

function is_active() {
    'use strict';
    //let
    // = Number(.value);
    //.innerHTML = String(c);
}

 function to_expand() {
    'use strict';
    if (customSwitch.value == 1)
    {
        document.getElementById("RadiosExpand").style.display = "none";
        document.getElementById("Search_by_name").style.display = "none";
        document.getElementById("Search_by_user").style.display = "none";
        customSwitch.value = 0
    } else {
        document.getElementById("RadiosExpand").style.display = "block";
        document.getElementById("Search_by_name").style.display = "block";
        document.getElementById("Search_by_user").style.display = "block";
        customSwitch.value = 1
    }
}

function voting_search() {
    'use strict';
    let voting_num = voting_id.value
    if (voting_num != '') {
        document.location.href = '/voting_info/' + String(voting_num);
    }
}


function card_creator() {
    let container = document.getElementById("card_container");
    for (let i = 0; i < array.length; i++) {
           container.innerHTML += '<div class="card" style="width: 18rem;">';
           container.innerHTML += '<div class="card-body">';
           container.innerHTML += '<h5 class="card-title"> </h5>';
           container.innerHTML += '<p class="card-text">Some text on the card about vote content.</p>';
           container.innerHTML += '<a href="#" class="btn btn-primary">More information</a>';
           container.innerHTML += '</div>';
           container.innerHTML += '</div>';
    }
}

function dec_offset() {
    "usestrict";
    offset_tag.value = Number(offset_tag.value) - {{ page_size }};
}

function inc_offset() {
    "usestrict";
    offset_tag.value = Number(offset_tag.value) + {{ page_size }};
}