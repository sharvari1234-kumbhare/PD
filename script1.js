function scanURL(){
    const url = document.getElementById("url").value;

    fetch("/scan",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({url:url})
    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("result").innerText="Result : "+data.result;
        setTimeout(()=>location.reload(),1000);
    });
}