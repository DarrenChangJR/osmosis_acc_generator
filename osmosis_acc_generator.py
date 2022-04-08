import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth
import requests
from json import loads
import names

email_generator_url = 'https://www.1secmail.com/api/v1/'

def generateEmailAddress():
	r = requests.get(email_generator_url, params = {'action': 'genRandomMailbox'})
	email_address = loads(r.text)[0]
	return email_address


def getVerificationLink(email_address):
	login, domain = email_address.split('@')
	r = requests.get(email_generator_url, params = {'action': 'getMessages', 'login': login, 'domain': domain})

	msg_id = loads(r.text)[0]['id']
	message = requests.get(email_generator_url, params={'action': 'readMessage', 'login': login, 'domain': domain, 'id': msg_id})

	verification_link = loads(message.text)['body'].split('href="')[1].split('"')[0]
	return verification_link

async def main():

	browser = await launch(headless=False, executablePath=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
	page = await browser.newPage()

	await stealth(page)

	await page.goto('https://www.osmosis.org/login?type=create')

	email_address = generateEmailAddress()
	await page.waitForSelector('.create-account-school-email')
	await page.type('.create-account-school-email', email_address)

	first_name = names.get_first_name()
	await page.waitForSelector('.create-account-first-name')
	await page.type('.create-account-first-name', first_name)

	last_name = names.get_last_name()
	await page.waitForSelector('.create-account-last-name')
	await page.type('.create-account-last-name', last_name)


	password = 'freeacc!'
	await page.waitForSelector('.create-account-input-password')
	await page.type('.create-account-input-password', password)

	await page.waitForSelector('.create-account-sign-up')
	await page.click('.create-account-sign-up')

	await page.waitFor(5000)
	verification_link = getVerificationLink(email_address)
	await page.goto(verification_link)

	with open('credentials.txt', 'w') as file:
		file.write(email_address)
		file.write('\n')
		file.write(password)
		file.write('\n')

	await page.waitForSelector('#radio-ft-student')
	await page.click('#radio-ft-student')

	await page.waitForSelector('#type-next-button')
	await page.click('#type-next-button')

	await page.waitForSelector('[data-test-id=MD]')
	await page.click('[data-test-id=MD]')

	await page.waitForSelector('#product-next-button')
	await page.click('#product-next-button')

	await page.waitForSelector('#attending')
	await page.click('#attending', clickCount=2)
	await page.keyboard.type('DC Institute')

	await page.waitForSelector('#pursuingDegree')
	await page.type('#pursuingDegree', 'Medicine (MD)')

	await page.waitForSelector('#classYear')
	await page.type('#classYear', 'First year')

	await page.waitForSelector('#school-next-button')
	await page.click('#school-next-button')

	await page.waitForSelector('[data-test-id=Preclinical]')
	await page.click('[data-test-id=Preclinical]')

	await page.waitForSelector('#stage-next-button')
	await page.click('#stage-next-button')

	await browser.close()

asyncio.get_event_loop().run_until_complete(main())
