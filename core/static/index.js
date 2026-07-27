const snapFile = document.getElementById("snap-file");
const fileBtn = document.getElementById("file-button");
const previewDock = document.getElementById("preview-dock");
const previewContainer = document.getElementById("preview-container");
const caption = document.getElementById("caption");

fileBtn.addEventListener("click", () => {
  snapFile.click();
});

snapFile.addEventListener("change", () => {
  const currentFile = snapFile.files[0];

  const image = ` <img
      id="preview-snap"
      src="${URL.createObjectURL(currentFile)}"
      alt="${currentFile.name}"
      class="object-cover h-full w-full"
    />`;
  previewContainer.innerHTML = image;
  caption.innerText = currentFile.name;
  previewDock.style.display = "block";
});
