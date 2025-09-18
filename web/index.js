// 
async function loadVideos() {
  let res = await fetch("https://platform-20mw.onrender.com/api/videos");
  let videos = await res.json();
  let container = document.getElementById("videos");
  container.innerHTML = "";
  videos.forEach((video) => {
    let card = `
          <div class="col-md-4 mb-4">
            <div class="card h-100">
              <video class="w-100" controls>
                <source src="${video.url}" type="video/mp4">
              </video>
              <div class="card-body text-center">
                <h5>${video.title}</h5>
              </div>
            </div>
          </div>`;
    container.innerHTML += card;
  });
}
loadVideos();
