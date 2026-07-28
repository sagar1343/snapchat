const snapFile = document.getElementById("snap-file");
const fileBtn = document.getElementById("file-button");
const previewDock = document.getElementById("preview-dock");
const previewContainer = document.getElementById("preview-container");
const caption = document.getElementById("caption");
const longi = document.getElementById("id_longitude");
const lati = document.getElementById("id_latitude");
const lf = document.getElementById("locationform");

if (fileBtn && snapFile) {
  fileBtn.addEventListener("click", () => snapFile.click());

  snapFile.addEventListener("change", () => {
    const file = snapFile.files[0];
    if (!file || !previewDock || !previewContainer || !caption) return;

    previewContainer.innerHTML = `<img src="${URL.createObjectURL(file)}" class="object-cover h-full w-full">`;
    caption.innerText = file.name;
    previewDock.classList.remove("hidden");
  });
}

// navigator.geolocation.getCurrentPosition(
//   (position) => {
//     latitude = position.coords.latitude;
//     longitude = position.coords.longitude;

//     lati.value = latitude;
//     longi.value = longitude;
//     lf.submit();
//   },
//   (err) => {},
// );
