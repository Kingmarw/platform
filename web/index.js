
    async function loadVideos() {
      try {
        const res = await fetch("/api/videos");
        const videos = await res.json();

        const container = document.getElementById("videos");
        if (!container) {
          console.error("❌ مفيش عنصر videos في الصفحة");
          return;
        }

        if (videos.length === 0) {
          container.innerHTML = "<p>لا توجد فيديوهات بعد 🎞️</p>";
          return;
        }

        videos.forEach(v => {
          container.innerHTML += `
            <div class="col-md-4 mb-4">
              <div class="card">
                <video controls>
                  <source src="uploads/${video.file}" type="video/mp4">
                  متصفحك لا يدعم الفيديو
                </video>
                <div class="card-body">
                  <h5 class="card-title">${video.name}</h5>
                </div>
              </div>
            </div>
          `;
        });
      } catch (err) {
        console.error("خطأ في جلب الفيديوهات:", err);
      }
    }

    loadVideos();

