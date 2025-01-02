import webbrowser

def redirect_to_intesa_online_banking():
    # URL for Intesa Sanpaolo online banking service
    online_banking_url ="https://www.intesasanpaolo.com/it/persone-e-famiglie/login-page.html"
    
    print("🔗 Redirecting you to Intesa Sanpaolo online banking...")
    # Open the URL in the default web browser
    webbrowser.open(online_banking_url)

if __name__ == "__main__":
    redirect_to_intesa_online_banking()
