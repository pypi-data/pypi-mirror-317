from selenium_stealth import stealth
import undetected_chromedriver as uc
import random

# 1. Alterar o User-Agent
def set_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    ]
    return random.choice(user_agents)

# 2. Configurar e iniciar o navegador com undetected_chromedriver
def launch_browser():

    # Configurações para o Chrome
    options = uc.ChromeOptions()

    # Alterar o User-Agent
    options.add_argument(f"user-agent={set_user_agent()}")

    # Default's
    profile = {
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
    }

    options.add_experimental_option('prefs', profile)

    # Configurações para reduzir detecção
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")

    # Inicializar o navegador com undetected_chromedriver
    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        return driver

    except Exception as e:
        print(f"Erro ao iniciar o driver: {e}")
