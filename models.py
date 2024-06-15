from flask_pymongo import MongoClient
from argon2 import PasswordHasher
import random
from datetime import datetime

class MUser():
    def __init__(self, nama=None, password=None, email=None, nohp=None):
        self.nama = nama
        self.password = password
        self.email = email
        self.nohp = nohp
        self.ph = PasswordHasher()
        
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.mountserv
        self.user = self.db.user
        self.gunung = self.db.gunung  
        self.produk = self.db.produk
        self.pesanan = self.db.pesanan
        self.barang = self.db.etalaseproduk  
        self.program = self.db.program  
        self.penggunaprogram = self.db.penggunaprogram

    def authenticate(self, email, password):
        imail = self.user.find_one({"email": email})
        if imail:
            try:
                if self.ph.verify(imail["password"], password):
                    return True
            except:
                pass
        return False

    def check_email_terdaftar(self, email):
        imail = self.user.find_one({"email": email})
        return imail

    def insertdata(self, nama, nohp, email, password):
        hashed_password = self.ph.hash(password)
        user_data = {
            "nama": nama,
            "nohp": (nohp),
            "email": email,
            "password": hashed_password,
            "tanggal_lahir":"",
            "provinsi":"",
            "kabupaten":"",
            "kecamatan":"",
            "kode_pos":"",
            "alamat":"",
            "role":'Pendaki',
            "gunung":'',
            "gambarprofil":""}
        self.user.insert_one(user_data) 
        
    def updatedataprofil(self, email, update_data):
        try:
            self.user.update_one({'email': email}, {'$set': update_data})
            return True
        except Exception as e:
            print(e)
            return False

    def ambildatauser(self, email):
        return self.user.find_one({"email": email})
    
    def ambildatapendaki(self, nama, nohp):
        return self.user.find_one({"nama": nama, "nohp": nohp})
    
    def ambildatatotalpesananporter(self, nama, nohp):
        return self.pesanan.count_documents({"namaporter": nama, "nohpporter": nohp})
    
    def ambildatatotalpesanantourguide(self, nama, nohp):
        return self.pesanan.count_documents({"namatourguide": nama, "nohptourguide": nohp})
    
    def ambildatatotalpesananpenyewaan(self, nama, nohp):
        return self.pesanan.count_documents({"namapenyewaan": nama, "nohppenyewaan": nohp})
    
    def ambildatatotalpenilaianpesananporter(self, nama, nohp):
        return self.pesanan.count_documents({"namaporter": nama, "nohpporter": nohp, "penilaianporter": {"$ne": ""}})
    
    def ambildatatotalpenilaianpesanantourguide(self, nama, nohp):
        return self.pesanan.count_documents({"namatourguide": nama, "nohptourguide": nohp, 'penilaiantourguide':{"$ne": ""}})
    
    def ambildatatotalpenilaianpesananpenyewaan(self, nama, nohp):
        return self.pesanan.count_documents({"namapenyewaan": nama, "nohppenyewaan": nohp, 'penilaianpenyewaan':{"$ne": ""}})
    
    def ambildatatotalbatalpesananporter(self, nama, nohp):
        return self.pesanan.count_documents({"namaporter": nama, "nohpporter": nohp, 'statuspesanan':'dibatalkan'})
    
    def ambildatatotalbatalpesanantourguide(self, nama, nohp):
        return self.pesanan.count_documents({"namatourguide": nama, "nohptourguide": nohp, 'statuspesanan':'dibatalkan'})
    
    def ambildatatotalbatalpesananpenyewaan(self, nama, nohp):
        return self.pesanan.count_documents({"namapenyewaan": nama, "nohppenyewaan": nohp, 'statuspesanan':'dibatalkan'})
    
    def ambildatatotalpendapatanpesananporter(self, nama, nohp):
        pendapatan = [
            {
                "$match": {
                    "namaporter": nama,
                    "nohpporter": nohp,
                    "hargaporter": {"$ne": None}  
                }
            },
            {
                "$group": {
                    "_id": None,
                    "totalHarga": {"$sum": "$hargaporter"}
                }
            }
        ]

        result = list(self.pesanan.aggregate(pendapatan))
        if result:
            return result[0]['totalHarga']
        else:
            return 0
        
    def ambildatatotalpendapatanpesanantourguide(self, nama, nohp):
        pendapatan = [
            {
                "$match": {
                    "namatourguide": nama,
                    "nohptourguide": nohp,
                    "hargatourguide": {"$ne": None}  
                }
            },
            {
                "$group": {
                    "_id": None,
                    "totalHarga": {"$sum": "$hargatourguide"}
                }
            }
        ]

        result = list(self.pesanan.aggregate(pendapatan))
        if result:
            return result[0]['totalHarga']
        else:
            return 0
        
    def ambildatatotalpendapatanpesananpenyewaan(self, nama, nohp):
        pendapatan = [
            {
                "$match": {
                    "namapenyewaan": nama,
                    "nohppenyewaan": nohp,
                    "hargapenyewaan": {"$ne": None}  
                }
            },
            {
                "$group": {
                    "_id": None,
                    "totalHarga": {"$sum": "$hargapenyewaan"}
                }
            }
        ]

        result = list(self.pesanan.aggregate(pendapatan))
        if result:
            return result[0]['totalHarga']
        else:
            return 0
        
    def ambildataprogram(self):
        return self.program.find()    
        
    def ambildatagunung(self, gunung):
        return self.gunung.find_one({"gunung": gunung})
    
    def ambildatajalur(self, jalur):
        return self.gunung.find_one({"jalur": jalur})
    
    def ambildataproduk(self,jalur,jenisproduk,namaproduk):
        return self.produk.find_one({"jalur": jalur,"jenisproduk": jenisproduk, "namaproduk": namaproduk})

    def ambildataproduklist(self,jenisproduk):
        return list(self.produk.find({"jenisproduk": jenisproduk}))
    
    def cari_idproduk(self, idproduk):
        idproduk= int(idproduk)
        return self.produk.find_one({"_id":idproduk})
    
    def ambildatapesanan(self, nama, nohp):
        return self.pesanan.find_one({"nama": nama, "nohp": nohp})
    
    def ambildatapesananstatus(self, nama, nohp, statuspesanan):
        return self.pesanan.find_one({"nama": nama, "nohp": nohp, "statuspesanan":statuspesanan})
    
    def ambildatapesananstatuslist(self, nama, nohp, statuspesanan):
        return list(self.pesanan.find({"nama": nama, "nohp": nohp, "statuspesanan":statuspesanan}))
       
    def ambildatapesananporterlistporter(self, nama):
        return list(self.pesanan.find({"namaporter": nama}))
    
    def ambildatapesananporterlistporterada(self, nama):
        return list(self.pesanan.find({"namaporter": nama, "penilaianporter": {"$ne": ""}}))

    def ambildatapesananporterlistjasaporter(self, nama, statuspesanan):
        return list(self.pesanan.find({"namaporter": nama, "statuspesanan": statuspesanan}))
    
    def ambildatapesananporterlisttourguide(self, nama):
        return list(self.pesanan.find({"namatourguide": nama}))
    
    def ambildatapesananporterlisttourguideada(self, nama):
        return list(self.pesanan.find({"namatourguide": nama, "penilaiantourguide": {"$ne": ""}}))
    
    def ambildatapesananporterlistjasatourguide(self, nama, statuspesanan):
        return list(self.pesanan.find({"namatourguide": nama, "statuspesanan": statuspesanan}))
    
    def ambildatapesananporterlistpenyewaan(self, nama):
        return list(self.pesanan.find({"namapenyewaan": nama}))
    
    def ambildatapesananporterlistpenyewaanada(self, nama):
        return list(self.pesanan.find({"namapenyewaan": nama, "penilaianpenyewaan": {"$ne": ""}}))
    
    def ambildatapesananporterlistjasapenyewaan(self, nama, statuspesanan):
        return list(self.pesanan.find({"namapenyewaan": nama, "statuspesanan": statuspesanan}))
    
    def caridataprogram(self):
        return list(self.penggunaprogram.find())
    
    
    
    def id_auto(self):
        counter = self.pesanan.find_one_and_update(
            {'_id': 'pesananid'},
            {'$inc': {'seq': 1}},
            upsert=True,
            return_document=True
        )
        return counter['seq']
    
    def id_autoprogram(self):
        counter = self.penggunaprogram.find_one_and_update(
            {'_id': 'pesananid'},
            {'$inc': {'seq': 1}},
            upsert=True,
            return_document=True
        )
        return counter['seq']
    
    def cari_id(self, pesananid):
        pesananid= int(pesananid)
        return self.pesanan.find_one({"_id":pesananid})
    
    def cari_idstring(self):
        return self.pesanan.find_one({"_id":"pesananid"})

    def cari_idprogram(self, pesananid):
        pesananid= int(pesananid)
        return self.program.find_one({"_id":pesananid})
    
    def insertpesanan(self, nama, nohp, gunung, jalur, jenisproduk, namaproduk, metodepembayaran,hargapaket, hargaporter, hargatourguide,hargapenyewaan, tanggalmendaki, tanggalturun, statuspesanan, total):
        skarang = datetime.now()
        waktu = skarang.strftime("%d-%m-%Y %H:%M")
        pesanan_id = self.id_auto()
        pesanan_data = {
            "_id": pesanan_id,
            "nama": nama,
            "nohp": nohp,
            "gunung": gunung,
            "jalur": jalur,
            "jenisproduk": jenisproduk,
            "namaproduk": namaproduk,
            "metodepembayaran": metodepembayaran,
            "hargapaket": hargapaket,
            "namaporter": '',
            "hargaporter": hargaporter,
            "nohpporter": '',
            "penilaianporter":'',
            "namatourguide": '',
            "hargatourguide": hargatourguide,
            "nohptourguide": '',
            "penilaiantourguide":'',
            "namapenyewaan": '',
            "barangsewa":'',
            "hargapenyewaan":hargapenyewaan,
            "nohppenyewaan": '',
            "penilaianpenyewaan":'',
            "tanggalmendaki": tanggalmendaki,
            "tanggalturun": tanggalturun,
            "statuspesanan": statuspesanan,
            "totalharga": total,
            "waktupesan": waktu,
            "waktubayar": ''
        }
        self.pesanan.insert_one(pesanan_data)
        
    def insertpesananpaket(self, nama, nohp, gunung, jalur, jenisproduk, namaproduk, metodepembayaran,hargapaket, hargaporter, hargatourguide,barangsewaan,hargapenyewaan, tanggalmendaki, tanggalturun, statuspesanan, total):
        skarang = datetime.now()
        waktu = skarang.strftime("%d-%m-%Y %H:%M")
        pesanan_id = self.id_auto()
        pesanan_data = {
            "_id": pesanan_id,
            "nama": nama,
            "nohp": nohp,
            "gunung": gunung,
            "jalur": jalur,
            "jenisproduk": jenisproduk,
            "namaproduk": namaproduk,
            "metodepembayaran": metodepembayaran,
            "hargapaket": hargapaket,
            "namaporter": '',
            "hargaporter": hargaporter,
            "nohpporter": '',
            "penilaianporter":'',
            "namatourguide": '',
            "hargatourguide": hargatourguide,
            "nohptourguide": '',
            "penilaiantourguide":'',
            "namapenyewaan": '',
            "barangsewa":barangsewaan,
            "hargapenyewaan":hargapenyewaan,
            "nohppenyewaan": '',
            "penilaianpenyewaan":'',
            "tanggalmendaki": tanggalmendaki,
            "tanggalturun": tanggalturun,
            "statuspesanan": statuspesanan,
            "totalharga": total,
            "waktupesan": waktu,
            "waktubayar": ''
        }
        self.pesanan.insert_one(pesanan_data)
        

    def insertprogram(self,nama,nohp,namaprogram,tanggal):
        pesanan_id = self.id_autoprogram()
        program = {
            "_id": pesanan_id,
            "nama": nama,
            "nohp": nohp,
            "namaprogram": namaprogram,
            "tanggal": tanggal
        }
        self.penggunaprogram.insert_one(program)

    def updatestatuspesananid(self, idpesanan,statuspesanan,ubahstatus):
        idpesanan = int(idpesanan)
        self.pesanan.update_one(
            {"_id":idpesanan ,"statuspesanan": statuspesanan},
            {"$set": {"statuspesanan": ubahstatus}}
        )
         
    def randomporter(self):
        porter_list = self.user.find({"role" :"Porter"})
        porter_list = list(porter_list)
        if porter_list:
            return random.choice(porter_list)

    def randomtourguide(self):
        tourguide_list = self.user.find({"role" :"Tour Guide"})
        tourguide_list = list(tourguide_list)
        if tourguide_list:
            return random.choice(tourguide_list)
    
    def randompenyewaan(self):
        penyewaan_list = self.user.find({"role" :"Penyewaan"})
        penyewaan_list = list(penyewaan_list)
        if penyewaan_list:
            return random.choice(penyewaan_list)
    
    
    def updatenamapesanan(self, idpesanan, update_pesanan):
        idpesanan = int(idpesanan)
        self.pesanan.update_one(
            {"_id": idpesanan},
            {"$set": update_pesanan}
        )
    
    def tampilbarang(self):
        return self.barang.find()
        
    def cari_idbarang(self, idbarang):
        idbarang= int(idbarang)
        return self.barang.find_one({"_id":idbarang})
