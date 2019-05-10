'''
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File: pay_constants.py
# Project: core.wecare.id
# File Created: Wednesday, 5th December 2018 12:07:34 am
# 
# Author: Arif Dzikrullah
#         ardzix@hotmail.com>
#         https://github.com/ardzix/>
# 
# Last Modified: Wednesday, 5th December 2018 12:07:34 am
# Modified By: arifdzikrullah (ardzix@hotmail.com>)
# 
# Handcrafted and Made with Love
# Copyright - 2018 Wecare.Id, wecare.id
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


from decimal import Decimal

AVAILABLE_PAYMENT_TYPE = [
    "wallet", 
    "credit-card", 
    "debit-card", 
    "credit-card-direct"
]

# fees 
YUNA_SHARE = Decimal(0.1)
FASPAY_CREDIT_CARD_FEES = Decimal(0.0285)

BILL_TYPE_CHOICES = (
    ("shipping", "Shipping Fee"),
    ("handling fee", "Handling Fee"),
    ("Campaign", "Campaign / Discount / Promotion"),
)
DELIVERY_STATUSES = (
    ('delivered', "Delivered"),
    ('not-received', "Not Received"),
)
CONFIRM_STATUSES = (
    ('accept', "Accept"),
    ('cancel', "Cancel/Refund"),
)
WEIGHT_UNIT_CHOICES = (
    (1, 'Kg'),
)
QUANTITY_UNIT = (
    (1, 'Pieces'),
    (2, 'Roll'),
)
STORE_TYPE_CHOICES = ( 
    (1, 'Virtual'),
    (2, 'Physical'),
)
TRANSACTION_TYPE_CHOICES = (
    (1, 'Online'),
    (2, 'Offline'),
)
CLEARENCE_TYPE_CHOICES = (
    ("order", "Order"),
    ("discount", "Discount or Coupon"),
)
CLEARENCE_STATUSES = (
    ("pending", "Pending"),
    ("success", "Success"),
    ("failed", "Failed"),
)
PREORDER_STATUSES = (
    ("requested", "Requested"),
    ("order-ready", "Order Ready"),
    ("not-available", "Product Not Available"), 
)
TRANSACTION_STATE_CHOICES = (
    ('transaction-start', 'Start Transaction'), ## ORDER BEGIN
    ('payment-waiting', 'Waiting for Payment'),
    ('payment-paid', 'Paid by Buyer'),
    ('payment-expired', 'Payment Expired'),
    ('ordered-pre', 'Pre Ordered'), ## BUYER PRE ORDER
    ('order-on-process', 'Order On Process'), ## BUYER ORDER ON PROCESS
    ('ready-to-pickup', 'Ready to Pick Up'), 
    ('picked-up', 'Picked Up'),
    ('on-delivery', 'On Delivery'), ## SELLER ON DELIVERY : COD OR SHIPPING
    ('received', 'Received'), ## SELLER ON DELIVERY : COD OR SHIPPING
    ('transaction-end', 'End Transaction'), ## ORDER DONE. PRODUCT ALREADY RECEIVED BY BUYER
    ('order-cancelled', 'Cancel Order'), ## PURGE / CANCEL EVERYTHING; NOT YET USED
    ('not-available', 'Order Not Available'), ## ITEM OR ORDER NOT AVAILABLE
    ('not-received', 'Not Received'), ## BUYER NOT RECEIVED
)
PAYMENT_TYPE_CHOICES = (
    ('order', 'Order'),
    ('topup', 'Top Up')
)
ORDER_STATUSES = TRANSACTION_STATE_CHOICES
ITEM_STATUSES = ORDER_STATUSES
ORDER_TYPE_CHOICES = (
    (1, 'Retail'),
    (2, 'Booking'),
    (3, 'Subscription'),
)
HANDLE_COST_CHOICES = (
    (1, 'Credit Card Payment Gateway Fee'),
    (2, 'Credit Card MDR (Merchant Discount Rate)'),
)
BILL_STATUSES = (
    ('authorize', 'Authorized'),
    ('capture', 'Captured'),
    ('settlement', 'Settled'),
    ('deny', 'Denied'),
    ('pending', 'Pending'),
    ('cancel', 'Canceled'),
    ('refund', 'Refunded'),
    ('partial_refund', 'Partially Refunded'),
    ('chargeback', 'Charged Back'),
    ('partial_chargeback', 'Partially Charged Back'),
    ('expire', 'Expired'),
    ('failure', 'Failed'),
)
PAYMENT_STATUSES = BILL_STATUSES
INVOICE_STATUSES = BILL_STATUSES
CASHOUT_STATUSES = (
    ('pending', 'Pending'),
    ('processed', 'On Process'),
    ('paid', 'Paid'),
    ('not-paid', 'Not Paid'),
)
TOPUP_STATUSES = (
    ("pending", "Pending"),
    ("success", "Approved"),
    ("failed", "Failed"),
)
SUBSCRIPTION_CHARGE_METHOD = (
    (1, "Credit Card"),
    (2, "Wallet")
)
BANK_CHOICES = (
    ("ANGLOMAS", "Anglomas International Bank"),
    ("BANGKOK", "Bangkok Bank"),
    ("AGRIS", "Bank Agris"),
    ("AGRONIAGA", "Bank BRI Agroniaga"),
    ("AMAR", "Bank Amar Indonesia (formerly Anglomas International Bank)"),
    ("ANDARA", "Bank Andara"),
    ("ANZ", "Bank ANZ Indonesia"),
    ("ARTA_NIAGA_KENCANA", "Bank Arta Niaga Kencana"),
    ("ARTHA", "Bank Artha Graha International"),
    ("ARTOS", "Bank Artos Indonesia"),
    ("BISNIS_INTERNASIONAL", "Bank Bisnis Internasional"),
    ("BJB", "Bank BJB"),
    ("BJB_SYR", "Bank BJB Syariah"),
    ("BNI_SYR", "Bank BNI Syariah"),
    ("BNP_PARIBAS", "Bank BNP Paribas"),
    ("BUKOPIN", "Bank Bukopin"),
    ("BUMI_ARTA", "Bank Bumi Arta"),
    ("CAPITAL", "Bank Capital Indonesia"),
    ("BCA", "Bank Central Asia (BCA)"),
    ("BCA_SYR", "Bank Central Asia (BCA) Syariah"),
    ("CHINATRUST", "Bank Chinatrust Indonesia"),
    ("CIMB", "Bank CIMB Niaga"),
    ("COMMONWEALTH", "Bank Commonwealth"),
    ("DANAMON", "Bank Danamon"),
    ("DANAMON_UUS", "Bank Danamon UUS"),
    ("DBS", "Bank DBS Indonesia"),
    ("DINAR_INDONESIA", "Bank Dinar Indonesia"),
    ("DKI", "Bank DKI"),
    ("DKI_UUS", "Bank DKI UUS"),
    ("FAMA", "Bank Fama International"),
    ("GANESHA", "Bank Ganesha"),
    ("HANA", "Bank Hana"),
    ("HARDA_INTERNASIONAL", "Bank Harda Internasional"),
    ("HIMPUNAN_SAUDARA", "Bank Himpunan Saudara 1906"),
    ("ICBC", "Bank ICBC Indonesia"),
    ("INA_PERDANA", "Bank Ina Perdania"),
    ("INDEX_SELINDO", "Bank Index Selindo"),
    ("JASA_JAKARTA", "Bank Jasa Jakarta"),
    ("JTRUST", "Bank JTrust Indonesia (formerly Bank Mutiara)"),
    ("KESEJAHTERAAN_EKONOMI", "Bank Kesejahteraan Ekonomi"),
    ("MANDIRI", "Bank Mandiri"),
    ("MASPION", "Bank Maspion Indonesia"),
    ("MAYAPADA", "Bank Mayapada International"),
    ("MAYBANK", "Bank Maybank"),
    ("MAYBANK_SYR", "Bank Maybank Syariah Indonesia"),
    ("MAYORA", "Bank Mayora"),
    ("MEGA", "Bank Mega"),
    ("MESTIKA_DHARMA", "Bank Mestika Dharma"),
    ("MITRA_NIAGA", "Bank Mitra Niaga"),
    ("MIZUHO", "Bank Mizuho Indonesia"),
    ("MNC_INTERNASIONAL", "Bank MNC Internasional"),
    ("MUAMALAT", "Bank Muamalat Indonesia"),
    ("MULTI_ARTA_SENTOSA", "Bank Multi Arta Sentosa"),
    ("NATIONALNOBU", "Bank Nationalnobu"),
    ("BNI", "Bank Negara Indonesia (BNI)"),
    ("NUSANTARA_PARAHYANGAN", "Bank Nusantara Parahyangan"),
    ("OCBC", "Bank OCBC NISP"),
    ("OCBC_UUS", "Bank OCBC NISP UUS"),
    ("BAML", "Bank of America Merill-Lynch"),
    ("BOC", "Bank of China (BOC)"),
    ("INDIA", "Bank of India Indonesia"),
    ("TOKYO", "Bank of Tokyo Mitsubishi UFJ"),
    ("OKE", "Bank Oke Indonesia (formerly Bank Andara)"),
    ("PANIN", "Bank Panin"),
    ("PANIN_SYR", "Bank Panin Syariah"),
    ("PERMATA", "Bank Permata"),
    ("PERMATA_UUS", "Bank Permata UUS"),
    ("QNB_INDONESIA", "Bank QNB Indonesia (formerly Bank QNB Kesawan)"),
    ("RABOBANK", "Bank Rabobank International Indonesia"),
    ("BRI", "Bank Rakyat Indonesia (BRI)"),
    ("RESONA", "Bank Resona Perdania"),
    ("ROYAL", "Bank Royal Indonesia"),
    ("SAHABAT_SAMPOERNA", "Bank Sahabat Sampoerna"),
    ("SBI_INDONESIA", "Bank SBI Indonesia"),
    ("SHINHAN", "Bank Shinhan Indonesia (formerly Bank Metro Express)"),
    ("SINARMAS", "Bank Sinarmas"),
    ("SINARMAS_UUS", "Bank Sinarmas UUS"),
    ("MITSUI", "Bank Sumitomo Mitsui Indonesia"),
    ("BRI_SYR", "Bank Syariah BRI"),
    ("BUKOPIN_SYR", "Bank Syariah Bukopin"),
    ("MANDIRI_SYR", "Bank Syariah Mandiri"),
    ("MEGA_SYR", "Bank Syariah Mega"),
    ("BTN", "Bank Tabungan Negara (BTN)"),
    ("BTN_UUS", "Bank Tabungan Negara (BTN) UUS"),
    ("TABUNGAN_PENSIUNAN_NASIONAL", "Bank Tabungan Pensiunan Nasional"),
    ("UOB", "Bank UOB Indonesia"),
    ("VICTORIA_INTERNASIONAL", "Bank Victoria Internasional"),
    ("VICTORIA_SYR", "Bank Victoria Syariah"),
    ("WOORI", "Bank Woori Indonesia"),
    ("WOORI_SAUDARA", "Bank Woori Saudara Indonesia 1906 (formerly Bank Himpunan Saudara and Bank Woori Indonesia)"),
    ("YUDHA_BHAKTI", "Bank Yudha Bhakti"),
    ("ACEH", "BPD Aceh"),
    ("ACEH_UUS", "BPD Aceh UUS"),
    ("BALI", "BPD Bali"),
    ("BANTEN", "BPD Banten (formerly Bank Pundi Indonesia)"),
    ("BENGKULU", "BPD Bengkulu"),
    ("DAERAH_ISTIMEWA", "BPD Daerah Istimewa Yogyakarta (DIY)"),
    ("DAERAH_ISTIMEWA_UUS", "BPD Daerah Istimewa Yogyakarta (DIY) UUS"),
    ("JAMBI", "BPD Jambi"),
    ("JAMBI_UUS", "BPD Jambi UUS"),
    ("JAWA_TENGAH", "BPD Jawa Tengah"),
    ("JAWA_TENGAH_UUS", "BPD Jawa Tengah UUS"),
    ("JAWA_TIMUR", "BPD Jawa Timur"),
    ("JAWA_TIMUR_UUS", "BPD Jawa Timur UUS"),
    ("KALIMANTAN_BARAT", "BPD Kalimantan Barat"),
    ("KALIMANTAN_BARAT_UUS", "BPD Kalimantan Barat UUS"),
    ("KALIMANTAN_SELATAN", "BPD Kalimantan Selatan"),
    ("KALIMANTAN_SELATAN_UUS", "BPD Kalimantan Selatan UUS"),
    ("KALIMANTAN_TENGAH", "BPD Kalimantan Tengah"),
    ("KALIMANTAN_TIMUR", "BPD Kalimantan Timur"),
    ("KALIMANTAN_TIMUR_UUS", "BPD Kalimantan Timur UUS"),
    ("LAMPUNG", "BPD Lampung"),
    ("MALUKU", "BPD Maluku"),
    ("NUSA_TENGGARA_BARAT", "BPD Nusa Tenggara Barat"),
    ("NUSA_TENGGARA_BARAT_UUS", "BPD Nusa Tenggara Barat UUS"),
    ("NUSA_TENGGARA_TIMUR", "BPD Nusa Tenggara Timur"),
    ("PAPUA", "BPD Papua"),
    ("RIAU_DAN_KEPRI", "BPD Riau Dan Kepri"),
    ("RIAU_DAN_KEPRI_UUS", "BPD Riau Dan Kepri UUS"),
    ("SULAWESI", "BPD Sulawesi Tengah"),
    ("SULAWESI_TENGGARA", "BPD Sulawesi Tenggara"),
    ("SULSELBAR", "BPD Sulselbar"),
    ("SULSELBAR_UUS", "BPD Sulselbar UUS"),
    ("SULUT", "BPD Sulut"),
    ("SUMATERA_BARAT", "BPD Sumatera Barat"),
    ("SUMATERA_BARAT_UUS", "BPD Sumatera Barat UUS"),
    ("SUMSEL_DAN_BABEL", "BPD Sumsel Dan Babel"),
    ("SUMSEL_DAN_BABEL_UUS", "BPD Sumsel Dan Babel UUS"),
    ("SUMUT", "BPD Sumut"),
    ("SUMUT_UUS", "BPD Sumut UUS"),
    ("BTPN_SYARIAH", "BTPN Syariah (formerly BTPN UUS and Bank Sahabat Purba Danarta)"),
    ("CENTRATAMA", "Centratama Nasional Bank"),
    ("CCB", "China Construction Bank Indonesia (formerly Bank Antar Daerah and Bank Windu Kentjana International)"),
    ("CITIBANK", "Citibank"),
    ("DEUTSCHE", "Deutsche Bank"),
    ("HSBC_UUS", "Hongkong and Shanghai Bank Corporation (HSBC) UUS"),
    ("HSBC", "HSBC Indonesia (formerly Bank Ekonomi Raharja)"),
    ("EXIMBANK", "Indonesia Eximbank (formerly Bank Ekspor Indonesia)"),
    ("JPMORGAN", "JP Morgan Chase Bank"),
    ("MANDIRI_TASPEN", "Mandiri Taspen Pos (formerly Bank Sinar Harapan Bali)"),
    ("PRIMA_MASTER", "Prima Master Bank"),
    ("RBS", "Royal Bank of Scotland (RBS)"),
    ("STANDARD_CHARTERED", "Standard Chartered Bank"),
)