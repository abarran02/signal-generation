document.querySelectorAll('input[name="formSwitch"]').forEach(radio => {
    radio.addEventListener('change', function() {
      document.querySelectorAll('.form').forEach(form => form.classList.remove('active'));
      document.getElementById(this.value).classList.add('active');
      document.getElementById('dynamicImage').style.display = 'none';
    });
  });

function displayImage(imageUrl) {
    // get all form data and serialize
    const form = document.querySelector('.form.active');
    const url = new URL(form.action);
    const params = new URLSearchParams(new FormData(form));
    params.set('form', 'png');

    // display image on page
    const imgElement = document.getElementById('dynamicImage');
    imgElement.src = `${url.pathname}?${params.toString()}`;
    imgElement.style.display = 'block';
  }

  function redirectInteractive(imageUrl) {
    // get all form data and serialize
    const form = document.querySelector('.form.active');
    const url = new URL(form.action);
    const params = new URLSearchParams(new FormData(form));
    params.set('form', 'graph');

    window.location.href = `${url.pathname}?${params.toString()}`;
  }
  function redirectThreeDim(imageURL) {
    // retrieve form data 
    const form = document.querySelector('.form.active');
    const url = new URL(form.action);
    const params = new URLSearchParams(new FormData(form));
    params.set('form', 'threeDim');

    window.location.href = `${url.pathname}?${params.toString()}`; //opens a new window
  }

