$(document).ready(function() {
    // Auto-hide alerts after 5 seconds
    window.setTimeout(function() {
        $(".alert").fadeTo(500, 0).slideUp(500, function() {
            $(this).remove();
        });
    }, 5000);
    
    // Like/Dislike Post
    $('.post-like-btn, .post-dislike-btn').on('click', function(e) {
        e.preventDefault();
        
        const button = $(this);
        const url = button.attr('href');
        
        $.ajax({
            url: url,
            type: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(data) {
                // Update like/dislike counts
                $('#post-likes-count').text(data.likes_count);
                $('#post-dislikes-count').text(data.dislikes_count);
                
                // Update buttons
                if (button.hasClass('post-like-btn')) {
                    if (data.liked) {
                        button.addClass('text-primary').removeClass('text-secondary');
                        $('.post-dislike-btn').addClass('text-secondary').removeClass('text-danger');
                    } else {
                        button.addClass('text-secondary').removeClass('text-primary');
                    }
                } else {
                    if (data.disliked) {
                        button.addClass('text-danger').removeClass('text-secondary');
                        $('.post-like-btn').addClass('text-secondary').removeClass('text-primary');
                    } else {
                        button.addClass('text-secondary').removeClass('text-danger');
                    }
                }
            }
        });
    });
    
    // Like/Dislike Comment
    $('.comment-like-btn, .comment-dislike-btn').on('click', function(e) {
        e.preventDefault();
        
        const button = $(this);
        const commentId = button.data('comment-id');
        const url = button.attr('href');
        
        $.ajax({
            url: url,
            type: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(data) {
                // Update like/dislike counts
                $(`#comment-${commentId}-likes-count`).text(data.likes_count);
                $(`#comment-${commentId}-dislikes-count`).text(data.dislikes_count);
                
                // Update buttons
                if (button.hasClass('comment-like-btn')) {
                    if (data.liked) {
                        button.addClass('text-primary').removeClass('text-secondary');
                        $(`.comment-dislike-btn[data-comment-id="${commentId}"]`).addClass('text-secondary').removeClass('text-danger');
                    } else {
                        button.addClass('text-secondary').removeClass('text-primary');
                    }
                } else {
                    if (data.disliked) {
                        button.addClass('text-danger').removeClass('text-secondary');
                        $(`.comment-like-btn[data-comment-id="${commentId}"]`).addClass('text-secondary').removeClass('text-primary');
                    } else {
                        button.addClass('text-secondary').removeClass('text-danger');
                    }
                }
            }
        });
    });
    
    // Toggle reply form
    $('.reply-toggle-btn').on('click', function(e) {
        e.preventDefault();
        const commentId = $(this).data('comment-id');
        $(`#reply-form-${commentId}`).toggle();
    });
    
    // Character counter for comment/reply forms
    $('.comment-input').on('input', function() {
        const maxLength = 500;
        const currentLength = $(this).val().length;
        const remainingChars = maxLength - currentLength;
        
        const counterElement = $(this).siblings('.char-counter');
        counterElement.text(`${remainingChars} characters remaining`);
        
        if (remainingChars < 50) {
            counterElement.addClass('text-danger');
        } else {
            counterElement.removeClass('text-danger');
        }
    });
    
    // Confirm post deletion
    $('#delete-post-btn').on('click', function(e) {
        if (!confirm('Are you sure you want to delete this post? This action cannot be undone.')) {
            e.preventDefault();
        }
    });
    
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Tags input enhancement
    if ($('#id_tags').length) {
        const tagsInput = $('#id_tags');
        const tagsList = $('<div class="tags-list mt-2"></div>');
        tagsInput.after(tagsList);
        
        function renderTags() {
            tagsList.empty();
            const tags = tagsInput.val().split(',').filter(tag => tag.trim() !== '');
            
            tags.forEach(tag => {
                const tagElement = $(`
                    <span class="badge bg-primary me-2 mb-2 p-2">
                        ${tag.trim()}
                        <button type="button" class="btn-close btn-close-white ms-2" style="font-size: 0.5rem;"></button>
                    </span>
                `);
                
                tagElement.find('.btn-close').on('click', function() {
                    const updatedTags = tagsInput.val()
                        .split(',')
                        .filter(t => t.trim() !== tag.trim())
                        .join(', ');
                    tagsInput.val(updatedTags);
                    renderTags();
                });
                
                tagsList.append(tagElement);
            });
        }
        
        tagsInput.on('blur', renderTags);
        tagsInput.on('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                const currentValue = tagsInput.val();
                const currentTag = currentValue.split(',').pop().trim();
                
                if (currentTag !== '') {
                    if (!currentValue.endsWith(',') && currentValue !== '') {
                        tagsInput.val(currentValue + ', ');
                    }
                    renderTags();
                }
            }
        });
        
        // Initial render
        renderTags();
    }
}); 