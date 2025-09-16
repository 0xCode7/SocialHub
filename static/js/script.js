document.addEventListener('DOMContentLoaded', () => {
    // Detect if we are on the post detail page
    const isDetailPage = document.body.classList.contains("post-detail-page");

    // --- Comment button ---
    document.querySelectorAll('.comment-button').forEach(btn => {
        btn.addEventListener('click', e => {
            e.preventDefault();
            const postCard = btn.closest('.post-card');
            const postId = postCard.dataset.postId;

            if (isDetailPage) {
                // Just toggle comments if we are on detail page
                const commentsSection = postCard.querySelector('.comments-section');
                commentsSection?.classList.toggle('hidden');
            } else {
                // Redirect to detail page if we are on feed/home
                window.location.href = `/post/${postId}/`;
            }
        });
    });

    // --- Follow Button ---
    document.querySelectorAll('.follow-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const userId = btn.dataset.userId;
            const response = await fetch(`/accounts/follow/${userId}/`, {
                method: 'POST', headers: {
                    'X-CSRFToken': csrfToken, 'Content-Type': 'application/json'
                }
            });
            if (response.ok) {
                const data = await response.json();
                btn.textContent = data.following ? 'Unfollow' : 'Follow';
            }
        });
    });

    // --- Like button handler ---
    document.querySelectorAll(".like-button").forEach(btn => {
        btn.addEventListener("click", async () => {
            const postId = btn.closest(".post-card").dataset.postId;

            const response = await fetch(`/post/${postId}/like/`, {
                method: "POST", headers: {
                    "X-CSRFToken": csrfToken, "Content-Type": "application/json",
                }
            });

            if (response.ok) {
                const data = await response.json();
                btn.innerHTML = `❤️ ${data.likes_count} Likes`;
                btn.classList.toggle("liked", data.liked);
            }
        });
    });

    // --- Comment form handler ---
    document.querySelectorAll(".comment-form").forEach(form => {
        form.addEventListener("submit", async e => {
            e.preventDefault();

            const postId = form.closest(".post-card").dataset.postId;
            const formData = new FormData(form);

            const response = await fetch(`/post/${postId}/comment/`, {
                method: "POST", headers: {"X-CSRFToken": csrfToken}, body: formData
            });

            if (response.ok) {
                const data = await response.json();
                if (data.success) {
                    const commentsList = form.closest(".post-card").querySelector(".comments-list");

                    const newComment = document.createElement("div");
                    newComment.classList.add("comment");
                    newComment.dataset.commentId = data.comment_id;

                    newComment.innerHTML = `
                        <p>
                            <span class="comment-author">${data.author}:</span>
                            ${data.content}
                        </p>
                        ${data.can_delete ? '<button class="delete-comment-btn" style="color:red;">🗑️</button>' : ''}
                    `;
                    commentsList.prepend(newComment);

                    form.reset();
                }
            }
        });
    });

    document.querySelectorAll('.comments-section').forEach(section => {
        section.addEventListener('click', async e => {
            if (e.target.classList.contains("delete-comment-btn")) {
                const commentDiv = e.target.closest('.comment')
                const commentId = commentDiv.dataset.commentId

                const response = await fetch(`/comment/${commentId}/delete/`, {
                    method: "POST", headers: {
                        "X-CSRFToken": csrfToken, "Content-Type": 'application/json'
                    }
                });

                if (response.ok) {
                    const data = await response.json()
                    if (data.success) {
                        commentDiv.remove();
                    } else {
                        alert(data.error || "Couldn't delete comment.")
                    }
                }
            }
        })
    })
});
