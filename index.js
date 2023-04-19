const puppeteer = require('puppeteer');
const { GoogleSpreadsheet } = require('google-spreadsheet');
const nodemailer = require('nodemailer');

const creds = require(process.env.SHEET_CREDS);

exports.main = async () => {
  const username = process.env.VANGUARD_USER;
  const password = process.env.VANGUARD_PASS;
  const sheetId = process.env.SHEET_ID;
  const mail_user = process.env.MAIL_USER;
  const mail_pass = process.env.MAIL_PASS;

  // Step 1: Navigate to vanguardinvestor.co.uk/login
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const pageUrl = 'https://login.vanguardinvestor.co.uk/login?state=hKFo2SB6ajd4YVVxNldoNE1QUmprMEw5SEsxelhxNWhuVnJTSaFupWxvZ2luo3RpZNkgaFIzU3VaZE9WM3JnempPTC10cGNfTmhTVFAzV0ZLMlWjY2lk2SBVbzlvcTgycGFONldCQ3FtSlp0S0puTkVqY2p2aTFtMw&client=Uo9oq82paN6WBCqmJZtKJnNEjcjvi1m3&protocol=oauth2&nonce=lNfr3NGO2NjeeyJyGqLzkNom&response_type=code&code_challenge_method=S256&audience=https%3A%2F%2Finternational.vanguard.com&code_challenge=kc1NQLkzLukahHFFvTmyohQ0jz9JNF530P3tSs49_rE&response_mode=query&redirect_uri=https%3A%2F%2Fsecure.vanguardinvestor.co.uk%2Flogin-callback&scope=openid%20offline_access';
  
  console.log('Navigate to the Vanguard login page');
  await page.goto(pageUrl);

  // Step 2: Login using the provided credentials
  await page.type('#vg-auth0-login-username', username);
  await page.type('#vg-auth0-login-password', password);

  console.log('Click login');
  await page.click('#vg-sign-in-header-1');

  const rateOfReturnXPath = '/html/body/div[4]/div/div[1]/div/div[2]/div[1]/div[3]/div[2]/div/div/div/div[1]/div[3]/div/div/div[1]/div/div/span';
  // Wait for the page to load after login
  await page.waitForXPath(rateOfReturnXPath);  

  // Step 3: Extract personal rate of return from the page
  const [rateOfReturnElement] = await page.$x(rateOfReturnXPath);
  const rateOfReturn = await page.evaluate(el => el.textContent, rateOfReturnElement);
  await browser.close();

  // Step 4: Send it to the specified Google Sheet
  const doc = new GoogleSpreadsheet(sheetId);
  console.log('Open the Google sheet')
  await doc.useServiceAccountAuth(creds);
  await doc.loadInfo();
  const sheet = doc.sheetsByIndex[0];
  const datetime = new Date().toString();

  console.log('Write the rate of return to the worksheet')
  await sheet.addRow([ datetime.toString(), rateOfReturn ]);

  // Step 5: Send email if rate of return is positive
  if (parseFloat(rateOfReturn) >= 0) {
    sendMail(rateOfReturn);
  }
}

function sendMail(rateOfReturn) {
  const mail_user = process.env.MAIL_USER;
  const mail_pass = process.env.MAIL_PASS;
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: mail_user,
      pass: mail_pass //'tsgqgrhefpeweugo'
    }
  });
  
  const mailOptions = {
    from: mail_user,
    to: mail_user,
    subject: 'Sell Vanguard ' + rateOfReturn,
    text: 'Vanguard investment net positive with rate of return ' + rateOfReturn + ', sell! sell! sell!'
  };
  
  transporter.sendMail(mailOptions, function(error, info){
    if (error) {
   console.log(error);
    } else {
      console.log('Email sent: ' + info.response);
      // do something useful
    }
  });
}


