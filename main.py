from PyQt6.QtWidgets import QApplication, QMainWindow
from bandau import Ui_MainWindow
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import csv




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.start.clicked.connect(self.adresas)

    def adresas(self):
        
        url = self.ui.link.text()

        if "https://elenta.lt/" in url:         
            nusta = Options()
            nusta.add_argument('--incognito')
            
            driver = webdriver.Chrome(nusta)
            driver.get(url)     
            
            visaSuma = 0

            with open('informacija.csv', mode='w', newline='', encoding='utf-8') as file:
                irasiti = csv.writer(file)
                irasiti.writerow(['Skelbimo pavadinimas', 'Kaina'])
                source = driver.page_source
                html = BeautifulSoup(source, "html.parser")

                kategorija = html.select_one("span[itemprop='itemListElement'] > span[itemprop='name']")
                kategorija = kategorija.text.strip().replace("»", "")

                skaicius = html.select_one(".counter")
                skaicius = skaicius.text.strip()

                while True:
                    migtukas = driver.find_elements(By.CSS_SELECTOR, '.fc-button-label')
                    if migtukas:
                        migtukas[0].click()

                    
                    for index in html.select(".units-list li"):
                        if index:    
                            pavadinimas = index.select_one(".ad-hyperlink")
                            pavadinimas = pavadinimas.text.strip() if pavadinimas else "Nenurodyta"
                            kaina = index.select_one(".price-box")
                            kaina = kaina.text.strip() if kaina else "0"
                            irasiti.writerow([pavadinimas, kaina])
                            kaina = kaina.replace("€", "").replace(" ", "")
                            visaSuma += int(kaina)

                    kitasPusla = driver.find_elements(By.CSS_SELECTOR, 'li.pagerNextPage')
                    if kitasPusla:
                        kitasPusla[0].click()
                        source = driver.page_source
                        html = BeautifulSoup(source, "html.parser")     
                        sleep(1)
                    else:
                        break      
    
            driver.quit()
            self.ui.atsakymas.setText(f"Kategorija yra: {kategorija} \nPaskelbta skelbimų: {skaicius} \nBendra skelbimų kainų suma: {str(visaSuma)}€")
        else:
            self.ui.atsakymas.setText(f"{url} \nKažką neteisingai įvedėte \nPabandykite dar kartą") 
 
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.setWindowTitle("Jonaitis (kažkas tokio)")
    window.show()
    app.exec()


    