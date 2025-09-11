(function($) {
    'use strict';

    // Main Virtual Stager class
    class VirtualStager {
        constructor() {
            // DOM elements
            this.form = $('#decor8-staging-form');
            this.uploadArea = $('#decor8-upload-area');
            this.fileInput = $('#decor8-image-upload');
            this.preview = $('#decor8-image-preview');
            this.progress = $('.decor8-vs-progress');
            this.error = $('.decor8-vs-error');
            this.results = $('.decor8-vs-results');
            
            // Bind events
            this.initializeEvents();
        }

        initializeEvents() {
            // Click to browse
            $('.decor8-vs-upload-placeholder').on('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.fileInput.click();
            });

            // Drag and drop handling
            this.uploadArea.on('dragenter dragover', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.uploadArea.addClass('drag-over');
            });

            this.uploadArea.on('dragleave drop', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.uploadArea.removeClass('drag-over');
            });

            this.uploadArea.on('drop', (e) => {
                const files = e.originalEvent.dataTransfer.files;
                if (files.length) {
                    this.fileInput[0].files = files;
                    this.handleFileSelect(files[0]);
                }
            });

            // File input change
            this.fileInput.on('change', (e) => {
                if (e.target.files.length) {
                    this.handleFileSelect(e.target.files[0]);
                }
            });

            // Remove image button
            this.preview.find('.decor8-vs-remove-image').on('click', () => {
                this.resetUpload();
            });

            // Form submission
            this.form.on('submit', (e) => {
                e.preventDefault();
                this.processImage();
            });

            // Start new staging button
            $('.decor8-vs-start-new').on('click', () => {
                this.resetForm();
            });
        }

        handleFileSelect(file) {
            // Validate file type
            if (!file.type.match('image/(jpeg|png)')) {
                this.showError(decor8VS.i18n.invalidFileType);
                return;
            }

            // Validate file size (10MB max)
            if (file.size > 10 * 1024 * 1024) {
                this.showError(decor8VS.i18n.fileTooLarge);
                return;
            }

            // Show preview
            const reader = new FileReader();
            reader.onload = (e) => {
                this.preview.find('img').attr('src', e.target.result);
                this.preview.show();
                $('.decor8-vs-upload-placeholder').hide();
            };
            reader.readAsDataURL(file);
        }

        processImage() {
            // Validate form
            if (!this.validateForm()) {
                console.log('Form validation failed');
                return;
            }

            // Prepare form data
            const formData = new FormData(this.form[0]);
            formData.append('action', 'decor8_process_image');
            formData.append('nonce', decor8VS.nonce);

            // Show progress
            this.showProgress();

            // Send AJAX request
            $.ajax({
                url: decor8VS.ajaxurl,
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: (response) => {
                    if (response.success) {
                        console.log('Image processing completed successfully');
                        this.showResults(response.data);
                    } else {
                        console.log('Server returned error:', response.data.message);
                        this.showError(response.data.message);
                    }
                },
                error: (xhr, status, error) => {
                    console.log('AJAX error:', status, error);
                    this.showError(decor8VS.i18n.processingError);
                },
                complete: () => {
                    this.hideProgress();
                }
            });
        }

        showResults(data) {
            // Update result images
            this.results.find('.decor8-vs-original img').attr('src', this.preview.find('img').attr('src'));
            this.results.find('.decor8-vs-staged img').attr('src', data.staged_image_url);
            
            // Update download button
            this.results.find('.decor8-vs-download').attr('href', data.staged_image_url);

            // Show results section
            this.form.hide();
            this.results.show();
        }

        showProgress() {
            this.progress.show();
            this.form.find('button[type="submit"]').prop('disabled', true);
        }

        hideProgress() {
            this.progress.hide();
            this.form.find('button[type="submit"]').prop('disabled', false);
        }

        showError(message) {
            this.error.find('.decor8-vs-error-message').text(message);
            this.error.show();
            setTimeout(() => {
                this.error.fadeOut();
            }, 5000);
        }

        validateForm() {
            if (!this.fileInput[0].files.length) {
                this.showError(decor8VS.i18n.noFileSelected);
                return false;
            }
            return true;
        }

        resetUpload() {
            this.fileInput.val('');
            this.preview.hide();
            this.preview.find('img').attr('src', '');
            $('.decor8-vs-upload-placeholder').show();
        }

        resetForm() {
            this.resetUpload();
            this.form[0].reset();
            this.form.show();
            this.results.hide();
            this.error.hide();
            this.progress.hide();
        }
    }

    // Initialize when document is ready
    $(document).ready(() => {
        new VirtualStager();
    });

})(jQuery);
