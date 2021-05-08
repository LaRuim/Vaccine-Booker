import requests
from datetime import date, datetime
import time
import selenium_utils
import otp
import winsound
import pygame
import argparse

file = './resources/sugar.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.set_volume(1)
parser = argparse.ArgumentParser()
parser.add_argument("mobile", type=int, help="Mobile Number to book for")
parser.add_argument("email", type=str, help="The dummy email the OTP is forwarded to.")
args = parser.parse_args()

MOBILE = str(args.mobile)
EMAIL = args.email

pincodes = [560011, 560017, 560060, 560076]
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
        requests.post("https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP", data = {
            "mobile": MOBILE
        })
        OTP = otp.get_otp(EMAIL)
        print(f"OTP: {OTP}")
        mobile = load('/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[1]/ion-grid/form/ion-row/ion-col[2]/ion-item/mat-form-field/div/div[1]/div/input', duration=3)
        time.sleep(1)
        mobile.send_keys(MOBILE)
        time.sleep(1)
        load('/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[1]/ion-grid/form/ion-row/ion-col[2]/div/ion-button').click()
        time.sleep(1)

        otp_form = load('/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col/ion-grid/form/ion-row/ion-col[2]/ion-item/mat-form-field/div/div[1]/div/input')
        otp_form.clear()
        otp_form.send_keys(OTP)
        load('/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col/ion-grid/form/ion-row/ion-col[3]/div/ion-button').click()
        wait_for_url('https://selfregistration.cowin.gov.in/dashboard', duration=180)
        time.sleep(3)

    

        #load('/html/body/app-root/ion-app/ion-router-outlet/app-beneficiary-dashboard/ion-content/div/div/ion-grid/ion-row/ion-col/ion-grid[1]/ion-row[3]/ion-col/ion-grid/ion-row[4]/ion-col[2]/ul/li/a').click()
        load('/html/body/app-root/ion-app/ion-router-outlet/app-beneficiary-dashboard/ion-content/div/div/ion-grid/ion-row/ion-col/ion-grid[1]/ion-row[3]/ion-col/ion-grid/ion-row[4]/ion-col[2]/ul/li[1]/a').click()
        time.sleep(1)

        load('/html/body/app-root/ion-app/ion-router-outlet/app-beneficiary-dashboard/ion-content/div/div/ion-grid/ion-row/ion-col/ion-grid[1]/ion-row[5]/ion-col/div/div[2]/div/ion-button').click()

    except Exception as e:
        print(e)
        return -1

    
def search(driver, load, click, wait_for_url):
    try:
        capture_time = time.strftime("%I:%M:%S %p", time.localtime())
        print(today, capture_time)
        print()
        print('Vaccination Center'+((40-len('Vaccination Center'))*' '), 'Pincode', ' '*2, 'Vaccine Type'+' '*4, 'Date'+((15-len('Date'))*' '), 'Status')
        print("-"*115)
        print("-"*115)
        for pincode in pincodes:

            pincode_box = load('/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[2]/mat-form-field/div/div[1]/div/input')
            pincode_box.clear()
            pincode_box.send_keys(pincode)
            load('/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[3]/ion-button').click()

            #print(session, center, centers, sep='\n\n')
            #vaccines = session['available_capacity']
            #slots = ' '.join(session['slots'])    

            #row = center_names.index(center['name'])+1
            centre_name = load(f"/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[1]/mat-list-option/div/div[2]/ion-row/ion-col[1]/div/h5").text
            
            ROWS = []
            for row in range(1,8):
                try:
                    centre_name = driver.find_element_by_xpath(f"/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[1]/div/h5").text
                    #print(centre_name.lower())
                    if 'manipal' in centre_name.lower() or 'apollo' in centre_name.lower() or 'bgs' in centre_name.lower():
                        ROWS.append(row)
                except:
                    break
            #column = int(session['date'].split('-')[0]) - int(today.split('-')[0]) + 1
            column = 2

            #print(ROWS)
            #print(row, column)
            #print(session['date'], center['name'])

            for row in ROWS:
                for column in range(1,7):
                    try:
                        type1 = f"/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[2]/ul/li[{column}]/div/div/a"
                        vaccines = load(type1)
                        if vaccines.text == 'Booked' or vaccines.text == 'NA':
                            center_name = load(f"/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[1]/div/h5").text
                            center_name += (40-len(center_name))*' '
                            vaccine_text = vaccines.text
                            if vaccine_text == 'Booked':
                                vaccine_type = load(f'/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[2]/ul/li[{column}]/div/div/div[1]/h5').text
                            else:
                                vaccine_type = 'Unknown'
                            vaccine_type += (16-len(vaccine_type))*' '
                            if column == 1:
                                print(center_name, pincode, ' '*3, vaccine_type, str(int(today[:2])+column-1).zfill(2)+today[2:]+' '*5,  vaccine_text)
                            else:
                                print(40*' ', ' '*6, ' '*3, vaccine_type, str(int(today[:2])+column-1).zfill(2)+today[2:]+' '*5, vaccine_text)
                            continue
                        if int(vaccines.text) >= 1:
                            try:
                                age_limit = load(f'/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[2]/ul/li[{column}]/div/div/div[2]/span').text
                                vaccine_type = load(f'/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[8]/div/div/mat-selection-list/div[{row}]/mat-list-option/div/div[2]/ion-row/ion-col[2]/ul/li[{column}]/div/div/div[1]/h5').text                        
                                print(age_limit)
                                if '45' in age_limit:
                                    continue
                                elif '18' not in age_limit:
                                    continue
                            except Exception as e:
                                print("NOOOOOOOOOO", e)
                                continue                    
                            
                        vaccines.click()
                        #winsound.Beep(4400, 2500) 
                        time.sleep(0.25)    
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
                                time.sleep(0.25)  
                        except Exception as e:
                            print('FATAL ERROR')
                            print(e)
                            return
                    load("/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[1]/div/ion-button[2]").click()
                    pygame.mixer.music.play()
                    input()
                    try:
                        load("/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row[3]/ion-col/div/ion-button").click()
                    except:
                        print('THIS IS WHAT HELPS!')
                        load("/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row[3]/ion-col/div/ion-button//button").click()
                    winsound.Beep(4400, 25000)
                    print(alertstring.format('Something', pincode, vaccines.text, vaccine_type))
                    #print(f"Nothing at {center['name']}")
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
        if (ecounter > 5):
            print("Rate limit reached. Rebooting.")
            winsound.Beep(4400, 2500)
            driver.quit()
            break
        if count % 15 == 0:
            driver.refresh()
        if (driver.current_url == "https://selfregistration.cowin.gov.in/"):
            requests.post("https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP", data = {
                "mobile": MOBILE
            })
            time.sleep(2)
            with open("logout.txt", "a+") as logs:
                logs.write(str(count)+"\n")
                count = 0
        count += 1
        print(f"\n\n\nCOUNT: {count}\n\n\n")

def main():
    while True:
        loopscan()

main()