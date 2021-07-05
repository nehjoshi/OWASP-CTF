const sidebar = document.querySelector(".sidebar-container");

const handleNav = () => {
    console.log("Clicked!");
    sidebar.className="sidebar-container-active";
}
const handleClose = () => {
    sidebar.className="sidebar-container";
}
const copyToClipboard = () => {
    const text = "docker pull owaspctf/tovc-1";
    const cp = new ClipboardJS('.fa-copy');
}
