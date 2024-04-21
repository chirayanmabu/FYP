id = document.getElementById("bookPackage").name
booking_date = document.getElementById("bookingDate").value
packageId = document.getElementById("bookPackage").getAttribute("data-package-id");
console.log(booking_date)
fetch("/config/")
.then((result) => {return result.json();})
.then((data) => {
    const stripe = Stripe(data.publicKey);
    const url = `/create-checkout-session/${packageId}/`


    document.querySelector("#bookPackage").addEventListener("click", () => {
        fetch(`${url}?booking_date=${booking_date}`)
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

function activeNav() {
    var nav_list = document.querySelectorAll(".sidebar .sidebar_a")
    const location = window.location.href;
    for (let i = 0; i < nav_list.length; i++) {
      if (location === nav_list[i].href) {
        nav_list[i].classList.add("active");
      } else {
        nav_list[i].classList.remove("active");
      }
    }
  };

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
