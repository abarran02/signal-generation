document.querySelectorAll('input[name="formSwitch"]').forEach(radio => {
  radio.addEventListener('change', function() {
    document.querySelectorAll('.form').forEach(form => form.classList.remove('active'));
    document.getElementById(this.value).classList.add('active');
    document.getElementById('dynamicIQvT').style.display = 'none';
    document.getElementById('dynamicIvQ').style.display = 'none';
  });
});

document.querySelectorAll('select[class="parent"]').forEach(dropdown => {
  dropdown.addEventListener('change', function() {
    const parent = dropdownSuboptions[this.name];
    const suboptions = parent.suboptions[this.value];
    const subelement = document.getElementById(parent.subelementId);  // get child dropdown
    subelement.innerHTML = "";  // clear subdropdown parent

    for (let i = 0; i < suboptions.length; i++) {
      let newOption = document.createElement('option');
      newOption.value = suboptions[i];
      newOption.innerHTML = suboptions[i];
      subelement.appendChild(newOption);
    }
  });

  dropdown.dispatchEvent(new Event('change'));
});

// save active form for going back from interactive graphs
localStorage.setItem('val', this.value);

// on initial render set the first radio button as checked and first form as active
document.querySelector('input[name="formSwitch"]').checked = true;
if (localStorage.getItem('val') === "undefined") {
  document.querySelector('form[class="form"]').classList.add('active');
} else {
  // otherwise pull from saved data
  document.querySelector(localStorage.getItem('val')).classList.add('active');
}

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
