#Ali KOCA ali.koskocaman@gmail.com
import os, time
from glob import glob
from os.path import getmtime
import exifread
import datetime
import sys, getopt
#https://github.com/ianare/exif-py
#pip3 install exifread

kaynak_dizin = ''
hedef_dizin = ''
dosya_nevi = ''
cp_mv = 'cp -rvfu '
argv = sys.argv[1:]

def resim_cekilme_tarihi_getir(pDosya): 
  with open(pDosya, 'rb') as fh:
    tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
    try: 
      dateTaken = tags["EXIF DateTimeOriginal"]
    except:
      return 'tarihsiz'    
  Str = str(dateTaken)[0:7].replace(':', '/')
  return Str


def dosyalari_getir(pDizin, pPattern):
  dosyalar = []
  for dir,_,_ in os.walk(pDizin):
    dosyalar.extend(glob(os.path.join(dir, pPattern)))
  return dosyalar 
   


try:
   opts, args = getopt.getopt(argv,"ytk:h:f:",["kaynakdizin=","hedefdizin=","dosya_nevi="])
except getopt.GetoptError:
   print('Komut dizisinde hata var. Yardım almak için -y parametresini kullanınız.')
   sys.exit(2)

for opt, arg in opts:
  if opt == '-y':
     print( 'Kullanımı: dosya_tasnif_et.py -k <kaynak_dizin> -h <hedef_dizin> -f <dosya_nevi> -t (dosyaları taşı)' )
     print( 'Misalen  : dosya_tasnif_et.py -k "/home/hasan/resimler/bitasnif" -h "/home/hasan/resimler/tasnif" -f "*.jpg" ')        
     sys.exit()
  elif opt in ("-k", "--kaynakdizin"):
     kaynak_dizin = arg
  elif opt in ("-h", "--hedefdizin"):
     hedef_dizin = arg
  elif opt in ("-f", "--dosya_nevi"):
     dosya_nevi = arg
  elif opt == '-t':
     cp_mv = "mv "  
if kaynak_dizin == '' or hedef_dizin == '' or dosya_nevi == '':
      print('Komut dizisinde hata var. Yardım almak için -y parametresini kullanınız.')
      sys.exit(2) 

 
if not os.path.exists(hedef_dizin):
    os.makedirs(hedef_dizin)
   
dosyalar = dosyalari_getir(kaynak_dizin, dosya_nevi)   
hedef_kok_dizin = hedef_dizin
for dosya in dosyalar:
  hedef_dizin = hedef_kok_dizin + resim_cekilme_tarihi_getir(dosya) + "/"
  if not os.path.exists(hedef_dizin):
    os.makedirs(hedef_dizin)
  hedef_dizin_ve_dosya = hedef_dizin + os.path.basename(dosya) 
  kopyalama_komutu = cp_mv + '"' + dosya  + '"  "' +  hedef_dizin_ve_dosya + '"'
  print( os.system(kopyalama_komutu) )
print( "   - " + str(os.system(kopyalama_komutu)) )
