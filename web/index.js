    fetch("/api/videos")
      .then(res => res.json())
      .then(videos => {
        const container = document.getElementById("videos");
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
                متصفحك لا يدعم تشغيل الفيديو
              </video>
            </div>
          `;
        });
      })
      .catch(err => {
        console.error("خطأ في جلب الفيديوهات:", err);
      });
