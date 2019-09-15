fetch("/list", {method: 'GET'})
.then(data => data.text())
.then(resp =>
    console.log(resp));
