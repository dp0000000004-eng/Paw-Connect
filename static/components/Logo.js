const logoEl = document.getElementById("logo")

export default function logo(){
    logoEl.addEventListener("mouseenter", () => {
        logoEl.innerText = "Thank's"
    })
}
console.log("Works")