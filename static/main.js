'use strict';

const $checkBtn = document.getElementById('checkBtn');
const $mailText = document.getElementById('mailText');
const $responseText = document.getElementsByClassName('response-text')[0];

$checkBtn.addEventListener('click', async function () {
  const mailContent = $mailText.value;

  if (mailContent.length < 1) {
    // show msg
    return false;
  }

  try {
    console.log('====================================');
    console.log('send req');
    console.log('====================================');
    const body = new FormData();
    body.append('mailContent', mailContent);

    $checkBtn.innerHTML = 'Loading';
    const res = await fetch('/check-email', {
      method: 'POST',
      body,
    });

    console.log('====================================');
    console.log(res);
    console.log('====================================');
    
	const data = await res.json();

	if (data.success) {
      $responseText.innerHTML = `${data.isSpam == 1 ? 'Is spam' : 'Is not spam'}, with probability ${data.probability}`;
    } else {
      throw new Error();
    }
  } catch (err) {
    console.log('====================================');
    console.log(err);
    console.log('====================================');
    $responseText.innerHTML = 'There was an error';
  } finally {
    $checkBtn.innerHTML = 'Check';
  }
});
