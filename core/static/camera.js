const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const capture = document.getElementById("capture");
const container = document.getElementById("camera-container");

let stream = null;

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({
      video: {
        facingMode: "user",
      },
      audio: false,
    });

    video.srcObject = stream;
  } catch (err) {
    alert("Unable to access camera.");
    console.error(err);
  }
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
    video.srcObject = null;
    stream = null;
  }
}

function goBack() {
  stopCamera();
  history.back();
}

capture.addEventListener("click", () => {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  const ctx = canvas.getContext("2d");

  ctx.drawImage(video, 0, 0);

  const image = canvas.toDataURL("image/png");
  console.log(image);

  container.innerHTML = `<img src="${image}" style="object-fit:cover;height:100%;width:100%">`;
  capture.style.display = "none";

  console.log(canvas);
});

window.addEventListener("beforeunload", stopCamera);
window.addEventListener("load", startCamera);
