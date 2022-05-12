// Static asset that would be rendered as the server loads
function like(postId) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);

        fetch(`/like-post/${postId}`, {method: "POST"})
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            if (data["likes"] == true) {
                likeButton.className = "fa-solid fa-heart"
            } else {
                likeButton.className = "fa-regular fa-heart"
            }
        })
        .catch((e) => alert("could not like post"));
}