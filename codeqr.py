import qrcode

url=input("Ingresa el link que deseas convertir: ")

qr = qrcode.QRCode(
    version=1,
    box_size=25,
    border=5,
)

qr.add_data(url)
qr.make(fit=True)#Repartir información en la imagen

img = qr.make_image(fill='black', back_color='white')
img.save("mi_qr.png")