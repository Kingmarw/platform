
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
            <div class="video-box">
              <h3>${v.title}</h3>
              <video controls>
                <source src="${v.url}" type="video/mp4">
              </video>
            </div>
          `;
        });
      } catch (err) {
        console.error("خطأ في جلب الفيديوهات:", err);
      }
    }

    loadVideos();
