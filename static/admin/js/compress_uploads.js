(function () {
  'use strict';

  var MAX_DIMENSION = 1600;
  var JPEG_QUALITY = 0.82;
  var SKIP_UNDER_BYTES = 700 * 1024;

  function compressImage(file) {
    return new Promise(function (resolve) {
      if (!file.type || file.type.indexOf('image/') !== 0 || file.type === 'image/svg+xml' || file.size < SKIP_UNDER_BYTES) {
        resolve(file);
        return;
      }
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () {
        URL.revokeObjectURL(url);
        var scale = Math.min(1, MAX_DIMENSION / Math.max(img.width, img.height));
        var canvas = document.createElement('canvas');
        canvas.width = Math.round(img.width * scale);
        canvas.height = Math.round(img.height * scale);
        var ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        canvas.toBlob(function (blob) {
          if (!blob || blob.size >= file.size) {
            resolve(file);
            return;
          }
          var newName = file.name.replace(/\.(png|jpe?g|webp|gif|bmp)$/i, '') + '.jpg';
          resolve(new File([blob], newName, { type: 'image/jpeg', lastModified: Date.now() }));
        }, 'image/jpeg', JPEG_QUALITY);
      };
      img.onerror = function () {
        URL.revokeObjectURL(url);
        resolve(file);
      };
      img.src = url;
    });
  }

  var pendingCount = 0;
  var submitButtons = [];

  function setButtonsDisabled(disabled) {
    if (!submitButtons.length) {
      submitButtons = Array.prototype.slice.call(document.querySelectorAll('.submit-row input[type="submit"]'));
    }
    submitButtons.forEach(function (btn) {
      btn.disabled = disabled;
      btn.style.opacity = disabled ? '0.6' : '';
    });
  }

  document.addEventListener('change', function (e) {
    var input = e.target;
    if (!input || input.tagName !== 'INPUT' || input.type !== 'file' || !input.files || !input.files.length) return;
    if (!/(^|-)image$/.test(input.name || '')) return;

    var originalFiles = Array.prototype.slice.call(input.files);
    pendingCount += 1;
    setButtonsDisabled(true);

    Promise.all(originalFiles.map(compressImage)).then(function (newFiles) {
      var dt = new DataTransfer();
      newFiles.forEach(function (f) { dt.items.add(f); });
      input.files = dt.files;
    }).catch(function () {
      // Keep the original file selection if compression fails for any reason.
    }).then(function () {
      pendingCount -= 1;
      if (pendingCount <= 0) {
        pendingCount = 0;
        setButtonsDisabled(false);
      }
    });
  }, true);
})();
