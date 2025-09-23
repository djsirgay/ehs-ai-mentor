import json
from datetime import datetime
from typing import List, Dict, Optional

class OnlineStore:
    def __init__(self):
        self.products_file = "store_products.json"
        self.products = self.load_products()
    
    def load_products(self) -> List[Dict]:
        """Load products from file"""
        try:
            with open(self.products_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create safety products organized by departments
            default_products = [
                # PPE Department
                {
                    "id": "safety-helmet-001",
                    "name": "Safety Hard Hat",
                    "description": "ANSI Z89.1 compliant safety helmet with adjustable suspension",
                    "price": 29.99,
                    "category": "PPE",
                    "department": "Personal Protection",
                    "image": "/safety-helmet.jpg",
                    "amazon_url": "https://www.amazon.com/Construction-Approved-LOHASPRO-Climbing-Arborist/dp/B09W9N4BCQ/ref=sr_1_2_sspa?crid=3V4OFEP2X3KB6&dib=eyJ2IjoiMSJ9.-NNKED59iTmzBQFhadOxhclhnxd4szxC795jGn6n8tPITCl4epenthL65zLWQG4FOnmhaOBgXBzeyaJB4aqefhUBS44yNpu1XLsGr8Ad-Q70MKp1H1eFnF2Ad0ctUiDdxtFPpUWgoEAt_IiY-8ljj3bXCSHCkQj6QR12fWBhZK0F2nfj6VyOdOyJ-AhnICU8_L3To3LP4tkx7cSmoIXsf4yuZ84zINlt2d4inAnKMlj2fgxHlVzlnlN07EinqE8ufsFNZPBpuzbmUKJcUQYk1HjQOKNGb67LCvjz6GmcAV4.mj3jpHOj3W1umZWNXXRTv0U7Nq_08ZTwAS-9yGmFkVM&dib_tag=se&keywords=Safety%2BHard%2BHat%2Bgreen&qid=1758566193&sprefix=safety%2Bhard%2Bhat%2Bgreen%2Caps%2C653&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
                    "rating": 4.8
                },
                {
                    "id": "safety-glasses-001", 
                    "name": "Safety Glasses",
                    "description": "ANSI Z87.1 certified safety glasses with anti-fog coating",
                    "price": 12.99,
                    "category": "PPE",
                    "department": "Personal Protection",
                    "image": "/safety-glasses.jpg",
                    "amazon_url": "https://www.amazon.com/TICONN-Glasses-Adjustable-Anti-Fog-Protection/dp/B0CWKTFPH2/ref=sr_1_2_sspa?crid=3JI9AS7H2DW5B&dib=eyJ2IjoiMSJ9.46vPbNg7Iw8I7I6uotZkPQBetFK6DTudKljxrtYQIefS7qPuanWjDY6wzK4BCNIkssChv87R0MDp1pUxYndz340L3iINu88JjQgNY6n51w5_9zlbUzNDrNXDZeGjIiO4Qfp5xGlFSnPbWJHe2NE2A1btAFT3SMDPMi8D5CTcufGHJJ0WXw1sDDU0T6355q__a5U6XMcG_dI0WmD8pButyNLV6XYydWcBqJ8j1OL7fLE8uBynrVhgPb7IylxHVlcCw06Lv2dhAzrowl8c-Qaz6W0gx_fb9b7J2AazTk-37rM.FBGxtnTDjPlQWJxTZRoIY_oP3vsG6FjiV8GvjyppK2g&dib_tag=se&keywords=Safety%2BGlasses%2B-%2BClear%2BLens&qid=1758518586&sprefix=safety%2Bglasses%2B-%2Bclear%2Blens%2Caps%2C345&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
                    "rating": 4.6
                },
                {
                    "id": "work-gloves-001",
                    "name": "Cut-Resistant Work Gloves",
                    "description": "Level A4 cut protection with excellent grip",
                    "price": 18.99,
                    "category": "PPE",
                    "department": "Personal Protection",
                    "image": "/work-gloves.jpg",
                    "amazon_url": "https://www.amazon.com/Schwer-Cut-Touchscreen-Woodworking-Construction/dp/B0D2VTLJXX/ref=sr_1_7?crid=2T3KUSFWQ97LS&dib=eyJ2IjoiMSJ9.qLID1KGCq_f84MDuNVGJqkYje4Rgose57F_XHKK25qXy2_J58AWAvicoAhpvDyop3sMqHpJBTNLpIgiLb1U4FN74VSFvN7PzvlfSdtLaf5Ijtgck1rg61nRcprhpVp39nrRf0AvrXZwDUCas9FZ9S38AzJXQO8WFRvzb1hi0GOY0aQ6OdzLkWEJojwLrRpnDFCsQVlXfrdtaEcPlkNMtutbczle2F1TdT74LV2ryWe_jWWax6ljP3eR2ZJx-WnMwXYHotlw6rQafe8Xrc-8kRIyz9U0qdQPNrVwELrbBGQ0.BX-xG8nHao9jWhpvGxYP23IYAU8ckycW44uiY9axLB0&dib_tag=se&keywords=Cut-Resistant%2BWork%2BGloves&qid=1758518736&sprefix=cut-resistant%2Bwork%2Bgloves%2Caps%2C591&sr=8-7&th=1",
                    "rating": 4.7
                },
                {
                    "id": "safety-vest-001",
                    "name": "High-Visibility Safety Vest",
                    "description": "Class 2 hi-vis vest with reflective stripes",
                    "price": 24.99,
                    "category": "PPE",
                    "department": "Personal Protection",
                    "image": "/safety-vest.jpg",
                    "amazon_url": "https://www.amazon.com/XIAKE-SAFETY-Visibility-Pockets-Standards/dp/B07DC1F7J4/ref=sr_1_5_sspa?crid=PSKQ274LI00X&dib=eyJ2IjoiMSJ9.4y4WXcKykAyp3c2qI9-rJoSy6jodDE2-eWoNLjf0Ikl373j7MTNLlgKsyexOXt0lpxBoNuFjJKGLI4zjCuaOIHRgmkZypIbnJE8pOfb_NwNgq0LdkebL86nLXPGZPr1MD8dPu6_rZl0oKAZTDRk69aSA5GFinmHwAsu5e2BGDsqWg8Ti6AJAftiWFO-2OHK5GxpqjF5AzAUw22XIfDAlTJuQYt15pITxqUMRgAKGlHt1ewdWysqbE_REphUg_jk-aEgBogTJ0tzCfhj7He5TSgXQ1RyF2PGD9T-8TjyyxMw.omBLuHF-VezGNTjJsHwQAL3NzOntmwp0RwNCNw1yejA&dib_tag=se&keywords=High-Visibility%2BSafety%2BVest&qid=1758518830&sprefix=high-visibility%2Bsafety%2Bvest%2Caps%2C420&sr=8-5-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1&psc=1",
                    "rating": 4.5
                },
                # Emergency Department
                {
                    "id": "first-aid-kit-001",
                    "name": "Workplace First Aid Kit",
                    "description": "OSHA compliant first aid kit for 25 people",
                    "price": 89.99,
                    "category": "Emergency",
                    "department": "Emergency Response",
                    "image": "/first-aid-kit.webp",
                    "amazon_url": "https://www.amazon.com/General-Medi-Pieces-Professional-First/dp/B0BZH1NBSS/ref=sr_1_34?crid=3DMVGY8R50T1Q&dib=eyJ2IjoiMSJ9.-7zBcP3Jq2sSxSK736YDdyxi8gJI0g_LJKz824jUJHmsydH7bIViFTqdRqwiDKDQHwphsUh4wX4lC0WsBQnHsiI1qljJANorXvrBpCXhPNv-AQOys_KzGt7O774C9vT_36uI_xbYPtxFYz26y3IuiG7w8-gSEehhAGU-iKii1TPGlX8m6eA19yIZ9qBO40rnUcGn8reRF5YQFoY9jWercMFj4KDPRgYLav9Gh7a4Br2gZZv0FTvu1HWAPOrH3Uq8gC3zBppkbOq_pSpCLSfhWd7clrO4ENTe2SWj8PmPHvI.z7tNh7e2Ce2-p0xoqmJbpmFUqbBm29ES5KYB30IkYNA&dib_tag=se&keywords=Workplace%2BFirst%2BAid%2BKit&qid=1758518898&sprefix=workplace%2Bfirst%2Baid%2Bkit%2Caps%2C317&sr=8-34&th=1",
                    "rating": 4.9
                },
                {
                    "id": "fire-extinguisher-001",
                    "name": "ZYX Fire Extinguisher - 5lb",
                    "description": "Multi-purpose dry chemical fire extinguisher",
                    "price": 45.99,
                    "category": "Emergency",
                    "department": "Emergency Response",
                    "image": "/fire-extinguisher.webp",
                    "amazon_url": "https://www.amazon.com/Ougist-ABC-Powder-Fire-Extinguisher/dp/B0DHGRDCLP/ref=sr_1_59?crid=3QKPKYPA98B4Q&dib=eyJ2IjoiMSJ9.Au9Cm4WJBVRo_uT8xZtpYtF2Qa_Hwq75SFqoqp0ACPXcEEHo22gHHFrNI8WiwESA3Az-1eMK5MgonWe3Q6dwp7i5UoYn_nbWyOCaNXbFrBkvlNjAPt5s9fGtKv501dx1upBoheU2HqWhPjA4CdRoXMPYl8xWSw1ULV9HFGgUqfO6Qh8Z8351uSjhSbMIWijkIkKL6rqFBzAbI8H4ejuWNVWQxYHvSVUl_QElYEZnXS3RuQNETjaB3dtlmck-l4L9Y90BzZtPk9gueHVky_5Eenk-h8pZJiY8EUg7Fr1Bpqg.Z6u4zuuwruAnhQea27JUJF-61Cii7H1PKs3sYkvs2GQ&dib_tag=se&keywords=ABC+Fire+Extinguisher+-+5lb&qid=1758518956&sprefix=abc+fire+extinguisher+-+5lb%2Caps%2C400&sr=8-59",
                    "rating": 4.8
                }
            ]
            self.save_products(default_products)
            return default_products
    
    def save_products(self, products: List[Dict]):
        """Save products to file"""
        with open(self.products_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        self.products = products
    
    def get_all_products(self) -> List[Dict]:
        """Get all products"""
        return self.products
    
    def get_categories(self) -> List[str]:
        """Get unique categories"""
        return list(set(product['category'] for product in self.products))
    
    def get_departments(self) -> List[str]:
        """Get unique departments"""
        return list(set(product['department'] for product in self.products))