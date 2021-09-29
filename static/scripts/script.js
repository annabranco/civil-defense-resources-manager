const { hash, origin } = window.location;
const hashArray = hash.substring(1).split("&");
const hashParams = {};

hashArray.forEach(param => {
  const paramInfo = param.split('=');
  if (paramInfo.length === 2) {
    hashParams[paramInfo[0]] = decodeURIComponent(paramInfo[1]);
  }
})

if (hashParams['access_token']) {
  const mainSection = document.querySelector('.main__wrapper');
  const header = document.createElement('h2');
  const headerText = document.createTextNode('Аccess token');
  const paragraph1 = document.createElement('p');
  const text1 = document.createTextNode('Copy this Access Token below and use it as Bearer on the authorization header of your requests to this API:')
  const accessTokenArea = document.createElement('textarea');
  const accessTokenText = document.createTextNode(hashParams['access_token'])
  const button = document.createElement('button');
  const textButton = document.createTextNode('Copy token to clipboard');
  const button2 = document.createElement('button');
  const textButton2 = document.createTextNode('Log  out');

  const copyToClipboard = () => {
    navigator.clipboard.writeText(hashParams['access_token']);
    button.innerHTML = 'Copied!';
    button.classList.add('copied');
    button.setAttribute('disabled', 'disabled');

    setTimeout(() => {
      button.innerHTML = 'Copy token to clipboard'
      button.classList.remove('copied');
      button.removeAttribute('disabled', 'disabled');
    }, 5000);
  }

  header.className = 'main__access-level';
  header.append(headerText);

  paragraph1.className = 'main__text';
  paragraph1.append(text1);

  accessTokenArea.className = 'main__textarea';
  accessTokenArea.setAttribute('disabled', 'disabled');

  accessTokenArea.append(accessTokenText);

  button.className = 'main__button';
  button.addEventListener("click", copyToClipboard);
  button.append(textButton);

  button2.className = 'main__button';
  button2.addEventListener("click", () => window.location.href = `${origin}/logout`);
  button2.append(textButton2);

  mainSection.appendChild(header);
  mainSection.appendChild(paragraph1);
  mainSection.appendChild(accessTokenArea);
  mainSection.appendChild(button);
  mainSection.appendChild(button2);

} else {
  const mainSection = document.querySelector('.main__wrapper');
  const paragraph1 = document.createElement('p');
  const paragraph2 = document.createElement('p');
  const button = document.createElement('button');
  const textButton = document.createTextNode('LOG IN');
  const text1 = document.createTextNode('It seems that you haven\'t already logged in.');
  const text2 = document.createTextNode('Please login to get your access token.');

  paragraph1.className = 'main__text';
  paragraph1.append(text1);

  paragraph2.className = 'main__text';
  paragraph2.append(text2);

  button.className = 'main__button';
  button.addEventListener("click", () => window.location.href = `${origin}/login`);
  button.append(textButton);

  mainSection.appendChild(paragraph1);
  mainSection.appendChild(paragraph2);
  mainSection.appendChild(button);
}
