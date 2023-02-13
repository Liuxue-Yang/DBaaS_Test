import http from "k6/http";

export let options = {
    vus: 10,
    iterations: 200
};

export
default
    function() {
        let payload = JSON.stringify({
            "address": "192.168.8.131",
            "port": 9669
        });
        let headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer WyJyb290IiwibmVidWxhIl0="
        };
        let res = http.post("http://192.168.8.131:7002/api-nebula/db/connect", payload, {
            headers: headers
        });
        if (res.status === 200) {
            console.log("Successful response with status code:", res.status);
            return 1;
        } else {
            console.log("Response with status code:", res.status);
            return 0;
        }
    };