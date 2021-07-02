const sidebar = document.querySelector(".sidebar-container");

const handleNav = () => {
    console.log("Clicked!");
    sidebar.className="sidebar-container-active";
}
const handleClose = () => {
    sidebar.className="sidebar-container";
}
