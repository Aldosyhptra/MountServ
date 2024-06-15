from flask import Flask, render_template, session, request, redirect, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from models import MUser
from argon2 import PasswordHasher
from datetime import datetime
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'




@app.route('/')
def index():
       
    if 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        return render_template('landingpage.html', buttonlogin=buttonlogin, buttonuser=buttonuser,gambarprofil=gambarprofil)
    
    else:
        buttonuser='d-none'
        buttonlogin=''
    
        
    return render_template('landingpage.html', buttonlogin=buttonlogin, buttonuser=buttonuser)

@app.route('/tentangkami')
def tentangkami():
    if 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        return render_template('tentangkami.html',buttonlogin=buttonlogin,buttonuser=buttonuser, gambarprofil=gambarprofil)
    
    else:
        buttonuser='d-none'
        buttonlogin=''
        return render_template('tentangkami.html',buttonlogin=buttonlogin,buttonuser=buttonuser)

@app.route('/gunung')
def mountain(): 
    if 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        return render_template('gunung.html',buttonlogin=buttonlogin,buttonuser=buttonuser, gambarprofil=gambarprofil)
    
    else:
        buttonuser='d-none'
        buttonlogin=''
        return render_template('gunung.html',buttonlogin=buttonlogin,buttonuser=buttonuser)

@app.route('/gunung/jalur',methods=["GET","POST"])
def gunungsumbing():
    session['gunung']='sumbing'
    session['jalur']='garung'

    if 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        return render_template('jalur.html',buttonlogin=buttonlogin,buttonuser=buttonuser, gambarprofil=gambarprofil)
    
    else:
        buttonuser='d-none'
        buttonlogin=''
        return render_template('jalur.html',buttonlogin=buttonlogin,buttonuser=buttonuser)

@app.route('/gunung/jalur/pricelist', methods=["GET", "POST"])
def pricelistgarung():

    if 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
            
        gunung = session.get('gunung')
        jalur = session.get('jalur')
        
        jenisprodukporter = "porter"
        jenisproduktourguide = 'tour guide'
        user_produk = MUser()
        porter_list = user_produk.ambildataproduklist(jenisprodukporter)
        paket=user_produk.ambildataproduklist('paket') 
        if porter_list is None:
            porter_list = []
        if isinstance(porter_list, list):
            porter_list.extend(paket)
        else:
            porter_list.append(paket)

        tourguide_list = user_produk.ambildataproduklist(jenisproduktourguide)

        if tourguide_list is None:
            tourguide_list = []
        if isinstance(tourguide_list, list):
            tourguide_list.extend(paket)
        else:
            tourguide_list.append(paket)              
            
        barang_list=user_produk.tampilbarang()
        
        if barang_list is None:
            barang_list=[]
        if paket is None:
                paket=[]   
        return render_template('pricelist.html', 
                                buttonlogin=buttonlogin, buttonuser=buttonuser, gunung=gunung, jalur=jalur, 
                                porter_list=porter_list, tourguide_list=tourguide_list,barang_list=barang_list,paket=paket,gambarprofil=gambarprofil)

    else:
        buttonuser='d-none'
        buttonlogin=''
        
        gunung = session.get('gunung')
        jalur = session.get('jalur')
        
        jenisprodukporter = "porter"
        jenisproduktourguide = 'tour guide'
        user_produk = MUser()
        porter_list = user_produk.ambildataproduklist(jenisprodukporter)
        paket=user_produk.ambildataproduklist('paket') 
        if porter_list is None:
            porter_list = []
        if isinstance(porter_list, list):
            porter_list.extend(paket)
        else:
            porter_list.append(paket)

        tourguide_list = user_produk.ambildataproduklist(jenisproduktourguide)

        if tourguide_list is None:
            tourguide_list = []
        if isinstance(tourguide_list, list):
            tourguide_list.extend(paket)
        else:
            tourguide_list.append(paket)              
        return render_template('pricelist.html', 
                                buttonlogin=buttonlogin, buttonuser=buttonuser, gunung=gunung, jalur=jalur, 
                                porter_list=porter_list, tourguide_list=tourguide_list)

@app.route('/gunung/jalur/pricelist/informasiproduk', methods=["GET", "POST"])
def informasipaketgarung():
    if 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
            
        if request.method == "POST":
            idpesanan = request.form['idproduk']
            user_produk = MUser()
            produk = user_produk.cari_idproduk(idpesanan)
            
            if produk:
                idproduk=produk.get('_id')
                gunung=produk.get('gunung')
                jalur=produk.get('jalur')
                namaproduk=produk.get('namaproduk')
                jenisproduk=produk.get('jenisproduk')
                harga=produk.get('harga')
                total=produk.get('harga')
                durasi=produk.get('durasi')
                maxbeban=produk.get('maxbeban')
                deskripsi=produk.get('deskripsi')
                deskripsifasilitas = [fasilitas['deskripsi'] for fasilitas in produk.get('fasilitas', [])]
                
            
            fitur = MUser().ambildatajalur(jalur)
            alamatbasecamp = fitur.get('alamat', '') 
            deskripsigunung = fitur.get('deskripsi')
            peta=fitur.get('peta')
            tabelharga1='d-none'
            barangsewa='d-none'
            paket='d-none'
                
                
            if fitur:
                deskripsirute = [rute['deskripsi'] for rute in fitur.get('rute', [])]
                deskripsisyarat = [syarat['deskripsi'] for syarat in fitur.get('syarat', [])]
                deskripsilarangan = [larangan['deskripsi'] for larangan in fitur.get('larangan', [])]
                
            if jenisproduk == 'paket':
                hargaporter=produk.get('hargaporter')
                hargatourguide=produk.get('hargatourguide')
                porter='porter'
                tourguide='tourguide'
                penyewaan='penyewaan'
                tabelharga='d-none'
                portertourguide='d-none'
                products=MUser().tampilbarang()
                return render_template('informasipricelist.html', buttonlogin=buttonlogin, buttonuser=buttonuser, gunung=gunung, jalur=jalur, 
                                namaproduk=namaproduk, durasi=durasi, maxbeban=maxbeban, deskripsi=deskripsi,
                                deskripsifasilitas=deskripsifasilitas,deskripsirute=deskripsirute,deskripsisyarat=deskripsisyarat, deskripsilarangan=deskripsilarangan,alamatbasecamp=alamatbasecamp,deskripsigunung=deskripsigunung,idproduk=idproduk,gambarprofil=gambarprofil, peta=peta, hargaporter=hargaporter, hargatourguide=hargatourguide, porter=porter, tourguide=tourguide, total=total,tabelharga=tabelharga, penyewaan=penyewaan, products=products,portertourguide=portertourguide)
                
            return render_template('informasipricelist.html', buttonlogin=buttonlogin, buttonuser=buttonuser, gunung=gunung, jalur=jalur, 
                                namaproduk=namaproduk, harga=harga, durasi=durasi, maxbeban=maxbeban, deskripsi=deskripsi,
                                deskripsifasilitas=deskripsifasilitas,deskripsirute=deskripsirute,deskripsisyarat=deskripsisyarat, deskripsilarangan=deskripsilarangan,alamatbasecamp=alamatbasecamp,deskripsigunung=deskripsigunung,idproduk=idproduk,gambarprofil=gambarprofil, peta=peta, jenisproduk=jenisproduk, tabelharga1=tabelharga1, total=harga,barangsewa=barangsewa, paket=paket)
    
    else:
        buttonuser='d-none'
        buttonlogin=''
            
        if request.method == "POST":
            idpesanan = request.form['idproduk']
            user_produk = MUser()
            produk = user_produk.cari_idproduk(idpesanan)
            
            if produk:
                idproduk=produk.get('_id')
                gunung=produk.get('gunung')
                jalur=produk.get('jalur')
                namaproduk=produk.get('namaproduk')
                jenisproduk=produk.get('jenisproduk')
                harga=produk.get('harga')
                total=produk.get('harga')
                durasi=produk.get('durasi')
                maxbeban=produk.get('maxbeban')
                deskripsi=produk.get('deskripsi')
                deskripsifasilitas = [fasilitas['deskripsi'] for fasilitas in produk.get('fasilitas', [])]
                
            
            fitur = MUser().ambildatajalur(jalur)
            alamatbasecamp = fitur.get('alamat', '') 
            deskripsigunung = fitur.get('deskripsi')
            peta=fitur.get('peta')
            tabelharga1='d-none'
            barangsewa='d-none'
            paket='d-none'
                
                
            if fitur:
                deskripsirute = [rute['deskripsi'] for rute in fitur.get('rute', [])]
                deskripsisyarat = [syarat['deskripsi'] for syarat in fitur.get('syarat', [])]
                deskripsilarangan = [larangan['deskripsi'] for larangan in fitur.get('larangan', [])]
                
            if jenisproduk == 'paket':
                hargaporter=produk.get('hargaporter')
                hargatourguide=produk.get('hargatourguide')
                porter='porter'
                tourguide='tourguide'
                penyewaan='penyewaan'
                tabelharga='d-none'
                portertourguide='d-none'
                return render_template('informasipricelist.html', buttonlogin=buttonlogin, buttonuser=buttonuser, gunung=gunung, jalur=jalur, 
                                namaproduk=namaproduk, durasi=durasi, maxbeban=maxbeban, deskripsi=deskripsi,
                                deskripsifasilitas=deskripsifasilitas,deskripsirute=deskripsirute,deskripsisyarat=deskripsisyarat, deskripsilarangan=deskripsilarangan,alamatbasecamp=alamatbasecamp,deskripsigunung=deskripsigunung,idproduk=idproduk, peta=peta, hargaporter=hargaporter, hargatourguide=hargatourguide, porter=porter, tourguide=tourguide, total=total,tabelharga=tabelharga,penyewaan=penyewaan,products=products,portertourguide=portertourguide)
                
            return render_template('informasipricelist.html', buttonlogin=buttonlogin, buttonuser=buttonuser, gunung=gunung, jalur=jalur, 
                                namaproduk=namaproduk, harga=harga, durasi=durasi, maxbeban=maxbeban, deskripsi=deskripsi,
                                deskripsifasilitas=deskripsifasilitas,deskripsirute=deskripsirute,deskripsisyarat=deskripsisyarat, deskripsilarangan=deskripsilarangan,alamatbasecamp=alamatbasecamp,deskripsigunung=deskripsigunung,idproduk=idproduk, peta=peta, jenisproduk=jenisproduk, tabelharga1=tabelharga1, total=harga,barangsewa=barangsewa, paket=paket)
        
@app.route('/checkout', methods=["GET", "POST"])
def checkout():
    if 'email' not in session:
        return redirect(url_for('login'))
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
    
    else:
        buttonuser='d-none'
        buttonlogin=''
        
    if request.method == "POST":
        email=session['email']
        idproduk = request.form['idproduk']
        tanggalmendaki = request.form['tanggalmendaki']
        tanggalturun = request.form['tanggalturun']
        user_produk = MUser()
        produk = user_produk.cari_idproduk(idproduk)
        gunung=produk.get('gunung')
        jalur=produk.get('jalur')
        namaproduk=produk.get('namaproduk')
        jenisproduk=produk.get('jenisproduk')
        harga=produk.get('harga')
        durasi=produk.get('durasi')
        maxbeban=produk.get('maxbeban')
        deskripsi=produk.get('deskripsi')
        user = MUser().ambildatauser(email)
        nama=user.get('nama')
        nohp=user.get('nohp')
        alamat=user.get('alamat')
        layanan = 1000
        total = int(harga) + int(layanan)
        session['total']=total
        fieldbarangsewa='d-none'
        if jenisproduk == 'paket':
            hargapenyewaan=request.form['hargapenyewaan']
            barangsewa=request.form['barangsewa']
            session['hargapenyewaan']=hargapenyewaan
            session['barangsewa']=barangsewa
            hargatotal = int(harga) + int(hargapenyewaan)
            total = int(harga) + int(layanan) + int(hargapenyewaan)
            session['total']=total
            return render_template('checkout.html', buttonlogin=buttonlogin, buttonuser=buttonuser, gunung=gunung, jalur=jalur, 
                                namaproduk=namaproduk, harga=hargatotal, durasi=durasi, maxbeban=maxbeban, deskripsi=deskripsi, nama=nama, nohp=nohp, alamat=alamat, layanan=layanan, total=total,idproduk=idproduk, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,barangsewa=barangsewa)
        return render_template('checkout.html', buttonlogin=buttonlogin, buttonuser=buttonuser, gunung=gunung, jalur=jalur, 
                                namaproduk=namaproduk, harga=harga, durasi=durasi, maxbeban=maxbeban, deskripsi=deskripsi, nama=nama, nohp=nohp, alamat=alamat, layanan=layanan, total=total,idproduk=idproduk, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,fieldbarangsewa=fieldbarangsewa)

@app.route('/checkout/bayar1', methods=["GET", "POST"])
def bayar():
    if 'email' not in session:
        return redirect(url_for('login'))
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
    
    else:
        buttonuser='d-none'
        buttonlogin=''
        
    if request.method == "POST":
        email=session['email']
        metodepembayaran = request.form['metodepembayaran']
        total=session['total']
        hargapenyewaan=session['hargapenyewaan']
        hargapenyewaan=int(hargapenyewaan)
        idproduk=request.form['idproduk']
        tanggalmendaki = request.form['tanggalmendaki']
        tanggalturun = request.form['tanggalturun'] 
        user_produk=MUser()
        produk = user_produk.cari_idproduk(idproduk)
        gunung=produk.get('gunung')
        jalur=produk.get('jalur')
        namaproduk=produk.get('namaproduk')
        jenisproduk=produk.get('jenisproduk')
        durasi=produk.get('durasi')
        maxbeban=produk.get('maxbeban')
        deskripsi=produk.get('deskripsi')
        user = MUser().ambildatauser(email)
        nama=user.get('nama')
        nohp=user.get('nohp')
        statuspembayaran='belum bayar'
        if metodepembayaran == 'Dana' or 'Qris' or 'Shopee':
            ewallet=''
            bank='d-none'
        elif metodepembayaran == 'Transfek Bank BNI' or 'Transfer Bank BRI':
            ewallet='d-none'
            bank=''
            
        if jenisproduk == 'porter':
            harga=produk.get('harga')
            user = MUser().insertpesanan(nama,nohp,gunung, jalur, jenisproduk, namaproduk, metodepembayaran, harga, harga, '','', tanggalmendaki, tanggalturun, statuspembayaran, total)
            generatei= MUser().cari_idstring()
            idpesanan=generatei.get('seq')
            session['idpesanan']=idpesanan
            idpesanan = session['idpesanan']
            user_pesan=MUser().cari_id(idpesanan)
            waktupesan=user_pesan.get('waktupesan')
            return render_template('bayar1.html', buttonlogin=buttonlogin, buttonuser=buttonuser, gunung=gunung, jalur=jalur, 
                            nama=nama,nohp=nohp,jenisproduk=jenisproduk, namaproduk=namaproduk, harga=harga, durasi=durasi,
                            maxbeban=maxbeban, deskripsi=deskripsi, metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun, statuspembayaran=statuspembayaran, idpesanan=idpesanan,gambarprofil=gambarprofil,ewallet=ewallet, bank=bank,waktupesan=waktupesan)
            
        elif jenisproduk == 'tour guide':
            harga=produk.get('harga')
            user = MUser().insertpesanan(nama,nohp,gunung, jalur, jenisproduk, namaproduk, metodepembayaran, harga, '', harga,'', tanggalmendaki, tanggalturun, statuspembayaran, total)
            generateid= MUser().cari_idstring()
            idpesanan=generateid.get('seq')
            session['idpesanan']=idpesanan
            idpesanan = session['idpesanan']
            user_pesan=MUser().cari_id(idpesanan)
            waktupesan=user_pesan.get('waktupesan')
            return render_template('bayar1.html', buttonlogin=buttonlogin, buttonuser=buttonuser, gunung=gunung, jalur=jalur, 
                            nama=nama,nohp=nohp,jenisproduk=jenisproduk, namaproduk=namaproduk, harga=harga, durasi=durasi,
                            maxbeban=maxbeban, deskripsi=deskripsi, metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun, statuspembayaran=statuspembayaran, idpesanan=idpesanan,gambarprofil=gambarprofil,ewallet=ewallet, bank=bank,waktupesan=waktupesan)
    
        else:
            barangsewa=session['barangsewa']
            hargaporter=produk.get('hargaporter')
            hargatourguide=produk.get('hargatourguide')
            hargapaket = int(hargaporter)+int(hargatourguide)+int(hargapenyewaan)
            user = MUser().insertpesananpaket(nama,nohp,gunung, jalur, jenisproduk, namaproduk, metodepembayaran,hargapaket, hargaporter, hargatourguide,barangsewa,hargapenyewaan, tanggalmendaki, tanggalturun, statuspembayaran, total)
            generatei= MUser().cari_idstring()
            idpesanan=generatei.get('seq')
            session['idpesanan']=idpesanan
            idpesanan = session['idpesanan']
            user_pesan=MUser().cari_id(idpesanan)
            waktupesan=user_pesan.get('waktupesan')
            return render_template('bayar1.html', buttonlogin=buttonlogin, buttonuser=buttonuser, gunung=gunung, jalur=jalur, 
                            nama=nama,nohp=nohp,jenisproduk=jenisproduk, namaproduk=namaproduk, harga=hargapaket, durasi=durasi,
                            maxbeban=maxbeban, deskripsi=deskripsi, metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun, statuspembayaran=statuspembayaran, idpesanan=idpesanan,gambarprofil=gambarprofil,ewallet=ewallet, bank=bank,waktupesan=waktupesan)
            
      

@app.route('/checkout/berhasilbayar', methods=["GET", "POST"])
def sudahbayar():
    if 'email' not in session:
        return redirect(url_for('login'))

    elif 'email' in session:
        buttonlogin = 'd-none'
        buttonuser = ''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'

    else:
        buttonuser = 'd-none'
        buttonlogin = ''

    if request.method == 'POST':
        email = session['email']
        user = MUser().ambildatauser(email)
        nama = user.get('nama')
        nohp = user.get('nohp')
        idpesanan = request.form['idpesanan']
        user_pesan=MUser().cari_id(idpesanan)
        statuspembayaran = user_pesan.get('statuspesanan')
        gunung=user_pesan.get('gunung')
        jalur=user_pesan.get('jalur')
        namaproduk=user_pesan.get('namaproduk')
        hargapaket=user_pesan.get('hargapaket')
        tanggalmendaki=user_pesan.get('tanggalmendaki')
        tanggalturun=user_pesan.get('tanggalturun')
        metodepembayaran=user_pesan.get('metodepembayaran')
        jenisproduk=user_pesan.get('jenisproduk')
        if jenisproduk == 'porter':
            if user_pesan:
                porter=''
                tourguide='d-none'
                penyewaan='d-none'
                hargaporter=user_pesan.get('hargaporter')
                porter = MUser().randomporter()
                nama_porter = porter.get('nama')
                email_porter = porter.get('email')
                user_porter = MUser().ambildatauser(email_porter)
                nohpporter= user_porter.get('nohp')
                if statuspembayaran == 'belum bayar':
                    skarang = datetime.now()
                    waktu = skarang.strftime("%d-%m-%Y %H:%M")
                    update_pesanan = {
                        "namaporter": nama_porter,
                        "nohpporter": nohpporter,
                        "waktubayar": waktu
                    }
                    MUser().updatenamapesanan(idpesanan, update_pesanan)
                    MUser().updatestatuspesananid(idpesanan, 'belum bayar', 'sudah bayar')
                    session.pop=('idpesanan')
                    if metodepembayaran == 'Dana' or 'Qris' or 'Shopee':
                        ewallet=''
                        bank='d-none'
                    elif metodepembayaran == 'Transfek Bank BNI' or 'Transfer Bank BRI':
                        ewallet='d-none'
                        bank=''
                    return render_template('sudahbayar.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                    namaproduk=namaproduk, harga=hargapaket, metodepembayaran=metodepembayaran, statuspembayaran=statuspembayaran,gambarprofil=gambarprofil, namaporter=nama_porter,nohpporter=nohpporter , hargaporter=hargaporter, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun, porter=porter, tourguide=tourguide, penyewaan=penyewaan, ewallet=ewallet, bank=bank,waktubayar=waktu)
        elif jenisproduk == 'tour guide':
            if user_pesan:
                porter='d-none'
                tourguide=''
                penyewaan='d-none'
                hargatourguide=user_pesan.get('hargatourguide')
                tourguide = MUser().randomtourguide()
                nama_tourguide = tourguide.get('nama')
                email_tourguide = tourguide.get('email')
                user_tourguide = MUser().ambildatauser(email_tourguide)
                nohptourguide= user_tourguide.get('nohp')
                if statuspembayaran == 'belum bayar':
                    hargatourguide=user_pesan.get('hargatourguide')
                    skarang = datetime.now()
                    waktu = skarang.strftime("%d-%m-%Y %H:%M")
                    update_pesanan = {
                        "namatourguide": nama_tourguide,
                        "nohptourguide": nohptourguide,
                        "waktubayar": waktu
                    }
                    MUser().updatenamapesanan(idpesanan, update_pesanan)
                    MUser().updatestatuspesananid(idpesanan, 'belum bayar', 'sudah bayar')
                    session.pop=('idpesanan')
                    if metodepembayaran == 'Dana' or 'Qris' or 'Shopee':
                        ewallet=''
                        bank='d-none'
                    elif metodepembayaran == 'Transfek Bank BNI' or 'Transfer Bank BRI':
                        ewallet='d-none'
                        bank=''
                    return render_template('sudahbayar.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                            gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                namaproduk=namaproduk, harga=hargapaket, metodepembayaran=metodepembayaran, statuspembayaran=statuspembayaran,gambarprofil=gambarprofil, namatourguide=nama_tourguide,nohptourguide=nohptourguide , hargatourguide=hargatourguide, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun, porter=porter, tourguide=tourguide, penyewaan=penyewaan, ewallet=ewallet, bank=bank,waktubayar=waktu)
                    
        elif jenisproduk == 'paket':
            if user_pesan:
                porter=''
                tourguide=''
                penyewaan=''
                listbarang=session['barangsewa']
                hargaporter=user_pesan.get('hargaporter')
                hargatourguide=user_pesan.get('hargatourguide')
                hargapenyewaan=user_pesan.get('hargapenyewaan')
                porter = MUser().randomporter()
                nama_porter = porter.get('nama')
                email_porter = porter.get('email')
                user_porter = MUser().ambildatauser(email_porter)
                nohpporter= user_porter.get('nohp')
                tourguide = MUser().randomtourguide()
                nama_tourguide = tourguide.get('nama')
                email_tourguide = tourguide.get('email')
                user_tourguide = MUser().ambildatauser(email_tourguide)
                nohptourguide= user_tourguide.get('nohp')
                penyewaan = MUser().randompenyewaan()
                nama_penyewaan = penyewaan.get('nama')
                email_penyewaan = penyewaan.get('email')
                user_penyewaan = MUser().ambildatauser(email_penyewaan)
                nohppenyewaan= user_penyewaan.get('nohp')
                if statuspembayaran == 'belum bayar':
                    skarang = datetime.now()
                    waktu = skarang.strftime("%d-%m-%Y %H:%M")
                    update_pesanan = {
                        "namaporter": nama_porter,
                        "nohpporter": nohpporter,
                        "namatourguide": nama_tourguide,
                        "nohptourguide": nohptourguide,
                        "namapenyewaan":nama_penyewaan,
                        "nohppenyewaan":nohppenyewaan,
                        "waktubayar": waktu
                    }
                    MUser().updatenamapesanan(idpesanan, update_pesanan)
                    MUser().updatestatuspesananid(idpesanan, 'belum bayar', 'sudah bayar')
                    session.pop=('idpesanan')
                    if metodepembayaran == 'Dana' or 'Qris' or 'Shopee':
                        ewallet=''
                        bank='d-none'
                    elif metodepembayaran == 'Transfek Bank BNI' or 'Transfer Bank BRI':
                        ewallet='d-none'
                        bank=''
                    return render_template('sudahbayar.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                            gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                namaproduk=namaproduk, harga=hargapaket, metodepembayaran=metodepembayaran, statuspembayaran=statuspembayaran,gambarprofil=gambarprofil, namaporter=nama_porter,nohpporter=nohpporter , hargaporter=hargaporter,namatourguide=nama_tourguide,nohptourguide=nohptourguide , hargatourguide=hargatourguide, namapenyewaan=nama_penyewaan,nohppenyewaan=nohppenyewaan , hargapenyewaan=hargapenyewaan,  tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun, porter=porter, tourguide=tourguide, penyewaan=penyewaan, ewallet=ewallet, bank=bank,waktubayar=waktu, listbarang=listbarang)
            
                
                
@app.route('/cuaca', methods=['GET','POST'])
def cuaca():
    if request.method == 'POST':
        lokasi = request.form.get('lokasi')
        if lokasi:
            session['lokasi'] = lokasi
        return redirect(url_for('cuaca'))
    
    lokasi = session.get('lokasi')
    
    if 'email' in session:
        buttonlogin = 'd-none'
        buttonuser = ''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
            
        return render_template('cuaca.html', lokasi=lokasi, buttonlogin=buttonlogin, buttonuser=buttonuser,gambarprofil=gambarprofil)
        
    else:
        buttonlogin = ''
        buttonuser = 'd-none'
    
    return render_template('cuaca.html', lokasi=lokasi, buttonlogin=buttonlogin, buttonuser=buttonuser)
                      

@app.route('/kontak')
def kontak():
    if 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        return render_template('kontak.html',buttonlogin=buttonlogin,buttonuser=buttonuser,gambarprofil=gambarprofil)
    
    else:
        buttonuser='d-none'
        buttonlogin=''
        
        return render_template('kontak.html',buttonlogin=buttonlogin,buttonuser=buttonuser)

    
@app.route('/profil', methods=['GET','POST'])
def profil():
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''
    else:
        buttonuser='d-none'
        buttonlogin=''      
    
    if 'email' in session:
        email = session['email']
        user = MUser().ambildatauser(email)
        nama=user.get('nama')
        nohp=user.get('nohp')
        email=user.get('email')
        tanggal_lahir=user.get('tanggal_lahir')
        provinsi=user.get('provinsi')
        kabupaten=user.get('kabupaten')
        kecamatan=user.get('kecamatan')
        kode_pos=user.get('kode_pos')
        alamat=user.get('alamat')
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        
    if request.method == 'POST':
        update_data = {
                'nama': request.form['nama'],
                'nohp': request.form['nohp'],
                'tanggal_lahir': request.form['tanggal_lahir'],
                'provinsi': request.form['provinsi'],
                'kabupaten': request.form['kabupaten'],
                'kecamatan': request.form['kecamatan'],
                'kode_pos': request.form['kode_pos'],
                'alamat': request.form['alamat']
        }
        user=MUser()
        if user.updatedataprofil(email, update_data):
            user = MUser().ambildatauser(email)
            nama=user.get('nama')
            nohp=user.get('nohp')
            email=user.get('email')
            tanggal_lahir=user.get('tanggal_lahir')
            provinsi=user.get('provinsi')
            kabupaten=user.get('kabupaten')
            kecamatan=user.get('kecamatan')
            kode_pos=user.get('kode_pos')
            alamat=user.get('alamat')
            msgbenar = 'Data Berhasil di Update'
            return render_template('profil.html', msgbenar=msgbenar,nama=nama, nohp=nohp, email=email, tanggal_lahir=tanggal_lahir, provinsi=provinsi, kabupaten=kabupaten, kecamatan=kecamatan, kode_pos=kode_pos, alamat=alamat,buttonlogin=buttonlogin, buttonuser=buttonuser,bukajasa=bukajasa, dashboard=dashboard,gambarprofil=gambarprofil)
        else:
            msgsalah = 'Data Gagal di Update'
            return render_template('profil.html',msgsalah=msgsalah,nama=nama, nohp=nohp, email=email, tanggal_lahir=tanggal_lahir, provinsi=provinsi, kabupaten=kabupaten, kecamatan=kecamatan, kode_pos=kode_pos, alamat=alamat,buttonlogin=buttonlogin, buttonuser=buttonuser,bukajasa=bukajasa, dashboard=dashboard,gambarprofil=gambarprofil)
        
    return render_template('profil.html',nama=nama, nohp=nohp, email=email, tanggal_lahir=tanggal_lahir, provinsi=provinsi, kabupaten=kabupaten, kecamatan=kecamatan, kode_pos=kode_pos, alamat=alamat,buttonlogin=buttonlogin, buttonuser=buttonuser,bukajasa=bukajasa, dashboard=dashboard,gambarprofil=gambarprofil)

@app.route('/profilpassword', methods=['GET','POST'])
def profilpassword():
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
        
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''
        
    else:
        buttonuser='d-none'
        buttonlogin=''
        
    if request.method == 'POST':
        if 'email' in session:   
            email = session['email']
            user = MUser().ambildatauser(email)
            nama=user.get('nama')
            nohp=user.get('nohp')
            email=user.get('email')
            tanggal_lahir=user.get('tanggal_lahir')
            provinsi=user.get('provinsi')
            kabupaten=user.get('kabupaten')
            kecamatan=user.get('kecamatan')
            kode_pos=user.get('kode_pos')
            alamat=user.get('alamat')
            gambarprofil=user.get('gambarprofil')
            enkripsi = PasswordHasher()
            password_lama = request.form['passwordlama']
            password_baru = request.form['passwordbaru']
            password=enkripsi.hash(password_baru)
            
            user = MUser()
            if user.authenticate(email, password_lama):
                update_data = {
                    'password': password
                }
                user = MUser()
                if user.updatedataprofil(email, update_data):
                    msgbenar = 'Password Berhasil di Update'
                    return render_template('profil.html', msgbenar=msgbenar,nama=nama, nohp=nohp, email=email, tanggal_lahir=tanggal_lahir, provinsi=provinsi, kabupaten=kabupaten, kecamatan=kecamatan, kode_pos=kode_pos, alamat=alamat,buttonlogin=buttonlogin, buttonuser=buttonuser,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil)
                else:
                    msgsalah = 'Password Gagal di Update'
            else:
                msgsalah = 'Password Yang Ingin di Update Tidak Ditemukan'
            return render_template('profil.html', msgsalah=msgsalah,nama=nama, nohp=nohp, email=email, tanggal_lahir=tanggal_lahir, provinsi=provinsi, kabupaten=kabupaten, kecamatan=kecamatan, kode_pos=kode_pos, alamat=alamat,buttonlogin=buttonlogin, buttonuser=buttonuser,bukajasa=bukajasa, dashboard=dashboard,gambarprofil=gambarprofil)

@app.route('/updatefotoprofil', methods=['POST'])
def updatefotoprofil():
    
    app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/static/uploads/profil'
    app.config['MAX_CONTENT_PATH'] = 10000000
    
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
        
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''
        
    else:
        buttonuser='d-none'
        buttonlogin=''
        
    if request.method == 'POST':
        if 'email' in session:   
            email = session['email']
            user = MUser().ambildatauser(email)
            nama=user.get('nama')
            nohp=user.get('nohp')
            email=user.get('email')
            tanggal_lahir=user.get('tanggal_lahir')
            provinsi=user.get('provinsi')
            kabupaten=user.get('kabupaten')
            kecamatan=user.get('kecamatan')
            kode_pos=user.get('kode_pos')
            alamat=user.get('alamat')
            
            f = request.files['fotoprofil']
            namagambar = secure_filename(f.filename)
            filename = app.config['UPLOAD_FOLDER'] + '/' + secure_filename(f.filename)
            f.save(filename)
            update_data={
                'gambarprofil' : namagambar
            }
            userupdate=MUser()
            if userupdate.updatedataprofil(email, update_data):
                msgbenar = "Foto Profil Sudah Di Ubah"
                gambarprofil=namagambar
                return render_template('profil.html', msgbenar=msgbenar,nama=nama, nohp=nohp, email=email, tanggal_lahir=tanggal_lahir, provinsi=provinsi, kabupaten=kabupaten, kecamatan=kecamatan, kode_pos=kode_pos, alamat=alamat,buttonlogin=buttonlogin, buttonuser=buttonuser,bukajasa=bukajasa, dashboard=dashboard,gambarprofil=gambarprofil)
    
           

@app.route('/profil/bukajasa',methods=["GET","POST"])
def bukajasa():
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''

        if 'email' in session:   
            email = session['email']
            user = MUser().ambildatauser(email)
            nama=user.get('nama')
            nohp=user.get('nohp')
            email=user.get('email')
            tanggal_lahir=user.get('tanggal_lahir')
            provinsi=user.get('provinsi')
            kabupaten=user.get('kabupaten')
            kecamatan=user.get('kecamatan')
            kode_pos=user.get('kode_pos')
            alamat=user.get('alamat')
            gambarprofil=user.get('gambarprofil')
            if request.method == "POST":
                update_data = {
                        'nama': request.form['nama'],
                        'nohp': request.form['nohp'],
                        'role':request.form['jasa'],
                        'gunung':request.form['gunung'],
                    }
                user=MUser()
                if user.updatedataprofil(email, update_data):
                    msgbenar = "Mohon Ditunggu Untuk di Verifikasi Terlebih Dahulu"
                    return render_template('profil.html', msgbenar=msgbenar,nama=nama, nohp=nohp, email=email, tanggal_lahir=tanggal_lahir, provinsi=provinsi, kabupaten=kabupaten, kecamatan=kecamatan, kode_pos=kode_pos, alamat=alamat,buttonlogin=buttonlogin, buttonuser=buttonuser,bukajasa=bukajasa, dashboard=dashboard,gambarprofil=gambarprofil)
        
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'        
        return render_template('bukajasa.html',nama=nama, nohp=nohp, email=email,buttonlogin=buttonlogin, buttonuser=buttonuser,bukajasa=bukajasa, dashboard=dashboard,gambarprofil=gambarprofil)
   
@app.route('/profil/pesananbelumbayar',methods=["GET","POST"])
def pesanbelumbayar():
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        role=user.get('role')
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''

    else:
        buttonuser='d-none'
        buttonlogin=''
       
    if 'email' in session:
        email = session['email']
        user = MUser().ambildatauser(email)
        
        nama = user.get('nama')
        nohp = user.get('nohp')
            
        user_pesan = MUser()
        user_produk = user_pesan.ambildatapesananstatuslist(nama,nohp,'belum bayar')

        if user_produk is None:
            user_produk = []
            return render_template('pesananbelumbayar.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                    pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil)
        else:
            return render_template('pesananbelumbayar.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                        pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil)
    else:
        return "User not found", 404

@app.route('/profil/pesananbelumbayar/detail', methods=["GET", "POST"])
def pesanbelumbayardetail():
    if 'email' not in session:
        return redirect(url_for('login'))

    elif 'email' in session:
        buttonlogin = 'd-none'
        buttonuser = ''
    else:
        buttonuser = 'd-none'
        buttonlogin = ''

    if request.method == 'POST':
        idpesanan = request.form['idpesanan']
        email = session['email']
        user = MUser().ambildatauser(email)
        nama = user.get('nama')
        nohp = user.get('nohp')
        role = user.get('role')
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        if role == 'Pendaki':
            bukajasa = ''
            dashboard = 'd-none'
            
        elif role == 'Porter':
            bukajasa = 'd-none'
            dashboard = ''

        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''

        if request.method == 'POST':
            idpesanan = request.form['idpesanan']
            email = session['email']
            user = MUser().ambildatauser(email)
            nama = user.get('nama')
            nohp = user.get('nohp')
            gambarprofil=user.get('gambarprofil')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            role = user.get('role')
            if role == 'Pendaki':
                bukajasa=''
                dashboard='d-none'
                
            elif role == 'Porter':
                bukajasa='d-none'
                dashboard=''

                
            user_pesan = MUser()
            existing_order = user_pesan.cari_id(idpesanan)
            porter = 'Porter'
            tourguide = 'Tour Guide'
            penyewaan = 'Penyewaan'
            totalharga = existing_order.get('totalharga')
            gunung = existing_order.get('gunung')
            jalur = existing_order.get('jalur')
            jenisproduk = existing_order.get('jenisproduk')
            namaproduk = existing_order.get('namaproduk')
            metodepembayaran = existing_order.get('metodepembayaran')
            tanggalmendaki = existing_order.get('tanggalmendaki')
            tanggalturun = existing_order.get('tanggalturun')
            statuspesanan = existing_order.get('statuspesanan')
            layanan = 1000
            subtotal= int(totalharga) - 1000
            if jenisproduk == 'porter':
                fieldtourguide='d-none'
                fieldpenyewaan='d-none'
                tourguide=''
                penyewaan=''
                namaporter = existing_order.get('namaporter')
                nohpporter = existing_order.get('nohpporter')
                hargaporter = existing_order.get('hargaporter')
                user_alamat = MUser().ambildatajalur(jalur)
                alamat = user_alamat.get('alamat')
                return render_template('pesananbelumbayarrincian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                    gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                    porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, bukajasa=bukajasa, dashboard=dashboard,nohpporter=nohpporter, gambarprofil=gambarprofil, fieldpenyewaan=fieldpenyewaan,fieldtourguide=fieldtourguide, idpesanan=idpesanan, layanan=layanan, subtotal=subtotal)
                    
            
                    
            elif jenisproduk == 'tour guide':
                fieldporter='d-none'
                fieldpenyewaan='d-none'
                porter=''
                penyewaan=''
                namatourguide = existing_order.get('namatourguide')
                nohptourguide = existing_order.get('nohptourguide')
                hargatourguide = existing_order.get('hargatourguide')
                user_alamat = MUser().ambildatajalur(jalur)
                alamat = user_alamat.get('alamat')
                return render_template('pesananbelumbayarrincian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                    gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk, totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                    porter=porter, tourguide=tourguide, penyewaan=penyewaan, bukajasa=bukajasa, dashboard=dashboard,  namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide, gambarprofil=gambarprofil, fieldpenyewaan=fieldpenyewaan, fieldporter=fieldporter, idpesanan=idpesanan, layanan=layanan, subtotal=subtotal)
                    
            elif jenisproduk == 'paket':
                namaporter = existing_order.get('namaporter')
                nohpporter = existing_order.get('nohpporter')
                hargaporter = existing_order.get('hargaporter')
                namatourguide = existing_order.get('namatourguide')
                nohptourguide = existing_order.get('nohptourguide')
                hargatourguide = existing_order.get('hargatourguide')
                namapenyewaan = existing_order.get('namapenyewaan')
                nohppenyewaan = existing_order.get('nohppenyewaan')
                hargapenyewaan = existing_order.get('hargapenyewaan')
                user_alamat = MUser().ambildatajalur(jalur)
                alamat = user_alamat.get('alamat')
                return render_template('pesananbelumbayarrincian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                    gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                    porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, bukajasa=bukajasa, dashboard=dashboard, nohpporter=nohpporter, namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide, gambarprofil=gambarprofil, namapenyewaan=namapenyewaan, nohppenyewaan=nohppenyewaan, hargapenyewaan=hargapenyewaan, idpesanan=idpesanan, layanan=layanan, subtotal=subtotal)
        
        


        
@app.route('/checkout/bayar2',methods=["GET","POST"])
def pesanmaubayar():
    if 'email' not in session:
        return redirect(url_for('login'))
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email=session['email']
        user=MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'

  
    else:
        buttonuser='d-none'
        buttonlogin=''
    
    if request.method == "POST":
        idpesanan=request.form['idpesanan']
        user_pesan=MUser().cari_id(idpesanan)
        gunung=user_pesan.get('gunung')
        jalur=user_pesan.get('jalur')
        jenisproduk=user_pesan.get('jenisproduk')
        namaproduk=user_pesan.get('namaproduk')
        metodepembayaran=user_pesan.get('metodepembayaran')
        tanggalmendaki=user_pesan.get('tanggalmendaki')
        tanggalturun=user_pesan.get('tanggalturun')
        hargapaket=user_pesan.get('hargapaket')
        waktupesan=user_pesan.get('waktupesan')
        
        nama=user.get('nama')
        nohp=user.get('nohp')
        
        if metodepembayaran == 'Dana' or 'Qris' or 'Shopee':
            ewallet=''
            bank='d-none'
        elif metodepembayaran == 'Transfek Bank BNI' or 'Transfer Bank BRI':
            ewallet='d-none'
            bank=''
        return render_template('bayar1.html', buttonlogin=buttonlogin, buttonuser=buttonuser, gunung=gunung, jalur=jalur, 
                            nama=nama,nohp=nohp,jenisproduk=jenisproduk, namaproduk=namaproduk, harga=hargapaket, metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun, idpesanan=idpesanan,gambarprofil=gambarprofil, ewallet=ewallet, bank=bank, waktupesan=waktupesan)

@app.route('/checkout/berhasilbayar2',methods=["GET","POST"])
def pesanselesaibayar():
    if 'email' not in session:
        return redirect(url_for('login'))

    elif 'email' in session:
        buttonlogin = 'd-none'
        buttonuser = ''

    else:
        buttonuser = 'd-none'
        buttonlogin = ''

    if request.method == 'POST':
        idpesanan = session['idpesanan']
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        nama = user.get('nama')
        nohp = user.get('nohp')
            
        user_pesan = MUser()
        existing_order = user_pesan.cari_id(idpesanan)
        statuspembayaran = existing_order.get('statuspesanan')
        gunung = existing_order.get('gunung')
        jalur = existing_order.get('jalur')
        jenisproduk = existing_order.get('jenisproduk')
        namaproduk = existing_order.get('namaproduk')
        harga = existing_order.get('harga')
        durasi = existing_order.get('durasi')
        maxbeban = existing_order.get('maxbeban')
        metodepembayaran = existing_order.get('metodepembayaran')
        tanggalmendaki = existing_order.get('tanggalmendaki')
        tanggalturun = existing_order.get('tanggalturun')

        if existing_order:
            porter = user_pesan.randomporter()
            nama_porter = porter.get('nama')
            email_porter = porter.get('email')
            user_porter = MUser().ambildatauser(email_porter)
            nohpporter= user_porter.get('nohp')
            tourguide = user_pesan.randomtourguide()
            nama_tourguide = tourguide.get('nama')
            email_tourguide = tourguide.get('email')
            user_tourguide = MUser().ambildatauser(email_tourguide)
            nohptourguide= user_tourguide.get('nohp')
            if statuspembayaran == 'belum bayar':
                user_pesan.updatenamapesanan(idpesanan,nama_porter, nohpporter, nama_tourguide, nohptourguide)
                user_pesan.updatestatuspesananid(idpesanan, 'sudah bayar')
                session.pop=('idpesanan')
                return render_template('sudahbayar.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                           gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                           jenisproduk=jenisproduk, namaproduk=namaproduk, harga=harga, durasi=durasi,
                                           maxbeban=maxbeban, metodepembayaran=metodepembayaran, statuspembayaran=statuspembayaran, gambarprofil=gambarprofil)

@app.route('/profil/pesanansudahbayar',methods=["GET","POST"])
def pesansudahbayar():
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''

    else:
        buttonuser='d-none'
        buttonlogin=''
        
    if 'email' in session:
        email = session['email']
        user = MUser().ambildatauser(email)
        
        nama = user.get('nama')
        nohp = user.get('nohp')
            
        user_pesan = MUser()
        user_produk = user_pesan.ambildatapesananstatuslist(nama,nohp,'sudah bayar')

        if user_produk is None:
            user_produk = []
        
        mendaki = user_pesan.ambildatapesananstatuslist(nama,nohp, 'perjalanan mendaki')    
        if user_produk is not None:
            if isinstance(user_produk, list):
                user_produk.extend(mendaki)
            else:
                user_produk.append(mendaki)
            return render_template('pesanansudahbayar.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                    pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil)
        else:
            return render_template('pesanansudahbayar.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                        pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil)
    else:
        return "User not found", 404


@app.route('/profil/pesanansudahbayar/detail',methods=["GET","POST"])
def pesanselesaibayardetail():
    if 'email' not in session:
        return redirect(url_for('login'))

    elif 'email' in session:
        buttonlogin = 'd-none'
        buttonuser = ''

    else:
        buttonuser = 'd-none'
        buttonlogin = ''

    if request.method == 'POST':
        idpesanan = request.form['idpesanan']
        email = session['email']
        user = MUser().ambildatauser(email)
        nama = user.get('nama')
        nohp = user.get('nohp')
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        role = user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

            
        user_pesan = MUser()
        existing_order = user_pesan.cari_id(idpesanan)
        porter = 'Porter'
        tourguide = 'Tour Guide'
        penyewaan = 'Penyewaan'
        totalharga = existing_order.get('totalharga')
        gunung = existing_order.get('gunung')
        jalur = existing_order.get('jalur')
        jenisproduk = existing_order.get('jenisproduk')
        namaproduk = existing_order.get('namaproduk')
        metodepembayaran = existing_order.get('metodepembayaran')
        tanggalmendaki = existing_order.get('tanggalmendaki')
        tanggalturun = existing_order.get('tanggalturun')
        statuspesanan = existing_order.get('statuspesanan')
        layanan = 1000
        subtotal= int(totalharga) - 1000
        pesanditerima='red'
        perjalananmendaki='red'
        selesai='#00FF1A'
        
        if jenisproduk == 'porter':
            if statuspesanan == 'sudah bayar':
                fieldtourguide='d-none'
                fieldpenyewaan='d-none'
                tourguide=''
                penyewaan=''
                namaporter = existing_order.get('namaporter')
                nohpporter = existing_order.get('nohpporter')
                hargaporter = existing_order.get('hargaporter')
                user_alamat = MUser().ambildatajalur(jalur)
                alamat = user_alamat.get('alamat')
                pesanditerima='#00FF1A'
                perjalananmendaki=''
                selesai=''
                return render_template('pesanansudahbayarrincian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                        gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                        jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                        metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                        porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, bukajasa=bukajasa, dashboard=dashboard,nohpporter=nohpporter, gambarprofil=gambarprofil, fieldpenyewaan=fieldpenyewaan,fieldtourguide=fieldtourguide, idpesanan=idpesanan, layanan=layanan, subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki)
            elif statuspesanan == 'perjalanan mendaki':
                fieldtourguide='d-none'
                fieldpenyewaan='d-none'
                tourguide=''
                penyewaan=''
                namaporter = existing_order.get('namaporter')
                nohpporter = existing_order.get('nohpporter')
                hargaporter = existing_order.get('hargaporter')
                user_alamat = MUser().ambildatajalur(jalur)
                alamat = user_alamat.get('alamat')
                pesanditerima='#00FF1A'
                perjalananmendaki='#00FF1A'
                selesai=''
                buttonbatal='d-none'
                return render_template('pesanansudahbayarrincian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                        gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                        jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                        metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                        porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, bukajasa=bukajasa, dashboard=dashboard,nohpporter=nohpporter, gambarprofil=gambarprofil, fieldpenyewaan=fieldpenyewaan,fieldtourguide=fieldtourguide, idpesanan=idpesanan, layanan=layanan, subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki,buttonbatal=buttonbatal)
                    
            
                    
        elif jenisproduk == 'tour guide':
            if statuspesanan == 'sudah bayar':
                fieldporter='d-none'
                fieldpenyewaan='d-none'
                porter=''
                penyewaan=''
                namatourguide = existing_order.get('namatourguide')
                nohptourguide = existing_order.get('nohptourguide')
                hargatourguide = existing_order.get('hargatourguide')
                user_alamat = MUser().ambildatajalur(jalur)
                alamat = user_alamat.get('alamat')
                pesanditerima='#00FF1A'
                perjalananmendaki=''
                selesai=''
                return render_template('pesanansudahbayarrincian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                        gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                        jenisproduk=jenisproduk, namaproduk=namaproduk, totalharga=totalharga,
                                                        metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                        porter=porter, tourguide=tourguide, penyewaan=penyewaan, bukajasa=bukajasa, dashboard=dashboard,  namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide, gambarprofil=gambarprofil, fieldpenyewaan=fieldpenyewaan, fieldporter=fieldporter, idpesanan=idpesanan, layanan=layanan, subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki)
                
            elif statuspesanan == 'perjalanan mendaki':
                fieldporter='d-none'
                fieldpenyewaan='d-none'
                porter=''
                penyewaan=''
                namatourguide = existing_order.get('namatourguide')
                nohptourguide = existing_order.get('nohptourguide')
                hargatourguide = existing_order.get('hargatourguide')
                user_alamat = MUser().ambildatajalur(jalur)
                alamat = user_alamat.get('alamat')
                pesanditerima='#00FF1A'
                perjalananmendaki='#00FF1A'
                selesai=''
                buttonbatal='d-none'
                return render_template('pesanansudahbayarrincian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                        gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                        jenisproduk=jenisproduk, namaproduk=namaproduk, totalharga=totalharga,
                                                        metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                        porter=porter, tourguide=tourguide, penyewaan=penyewaan, bukajasa=bukajasa, dashboard=dashboard,  namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide, gambarprofil=gambarprofil, fieldpenyewaan=fieldpenyewaan, fieldporter=fieldporter, idpesanan=idpesanan, layanan=layanan, subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki,buttonbatal=buttonbatal)
                    
        elif jenisproduk == 'paket':
            if statuspesanan == 'sudah bayar':
                namaporter = existing_order.get('namaporter')
                nohpporter = existing_order.get('nohpporter')
                hargaporter = existing_order.get('hargaporter')
                namatourguide = existing_order.get('namatourguide')
                nohptourguide = existing_order.get('nohptourguide')
                hargatourguide = existing_order.get('hargatourguide')
                namapenyewaan = existing_order.get('namapenyewaan')
                nohppenyewaan = existing_order.get('nohppenyewaan')
                hargapenyewaan = existing_order.get('hargapenyewaan')
                user_alamat = MUser().ambildatajalur(jalur)
                alamat = user_alamat.get('alamat')
                pesanditerima='#00FF1A'
                perjalananmendaki=''
                selesai=''
                return render_template('pesanansudahbayarrincian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                        gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                        jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                        metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                        porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, bukajasa=bukajasa, dashboard=dashboard, nohpporter=nohpporter, namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide, gambarprofil=gambarprofil, namapenyewaan=namapenyewaan, nohppenyewaan=nohppenyewaan, hargapenyewaan=hargapenyewaan, idpesanan=idpesanan, layanan=layanan, subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki)
                
            elif statuspesanan == 'perjalanan mendaki':
                namaporter = existing_order.get('namaporter')
                nohpporter = existing_order.get('nohpporter')
                hargaporter = existing_order.get('hargaporter')
                namatourguide = existing_order.get('namatourguide')
                nohptourguide = existing_order.get('nohptourguide')
                hargatourguide = existing_order.get('hargatourguide')
                namapenyewaan = existing_order.get('namapenyewaan')
                nohppenyewaan = existing_order.get('nohppenyewaan')
                hargapenyewaan = existing_order.get('hargapenyewaan')
                user_alamat = MUser().ambildatajalur(jalur)
                alamat = user_alamat.get('alamat')
                pesanditerima='#00FF1A'
                perjalananmendaki='#00FF1A'
                selesai=''
                buttonbatal='d-none'
                return render_template('pesanansudahbayarrincian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                        gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                        jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                        metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                        porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, bukajasa=bukajasa, dashboard=dashboard, nohpporter=nohpporter, namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide, gambarprofil=gambarprofil, namapenyewaan=namapenyewaan, nohppenyewaan=nohppenyewaan, hargapenyewaan=hargapenyewaan, idpesanan=idpesanan, layanan=layanan, subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki,buttonbatal=buttonbatal)
                
@app.route('/profil/pesananselesai',methods=["GET","POST"])
def pesanselesai():
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''

    else:
        buttonuser='d-none'
        buttonlogin=''
       
    if 'email' in session:
        email = session['email']
        user = MUser().ambildatauser(email)
        
        nama = user.get('nama')
        nohp = user.get('nohp')
            
        user_pesan = MUser()
        user_produk = user_pesan.ambildatapesananstatuslist(nama,nohp,'selesai')

        if user_produk is None:
            user_produk = []
            return render_template('pesananselesai.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                    pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil)
        else:
            return render_template('pesananselesai.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                        pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil)
    else:
        return "User not found", 404
    
@app.route('/profil/pesananselesai/penilaian',methods=["GET","POST"])
def penilaian():
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''

    else:
        buttonuser='d-none'
        buttonlogin=''
        
    if request.method == 'POST':
        idpesanan = request.form['idpesanan']
        email = session['email']
        user = MUser().ambildatauser(email)
        nama = user.get('nama')
        nohp = user.get('nohp')
            
        user_pesan = MUser()
        existing_order = user_pesan.cari_id(idpesanan)
        porter = 'Porter'
        tourguide = 'Tour Guide'
        penyewaan = 'Penyewaan'
        totalharga = existing_order.get('totalharga')
        gunung = existing_order.get('gunung')
        jalur = existing_order.get('jalur')
        jenisproduk = existing_order.get('jenisproduk')
        namaproduk = existing_order.get('namaproduk')
        metodepembayaran = existing_order.get('metodepembayaran')
        tanggalmendaki = existing_order.get('tanggalmendaki')
        tanggalturun = existing_order.get('tanggalturun')
        statuspesanan = existing_order.get('statuspesanan')
        layanan = 1000
        subtotal= int(totalharga) - 1000
        pesanditerima='#00FF1A'
        perjalananmendaki='#00FF1A'
        selesai='#00FF1A'
        if jenisproduk == 'porter':
            fieldtourguide='d-none'
            fieldpenyewaan='d-none'
            tourguide=''
            penyewaan=''
            namaporter = existing_order.get('namaporter')
            nohpporter = existing_order.get('nohpporter')
            hargaporter = existing_order.get('hargaporter')
            user_alamat = MUser().ambildatajalur(jalur)
            alamat = user_alamat.get('alamat')
            return render_template('pesananpenilaian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, bukajasa=bukajasa, dashboard=dashboard,nohpporter=nohpporter, gambarprofil=gambarprofil, layanan=layanan,subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki, fieldpenyewaan=fieldpenyewaan,fieldtourguide=fieldtourguide,idpesanan=idpesanan)
                
                
        elif jenisproduk == 'tour guide':
            fieldporter='d-none'
            fieldpenyewaan='d-none'
            porter=''
            penyewaan=''
            namatourguide = existing_order.get('namatourguide')
            nohptourguide = existing_order.get('nohptourguide')
            hargatourguide = existing_order.get('hargatourguide')
            user_alamat = MUser().ambildatajalur(jalur)
            alamat = user_alamat.get('alamat')
            return render_template('pesananpenilaian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                jenisproduk=jenisproduk, namaproduk=namaproduk, totalharga=totalharga,
                                                metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                porter=porter, tourguide=tourguide, penyewaan=penyewaan, bukajasa=bukajasa, dashboard=dashboard, namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide, gambarprofil=gambarprofil, layanan=layanan,subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki, fieldpenyewaan=fieldpenyewaan, fieldporter=fieldporter,idpesanan=idpesanan)
            
                
        elif jenisproduk == 'paket':
            namaporter = existing_order.get('namaporter')
            nohpporter = existing_order.get('nohpporter')
            hargaporter = existing_order.get('hargaporter')
            namatourguide = existing_order.get('namatourguide')
            nohptourguide = existing_order.get('nohptourguide')
            hargatourguide = existing_order.get('hargatourguide')
            namapenyewaan = existing_order.get('namapenyewaan')
            nohppenyewaan = existing_order.get('nohppenyewaan')
            hargapenyewaan = existing_order.get('hargapenyewaan')
            user_alamat = MUser().ambildatajalur(jalur)
            alamat = user_alamat.get('alamat')
            return render_template('pesananpenilaian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat, namapenyewaan=namapenyewaan, nohppenyewaan=nohppenyewaan, hargapenyewaan=hargapenyewaan,
                                                porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, bukajasa=bukajasa, dashboard=dashboard, nohpporter=nohpporter, namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide, gambarprofil=gambarprofil, layanan=layanan,subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki,idpesanan=idpesanan)


@app.route('/profil/pesananselesai/penilaianberhasil',methods=["GET","POST"])
def penilaianberhasil():
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''

    else:
        buttonuser='d-none'
        buttonlogin=''
        
    if request.method == 'POST':
        idpesanan = request.form['idpesanan']
        jenisproduk = request.form['jenisproduk']
        email = session['email']
        user = MUser().ambildatauser(email)
        nama = user.get('nama')
        nohp = user.get('nohp')
        if jenisproduk == 'porter':
            penilaianporter=request.form['penilaianporter']
            update_data={
                "penilaianporter":penilaianporter
            }
            user_pesan=MUser().updatenamapesanan(idpesanan,update_data)
            user_pesan = MUser()
            user_produk = user_pesan.ambildatapesananstatuslist(nama,nohp,'selesai')

            if user_produk is None:
                user_produk = []
            return render_template('pesananselesai.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                    pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil,idpesanan=idpesanan)
                
        elif jenisproduk == 'tour guide':
            penilaiantourguide=request.form['penilaiantourguide']
            update_data={
                "penilaiantourguide":penilaiantourguide
            }
            user_pesan=MUser().updatenamapesanan(idpesanan,update_data)
            user_pesan = MUser()
            user_produk = user_pesan.ambildatapesananstatuslist(nama,nohp,'selesai')

            if user_produk is None:
                user_produk = []
            return render_template('pesananselesai.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                    pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil,idpesanan=idpesanan)
            
        elif jenisproduk == 'paket':
            penilaianporter=request.form['penilaianporter']
            penilaiantourguide=request.form['penilaiantourguide']
            penilaianpenyewaan=request.form['penilaianpenyewaan']
            update_data={
                "penilaianporter":int(penilaianporter),
                "penilaiantourguide":int(penilaiantourguide),
                "penilaianpenyewaan":int(penilaianpenyewaan)
            }
            user_pesan=MUser().updatenamapesanan(idpesanan,update_data)
            user_pesan = MUser()
            user_produk = user_pesan.ambildatapesananstatuslist(nama,nohp,'selesai')

            if user_produk is None:
                user_produk = []
            return render_template('pesananselesai.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                    pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil,idpesanan=idpesanan)


@app.route('/profil/pesananselesai/penilaiandetail',methods=["GET","POST"])
def penilaiantampil():
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''

    else:
        buttonuser='d-none'
        buttonlogin=''
        
    if request.method == 'POST':
        idpesanan = request.form['idpesanan']
        email = session['email']
        user = MUser().ambildatauser(email)
        nama = user.get('nama')
        nohp = user.get('nohp')
            
        user_pesan = MUser()
        existing_order = user_pesan.cari_id(idpesanan)
        porter = 'Porter'
        tourguide = 'Tour Guide'
        penyewaan = 'Penyewaan'
        totalharga = existing_order.get('totalharga')
        gunung = existing_order.get('gunung')
        jalur = existing_order.get('jalur')
        jenisproduk = existing_order.get('jenisproduk')
        namaproduk = existing_order.get('namaproduk')
        metodepembayaran = existing_order.get('metodepembayaran')
        tanggalmendaki = existing_order.get('tanggalmendaki')
        tanggalturun = existing_order.get('tanggalturun')
        statuspesanan = existing_order.get('statuspesanan')
        layanan = 1000
        subtotal= int(totalharga) - 1000
        pesanditerima='#00FF1A'
        perjalananmendaki='#00FF1A'
        selesai='#00FF1A'
        if jenisproduk == 'porter':
            fieldtourguide='d-none'
            fieldpenyewaan='d-none'
            tourguide=''
            penyewaan=''
            namaporter = existing_order.get('namaporter')
            nohpporter = existing_order.get('nohpporter')
            hargaporter = existing_order.get('hargaporter')
            penilaianporter = existing_order.get('penilaianporter')
            user_alamat = MUser().ambildatajalur(jalur)
            alamat = user_alamat.get('alamat')
            return render_template('pesananpenilaianselesai.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, bukajasa=bukajasa, dashboard=dashboard,nohpporter=nohpporter, gambarprofil=gambarprofil, layanan=layanan,subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki, fieldpenyewaan=fieldpenyewaan,fieldtourguide=fieldtourguide,idpesanan=idpesanan,penilaianporter=penilaianporter)
                
                
        elif jenisproduk == 'tour guide':
            fieldporter='d-none'
            fieldpenyewaan='d-none'
            porter=''
            penyewaan=''
            namatourguide = existing_order.get('namatourguide')
            nohptourguide = existing_order.get('nohptourguide')
            hargatourguide = existing_order.get('hargatourguide')
            penilaiantourguide = existing_order.get('penilaiantourguide')
            user_alamat = MUser().ambildatajalur(jalur)
            alamat = user_alamat.get('alamat')
            return render_template('pesananpenilaianselesai.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                jenisproduk=jenisproduk, namaproduk=namaproduk, totalharga=totalharga,
                                                metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                porter=porter, tourguide=tourguide, penyewaan=penyewaan, bukajasa=bukajasa, dashboard=dashboard, namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide, gambarprofil=gambarprofil, layanan=layanan,subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki, fieldpenyewaan=fieldpenyewaan, fieldporter=fieldporter,idpesanan=idpesanan,penilaiantourguide=penilaiantourguide)
            
                
        elif jenisproduk == 'paket':
            namaporter = existing_order.get('namaporter')
            nohpporter = existing_order.get('nohpporter')
            hargaporter = existing_order.get('hargaporter')
            namatourguide = existing_order.get('namatourguide')
            nohptourguide = existing_order.get('nohptourguide')
            hargatourguide = existing_order.get('hargatourguide')
            namapenyewaan = existing_order.get('namapenyewaan')
            nohppenyewaan = existing_order.get('nohppenyewaan')
            hargapenyewaan = existing_order.get('hargapenyewaan')
            penilaianporter = existing_order.get('penilaianporter')
            penilaiantourguide = existing_order.get('penilaiantourguide')
            penilaianpenyewaan = existing_order.get('penilaianpenyewaan')
            user_alamat = MUser().ambildatajalur(jalur)
            alamat = user_alamat.get('alamat')
            return render_template('pesananpenilaianselesai.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat, namapenyewaan=namapenyewaan, nohppenyewaan=nohppenyewaan, hargapenyewaan=hargapenyewaan,
                                                porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, bukajasa=bukajasa, dashboard=dashboard, nohpporter=nohpporter, namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide, gambarprofil=gambarprofil, layanan=layanan,subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki,idpesanan=idpesanan, penilaianpenyewaan=penilaianpenyewaan, penilaianporter=penilaianporter, penilaiantourguide=penilaiantourguide)
        
          
@app.route('/profil/pesananbatal',methods=["GET","POST"])
def pesanbatal():
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''

    else:
        buttonuser='d-none'
        buttonlogin=''
        
    if 'email' in session:
        email = session['email']
        user = MUser().ambildatauser(email)
        
        nama = user.get('nama')
        nohp = user.get('nohp')
            
        user_pesan = MUser()
        user_produk = user_pesan.ambildatapesananstatuslist(nama,nohp,'dibatalkan')

        if user_produk is None:
            jenisproduk=user_produk.get('jenisproduk')
            if jenisproduk=='porter':
                fieldporter=''
                fieldtourguide='d-none'
                fieldpenyewaan='d-none'
            elif jenisproduk=='tour guide':
                fieldporter='d-none'
                fieldtourguide=''
                fieldpenyewaan='d-none'
            elif jenisproduk=='paket':
                fieldporter=''
                fieldtourguide=''
                fieldpenyewaan=''
            user_produk = []
            return render_template('pesananbatal.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                    pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil, fieldporter=fieldporter, fieldtourguide=fieldtourguide, fieldpenyewaan=fieldpenyewaan)
        else:
            return render_template('pesananbatal.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                        pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil)
        
@app.route('/profil/pesananbatal/detail',methods=["GET","POST"])
def pesanbataldetail():
    if 'email' not in session:
        return redirect(url_for('login'))

    elif 'email' in session:
        buttonlogin = 'd-none'
        buttonuser = ''

    else:
        buttonuser = 'd-none'
        buttonlogin = ''

    if request.method == 'POST':
        idpesanan = request.form['idpesanan']
        email = session['email']
        user = MUser().ambildatauser(email)
        nama = user.get('nama')
        nohp = user.get('nohp')
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        role = user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

            
        user_pesan = MUser()
        existing_order = user_pesan.cari_id(idpesanan)
        porter = 'Porter'
        tourguide = 'Tour Guide'
        penyewaan = 'Penyewaan'
        totalharga = existing_order.get('totalharga')
        gunung = existing_order.get('gunung')
        jalur = existing_order.get('jalur')
        jenisproduk = existing_order.get('jenisproduk')
        namaproduk = existing_order.get('namaproduk')
        metodepembayaran = existing_order.get('metodepembayaran')
        tanggalmendaki = existing_order.get('tanggalmendaki')
        tanggalturun = existing_order.get('tanggalturun')
        statuspesanan = existing_order.get('statuspesanan')
        layanan = 1000
        subtotal= int(totalharga) - 1000
        pesanditerima='red'
        perjalananmendaki='red'
        selesai='#00FF1A'
        
        if jenisproduk == 'porter':
            fieldtourguide='d-none'
            fieldpenyewaan='d-none'
            tourguide=''
            penyewaan=''
            namaporter = existing_order.get('namaporter')
            nohpporter = existing_order.get('nohpporter')
            hargaporter = existing_order.get('hargaporter')
            user_alamat = MUser().ambildatajalur(jalur)
            alamat = user_alamat.get('alamat')
            return render_template('pesananbatalrincian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                    gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                    porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, bukajasa=bukajasa, dashboard=dashboard,nohpporter=nohpporter, gambarprofil=gambarprofil, fieldpenyewaan=fieldpenyewaan,fieldtourguide=fieldtourguide, idpesanan=idpesanan, layanan=layanan, subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki)
                    
            
                    
        elif jenisproduk == 'tour guide':
            fieldporter='d-none'
            fieldpenyewaan='d-none'
            porter=''
            penyewaan=''
            namatourguide = existing_order.get('namatourguide')
            nohptourguide = existing_order.get('nohptourguide')
            hargatourguide = existing_order.get('hargatourguide')
            user_alamat = MUser().ambildatajalur(jalur)
            alamat = user_alamat.get('alamat')
            return render_template('pesananbatalrincian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                    gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk, totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                    porter=porter, tourguide=tourguide, penyewaan=penyewaan, bukajasa=bukajasa, dashboard=dashboard,  namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide, gambarprofil=gambarprofil, fieldpenyewaan=fieldpenyewaan, fieldporter=fieldporter, idpesanan=idpesanan, layanan=layanan, subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki)
                    
        elif jenisproduk == 'paket':
            namaporter = existing_order.get('namaporter')
            nohpporter = existing_order.get('nohpporter')
            hargaporter = existing_order.get('hargaporter')
            namatourguide = existing_order.get('namatourguide')
            nohptourguide = existing_order.get('nohptourguide')
            hargatourguide = existing_order.get('hargatourguide')
            namapenyewaan = existing_order.get('namapenyewaan')
            nohppenyewaan = existing_order.get('nohppenyewaan')
            hargapenyewaan = existing_order.get('hargapenyewaan')
            user_alamat = MUser().ambildatajalur(jalur)
            alamat = user_alamat.get('alamat')
            return render_template('pesananbatalrincian.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                    gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                    porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, bukajasa=bukajasa, dashboard=dashboard, nohpporter=nohpporter, namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide, gambarprofil=gambarprofil, namapenyewaan=namapenyewaan, nohppenyewaan=nohppenyewaan, hargapenyewaan=hargapenyewaan, idpesanan=idpesanan, layanan=layanan, subtotal=subtotal,selesai=selesai, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki)
        
@app.route('/profil/batalkanpesanan',methods=["GET","POST"])
def pesanmaubatal():
    if 'email' not in session:
        return redirect(url_for('login'))

    elif 'email' in session:
        buttonlogin = 'd-none'
        buttonuser = ''

    else:
        buttonuser = 'd-none'
        buttonlogin = ''

    if request.method == 'POST':
        idpesanan = request.form['idpesanan']
        email = session['email']
        user = MUser().ambildatauser(email)
        nama = user.get('nama')
        nohp = user.get('nohp')
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        role = user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

            
        user_pesan = MUser()
        existing_order = user_pesan.cari_id(idpesanan)
        porter = 'Porter'
        tourguide = 'Tour Guide'
        penyewaan = 'Penyewaan'
        totalharga = existing_order.get('totalharga')
        gunung = existing_order.get('gunung')
        jalur = existing_order.get('jalur')
        jenisproduk = existing_order.get('jenisproduk')
        namaproduk = existing_order.get('namaproduk')
        metodepembayaran = existing_order.get('metodepembayaran')
        tanggalmendaki = existing_order.get('tanggalmendaki')
        tanggalturun = existing_order.get('tanggalturun')
        statuspesanan = existing_order.get('statuspesanan')
        return render_template('pesananmaubatal.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                                    gunung=gunung, jalur=jalur, nama=nama, nohp=nohp,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk,totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,
                                                    porter=porter, tourguide=tourguide, penyewaan=penyewaan,bukajasa=bukajasa, dashboard=dashboard,gambarprofil=gambarprofil, idpesanan=idpesanan )
                    
            
                    

            
@app.route('/profil/berhasilbatal',methods=["GET","POST"])
def pesanbatalkanpesanan():
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''

    else:
        buttonuser='d-none'
        buttonlogin=''
        
    if request.method == "POST":
        idpesanan=request.form['idpesanan']
        alasanpembatalan=request.form['alasanpembatalan']
        update_data={
                        "statuspesanan":"dibatalkan",
                        "alasanpembatalan":alasanpembatalan
                    }
        user_pesan=MUser().updatenamapesanan(idpesanan,update_data)
        msg="Pesanan Berhasil Di Batalkan"    
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            
            nama = user.get('nama')
            nohp = user.get('nohp')
                
            user_pesan = MUser()
            user_produk = user_pesan.ambildatapesananstatuslist(nama,nohp,'dibatalkan')

            if user_produk is None:
                user_produk = []
                return render_template('pesananbatal.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                        pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil, msg=msg)
            else:
                return render_template('pesananbatal.html', buttonlogin=buttonlogin, buttonuser=buttonuser,
                                            pesanan_list=user_produk,bukajasa=bukajasa, dashboard=dashboard, gambarprofil=gambarprofil, msg=msg)      

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            nama = user.get('nama')
            nohp = user.get('nohp')
            role = user.get('role')
            
            if role == 'Porter':
                user_pesan = MUser()
                user_produk = user_pesan.ambildatapesananporterlistjasaporter(nama,'sudah bayar')
                user_dibatalkan = user_pesan.ambildatapesananporterlistjasaporter(nama,'dibatalkan')
                if user_produk is None:
                    user_produk = []
                
                if user_dibatalkan is None:
                    user_dibatalkan=[]
                
                total=MUser().ambildatatotalpesananporter(nama,nohp)
                totalbatal=MUser().ambildatatotalbatalpesananporter(nama,nohp)
                totalpenilaian=MUser().ambildatatotalpenilaianpesananporter(nama,nohp)
                totalpendapatan=MUser().ambildatatotalpendapatanpesananporter(nama,nohp)
                
            elif role == 'Tour Guide':
                user_pesan = MUser()
                user_produk = user_pesan.ambildatapesananporterlistjasatourguide(nama,'sudah bayar')
                user_dibatalkan = user_pesan.ambildatapesananporterlistjasatourguide(nama,'dibatalkan')
                if user_produk is None:
                    user_produk = []
                    
                if user_dibatalkan is None:
                    user_dibatalkan=[]
                    
                total=MUser().ambildatatotalpesanantourguide(nama,nohp)
                totalbatal=MUser().ambildatatotalbatalpesanantourguide(nama,nohp)
                totalpenilaian=MUser().ambildatatotalpenilaianpesanantourguide(nama,nohp)
                totalpendapatan=MUser().ambildatatotalpendapatanpesanantourguide(nama,nohp)
                    
            elif role == 'Penyewaan':
                user_pesan = MUser()
                user_produk = user_pesan.ambildatapesananporterlistjasapenyewaan(nama,'sudah bayar')
                user_dibatalkan = user_pesan.ambildatapesananporterlistjasapenyewaan(nama,'dibatalkan')
                if user_produk is None:
                    user_produk = []
                if user_dibatalkan is None:
                    user_dibatalkan=[]
                    
                total=MUser().ambildatatotalpesananpenyewaan(nama,nohp)  
                totalbatal=MUser().ambildatatotalbatalpesananpenyewaan(nama,nohp)  
                totalpenilaian=MUser().ambildatatotalpenilaianpesananpenyewaan(nama,nohp)
                totalpendapatan=MUser().ambildatatotalpendapatanpesananpenyewaan(nama,nohp)
                
            return render_template('dashboardjasa.html', pesanan_list=user_produk, pesananbatal_list=user_dibatalkan, nama=nama,gambarprofil=gambarprofil,totalpesanan=total, totalbatal=totalbatal, totalpenilaian=totalpenilaian, totalpendapatan=totalpendapatan)
        
        
@app.route('/dashbooard/profil', methods=['GET','POST'])
def dashboardprofil():
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''
    else:
        buttonuser='d-none'
        buttonlogin=''      
    
    if 'email' in session:
        email = session['email']
        user = MUser().ambildatauser(email)
        nama=user.get('nama')
        nohp=user.get('nohp')
        email=user.get('email')
        tanggal_lahir=user.get('tanggal_lahir')
        provinsi=user.get('provinsi')
        kabupaten=user.get('kabupaten')
        kecamatan=user.get('kecamatan')
        kode_pos=user.get('kode_pos')
        alamat=user.get('alamat')
        gambarprofil=user.get('gambarprofil')
        if gambarprofil == '':
            gambarprofil='profil.svg'
        
    if request.method == 'POST':
        update_data = {
                'nohp': request.form['nohp'],
                'tanggal_lahir': request.form['tanggal_lahir'],
                'provinsi': request.form['provinsi'],
                'kabupaten': request.form['kabupaten'],
                'kecamatan': request.form['kecamatan'],
                'kode_pos': request.form['kode_pos'],
                'alamat': request.form['alamat']
        }
        user=MUser()
        if user.updatedataprofil(email, update_data):
            user = MUser().ambildatauser(email)
            nama=user.get('nama')
            nohp=user.get('nohp')
            email=user.get('email')
            tanggal_lahir=user.get('tanggal_lahir')
            provinsi=user.get('provinsi')
            kabupaten=user.get('kabupaten')
            kecamatan=user.get('kecamatan')
            kode_pos=user.get('kode_pos')
            alamat=user.get('alamat')
            msgbenar = 'Data Berhasil di Update'
            return render_template('dashboardprofil.html', msgbenar=msgbenar,nama=nama, nohp=nohp, email=email, tanggal_lahir=tanggal_lahir, provinsi=provinsi, kabupaten=kabupaten, kecamatan=kecamatan, kode_pos=kode_pos, alamat=alamat,buttonlogin=buttonlogin, buttonuser=buttonuser,bukajasa=bukajasa, dashboard=dashboard,gambarprofil=gambarprofil)
        else:
            msgsalah = 'Data Gagal di Update'
            return render_template('dashboardprofil.html',msgsalah=msgsalah,nama=nama, nohp=nohp, email=email, tanggal_lahir=tanggal_lahir, provinsi=provinsi, kabupaten=kabupaten, kecamatan=kecamatan, kode_pos=kode_pos, alamat=alamat,buttonlogin=buttonlogin, buttonuser=buttonuser,bukajasa=bukajasa, dashboard=dashboard,gambarprofil=gambarprofil)
        
    return render_template('dashboardprofil.html',nama=nama, nohp=nohp, email=email, tanggal_lahir=tanggal_lahir, provinsi=provinsi, kabupaten=kabupaten, kecamatan=kecamatan, kode_pos=kode_pos, alamat=alamat,buttonlogin=buttonlogin, buttonuser=buttonuser,bukajasa=bukajasa, dashboard=dashboard,gambarprofil=gambarprofil)

@app.route('/dashboard/updatefotoprofil', methods=['POST'])
def dashboardupdatefotoprofil():
    
    app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/static/uploads/profil'
    app.config['MAX_CONTENT_PATH'] = 10000000
    
    if 'email' not in session:
        return url_for('login')
        
    elif 'email' in session:
        buttonlogin='d-none'
        buttonuser=''
        email = session['email']
        user = MUser().ambildatauser(email)
        role=user.get('role')
        if role == 'Pendaki':
            bukajasa=''
            dashboard='d-none'
            
        elif role == 'Porter':
            bukajasa='d-none'
            dashboard=''

        elif role == 'Tour Guide':
            bukajasa='d-none'
            dashboard=''
            
        elif role == 'Penyewaan':
            bukajasa='d-none'
            dashboard=''
        
    else:
        buttonuser='d-none'
        buttonlogin=''
        
    if request.method == 'POST':
        if 'email' in session:   
            email = session['email']
            user = MUser().ambildatauser(email)
            nama=user.get('nama')
            nohp=user.get('nohp')
            email=user.get('email')
            tanggal_lahir=user.get('tanggal_lahir')
            provinsi=user.get('provinsi')
            kabupaten=user.get('kabupaten')
            kecamatan=user.get('kecamatan')
            kode_pos=user.get('kode_pos')
            alamat=user.get('alamat')
            
            f = request.files['fotoprofil']
            namagambar = secure_filename(f.filename)
            filename = app.config['UPLOAD_FOLDER'] + '/' + secure_filename(f.filename)
            f.save(filename)
            update_data={
                'gambarprofil' : namagambar
            }
            userupdate=MUser()
            if userupdate.updatedataprofil(email, update_data):
                msgbenar = "Foto Profil Sudah Di Ubah"
                gambarprofil=namagambar
                return render_template('dashboardprofil.html', msgbenar=msgbenar,nama=nama, nohp=nohp, email=email, tanggal_lahir=tanggal_lahir, provinsi=provinsi, kabupaten=kabupaten, kecamatan=kecamatan, kode_pos=kode_pos, alamat=alamat,buttonlogin=buttonlogin, buttonuser=buttonuser,bukajasa=bukajasa, dashboard=dashboard,gambarprofil=gambarprofil)
    
 
@app.route('/dashboard/pesanan')
def dashboardpesanan():
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            nama=user.get('nama')
            role=user.get('role')
            if role == 'Porter':
                user_pesan = MUser()
                user_pesanan = user_pesan.ambildatapesananporterlistporter(nama)
                
                if user_pesanan is None:
                    user_pesanan = []
                    return render_template('dashboardpesanan.html',pesanan_list=user_pesanan, nama=nama,gambarprofil=gambarprofil)
                else:
                    return render_template('dashboardpesanan.html',pesanan_list=user_pesanan,nama=nama,gambarprofil=gambarprofil)
        
            elif role == 'Tour Guide':
                    user_pesan = MUser()
                    user_pesanan = user_pesan.ambildatapesananporterlisttourguide(nama)
                    
                    if user_pesanan is None:
                        user_pesanan = []
                        return render_template('dashboardpesanan.html',pesanan_list=user_pesanan, nama=nama,gambarprofil=gambarprofil)
                    else:
                        return render_template('dashboardpesanan.html',pesanan_list=user_pesanan,nama=nama,gambarprofil=gambarprofil)

            elif role == 'Penyewaan':
                    user_pesan = MUser()
                    user_pesanan = user_pesan.ambildatapesananporterlistpenyewaan(nama)
                    
                    if user_pesanan is None:
                        user_pesanan = []
                        return render_template('dashboardpesanan.html',pesanan_list=user_pesanan, nama=nama,gambarprofil=gambarprofil)
                    else:
                        return render_template('dashboardpesanan.html',pesanan_list=user_pesanan,nama=nama,gambarprofil=gambarprofil)
                    
@app.route('/dashboard/pesanan/penilaian', methods=["GET","POST"])
def dashboardpesananpenilaian():
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            nama=user.get('nama')
            role=user.get('role')
            
        if request.method == 'POST':
            idpesanan = request.form['idpesanan']

            user_pesan = MUser()
            existing_order = user_pesan.cari_id(idpesanan)
            namapendaki=existing_order.get('nama')
            nohppendaki=existing_order.get('nohp')
            user_pendaki=MUser().ambildatapendaki(namapendaki, nohppendaki)
            emailpendaki=user_pendaki.get('email')
            porter = 'Porter'
            tourguide = 'Tour Guide'
            penyewaan = 'Penyewaan'
            totalharga = existing_order.get('totalharga')
            gunung = existing_order.get('gunung')
            jalur = existing_order.get('jalur')
            jenisproduk = existing_order.get('jenisproduk')
            namaproduk = existing_order.get('namaproduk')
            metodepembayaran = existing_order.get('metodepembayaran')
            tanggalmendaki = existing_order.get('tanggalmendaki')
            tanggalturun = existing_order.get('tanggalturun')
            statuspesanan = existing_order.get('statuspesanan')
            pesanditerima='#00FF1A'
            perjalananmendaki='#00FF1A'
            selesai='#00FF1A'
            fieldporter=''
            fieldtourguide=''
            fieldpenyewaan=''
            if role == 'Porter':
                fieldtourguide='d-none'
                fieldpenyewaan='d-none'
                tourguide=''
                penyewaan=''
                namaporter = existing_order.get('namaporter')
                nohpporter = existing_order.get('nohpporter')
                hargaporter = existing_order.get('hargaporter')
                penilaianporter=existing_order.get('penilaianporter')
                                        
                return render_template('dashboardpesananpenilaian.html',
                                                    gunung=gunung, jalur=jalur, nama=nama,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,penilaianporter=penilaianporter,
                                                    porter=porter,  penyewaan=penyewaan,namaporter=namaporter, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki, selesai=selesai,nohpporter=nohpporter,gambarprofil=gambarprofil, idpesanan=idpesanan, namapendaki=namapendaki, nohppendaki=nohppendaki,fieldporter=fieldporter,fieldtourguide=fieldtourguide,fieldpenyewaan=fieldpenyewaan,emailpendaki=emailpendaki)
                    
            elif role == 'Tour Guide':
                fieldporter='d-none'
                fieldpenyewaan='d-none'
                porter=''
                penyewaan=''
                namatourguide = existing_order.get('namatourguide')
                nohptourguide = existing_order.get('nohptourguide')
                hargatourguide = existing_order.get('hargatourguide')   
                penilaiantourguide=existing_order.get('penilaiantourguide')              
                    
                return render_template('dashboardpesananpenilaian.html',
                                                    gunung=gunung, jalur=jalur, nama=nama,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk,totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,penilaiantourguide=penilaiantourguide,
                                                    porter=porter, tourguide=tourguide, penyewaan=penyewaan, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki, selesai=selesai,namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide,gambarprofil=gambarprofil, idpesanan=idpesanan, namapendaki=namapendaki, nohppendaki=nohppendaki,fieldporter=fieldporter,fieldtourguide=fieldtourguide,fieldpenyewaan=fieldpenyewaan,emailpendaki=emailpendaki)
                
            elif role == 'Penyewaan':
                fieldtourguide='d-none'
                fieldporter='d-none'
                porter=''
                tourguide=''
                namapendaki = existing_order.get('nama')
                nohppendaki = existing_order.get('nohppendaki')
                hargapenyewaan = existing_order.get('hargaporter')
                penilaianpenyewaan=existing_order.get('penilaianpenyewaan')
               
                return render_template('dashboardpesananpenilaian.html',
                                                    gunung=gunung, jalur=jalur, nama=nama,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk,totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,
                                                    porter=porter, tourguide=tourguide, penyewaan=penyewaan,hargapenyewaan=hargapenyewaan, penilaianpenyewaan=penilaianpenyewaan,pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki, selesai=selesai,gambarprofil=gambarprofil, idpesanan=idpesanan, namapendaki=namapendaki, nohppendaki=nohppendaki,fieldporter=fieldporter,fieldtourguide=fieldtourguide,fieldpenyewaan=fieldpenyewaan,emailpendaki=emailpendaki)
                
@app.route('/dashboard/pesanan/detail', methods=["GET","POST"])
def dashboardpesanandetail():
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            nama=user.get('nama')
            role=user.get('role')
            
        if request.method == 'POST':
            idpesanan = request.form['idpesanan']

            user_pesan = MUser()
            existing_order = user_pesan.cari_id(idpesanan)
            namapendaki=existing_order.get('nama')
            nohppendaki=existing_order.get('nohp')
            porter = 'Porter'
            tourguide = 'Tour Guide'
            penyewaan = 'Penyewaan'
            totalharga = existing_order.get('totalharga')
            gunung = existing_order.get('gunung')
            jalur = existing_order.get('jalur')
            jenisproduk = existing_order.get('jenisproduk')
            namaproduk = existing_order.get('namaproduk')
            metodepembayaran = existing_order.get('metodepembayaran')
            tanggalmendaki = existing_order.get('tanggalmendaki')
            tanggalturun = existing_order.get('tanggalturun')
            statuspesanan = existing_order.get('statuspesanan')
            fieldporter=''
            fieldtourguide=''
            fieldpenyewaan=''
            if jenisproduk == 'porter':
                fieldtourguide='d-none'
                fieldpenyewaan='d-none'
                tourguide=''
                penyewaan=''
                namaporter = existing_order.get('namaporter')
                nohpporter = existing_order.get('nohpporter')
                hargaporter = existing_order.get('hargaporter')
                if statuspesanan == 'sudah bayar':
                    pesanditerima='#00FF1A'
                    perjalananmendaki=''
                    selesai=''
                    buttonupdate=''
                    fieldpembatalan='d-none'
                    alasanpembatalan= ''
                    user_alamat = MUser().ambildatajalur(jalur)
                    alamat = user_alamat.get('alamat')
                    
                elif statuspesanan == 'perjalanan mendaki':
                    pesanditerima='#00FF1A'
                    perjalananmendaki='#00FF1A'
                    selesai=''
                    buttonupdate=''
                    fieldpembatalan='d-none'
                    alasanpembatalan= ''
                    user_alamat = MUser().ambildatajalur(jalur)
                    alamat = user_alamat.get('alamat')
                    
                elif statuspesanan == 'selesai':
                    pesanditerima='#00FF1A'
                    perjalananmendaki='#00FF1A'
                    selesai='#00FF1A'
                    buttonupdate='d-none'
                    fieldpembatalan='d-none'
                    alasanpembatalan= ''
                    user_alamat = MUser().ambildatajalur(jalur)
                    alamat = user_alamat.get('alamat')
                    
                elif statuspesanan == 'dibatalkan':
                    pesanditerima='red'
                    perjalananmendaki='red'
                    selesai='#00FF1A'
                    buttonupdate='d-none'
                    fieldpembatalan=''
                    alasanpembatalan= existing_order.get('alasanpembatalan')
                    user_alamat = MUser().ambildatajalur(jalur)
                    alamat = user_alamat.get('alamat')
                    
                    
                return render_template('dashboardpesananstatus.html',
                                                    gunung=gunung, jalur=jalur, nama=nama,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                    porter=porter,  penyewaan=penyewaan,namaporter=namaporter, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki, selesai=selesai,nohpporter=nohpporter,gambarprofil=gambarprofil, idpesanan=idpesanan, namapendaki=namapendaki, nohppendaki=nohppendaki,buttonupdate=buttonupdate, fieldpembatalan=fieldpembatalan, alasanpembatalan=alasanpembatalan,fieldpenyewaan=fieldpenyewaan,fieldporter=fieldporter,fieldtourguide=fieldtourguide,statuspesanan=statuspesanan)
                    
            elif jenisproduk == 'tour guide':
                porter=''
                penyewaan=''
                fieldporter='d-none'
                fieldpenyewaan='d-none'
                namatourguide = existing_order.get('namatourguide')
                nohptourguide = existing_order.get('nohptourguide')
                hargatourguide = existing_order.get('hargatourguide')
                if statuspesanan == 'sudah bayar':
                    pesanditerima='#00FF1A'
                    perjalananmendaki=''
                    selesai=''
                    buttonupdate=''
                    fieldpembatalan='d-none'
                    alasanpembatalan= ''
                    user_alamat = MUser().ambildatajalur(jalur)
                    alamat = user_alamat.get('alamat')
                
                elif statuspesanan == 'perjalanan mendaki':
                    pesanditerima='#00FF1A'
                    perjalananmendaki='#00FF1A'
                    selesai=''
                    buttonupdate=''
                    fieldpembatalan='d-none'
                    alasanpembatalan= ''
                    user_alamat = MUser().ambildatajalur(jalur)
                    alamat = user_alamat.get('alamat')
                    
                elif statuspesanan == 'selesai':
                    pesanditerima='#00FF1A'
                    perjalananmendaki='#00FF1A'
                    selesai='#00FF1A'
                    buttonupdate='d-none'
                    fieldpembatalan='d-none'
                    alasanpembatalan= ''
                    user_alamat = MUser().ambildatajalur(jalur)
                    alamat = user_alamat.get('alamat')
                    
                elif statuspesanan == 'dibatalkan':
                    pesanditerima='red'
                    perjalananmendaki='red'
                    selesai='#00FF1A'
                    buttonupdate='d-none'
                    fieldpembatalan=''
                    alasanpembatalan= existing_order.get('alasanpembatalan')
                    user_alamat = MUser().ambildatajalur(jalur)
                    alamat = user_alamat.get('alamat')
                 
                    
                return render_template('dashboardpesananstatus.html',
                                                    gunung=gunung, jalur=jalur, nama=nama,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk,totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                    porter=porter, tourguide=tourguide, penyewaan=penyewaan, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki, selesai=selesai,namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide,gambarprofil=gambarprofil, idpesanan=idpesanan, namapendaki=namapendaki, nohppendaki=nohppendaki,buttonupdate=buttonupdate,fieldpembatalan=fieldpembatalan, alasanpembatalan=alasanpembatalan,fieldpenyewaan=fieldpenyewaan,fieldporter=fieldporter,fieldtourguide=fieldtourguide,statuspesanan=statuspesanan)
                
            elif jenisproduk == 'paket':
                namaporter = existing_order.get('namaporter')
                nohpporter = existing_order.get('nohpporter')
                hargaporter = existing_order.get('hargaporter')
                namatourguide = existing_order.get('namatourguide')
                nohptourguide = existing_order.get('nohptourguide')
                hargatourguide = existing_order.get('hargatourguide')
                namapenyewaan = existing_order.get('namapenyewaan')
                nohppenyewaan = existing_order.get('nohppenyewaan')
                hargapenyewaan = existing_order.get('hargapenyewaan')
                if statuspesanan == 'sudah bayar':
                    pesanditerima='#00FF1A'
                    perjalananmendaki=''
                    selesai=''
                    buttonupdate=''
                    fieldpembatalan='d-none'
                    alasanpembatalan= ''
                    user_alamat = MUser().ambildatajalur(jalur)
                    alamat = user_alamat.get('alamat')
                
                elif statuspesanan == 'perjalanan mendaki':
                    pesanditerima='#00FF1A'
                    perjalananmendaki='#00FF1A'
                    selesai=''
                    buttonupdate=''
                    fieldpembatalan='d-none'
                    alasanpembatalan= ''
                    user_alamat = MUser().ambildatajalur(jalur)
                    alamat = user_alamat.get('alamat')
                    
                elif statuspesanan == 'selesai':
                    pesanditerima='#00FF1A'
                    perjalananmendaki='#00FF1A'
                    selesai='#00FF1A'
                    buttonupdate='d-none'
                    fieldpembatalan='d-none'
                    alasanpembatalan= ''
                    user_alamat = MUser().ambildatajalur(jalur)
                    alamat = user_alamat.get('alamat')
                    
                elif statuspesanan == 'dibatalkan':
                    pesanditerima='red'
                    perjalananmendaki='red'
                    selesai='#00FF1A'
                    buttonupdate='d-none'
                    fieldpembatalan=''
                    alasanpembatalan= existing_order.get('alasanpembatalan')
                    user_alamat = MUser().ambildatajalur(jalur)
                    alamat = user_alamat.get('alamat')
                 

                return render_template('dashboardpesananstatus.html',
                                                    gunung=gunung, jalur=jalur, nama=nama,
                                                    jenisproduk=jenisproduk, namaproduk=namaproduk, hargaporter=hargaporter,totalharga=totalharga,
                                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun,alamat=alamat,
                                                    porter=porter, tourguide=tourguide, penyewaan=penyewaan,namaporter=namaporter, pesanditerima=pesanditerima, perjalananmendaki=perjalananmendaki, selesai=selesai,nohpporter=nohpporter,namatourguide=namatourguide, nohptourguide=nohptourguide, hargatourguide=hargatourguide,namapenyewaan=namapenyewaan,hargapenyewaan=hargapenyewaan, nohppenyewaan=nohppenyewaan,gambarprofil=gambarprofil, idpesanan=idpesanan, namapendaki=namapendaki, nohppendaki=nohppendaki,buttonupdate=buttonupdate,fieldpembatalan=fieldpembatalan, alasanpembatalan=alasanpembatalan,fieldpenyewaan=fieldpenyewaan,fieldporter=fieldporter,fieldtourguide=fieldtourguide,statuspesanan=statuspesanan)
            
            
@app.route('/dashboard/pesanan/ubahstatus', methods=["GET", "POST"])
def ubahstatuspesanan():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    email = session['email']
    user = MUser().ambildatauser(email)
    gambarprofil = user.get('gambarprofil', 'profil.svg')
    nama = user.get('nama')
    role = user.get('role')

    if request.method == 'POST':
        idpesanan = request.form['idpesanan']
        user_pesan = MUser()
        existing_order = user_pesan.cari_id(idpesanan)

        if existing_order:
            namapendaki = existing_order.get('nama')
            nohppendaki = existing_order.get('nohp')
            totalharga = existing_order.get('totalharga')
            gunung = existing_order.get('gunung')
            jalur = existing_order.get('jalur')
            jenisproduk = existing_order.get('jenisproduk')
            namaproduk = existing_order.get('namaproduk')
            metodepembayaran = existing_order.get('metodepembayaran')
            tanggalmendaki = existing_order.get('tanggalmendaki')
            tanggalturun = existing_order.get('tanggalturun')
            statuspesanan = existing_order.get('statuspesanan')
            user_alamat = MUser().ambildatajalur(jalur)
            alamat = user_alamat.get('alamat')
            if statuspesanan == 'perjalanan mendaki':
                aturstatuspesanan = 'd-none'
            else:
                aturstatuspesanan=''

            if jenisproduk == 'porter':
                if statuspesanan == 'sudah bayar':
                    pesanditerima = '#00FF1A'
                    perjalananmendaki = ''
                    selesai = ''
                elif statuspesanan == 'perjalanan mendaki':
                    pesanditerima = '#00FF1A'
                    perjalananmendaki = '#00FF1A'
                    selesai = ''
                    
                return render_template('dashboardubahstatus.html',
                                    gunung=gunung, jalur=jalur, nama=nama,
                                    jenisproduk=jenisproduk, namaproduk=namaproduk, totalharga=totalharga,
                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun, alamat=alamat, pesanditerima=pesanditerima, 
                                    perjalananmendaki=perjalananmendaki, selesai=selesai,gambarprofil=gambarprofil, idpesanan=idpesanan, statuspesanan=statuspesanan, aturstatuspesanan=aturstatuspesanan)

            elif jenisproduk == 'tour guide':
                if statuspesanan == 'sudah bayar':
                    pesanditerima = '#00FF1A'
                    perjalananmendaki = ''
                    selesai = ''
                elif statuspesanan == 'perjalanan mendaki':
                    pesanditerima = '#00FF1A'
                    perjalananmendaki = '#00FF1A'
                    selesai = ''
                    
                return render_template('dashboardubahstatus.html',
                                    gunung=gunung, jalur=jalur, nama=nama,
                                    jenisproduk=jenisproduk, namaproduk=namaproduk, totalharga=totalharga,
                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun, alamat=alamat, pesanditerima=pesanditerima, 
                                    perjalananmendaki=perjalananmendaki, selesai=selesai,gambarprofil=gambarprofil, idpesanan=idpesanan, 
                                    namapendaki=namapendaki, nohppendaki=nohppendaki, statuspesanan=statuspesanan, aturstatuspesanan=aturstatuspesanan)

            elif jenisproduk == 'paket':
                if statuspesanan == 'sudah bayar':
                    pesanditerima = '#00FF1A'
                    perjalananmendaki = ''
                    selesai = ''
                elif statuspesanan == 'perjalanan mendaki':
                    pesanditerima = '#00FF1A'
                    perjalananmendaki = '#00FF1A'
                    selesai = ''

                return render_template('dashboardubahstatus.html',
                                    gunung=gunung, jalur=jalur, nama=nama,
                                    jenisproduk=jenisproduk, namaproduk=namaproduk, totalharga=totalharga,
                                    metodepembayaran=metodepembayaran, tanggalmendaki=tanggalmendaki, tanggalturun=tanggalturun, alamat=alamat,pesanditerima=pesanditerima, 
                                    perjalananmendaki=perjalananmendaki, selesai=selesai, gambarprofil=gambarprofil, idpesanan=idpesanan, 
                                    namapendaki=namapendaki, nohppendaki=nohppendaki, statuspesanan=statuspesanan, aturstatuspesanan=aturstatuspesanan)
                
                
                
@app.route('/dashboard/pesanan/berhasilubahstatus', methods=["GET", "POST"])
def simpanubahstatus():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    else:
        if request.method == "POST":
            if 'email' in session:
                email = session['email']
                idpesanan=request.form['idpesanan']
                if idpesanan:
                    statuspembayaranubah=request.form['statuspesanan']
                    update_data={
                        "statuspesanan": statuspembayaranubah
                    }
                    user_pesan=MUser().updatenamapesanan(idpesanan,update_data)
                    msg="Status Pesanan Berhasil Di Ubah, No ID Pesanan : "
                user = MUser().ambildatauser(email)
                gambarprofil=user.get('gambarprofil')
                if gambarprofil == '':
                    gambarprofil='profil.svg'
                nama=user.get('nama')
                role=user.get('role')
                if role == 'Porter':
                    user_pesan = MUser()
                    user_pesanan = user_pesan.ambildatapesananporterlistporter(nama)
                    
                    if user_pesanan is None:
                        user_pesanan = []

                    return render_template('dashboardpesanan.html',pesanan_list=user_pesanan,nama=nama,gambarprofil=gambarprofil, msg=msg, idpesanan=idpesanan)
            
                elif role == 'Tour Guide':
                        user_pesan = MUser()
                        user_pesanan = user_pesan.ambildatapesananporterlisttourguide(nama)
                        
                        if user_pesanan is None:
                            user_pesanan = []

                        return render_template('dashboardpesanan.html',pesanan_list=user_pesanan,nama=nama,gambarprofil=gambarprofil, msg=msg, idpesanan=idpesanan)
                        

@app.route('/dashboard/daftarharga')
def dashboarddaftarharga():
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            nama=user.get('nama')
            role=user.get('role')
            jenisprodukporter='porter'
            jenisproduktourguide='tour guide'
            user_produk = MUser()
            if role == 'Porter':
                user_listproduk = user_produk.ambildataproduklist(jenisprodukporter)
                paket=user_produk.ambildataproduklist('paket') 
                if user_listproduk is None:
                    user_listproduk = []
                if isinstance(user_listproduk, list):
                    user_listproduk.extend(paket)
                else:
                    user_listproduk.append(paket)
                    
                return render_template('dashboarddaftarharga.html', produk_list=user_listproduk, nama=nama,gambarprofil=gambarprofil)

            elif role == 'Tour Guide':
                user_listproduk = user_produk.ambildataproduklist(jenisproduktourguide)
                paket=user_produk.ambildataproduklist('paket') 
                if user_listproduk is None:
                    user_listproduk = []
                if isinstance(user_listproduk, list):
                    user_listproduk.extend(paket)
                else:
                    user_listproduk.append(paket)

                return render_template('dashboarddaftarharga.html', produk_list=user_listproduk, nama=nama,gambarprofil=gambarprofil)
                
            elif role == 'Penyewaan':
                user_listproduk = user_produk.tampilbarang()
                paket=user_produk.ambildataproduklist('paket') 
                if user_listproduk is None:
                    user_listproduk = []
                    if paket is None:
                        paket=[]

                return render_template('dashboarddaftarharga.html', baranglist=user_listproduk, nama=nama,gambarprofil=gambarprofil)

@app.route('/dashboard/analisis')
def dashboardanalisis():
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            nama=user.get('nama')
            nohp=user.get('nohp')
            role = user.get('role')
            
            if role == 'Porter':
                total=MUser().ambildatatotalpesananporter(nama,nohp)
                totalbatal=MUser().ambildatatotalbatalpesananporter(nama,nohp)
                totalpenilaian=MUser().ambildatatotalpenilaianpesananporter(nama,nohp)
                totalpendapatan=MUser().ambildatatotalpendapatanpesananporter(nama,nohp)
                
            elif role == 'Tour Guide':
                total=MUser().ambildatatotalpesanantourguide(nama,nohp)
                totalbatal=MUser().ambildatatotalbatalpesanantourguide(nama,nohp)
                totalpenilaian=MUser().ambildatatotalpenilaianpesanantourguide(nama,nohp)
                totalpendapatan=MUser().ambildatatotalpendapatanpesanantourguide(nama,nohp)
                    
            elif role == 'Penyewaan':

                total=MUser().ambildatatotalpesananpenyewaan(nama,nohp)  
                totalbatal=MUser().ambildatatotalbatalpesananpenyewaan(nama,nohp)  
                totalpenilaian=MUser().ambildatatotalpenilaianpesananpenyewaan(nama,nohp)
                totalpendapatan=MUser().ambildatatotalpendapatanpesananpenyewaan(nama,nohp)
                
            return render_template('dashboardanalisis.html', nama=nama,gambarprofil=gambarprofil,totalpesanan=total, totalbatal=totalbatal, totalpenilaian=totalpenilaian, totalpendapatan=totalpendapatan)
        
            
    
@app.route('/dashboard/keuangan')
def dashboardkeuangan():
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            nama=user.get('nama')
            nohp=user.get('nohp')
            role = user.get('role')
            if role == 'Porter':
                total=MUser().ambildatatotalpesananporter(nama,nohp)
                totalbatal=MUser().ambildatatotalbatalpesananporter(nama,nohp)
                totalpenilaian=MUser().ambildatatotalpenilaianpesananporter(nama,nohp)
                totalpendapatan=MUser().ambildatatotalpendapatanpesananporter(nama,nohp)
                
            elif role == 'Tour Guide':
                total=MUser().ambildatatotalpesanantourguide(nama,nohp)
                totalbatal=MUser().ambildatatotalbatalpesanantourguide(nama,nohp)
                totalpenilaian=MUser().ambildatatotalpenilaianpesanantourguide(nama,nohp)
                totalpendapatan=MUser().ambildatatotalpendapatanpesanantourguide(nama,nohp)
                    
            elif role == 'Penyewaan':
                total=MUser().ambildatatotalpesananpenyewaan(nama,nohp)  
                totalbatal=MUser().ambildatatotalbatalpesananpenyewaan(nama,nohp)  
                totalpenilaian=MUser().ambildatatotalpenilaianpesananpenyewaan(nama,nohp)
                totalpendapatan=MUser().ambildatatotalpendapatanpesananpenyewaan(nama,nohp)

            return render_template('dashboardkeuangan.html',  nama=nama,gambarprofil=gambarprofil, totalpendapatan=totalpendapatan)
            
@app.route('/dashboard/daftarharga/detail', methods=["GET","POST"])
def dashboarddaftarhargadetail():
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            nama=user.get('nama')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            if request.method == "POST":
                idpesanan = request.form['idproduk']
                user_produk = MUser()
                produk = user_produk.cari_idproduk(idpesanan)
                
                if produk:
                    idproduk=produk.get('_id')
                    gunung=produk.get('gunung')
                    jalur=produk.get('jalur')
                    namaproduk=produk.get('namaproduk')
                    jenisproduk=produk.get('jenisproduk')
                    harga=produk.get('harga')
                    durasi=produk.get('durasi')
                    maxbeban=produk.get('maxbeban')
                    deskripsi=produk.get('deskripsi')
                    
                    
                
                fitur = MUser().ambildatajalur(jalur)
                alamatbasecamp = fitur.get('alamat', '') 
                deskripsigunung = fitur.get('deskripsi')
                peta=fitur.get('peta')
  
                if fitur:
                    deskripsirute = [rute['deskripsi'] for rute in fitur.get('rute', [])]
                    deskripsisyarat = [syarat['deskripsi'] for syarat in fitur.get('syarat', [])]
                    deskripsilarangan = [larangan['deskripsi'] for larangan in fitur.get('larangan', [])]

                return render_template('dashboarddaftarhargadetail.html',gunung=gunung, jalur=jalur, gambarprofil=gambarprofil,nama=nama,
                                namaproduk=namaproduk, harga=harga, durasi=durasi, maxbeban=maxbeban, deskripsi=deskripsi,
                                deskripsirute=deskripsirute,deskripsisyarat=deskripsisyarat, deskripsilarangan=deskripsilarangan,alamatbasecamp=alamatbasecamp,deskripsigunung=deskripsigunung,idproduk=idproduk,peta=peta, jenisproduk=jenisproduk,total=harga)

@app.route('/dashboard/ulasan')
def dashboardulasan():
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            nama=user.get('nama')
            role=user.get('role')
            
            fieldporter=''
            fieldtourguide=''
            fieldpenyewaan=''
            if role == 'Porter':
                fieldtourguide='d-none'
                fieldpenyewaan='d-none'
                
                user_pesan = MUser()
                user_pesanan = user_pesan.ambildatapesananporterlistporterada(nama)
                
                if user_pesanan is None:
                    user_pesanan = []
                                        
                return render_template('dashboardulasan.html',
                                                    nama=nama,gambarprofil=gambarprofil, user_pesanan=user_pesanan,
                                                    fieldporter=fieldporter,fieldtourguide=fieldtourguide,fieldpenyewaan=fieldpenyewaan)
                    
            elif role == 'Tour Guide':
                fieldporter='d-none'
                fieldpenyewaan='d-none'
                user_pesan = MUser()
                user_pesanan = user_pesan.ambildatapesananporterlisttourguideada(nama)
                
                if user_pesanan is None:
                    user_pesanan = []          
                    
                return render_template('dashboardulasan.html',
                                                    nama=nama,gambarprofil=gambarprofil, user_pesanan=user_pesanan,
                                                    fieldporter=fieldporter,fieldtourguide=fieldtourguide,fieldpenyewaan=fieldpenyewaan)
                
            elif role == 'Penyewaan':
                fieldtourguide='d-none'
                fieldporter='d-none'
                user_pesan = MUser()
                user_pesanan = user_pesan.ambildatapesananporterlistpenyewaanada(nama)
                
                if user_pesanan is None:
                    user_pesanan = []          
                    
               
                return render_template('dashboardulasan.html',
                                                    nama=nama,gambarprofil=gambarprofil, user_pesanan=user_pesanan,
                                                    fieldporter=fieldporter,fieldtourguide=fieldtourguide,fieldpenyewaan=fieldpenyewaan)
                
                    
@app.route('/dashboard/cuaca')
def dashboardcuaca():
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            nama=user.get('nama')
            role=user.get('role')

            return render_template('dashboardcuaca.html', nama=nama,gambarprofil=gambarprofil)
                    
@app.route('/dashboard/program')
def dashboardprogram():            
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            nama=user.get('nama')
            nohp=user.get('nohp')
            role=user.get('role')
            
            program=MUser().ambildataprogram()
            if program is None:
                program=[]
            
            sudahprogram=MUser().caridataprogram()
            if sudahprogram is None:
                sudahprogram=[]
            
            return render_template('dashboardprogram.html', nama=nama,gambarprofil=gambarprofil,program=program,sudahprogram=sudahprogram)        

@app.route('/dashboard/program/detail', methods=["GET","POST"])
def dashboarddaftarprogram():
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            nama=user.get('nama')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            if request.method == "POST":
                idpesanan = request.form['idprogram']
                user_program = MUser()
                program = user_program.cari_idprogram(idpesanan)
                namaprogram=program.get('namaprogram')
                tanggal=program.get('tanggal')
                alamat=program.get('alamat')
                gambar=program.get('gambar')
                
                return render_template('dashboardprogramdetail.html',gambar=gambar,gambarprofil=gambarprofil,nama=nama,namaprogram=namaprogram,tanggal=tanggal,alamat=alamat,idprogram=idpesanan)                    

@app.route('/dashboard/program/berhasil', methods=["GET","POST"])
def daftarprogram():
    if 'email' not in session:
        return url_for('login')
        
    else:
        if 'email' in session:
            email = session['email']
            user = MUser().ambildatauser(email)
            gambarprofil=user.get('gambarprofil')
            nama=user.get('nama')
            nohp=user.get('nohp')
            if gambarprofil == '':
                gambarprofil='profil.svg'
            if request.method == "POST":
                idpesanan = request.form['idprogram']
                user_program = MUser()
                program = user_program.cari_idprogram(idpesanan)
                namaprogram=program.get('namaprogram')
                tanggal=program.get('tanggal')
                MUser().insertprogram(nama,nohp,namaprogram,tanggal)
                msg="Berhasil Daftar Program"
                
                program=MUser().ambildataprogram()
                if program is None:
                    program=[]
                    
                sudahprogram=MUser().caridataprogram()
                if sudahprogram is None:
                    sudahprogram=[]
                return render_template('dashboardprogram.html', nama=nama,gambarprofil=gambarprofil,program=program,msg=msg,sudahprogram=sudahprogram)    
            
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = MUser()
        if user.authenticate(email, password):
            session['email'] = email
            return redirect(url_for('index'))
        msg = 'Email/Password salah'
        return render_template('login.html', msg=msg)
    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        nama = request.form['nama']
        nohp = request.form['nohp']
        email = request.form['email']
        password = request.form['password']

        user = MUser(email)
        if user.check_email_terdaftar(email):
            return render_template("register.html", msg="Email sudah terdaftar")

        user = MUser(nama, nohp, email, password)
        user.insertdata(nama, nohp, email, password)
        session['email'] = email
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('email','')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
