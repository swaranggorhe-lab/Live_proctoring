export const showToast = (msg, color="#ff4444") => {
  const t = document.getElementById("toast");
  t.innerText = msg;
  t.style.display = "block";
  t.style.background = color;
  setTimeout(()=> t.style.display = "none", 3000);
};
