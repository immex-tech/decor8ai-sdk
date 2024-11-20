class ImageCompareSlider {
  constructor(container) {
    this.container = container;
    this.handle = container.querySelector('.slider-handle');
    this.beforeImage = container.querySelector('.before-image');
    this.afterImage = container.querySelector('.after-image');
    this.isDragging = false;

    // Set initial position
    this.container.style.setProperty('--clip-pos', '50%');
    this.initializeEvents();
  }

  show() {
    this.container.classList.add('visible');
  }

  hide() {
    this.container.classList.remove('visible');
  }

  setImages(beforeSrc, afterSrc) {
    // Set the images
    this.beforeImage.src = beforeSrc;
    this.afterImage.src = afterSrc || beforeSrc;

    // Show the slider once images are loaded
    Promise.all([
      this.loadImage(this.beforeImage),
      this.loadImage(this.afterImage)
    ]).then(() => {
      this.show();
    }).catch(error => {
      console.error('Error loading images:', error);
      this.hide();
    });
  }

  loadImage(imgElement) {
    return new Promise((resolve, reject) => {
      if (imgElement.complete) {
        resolve();
      } else {
        imgElement.onload = () => resolve();
        imgElement.onerror = () => reject(new Error('Image load failed'));
      }
    });
  }

  clear() {
    this.beforeImage.src = '';
    this.afterImage.src = '';
    this.hide();
  }

  updateSliderPosition(clientX) {
    const rect = this.container.getBoundingClientRect();
    const x = Math.max(0, Math.min(clientX - rect.left, rect.width));
    const pos = (x / rect.width) * 100;
    this.container.style.setProperty('--clip-pos', `${pos}%`);
  }

  initializeEvents() {
    // Mouse events
    this.handle.addEventListener('mousedown', () => this.isDragging = true);
    window.addEventListener('mousemove', (e) => {
      if (this.isDragging) this.updateSliderPosition(e.clientX);
    });
    window.addEventListener('mouseup', () => this.isDragging = false);

    // Touch events
    this.handle.addEventListener('touchstart', (e) => {
      this.isDragging = true;
      e.preventDefault();
    });
    window.addEventListener('touchmove', (e) => {
      if (this.isDragging) {
        this.updateSliderPosition(e.touches[0].clientX);
        e.preventDefault();
      }
    });
    window.addEventListener('touchend', () => this.isDragging = false);
  }

  static createContainer() {
    const container = document.createElement('div');
    container.className = 'image-compare';
    container.innerHTML = `
      <div class="image-labels">
        <span>Before</span>
        <span>After</span>
      </div>
      <img class="before-image" alt="Before">
      <img class="after-image" alt="After">
      <div class="slider-handle"></div>
    `;
    return container;
  }
}

// Helper function to create and initialize a new slider
function createImageCompareSlider(parentElement) {
  const container = ImageCompareSlider.createContainer();
  parentElement.appendChild(container);
  return new ImageCompareSlider(container);
} 