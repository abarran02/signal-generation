let buttonSelected = this.value;
document.querySelectorAll('input[name="formSwitch"]').forEach(radio => {
  radio.addEventListener('change', function() {
    document.querySelectorAll('.form').forEach(form => form.classList.remove('active'));
    document.getElementById(this.value).classList.add('active');
    document.getElementById('dynamicImage').style.display = 'none';
  });
});

// set the first radio button as checked and first form as active
document.querySelector('input[name="formSwitch"]').checked = true;
document.querySelector(localStorage.getItem('val')).classList.add('active');

function displayImage() {
  // get all form data and serialize
  const form = document.querySelector('.form.active');
  const url = new URL(form.action);
  const params = new URLSearchParams(new FormData(form));
  params.set('form', 'png');

  // display image on page
  const imgElement = document.getElementById('dynamicImage');
  imgElement.src = `${url.pathname}?${params.toString()}`;
  imgElement.style.display = 'block';
  localStorage.setItem('val', this.value);
}

function redirectInteractive() {
  // get all form data and serialize
  const form = document.querySelector('.form.active');
  const url = new URL(form.action);
  const params = new URLSearchParams(new FormData(form));
  params.set('form', 'graph');
  localStorage.setItem('val', this.value);

  window.location.href = `${url.pathname}?${params.toString()}`;
}

function redirectThreeDim() {
  // retrieve form data
  const form = document.querySelector('.form.active');
  const url = new URL(form.action);
  const params = new URLSearchParams(new FormData(form));
  params.set('form', 'threeDim');
  localStorage.setItem('val', this.value);

  window.location.href = `${url.pathname}?${params.toString()}`; //opens a new window
}
