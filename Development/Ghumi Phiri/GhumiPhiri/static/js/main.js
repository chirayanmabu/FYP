id = document.getElementById("bookPackage").name
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


// Dashboard sidebar
function toggleNav() {
    var sidebar = document.getElementById("mySidebar");
    var main = document.getElementById("main");

    if (sidebar.style.width === "250px") {
        sidebar.style.width = "0";
        main.style.marginLeft = "0";
    } else {
        sidebar.style.width = "250px";
        main.style.marginLeft = "250px";
    }
}



// Package comparision
var packageId1 = "";
var packageId2 = "";
function addToCompare(packageId) {
    if (!packageId1) {
        packageId1 = packageId;
    } else if (!packageId2) {
        packageId2 = packageId;
        openCompareModal();
    }
} 

function openCompareModal() {
    // Update modal content with package details
    updateModalContent();
    // Show the modal
    var compareModal = new bootstrap.Modal(document.getElementById('compareModal'));
    compareModal.show();

    document.getElementById('compareModal').addEventListener('hidden.bs.modal', function () {
        // Reset packageId1 and packageId2 to empty strings
        packageId1 = "";
        packageId2 = "";
    });
}

function updateModalContent() {
    var compareUrl = document.getElementById("compareModal").dataset.compareUrl;
    // AJAX request to fetch package details
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            // Update modal body with package details
            var modalBody = document.getElementById("compareModalBody");
            modalBody.innerHTML = `
            <p>Package 1:</p>
            <p>Title: ${response.package1.title}</p>
            <p>Author: ${response.package1.author}</p>
            <hr>
            <p>Package 2:</p>
            <p>Title: ${response.package2.title}</p>
            <p>Author: ${response.package2.author}</p>
            `;
            // Show the modal
            var compareModal = new bootstrap.Modal(document.getElementById('compareModal'));
            compareModal.show();
        }
    };
    xhr.open("GET", compareUrl + "?package1=" + packageId1 + "&package2=" + packageId2, true);
    xhr.send();
}


const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

// Write feedback
$("#post_comment").submit(function(e){
    e.preventDefault();

    let dt = new Date();
    let time = dt.getDay() + " " + monthNames[dt.getUTCMonth] + ", "  + dt.getFullYear();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",
        success: function(response){
            console.log("Feedback saved")

            if(response.bool == true){
                $("#feedback-resp").html("Feedback added successfuly.")
                $(".hide-feedback-btn").hide()

                let _html = '<div class="row mb-3 feedback-content">'
                    _html +=        '<div class="container px-0">'
                    _html +=            '<div class="row row g-0 mb-1">'
                    _html +=                '<div class="col-md-2 comment-profile-picture">'
                    _html +=                    '<img src="{{ feedback.feedback_author.profile.profile_pic.url }}" alt="">'
                    _html +=                '</div>'
                    _html +=                '<div class="col ms-3">'
                    _html +=                    '<div class="comment-author-info">'
                    _html +=                        '<span>'+ response.context.user +'</span>'
                    _html +=                        '<span class="ms-3" style="font-weight: 200;">' + time + '</span>'
                    _html +=                    '</div>'
                    _html +=                    '<div class="comment-rating">'
                    _html +=                        '<a href="#5" title="Give 5 stars">★</a>'
                    _html +=                        '<a href="#4" title="Give 4 stars">★</a>'
                    _html +=                        '<a href="#3" title="Give 3 stars">★</a>'
                    _html +=                        '<a href="#2" title="Give 2 stars">★</a>'
                    _html +=                        '<a href="#1" title="Give 1 star">★</a>'
                    _html +=                    '</div>'
                    _html +=                '</div>'
                    _html +=            '</div>'
                    _html +=            '<div class="row">'
                    _html +=                '<div class="col">'
                    _html +=                    '<span>'+ response.context.comment +'</span>'
                    _html +=                '</div>'
                    _html +=            '</div>'
                    _html +=        '</div>'
                    _html +=        '</div>'
                    $(".feedback-list").prepend(_html)
            }
        }
    })
})
