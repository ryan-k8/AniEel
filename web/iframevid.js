eel.iframe_src_link("return iframe src!")(ifits)
function ifits(if_src){
    if (if_src == "null"){
        var Div = document.getElementById("iframe-div");
        Div.style.display = "none";
    } else {
            function hid_vidt_ornot(x){
                if (x=="null"){
                document.getElementById("video-frame").style.display= "none";
                } else {
                    document.getElementById("iframe-div").style.display = "none";
                }
            }
            var vid_src = document.getElementById("video-src").src;
            eel.check_js_vid(vid_src)(hid_vidt_ornot) 
            document.getElementById("IFRAME").src = if_src;
        }
    }