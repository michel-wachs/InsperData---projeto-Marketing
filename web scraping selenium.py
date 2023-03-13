from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from unidecode import unidecode
import pandas as pd

import time
import pprint

driver = webdriver.Chrome(executable_path=r"C:\Users\Michel.LAPTOP-16TFAQA2\Downloads\chromedriver_win32\chromedriver.exe")
driver.get("https://www.google.com/travel/hotels/Rio%20de%20Janeiro?gsas=1&rp=CiFYAGAAmgEaCggvbS8wNmdtchIOUmlvIGRlIEphbmVpcm-oAgA&ts=CAESABo6ChwSGgoIL20vMDZnbXI6DlJpbyBkZSBKYW5laXJvEhoSFAoHCOYPEAUYHhIHCOYPEAUYHxgBMgIQAA&ved=0CAAQ5JsGahcKEwigl4aDgdH3AhUAAAAAHQAAAAAQbg")


def get_info(arg):    
    
    arg.click()
    time.sleep(.5)
    driver.switch_to.window(driver.window_handles[1])
    
    driver.find_element_by_xpath('//*[@id="overview"]/span').click()
    time.sleep(.5)
    
    try:
        driver.find_element_by_class_name('RZOZe')
        print("achou")
    except:
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        print("não achou")
        return [], [], [], []   #, []
    

    name = driver.find_element_by_class_name('fZscne').text

    price = driver.find_element_by_class_name('hYxGrb').text.split("\nOFERTA")[0]
    price = price.split("/")[0]
    price = float(price.split(" ")[-1])
    
    total_score = float(driver.find_element_by_class_name('RZOZe').text.replace(',', '.'))
    total_number = driver.find_element_by_class_name('eS7K5e').text.split(" ")[0]
        
    '''driver.find_element_by_xpath('//*[@id="reviews"]/span').click()
        
    total_score = float(driver.find_element_by_class_name('BARtsb').text.replace(',', '.'))
    total_number = float(driver.find_element_by_class_name('YRxmGc').text.split(" ")[0])

    body = driver.find_element_by_tag_name('body')
    while True:
        body.send_keys(Keys.PAGE_DOWN)
        temp = driver.find_elements_by_class_name("bKhjM")
        if len(temp) > 50 or len(temp) == total_number:
            break
        
    reviews = driver.find_elements_by_class_name("bKhjM")
    for aval in reviews:
        try:
            aval.find_element_by_class_name('Jmi7d').click()
        except:
            1

    review_response =[]
    for review in reviews:
        text = unidecode(review.find_element_by_class_name('K7oBsc').text)
        score = review.find_element_by_class_name('MfbzKb').text.split('/')[0]
        score = float(score.replace(",", "."))
        review_response.append([score, text])'''

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    return name, price, total_score, total_number   #, review_response


if __name__ == "__main__":
    response = pd.DataFrame()
    #avaliacoes = pd.DataFrame()
    
    '''corpo = driver.find_element_by_tag_name('body')
    while True:
        corpo.send_keys(Keys.PAGE_DOWN)
        thoteis = driver.find_elements_by_class_name("kY4wqf")
        if len(thoteis) > 50:
            break''' #caso não tenha botão de proxima pagina mas seja para descer a pagina
    
    hotels = driver.find_elements_by_class_name("PVOOXe")
        
    #avaliacoes["Nota", "Avaliações", "Nome"] = pd.Series()
    
    response["Nome", "Preço", "Score", "Num de Aval"] = pd.Series()
    
    
    for i in range(1,10):
        for hotel in hotels[0:]:
            name, price, total_score, total_number = get_info(hotel)    #, review_response   
            
            response = response.append({"Nome": name, 
                                        "Preço": price, 
                                        "Score": total_score, 
                                        "Num de Aval": total_number}, ignore_index = True)
            
            '''for j in range(len(review_response)):
                avaliacoes = avaliacoes.append({"Nota": review_response[j][0],
                                                "Avaliações": review_response[j][1],
                                                "Nome": name}, ignore_index = True)'''
        
        if i == 1:
            prox = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div[2]/div[1]/div/main/div/c-wiz/div[1]/div[7]/button'
        else:
            prox = '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/div[2]/div[2]/div[1]/div/main/div/c-wiz/div[1]/div[7]/button[2]'
        driver.find_element_by_xpath(prox).click()
        time.sleep(1)
        
        pag_atual = driver.current_url
        driver.get(pag_atual)
        hotels = driver.find_elements_by_class_name("PVOOXe") 

    
    #pprint.pprint(avaliacoes)
    pprint.pprint(response)
    driver.close()
    
    response.to_excel(r'C:\Users\Michel.LAPTOP-16TFAQA2\Documents\Michel\Insper\Entidades\Insper Data\Marketing 2022.1\Base_selenium.xlsx', index = False)
    



