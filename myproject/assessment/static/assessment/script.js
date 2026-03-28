document.addEventListener("DOMContentLoaded", () => {

    const path = window.location.pathname;

    // ================= HOME PAGE =================
    if (path === "/" || path === "/home/") {

        const welcomeDiv = document.getElementById("welcomeMessage");
        const nameInput = document.querySelector("input[name='name']");

        const savedUsername = localStorage.getItem("mindsteps_username");

        if (welcomeDiv) {
            if (savedUsername) {
                welcomeDiv.textContent = `أهلاً بك يا ${savedUsername}! 👋`;
            } else {
                welcomeDiv.textContent = "أهلاً بك يا بطل 👋";
            }
        }

        const form = document.querySelector("form");

        if (form) {
            form.addEventListener("submit", () => {
                const name = nameInput.value;
                localStorage.setItem("mindsteps_username", name);
            });
        }

        // 🔥 حركة الزر
        const btn = document.querySelector("button");

        if (btn) {
            btn.addEventListener("click", () => {
                btn.style.transform = "scale(1.05)";
                setTimeout(() => {
                    btn.style.transform = "scale(1)";
                }, 150);
            });
        }
    }

});