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
            var package1Id = response.package1.id;
            var viewDetailPackage1Url = "/package-detail/" + package1Id;
            var package2Id = response.package2.id;
            var viewDetailPackage2Url = "/package-detail/" + package2Id;
            // Update modal body with package details
            var modalBody = document.getElementById("compareModalBody");
            modalBody.innerHTML = `
            <div class="containter">
                <div class="row">
                    <div class="col-6">
                        <p class="package-header">${response.package1.title}</p>
                        <div class="package-author-font">   
                            <p class="mb-0">By: ${response.package1.author}</p>
                            <p class="mb-0">Location: ${response.package1.location}</p>
                        </div>
                        <div class="row mt-3">
                            <div class="compare-img">
                                ${response.package1.image_url ? `<img src="${response.package1.image_url}" alt="Package Image">` : ''}
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col">
                                <p class="subheadings mb-0">About</p>
                                <p>${response.package1.desc}</p>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col d-flex justify-content-end">
                                <a href="${viewDetailPackage1Url}"><button class="view-package-btn">View Detail</button></a>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <p class="package-header">${response.package2.title}</p>
                        <div class="package-author-font">   
                            <p class="mb-0">By: ${response.package2.author}</p>
                            <p class="mb-0">Location: ${response.package2.location}</p>
                        </div>
                        <div class="row mt-3">
                            <div class="compare-img">
                                ${response.package2.image_url ? `<img src="${response.package2.image_url}" alt="Package Image">` : ''}
                            </div>
                        </div>
                        <div class="row mt-3">
                            <div class="col">
                                <p class="subheadings mb-0">About</p>
                                <p>${response.package2.desc}</p>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col d-flex justify-content-end">
                                <a href="${viewDetailPackage2Url}"><button class="view-package-btn">View Detail</button></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            `;
            initStarRatings();
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
