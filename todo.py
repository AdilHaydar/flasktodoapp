from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/adilc/PycharmProjects/flasktodoapp/todo.db' #todo.db'mizin adresini veriyoruz burda. C:// yi sildik buna gerek yok.
db = SQLAlchemy(app)
@app.route("/")
def index():
    todos = Todo.query.all() #bu bize bir liste dönücek ve bu listede bizim todolarımızın özellikleri sözlük yapısı şeklinde gelicek.
    
    return render_template("index.html",todos = todos) #todos'umuzu index.html'e todos olarak gönderiyoruz.
@app.route("/complete/<string:id>") #NOT : BU FONKSİYONDA FORM GÖNDERME İŞLEMİ OLMADIĞI İÇİN POST METODU KULLANILMADI. TAMAMLA BUTONUNA BASILDIĞINDA GET METODU ÇALIŞACAK VE TABLODAKİ todo DURUM değişecek.
def completeTodo(id): #string:id deki id'yi göndermiş oluyoruz bu fonksiyona id parametresi ile.
    todo = Todo.query.filter_by(id = id).first() #o id'ye göre ilk değeri alıcak demek .first fonksiyonu. aslında bizde her adi primary key olduğu için buna gerek yok.
    #burada filter_by(id=id) de dinamik url'e gönderilecek id ye karşılık gelen id değerli veriyi veri tabanından al demek.
    """if todo.complete == True:
        todo.complete = False
    else:
        todo.complete = True #burada eğer todo complete'imiz true ise false, false ise true olucak demek"""
    todo.complete = not todo.complete #bu kod yukarıda yoruma alınmış if koşulu ile aynı işlemi yapıyor fakat bu tek satırlık bir işlem.
    #burada da yine false ise true, true ise false yapacak todo complete'yi.
    db.session.commit() #veritabanında değişiklik yaptığımız için commit ediyoruz.
    return redirect(url_for("index"))
@app.route("/add", methods = ["POST"]) #burada sadece post requeste izin veriyoruz.
def addTodo():
    title = request.form.get("title") #inputa verdiğimiz name="title" daki title'ı burada alıyoruz.
    newTodo = Todo(title = title,complete = False) #todo classından bir obje oluşturuyoruz. bu class'ın title'ını name'den aldığımız title(yani kullanıcının girdiği input), complete ise False olarak başlatıyoruz.
    db.session.add(newTodo) #oluşturduğumuz objemizi veritabanına ekliyoruz.
    db.session.commit() #veritabanı üzerinde bir değişiklik yaptığımız için burada commit ediyoruz.

    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id = id).first()#completeTodo fonksiyonundan kopyaladık.
    db.session.delete(todo) #todo.query.filter_by fonkisoyun ile dinamik url'den gelen id değerleri todo'yu veritabanından sil demek.
    db.session.commit()
    return redirect(url_for("index"))



class Todo(db.Model): #Todo isminde bir tablo oluşturuyoruz burda.
    #ORM nin faydası burdadır. SQL sorgusu yazmadan class yapısı ile SQL'e komut göndeririz ORM kendisi bu komutları SQL sorgusu haline getirir.
    id = db.Column(db.Integer, primary_key=True) #db.integer bu alan integer demek, ikinci parametrede ise bunun primary key olduğunu belirtiyoruz ve bu auto increment şeklinde artıyor.
    title = db.Column(db.String(80)) #db.column bir kolon oluştur anlamına geliyor. db.String(80) max 80 karakter alsın ve string olsun demek.
    complete = db.Column(db.Boolean) #ya 1(True) yada 0(False) değerini alıcak demek Boolean
    #her todo aslında tamamlanmamış bir iş tamamladığımızda True yapıcaz ve complete False olarak başlatıyoruz.
if __name__ == "__main__":
    db.create_all() #bu komut uygulama tam çalışmadan çalışacak ve oluşturduğumuz classları tablo olarak oluşturmuş oluyoruz. eğer  tablo varsa tekrardan oluşturmuyor veya hata vermiyor.
    app.run(debug=True)
