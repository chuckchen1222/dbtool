/*
Author: chzhang@tripadvisor.com
Date: 2019-04-09
Version: 20190409
*/

function ajax(url, fnSucc, fnFaild){
    if(window.XMLHttpRequest){
        var oAjax = new XMLHttpRequest();
    }
    else{
        var oAjax = new ActiveXObject("Microsoft.XMLHTTP");
    }

    oAjax.open('POST',url,true);

    oAjax.send();

    oAjax.onreadystatechange = function(){
        if (oAjax.readyState == 4){
            if (oAjax.status == 200){
                fnSucc(oAjax.responseText);
            }
            else{
                if(fnFaild){
                    fnFaild(oAjax.status)
                }
            }
        }
    }

}



