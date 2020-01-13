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
        customSwitch.value = 0
    } else {
        document.getElementById("RadiosExpand").style.display = "block";
        customSwitch.value = 1
    }
}