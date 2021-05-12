import requests
from datetime import date, datetime
import time
import selenium_utils
import otp
import winsound
import pygame
import argparse

file = './resources/alert.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.set_volume(1)
parser = argparse.ArgumentParser()
parser.add_argument("mobile", type=int, help="Mobile Number to book for.")
parser.add_argument("email", type=str, help="The dummy email the OTP is forwarded to.")
parser.add_argument("beneficiaries", type=int, help="Total number of beneficiaries registered for your mobile number.")
parser.add_argument('id', nargs='?', const=1, type=int, help="Which beneficiary? 1, 2, etc.")
parser.add_argument("-s", "--selective", action='store_true', help="Filters centers by names specified in centers.txt; Make sure to include a key-word (such as 'apollo'), not a hyper-specific name! (such as 'Apollo Multispeciality Hospital'")
parser.add_argument('--slow', action='store_true', help="Adjusts delays for slow internet.")
args = parser.parse_args()

MOBILE = str(args.mobile)
EMAIL = args.email
VERSION = "2.2.0"
total = args.beneficiaries
beneficiary_id = args.id
if beneficiary_id == None:
    beneficiary_id = 1
delays = dict()
if args.slow:
    delays['mobile_form'] = 3
    delays['empty_pincode'] = 1
    delays['under45_filter'] = 0.4
    delays['load_dashboard'] = 5
else:
    delays['mobile_form'] = 1
    delays['empty_pincode'] = 0.6
    delays['under45_filter'] = 0.15
    delays['load_dashboard'] = 3

pincodes = []
with open('resources/pincodes.txt', 'r') as pincodes_file:
    for pincode in pincodes_file:
        pincode.strip().replace('\n', '')
        pincodes.append(pincode)
if len(pincodes) == 0:
    print("Please enter at least one pincode in pincodes.txt.")

center_keywords = []
with open('resources/center_keywords.txt', 'r') as centers_file:
    for center_keyword in centers_file:
        center_keyword.strip().replace('\n', '')
        center_keywords.append(center_keyword)

alertstring = "Vaccine available at {}, Pincode {}\nRemaining doses: {}\nVaccination type: {}\n"

try:
    assert '@gmail.com' in EMAIL
except:
    print('Your dummy account must be a gmail account.')
    exit()

today = date.today().strftime("%d-%m-%Y")

winsound.Beep(4400, 2500) 
time.sleep(0.25)  

def login(driver, load, click, wait_for_url):
    try:
        mobile = load('/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[1]/ion-grid/form/ion-row/ion-col[2]/ion-item/mat-form-field/div/div[1]/div/input', duration=delays['mobile_form'])
        mobile.send_keys(MOBILE)
        time.sleep(1)
        load('/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[1]/ion-grid/form/ion-row/ion-col[2]/div/ion-button').click()

        OTP = otp.get_otp(EMAIL)
        print(f"OTP: {OTP}")
        otp_form = load('/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col/ion-grid/form/ion-row/ion-col[2]/ion-item/mat-form-field/div/div[1]/div/input')
        otp_form.clear()
        otp_form.send_keys(OTP)
        load('/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col/ion-grid/form/ion-row/ion-col[3]/div/ion-button').click()
        wait_for_url('https://selfregistration.cowin.gov.in/dashboard', duration=180)
        time.sleep(delays['load_dashboard'])
        driver.execute_script('document.querySelector("#main-content > app-beneficiary-dashboard > ion-content > div > div > ion-grid > ion-row > ion-col > ion-grid.beneficiary-box.md.hydrated > ion-row:nth-child(' + str(beneficiary_id+1) + ') > ion-col > ion-grid > ion-row.dose-data.md.hydrated > ion-col:nth-child(2) > ul > li > a").scrollIntoView()')
        
        #Another driver.execute_script to scroll into view the confirmation button, if need be.
        schedule_button = load('/html/body/app-root/ion-app/ion-router-outlet/app-beneficiary-dashboard/ion-content/div/div/ion-grid/ion-row/ion-col/ion-grid[1]/ion-row[' + str(beneficiary_id+1) + ']/ion-col/ion-grid/ion-row[4]/ion-col[2]/ul/li/a')
        driver.execute_script("arguments[0].click();", schedule_button)
        try:
            #driver.execute_script(f'document.querySelector("#main-content > app-beneficiary-dashboard > ion-content > div > div > ion-grid > ion-row > ion-col > ion-grid.beneficiary-box.md.hydrated > ion-row:nth-child({int(total)+3}) > ion-col > div > div:nth-child(2) > div > ion-button".scrollIntoView()')
            confirm_button = load(f'/html/body/app-root/ion-app/ion-router-outlet/app-beneficiary-dashboard/ion-content/div/div/ion-grid/ion-row/ion-col/ion-grid[1]/ion-row[{int(total)+3}]/ion-col/div/div[2]/div/ion-button')
            driver.execute_script("arguments[0].click();", confirm_button)
        except:
            pass
        return 1
    except Exception as e:
        print(e)
        return -1


    
def search(driver, load, click, wait_for_url):
    time_now = datetime.now().time()
    hour = int(str(time_now).split(':')[0])
    start_date = 1
    if hour > 16:
        start_date = 2
    try:
        capture_time = time.strftime("%I:%M:%S %p", time.localtime())
        print(today, capture_time)
        print()
        
        print("-"*115)
        print("-"*115)
        for pincode in pincodes:

            pincode_box = load('/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[2]/mat-form-field/div/div[1]/div/input')
            pincode_box.clear()
            pincode_box.send_keys(pincode)
            load('/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[3]/ion-button').click()
            driver.execute_script('document.querySelector("#c1").click()')
            time.sleep(delays['under45_filter'])
            #print("18+ Filter enabled")
            try:
                centre_name = load(f"/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[1]/mat-list-option/div/div[2]/ion-row/ion-col[1]/div/h5", duration=delays['empty_pincode']).text
            except:
                print("No 18+ centers in this pincode.")
                continue
            ROWS = []
            for row in range(1,8):
                try:
                    centre_name = driver.find_element_by_xpath(f"/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[1]/div/h5").text
                    #print(centre_name.lower())
                    if parser.selective:
                        for center_keyword in center_keywords:
                            if center_keyword.lower() in centre_name.lower():
                                ROWS.append(row)
                    else:
                        ROWS.append(row)
                except:
                    break

            column = 2
            print("Obtained centers. The indices are:", ROWS)
            print('Vaccination Center'+((40-len('Vaccination Center'))*' '), 'Pincode', ' '*2, 'Vaccine Type'+' '*4, 'Date'+((15-len('Date'))*' '), 'Status')
            for row in ROWS:
                for column in range(start_date,start_date+3):
                    try:
                        type1 = f"/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[2]/ul/li[{column}]/div/div/a"
                        vaccines = load(type1)
                        if vaccines.text == 'Booked' or vaccines.text == 'NA':
                            center_name = driver.find_element_by_xpath(f"/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[1]/div/h5").text
                            center_name += (40-len(center_name))*' '
                            vaccine_text = vaccines.text
                            if vaccine_text == 'Booked':
                                vaccine_type = driver.find_element_by_xpath(f'/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[2]/ul/li[{column}]/div/div/div[1]/h5').text
                            else:
                                vaccine_type = 'Unknown'
                            vaccine_type += (16-len(vaccine_type))*' '
                            if column == start_date:
                                print(center_name, pincode, ' '*3, vaccine_type, str(int(today[:2])+column-1).zfill(2)+today[2:]+' '*5,  vaccine_text)
                            else:
                                print(40*' ', ' '*6, ' '*3, vaccine_type, str(int(today[:2])+column-1).zfill(2)+today[2:]+' '*5, vaccine_text)
                            continue
                        if int(vaccines.text) >= 1:
                            try:
                                age_limit = driver.find_element_by_xpath(f'/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[2]/ul/li[{column}]/div/div/div[2]/span').text
                                vaccine_type = driver.find_element_by_xpath(f'/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[2]/ul/li[{column}]/div/div/div[1]/h5').text                        
                                print(age_limit)
                                if '45' in age_limit:
                                    continue
                                elif '18' not in age_limit:
                                    continue
                            except Exception as e:
                                print(e)
                                continue                    
                            
                        vaccines.click()
                        pygame.mixer.music.play()
                        #winsound.Beep(4400, 2500) 
                    except Exception as e:
                        print("Double Slot Error\n")
                        print(e)
                        print()
                        try:
                            for subcolumn in [1,2]:
                                type2 = f"/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[2]/ul/li[{column}]/div[{subcolumn}]/div/a"
                                vaccines = load(type2)
                                if vaccines.text == 'Booked' or vaccines.text == 'NA':
                                    continue
                                vaccines.click()
                                pygame.mixer.music.play()
                        except Exception as e:
                            print('FATAL ERROR')
                            print(e)
                            return
                    load("/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[1]/div/ion-button[2]").click()
                    input("Press Enter to resume.")
                print("-"*115)
                #time.sleep(1)
    except Exception as e:
        print(e)
        return -1

def loopscan():
    driver = selenium_utils.make_driver(profile=3)
    load = selenium_utils.load(driver)
    click = selenium_utils.click(driver)
    wait_for_url = selenium_utils.wait_for_url(driver)
    driver.get("https://selfregistration.cowin.gov.in/")
    login(driver, load, click, wait_for_url)
    count = 0
    ecounter = 0
    while True:
        if (search(driver, load, click, wait_for_url) == -1):
            ecounter += 1
        if (ecounter > 2):
            print("Rate limit reached. Rebooting.")
            winsound.Beep(4400, 250)
            driver.quit()
            break
        if count % 15 == 0:
            driver.refresh()
        if (driver.current_url == "https://selfregistration.cowin.gov.in/"):
            requests.post("https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP", data = {
                "mobile": MOBILE
            })
            time.sleep(2)
            count = 0
        count += 1
        print(f"\n\n\nCOUNT: {count}\n\n\n")

def main():
    while True:
        loopscan()

print(f"Perseverance v{VERSION}")
main()