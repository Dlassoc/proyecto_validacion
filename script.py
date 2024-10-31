from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException, ElementClickInterceptedException
import time

driver = webdriver.Chrome()

try:
    driver.get('http://127.0.0.1:8000/') 
    print("Página cargada.")

    origin_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'flight-from'))
    )

    origin_input.click() 
    time.sleep(1) 

    nyc_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'del'))
    )
    nyc_option.click() 

    destination_input = driver.find_element(By.ID, 'flight-to')
    destination_input.click()
    time.sleep(1)  

    nrt_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'BOM'))
    )
    nrt_option.click()
    
    departure_date_input = driver.find_element(By.ID, 'depart_date')
    departure_date_input.send_keys('08122024')

    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
    )

    submit_button.click()

except UnexpectedAlertPresentException as e:
    alert = driver.switch_to.alert
    print("Alerta detectada:", alert.text)
    alert.accept()

except NoSuchElementException as e:
    print("Un elemento no fue encontrado:", e)

finally:
    time.sleep(10)
    driver.quit()
    print("Navegador cerrado.")
