from fpdf import FPDF
import os

def make_pdf(dirname="images", imglist=None, filename="YourPDF"):
    if imglist == None:
        imglist=[]
        for f in os.listdir(dirname):
            if f.endswith(".jpg"):
                imglist.append(f)

    pdf = FPDF(unit="pt",format ="A4")

    print("\nmaking pdf...\n")
    for page in imglist:
        pdf.add_page()
        #x and y are position therefore 0,0 and w,h = 595x842 pixels for A4
        pdf.image(os.path.join(dirname,page),0,0,595,842)

    try:
        pdf.output(f"{filename}.pdf","F")
    except PermissionError:
        if os.path.exists(f'{filename}.pdf'):
            os.remove(f'{filename}.pdf')
        pdf.output(f"{filename}.pdf","F")

    print(f"Done pdf saved to {os.path.abspath(f'{filename}.pdf')}")

if __name__=="__main__":
    make_pdf("images_keerthi",filename="keerthi_kireetalu_1")

