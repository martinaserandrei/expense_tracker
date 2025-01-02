import webbrowser

def redirect_to_unicredit_online_banking():
    # URL for Intesa Sanpaolo online banking service
    online_banking_url ="https://www.unicredit.it/wpc/portal/retail/it/login/login/!ut/p/z1/jZDNDoIwEISfhiu7VALoDYOG-Fc5ELAXA0ktTYCSUuX1JepFo8S57eSbnWSAQQ6sLW5SFEaqtqjH-8S8c4xbErsUnbm_W2JyQBqt6Z4EjgPZA8AfChHYP_kJgE2_z4BNVlD8BOKIrDDxfXcZpZQgei9gomQDTNSqfO4RtuUsEMA0v3DNtX3Vo10Z0_ULCy0chsEWSoma29JY-C1Rqd5A_gZC16Q5ymOTBX14B7s6Lp4!/dz/d5/L2dBISEvZ0FBIS9nQSEh/"
    
    print("🔗 Redirecting you to Unicredit online banking...")
    # Open the URL in the default web browser
    webbrowser.open(online_banking_url)

if __name__ == "__main__":
    redirect_to_unicredit_online_banking()