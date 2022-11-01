from flask import Flask, render_template, request, session, redirect, send_file
from DBConnection import Db
from werkzeug.utils import secure_filename
import os
import time

app = Flask(__name__)
app.secret_key='hi'
static_path="E:\\filededuplication\\filededuplication\\static\\"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')

ALLOWED_EXTENSIONS = {'pdf','txt','pptx','docx','jpg','mp3','mp4'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/')
def admin():
    return render_template('newestlogin.html')



@app.route('/login',methods=['post'])
def login():
    s=Db()
    name=request.form['textfield']
    password=request.form['textfield2']
    qry="select * from login WHERE username='"+name+"' and password= '"+password+"'"
    res=s.selectOne(qry)
    if res is not None:
        session['lid'] = res['login_id']
        type=res['user_type']
        if type=='admin':
            return redirect('/adminanalysis')
        elif type=='user':
            return  redirect('/useranalysis')
        elif type=='pending':
            return '''<script> alert("registration pending....!!"); window.location='/'</script>'''
        else:
            return '''<script> alert("invalid username or password....!!"); window.location='/'</script>'''
    else:
        return '''<script> alert("invalid username or password....!!"); window.location='/'</script>'''

# @app.route('/adminview')
# def admin1():
#     s=Db()
#     qr="select * from signup"
#     res=s.select(qr)
#     return render_template('admin/adminview.html')

@app.route('/view')
def view():
    s=Db()
    qr="select signup.*,login.* from signup inner join login on  login.login_id=signup.login_id where user_type='pending'"
    res=s.select(qr)
    return render_template('admin/adminview.html',data=res)


@app.route('/approvedusers')
def viewapproved():
    s = Db()
    qr = "select signup.*,login.* from signup inner join login on  login.login_id=signup.login_id where user_type='user'"
    res = s.select(qr)
    return render_template('admin/adminviewapproved.html', data=res)

@app.route('/storagesummary/<lid>')
def viewstoragesummary(lid):
    s = Db()
    qry = "select count(*) as 'cnt' from block where block_id IN(select block_id from indexes where file_id in(select file_id from fileupload where u_id = '" + str(lid) + "'))"
    qry1 = "select count(*) as 'cnt' from indexes where block_id IN(select block_id from indexes where file_id in(select file_id from fileupload where u_id = '" + str(lid) + "'))"
    res = s.selectOne(qry)
    res1 = s.selectOne(qry1)
    totalusagewithout = res1['cnt'] * 8 * 1024
    totalusagewith = res['cnt'] * 8 * 1024

    return render_template('admin/usersummary.html', a=totalusagewith, b=totalusagewithout)


@app.route('/approve/<id>')
def approve(id):
    s=Db()
    qr="update login set user_type='user' where login_id='"+id+"'"
    s.update(qr)
    return view()

@app.route('/reject/<id>')
def reject(id):
    s=Db()
    qr="delete from signup where login_id='"+id+"'"
    s.delete(qr)
    qr1="delete from login where login_id='"+id+"'"
    s.delete(qr1)
    return view()

@app.route('/signup')
def user():
    return render_template('regindex.html')


@app.route('/reg',methods=['post'])
def reg():
    s=Db()
    name =request.form['textfield']
    dob =request.form['textfield2']
    gender=request.form['RadioGroup1']
    # print(gender)
    phone=request.form['textfield3']
    email=request.form['textfield4']
    password=request.form['textfield5']
    qr ="insert into login values(null,'"+email+"','"+password+"','pending')"
    res =s.insert(qr)
    qry ="insert into signup values(null,'"+name+"','"+dob+"','"+gender+"','"+phone+"','"+email+"','"+str(res)+"')"
    s.insert(qry)


    return redirect('/')


@app.route('/userhome')
def home():

    return render_template('user/newtemp.html')


@app.route('/upload')
def user2():

    return render_template('user/upload.html')

@app.route('/up',methods=['post'])

def up():
    s=Db()
    picture=request.files['fileField']

    if picture and allowed_file(picture.filename):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filen = timestr + secure_filename(picture.filename)
        picture.save(static_path+"uploads\\"+filen)
        filepath='/static/uploads/'+filen
    qr = "insert into fileupload values(null,'" +filen + "',curdate(),'"+str(session['lid'])+"')"
    fileid=s.insert(qr)
    import random
    import os
    # bufferSize = 64 * 1024


    file1 = open(static_path+"uploads\\"+filen, "rb")

    f=file1.read()
    # print("read data====",f)
    b=bytearray(f)
    #
    # pyAesCrypt.encryptFile(filepath, filepath + ".aes", k, bufferSize)
    # with open(filepath + ".aes", "rb")as image:
    #
    #     f = image.read()
    #     b = bytearray(f)
    import hashlib

    blocksize = 2064
    totalblocks = int(len(b) / blocksize)
    for n in range(0, totalblocks):
        blocksingle = bytearray([b[i] for i in range(n * blocksize, (n * blocksize) + blocksize)])
        result = hashlib.sha256(blocksingle)
        hashval = result.hexdigest()
        checkhash(hashval,fileid,blocksingle)

    #     qry = "INSERT INTO `fileblocks`(`fileid`,`blockid`) VALUES (" + str(fid) + "," + blckid + ")"
    #     c.nonreturn(qry)
    #
    if totalblocks * blocksize < len(b):
        blocksingle = bytearray([b[i] for i in range(totalblocks * blocksize, len(b))])
        result = hashlib.sha256(blocksingle)
        hashval = result.hexdigest()
        checkhash(hashval,fileid,blocksingle)
    #     qry = "select block_id from blocks where hash_value='" + hashval + "'"
    #     rf = c.selectone(qry)
    #     blckid = ""
    #     if rf is not None:
    #         blckid = str(rf[0])
    #     else:
    #         sq = "select max(block_id) from blocks"
    #         blckid = str(c.mid(sq))
    #         qry = "INSERT INTO blocks (hash_value) VALUES ('" + hashval + "')"
    #         str(c.nonreturn(qry))
    #
    #         with open("C:\\Users\\jnh\\PycharmProjects\\CP-ABE\\static\\fileblocks\\" + blckid,
    #                   "wb") as mypicklefile:
    #             mypicklefile.write(blocksingle)
    #     qry = "INSERT INTO `fileblocks`(`fileid`,`blockid`) VALUES (" + str(fid) + "," + blckid + ")"
    #     c.nonreturn(qry)
    return user2()
    # '''<script>alert('uploaded');window.location='/upload'</script>'''

@app.route('/filedownload')
def user3():
    return render_template('user/filedownload.html')

@app.route('/download')
def download():
    s=Db()
    qr="select * from fileupload where u_id='"+str(session['lid'])+"'"
    res=s.select(qr)
    return render_template('user/filedownload.html',data=res)

@app.route('/viewprofile')
def user4():
    return render_template('user/viewprofile.html')

@app.route('/updateprofile',methods=['post'])
def update():
    name=request.form['textfield']
    dob=request.form['textfield2']
    gender=request.form['textfield3']
    phone=request.form['textfield4']
    id=request.form['hid']
    db=Db()
    qry="update signup set Name='"+name+"',Dob='"+dob+"',gender='"+gender+"',phone_no='"+phone+"' where sign_id='"+id+"'"
    db.update(qry)
    return redirect('/viewprfl')




@app.route('/viewprfl')
def view1():
    s=Db()
    qry="select * from signup where login_id='"+str(session['lid'])+"'"
    res=s.selectOne(qry)
    return render_template('user/viewprofile.html',data=res)





def blockview(content):
    pass
def checkhash(hashvalue,fileid,fileblocks):
    s=Db()
    qry="select * from block where hash='"+hashvalue+"' "
    # print(qry)
    res=s.selectOne(qry)
    if res is not None:
        bid=res['block_id']
        qr="insert into indexes VALUES (NULL ,'"+str(bid)+"','"+str(fileid)+"')"
        res=s.insert(qr)
        return "ok"
    else:
        qr="insert into block VALUES (null,'"+hashvalue+"') "
        id=s.insert(qr)

        blockfilefolder = "E:\\filededuplication\\filededuplication\\static\\fileblocks\\"

        with open(blockfilefolder +str(id)+".txt",mode='wb') as hn:
            hn.write(fileblocks)





        qr = "insert into indexes VALUES (NULL ,'"+str(id)+"','"+str(fileid)+"')"
        res = s.insert(qr)
        return id


def index(fid,index1):
    qr="insert into indexes VALUES(NULL,'"+index1+"',) "
    s=Db()
    res=s.insert(qr)




    return "yes"

@app.route('/downloadfile/<id>/<fname>')
def  downloadfile(id,fname):

    s=Db()
    qry="select * from indexes WHERE file_id='"+id+"' order by index_id"
    res=s.select(qry)

    a=bytearray(100000000)

    indx=0

    for i in res:
        blockid=i['block_id']

        d="E:\\filededuplication\\filededuplication\\static\\fileblocks\\"+ str(blockid) +".txt"
        with open(d,mode='rb') as h:
            f=h.read()
            a[indx: indx+len(f)]=f
            indx=indx+ len(f)

    b=a[0:indx]

    filepathnew="E:\\filededuplication\\filededuplication\\static\\"+ fname

    with open(filepathnew,"wb") as h:
        h.write(b)


    return send_file(filepathnew,as_attachment=True)



@app.route('/adminanalysis')
def analysis():
    s=Db()
    qry="select count(*) as 'cnt' from block"
    qry1="select count(*) as 'cnt' from indexes"
    res=s.selectOne(qry)
    res1=s.selectOne(qry1)

    totalusagewithout=res1['cnt'] * 8 *1024
    totalusagewith=res['cnt'] * 8 *1024


    return  render_template('admin/admin_home.html',a=totalusagewith,b=totalusagewithout)

@app.route('/useranalysis')
def analysis1():
    s=Db()
    qry = "select count(*) as 'cnt' from block where block_id IN(select block_id from indexes where file_id in(select file_id from fileupload where u_id = '"+str(session['lid'])+"'))"
    qry1 = "select count(*) as 'cnt' from indexes where block_id IN(select block_id from indexes where file_id in(select file_id from fileupload where u_id = '"+str(session['lid'])+"'))"
    res = s.selectOne(qry)
    res1 = s.selectOne(qry1)

    totalusagewithout = res1['cnt'] * 8 * 1024
    totalusagewith = res['cnt'] * 8 * 1024

    return render_template('user/user_home.html', a=totalusagewith, b=totalusagewithout)


if __name__ == '__main__':
    app.run(debug=True)
