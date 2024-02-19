// console.log("Hello");
id = document.getElementById("bookPackage").name
// console.log("Hello2")
fetch("/config/")
.then((result) => {return result.json();})
.then((data) => {
    const stripe = Stripe(data.publicKey);
    const url = `/create-checkout-session/${id}`


    document.querySelector("#bookPackage").addEventListener("click", () => {
        fetch(url)
        .then((result) => {
            return result.json();
        })
        .then((data) => {
            console.log(data);
            return stripe.redirectToCheckout({sessionId: data.sessionId})
        })
        .then((res) => {
            console.log(res);
        });
    });
});