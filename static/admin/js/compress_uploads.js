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

  var pending = [];

  document.addEventListener('change', function (e) {
    var input = e.target;
    if (!input || input.tagName !== 'INPUT' || input.type !== 'file' || !input.files || !input.files.length) return;
    if (!/(^|-)image$/.test(input.name || '')) return;

    var originalFiles = Array.prototype.slice.call(input.files);
    var task = Promise.all(originalFiles.map(compressImage)).then(function (newFiles) {
      var dt = new DataTransfer();
      newFiles.forEach(function (f) { dt.items.add(f); });
      input.files = dt.files;
    });
    pending.push(task);
    task.then(function () {
      var idx = pending.indexOf(task);
      if (idx > -1) pending.splice(idx, 1);
    });
  }, true);

  document.addEventListener('submit', function (e) {
    if (!pending.length) return;
    var form = e.target;
    if (form.dataset.imgCompressWaiting) return;
    e.preventDefault();
    form.dataset.imgCompressWaiting = '1';
    var submitter = e.submitter;
    Promise.all(pending).then(function () {
      delete form.dataset.imgCompressWaiting;
      if (form.requestSubmit) {
        form.requestSubmit(submitter);
      } else {
        form.submit();
      }
    });
  }, true);
})();
