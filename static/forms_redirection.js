document.querySelectorAll('input[name="formSwitch"]').forEach(radio => {
  radio.addEventListener('change', function() {
    document.querySelectorAll('.form').forEach(form => form.classList.remove('active'));
    document.getElementById(this.value).classList.add('active');
    document.getElementById('dynamicIQvT').style.display = 'none';
    document.getElementById('dynamicIvQ').style.display = 'none';
  });
});

// set the first radio button as checked and first form as active
document.querySelector('input[name="formSwitch"]').checked = true;
document.querySelector('form[class="form"]').classList.add('active');

function displayImage() {
  // get all form data and serialize
  const form = document.querySelector('.form.active');
  const url = new URL(form.action);
  const params = new URLSearchParams(new FormData(form));
  params.set('form', 'png');
  params.set('axes', 'iqvt');

  // display images on page
  const iqvt = document.getElementById('dynamicIQvT');
  iqvt.src = `${url.pathname}?${params.toString()}`;
  iqvt.style.display = 'block';

  params.set('axes', 'ivq');
  const ivq = document.getElementById('dynamicIvQ');
  ivq.src = `${url.pathname}?${params.toString()}`;
  ivq.style.display = 'block';
}

function redirectInteractive() {
  // get all form data and serialize
  const form = document.querySelector('.form.active');
  const url = new URL(form.action);
  const params = new URLSearchParams(new FormData(form));
  params.set('form', 'graph');

  window.location.href = `${url.pathname}?${params.toString()}`;
}

function redirectThreeDim() {
  // retrieve form data
  const form = document.querySelector('.form.active');
  const url = new URL(form.action);
  const params = new URLSearchParams(new FormData(form));
  params.set('form', 'threeDim');

  window.location.href = `${url.pathname}?${params.toString()}`; //opens a new window
}
