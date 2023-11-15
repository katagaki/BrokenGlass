document.getElementById("matomeru-button").addEventListener("click", async () => {
    const file = document.getElementById("file-selector").files[0];
    if (!file) {
        alert("ファイルを選択してください。");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("matomeru-button-section").remove();
    document.getElementById("upload-button-title").remove();
    document.getElementById("upload-button-section").remove();
    document.getElementById("matome-title").removeAttribute("hidden");
    document.getElementById("matome-section").removeAttribute("hidden");

    try {
        const response = await fetch("/mypage/matome/upload", {
            method: "POST",
            body: formData,
        });

        if (response.ok) {
            const fileID = await response.text();
            const eventSource = new EventSource("/mypage/matome/stream?id=" + fileID);
            var hasTextBeenReplaced = false;
            eventSource.onmessage = (event) => {
                const responseText = event.data;
                if (!hasTextBeenReplaced) {
                    document.getElementById("streamed-response").innerText = responseText;
                    hasTextBeenReplaced = true;
                } else {
                    document.getElementById("streamed-response").innerText += responseText;
                }
            };

            eventSource.onerror = (error) => {
                console.error(error);
            };
            // document.getElementById("streamed-response").innerText = result;
        } else {
            console.error(response.status);
        }
    } catch (error) {
        console.error(error);
    }
});
