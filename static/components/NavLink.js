const navLinkEl = document.querySelectorAll("#navEl")



document.addEventListener("DOMContentLoaded", () => {

    navLinkEl.forEach(link => {
    link.addEventListener('click', () => {
        document.querySelector('#navEl.active')?.classList.remove('active')
        
        this.classList.add('active')
    })
    })

    console.log(navLinkEl)
    console.log('Hello, World')

})
