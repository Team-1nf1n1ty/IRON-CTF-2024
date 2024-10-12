const link = new URL(window.location.href).pathname
const secretTokenHolder = document.querySelector(".container")
function getCookie(name) {
    const nameEQ = `${name}=`;
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i];
        while (cookie.charAt(0) === ' ') cookie = cookie.substring(1);
        if (cookie.indexOf(nameEQ) === 0) {
            return decodeURIComponent(cookie.substring(nameEQ.length, cookie.length));
        }
    }
    return null; // Return null if the cookie was not found
}
secretTokenHolder.setAttribute("secret", getCookie("token") ? getCookie("token") : "f00bar")
async function fetchButtonData(uuid) {
    try {
        const result = await fetch(`/button/${uuid}`);
        const jsonData = await result.json();
        return jsonData;
    } catch (error) {
        console.error("Error fetching button data:", error);
    }
}
if (link.startsWith("/show/")) {
    (async () => {
        const button = await fetchButtonData(link.replace('/show/', ''));
        const sheet = new CSSStyleSheet();
        sheet.replaceSync(`
            .btn_container{
                width: 100%; 
                height: 100%;
            } 
            .buttonstuff{
                align-items: center; 
                display: flex; 
                justify-content: center;
            }
            button { 
                background-color: ${button.bgcolor}; 
                font-size: ${button.size}; 
                border-radius: ${button.borderRadius}px; 
            }`);
        const host = document.querySelector("#button-preview");
        const shadow = host.attachShadow({ mode: "open" });
        shadow.adoptedStyleSheets = [sheet];
        const btn_container = document.createElement("div");
        const holder = document.createElement("div");
        btn_container.classList = ["btn_container"]
        holder.classList = ["buttonstuff"]
        holder.innerHTML = `<button>${button.text}</button>`
        btn_container.appendChild(holder)
        shadow.appendChild(btn_container)
    })();
}
