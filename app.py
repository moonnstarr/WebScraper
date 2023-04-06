import pandas as pd
import xlwings as xw
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pythoncom

phone_list = pd.read_csv('stock.csv')
print("============================================================")
print("Input file loaded successfully!")

main_df = pd.DataFrame(columns=['model',
                                    # 'category',
                                    'grade',
                                    # 'wesell',
                                    'webuy_cash',
                                    # 'webuy_voucher',
                                    'low_margin %',
                                    'mid_margin %',
                                    'high_margin %'])

for i, row in phone_list.iterrows():
    website = f"https://uk.webuy.com/search?stext=+{row[0]} {row[1]}&Grade={row[3]}"
    print("================================")
    print(f"{row[0]} {row[1]}")
    print("================================")
    # Selenium and Chrome webscraping configs
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0"

    options = webdriver.ChromeOptions()
    # options.headless = True
    options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    # driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
    driver = webdriver.Chrome(options=options)
    driver.get(website)

    # Wait for the cookie acceptance button to be visible
    wait = WebDriverWait(driver, 10)
    cookie_button = wait.until(EC.visibility_of_element_located((By.ID, "onetrust-accept-btn-handler")))

    # Click the acceptance button
    cookie_button.click()

    # Extracting the data from the website
    phone_models = driver.find_elements(By.XPATH, "//div[@class='desc']")

    # List to append the extracted data
    model = []
    grade = []
    webuy_cash = []
    low_margin = []
    mid_margin = []
    high_margin = []

    print("============================================================")
    print("Accessing the CEX website...")

    # Looping through each phone search results to get the values
    for models in phone_models:
        try:
            name = models.find_element(By.XPATH, ".//span[@class='ais-Highlight']").text
            if name != "":
                model.append(name)
                grade.append(str(name)[-1])
                webuy_cash.append(models.find_element(By.XPATH, ".//div[starts-with(@class,'priceTxt') and starts-with(text(),'WeBuy for cash')]").text)
                low_margin.append(0.20)
                mid_margin.append(0.25)
                high_margin.append(0.30)
            else:
                def null_data():
                    print("============================")
                    print(f"Data extraction unsuccessful for {row[0]} {row[1]}")
                    print("============================")
                    model.append("N/A")
                    grade.append("N/A")
                    webuy_cash.append("N/A")
                    low_margin.append(0.20)
                    mid_margin.append(0.25)
                    high_margin.append(0.30)
        except:
            print("============================")
            print(f"Data extraction unsuccessful for {row[0]} {row[1]}")
            print("============================")
            model.append("N/A")
            grade.append("N/A")
            webuy_cash.append("N/A")
            low_margin.append(0.20)
            mid_margin.append(0.25)
            high_margin.append(0.30)

    print("============================")
    print("Data retrieve in-progres...")
    print("============================")

    # Rearranging the data into a data frame
    df = pd.DataFrame({'model': model,
                       'grade': grade,
                       'webuy_cash': webuy_cash,
                       'low_margin %': low_margin,
                       'mid_margin %': mid_margin,
                       'high_margin %': high_margin})

    first_row = df[:1]

    main_df = main_df.append(first_row, ignore_index=True)
    # main_df = pd.concat([main_df, first_row], axis=0)

final_df = pd.concat([phone_list, main_df], axis=1)

# Converting text into numbers and calculations
final_df['webuy_cash'] = final_df['webuy_cash'].str.replace('WeBuy for cash £', '').astype(float)
final_df['low_margin_cost'] = final_df['webuy_cash'] * 0.80
final_df['mid_margin_cost'] = final_df['webuy_cash'] * 0.75
final_df['high_margin_cost'] = final_df['webuy_cash'] * 0.70
final_df['low_margin %'] = final_df['low_margin %'].map('{:.1%}'.format)
final_df['mid_margin %'] = final_df['mid_margin %'].map('{:.1%}'.format)
final_df['high_margin %'] = final_df['high_margin %'].map('{:.1%}'.format)

print("============================================================")
print("Data rearranged to export")

# Rename columns
final_df = final_df.rename(columns={'Name': 'Supplier_Name',
                                    'Grade': 'Supplier_Grade',
                                    'Qty': 'Supplier_Qty',
                                    'Cost': 'Supplier_Cost'})

final_df = final_df[[
            'Supplier_Name',
            'Capacity',
            'Color',
            'Supplier_Grade',
            'Supplier_Qty',
            'Supplier_Cost',
            'model',
            'grade',
            'webuy_cash',
            'low_margin %',
            'low_margin_cost',
            'mid_margin %',
            'mid_margin_cost',
            'high_margin %',
            'high_margin_cost'
    ]]


def save_to_excel():
    with xw.App(visible=False) as app:
        wb = app.books.open('Template.xlsx')
        wb.sheets['Sheet1'].range('A3').value = final_df
        wb.sheets['Sheet1'].range('3:3').delete()
        wb.save("CEX_Product_Price.xlsx")
    print("============================================================")
    print("Data Export Completed Successfully!")

save_to_excel()
