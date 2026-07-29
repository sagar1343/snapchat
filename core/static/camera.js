const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const capture = document.getElementById("capture");
const container = document.getElementById("camera-container");
const captureBar = document.getElementById("capture-bar");
const previewActions = document.getElementById("preview-actions");
const retakeBtn = document.getElementById("retake");
const openSendToBtn = document.getElementById("open-send-to");
const sendToSheet = document.getElementById("send-to-sheet");
const closeSendToBtn = document.getElementById("close-send-to");
const imageDataInput = document.getElementById("image-data");
const snapThumb = document.getElementById("snap-thumb");
const sendSnapForm = document.getElementById("send-snap-form");

if (video && canvas && capture) {
  let stream = null;
  let cameraReady = false;

  async function startCamera() {
    cameraReady = false;
    capture.disabled = true;
    capture.style.opacity = "0.5";

    try {
      stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user" },
        audio: false,
      });
    } catch (err) {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });
      } catch (err2) {
        alert("Unable to access camera.");
        console.error(err2);
        return;
      }
    }

    video.srcObject = stream;

    video.onloadedmetadata = async function () {
      try {
        await video.play();
      } catch (err) {
        console.error(err);
      }
      cameraReady = true;
      capture.disabled = false;
      capture.style.opacity = "1";
    };
  }

  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      video.srcObject = null;
      stream = null;
    }
    cameraReady = false;
  }

  function goBack() {
    stopCamera();
    history.back();
  }
  window.goBack = goBack;

  capture.addEventListener("click", () => {
    if (!cameraReady || !video.videoWidth || !video.videoHeight) {
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);

    const photo = canvas.toDataURL("image/jpeg", 0.85);
    imageDataInput.value = photo;

    stopCamera();
    container.innerHTML = `<img src="${photo}" class="w-full h-full object-cover">`;
    if (snapThumb) {
      snapThumb.innerHTML = `<img src="${photo}" class="w-full h-full object-cover">`;
    }

    captureBar.style.display = "none";
    previewActions.style.display = "flex";
  });

  retakeBtn.addEventListener("click", () => {
    location.reload();
  });

  if (openSendToBtn && sendToSheet) {
    openSendToBtn.addEventListener("click", () => {
      sendToSheet.style.display = "flex";
    });
  }

  if (closeSendToBtn && sendToSheet) {
    closeSendToBtn.addEventListener("click", () => {
      sendToSheet.style.display = "none";
    });
  }

  if (sendSnapForm) {
    sendSnapForm.addEventListener("submit", (e) => {
      if (!imageDataInput.value) {
        e.preventDefault();
        alert("Please take a photo first.");
        return;
      }

      const checked = document.querySelectorAll(".friend-check:checked");
      const hasDirectFriend = sendSnapForm.querySelector('input[name="friend_ids"][type="hidden"]');
      if (!hasDirectFriend && checked.length === 0) {
        e.preventDefault();
        alert("Please select at least one friend.");
      }
    });
  }

  window.addEventListener("beforeunload", stopCamera);
  window.addEventListener("load", startCamera);
}
