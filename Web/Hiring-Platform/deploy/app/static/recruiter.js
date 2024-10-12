// var PRODUCTION = true
let portfolio = document.querySelector(".portfolio-block");
portfolio.innerHTML = atob(portfolio.innerHTML)
portfolio.classList.remove("nodisplay");
portfolio = document.querySelector(".portfolio-block");
portfolio.innerHTML = portfolio.innerHTML.replace(/<script\b[^>]*><\/script>/gi, "")
if (PRODUCTION) {
    const formContainer = document.querySelector(".selectionForm");
    const user = document.querySelector("#email").innerHTML
    formContainer.innerHTML = `<form method="post" action="/recruiter/select" id="select_humans">
            <input type="text" name="email" value="${btoa(user)}" hidden>
            <input type="submit" value="Call for interview">
        </form>`
}