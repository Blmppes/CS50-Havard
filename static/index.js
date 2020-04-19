
document.getElementById("form").onsubmit = () => {
    const request = new XMLHttpRequest();
    const currency = document.getElementById("currency").value;
    request.open("POST", '/convert');

    request.onload = () => {
        console.log(request.responseText)
        const data = JSON.parse(request.responseText);

        if(data.success){
            const contents = `1 USD equal to ${data.rate} ${currency}`;
            document.getElementById("result").innerHTML = contents;
        }else{
            document.getElementById("result").innerHTML = data.error;
        }
    }

    const data = new FormData();
    data.append('currency', currency);

    request.send(data);
    return false;
}
