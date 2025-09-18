    fetch("/api/videos")
      .then(res => res.json())
      .then(videos => {
        const container = document.getElementById("videos");
        videos.forEach(v => {
          container.innerHTML += `
            <h3>${v.title}</h3>
            <video controls width="400">
              <source src="${v.url}" type="video/mp4">
            </video>
          `;
        });
      });
