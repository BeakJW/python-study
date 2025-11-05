from flask import Flask, request
from sqlalchemy import text
import datetime as dt
from mylibrary import MyDB

app = Flask(__name__)
app.json.sort_keys = False

@app.route("/departments",methods=['GET'])
def get_list():
    sql = text("Select id,dname,loc,phone,email FROM departments")

    conn = MyDB.connect()
    result = conn.execute(sql)
    MyDB.disconnect()

    resultset = result.mappings().all()

    for i in range(0,len(resultset)):
        resultset[i] = dict(resultset[i])

    return {
        "result":resultset,
        "timestamp":dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route("/departments/<id>",methods=['PUT'])
def get_item(id):
    sql = text("""SELECT id,dname,loc,phone,email,established,homepage
               FROM departments WHERE id=:id""")
    
    conn = MyDB.connect()
    result = conn.execute(sql, {"id": id})
    MyDB.disconnect()

    resultset = result.mappings().all()
    #print(resultset)

    return {
        "result":dict(resultset[0]),
        "timestamp":dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.route("/departments",methods=['POST'])
def post():
    conn = MyDB.connect()
    
    dname = request.form.get("dname")
    loc = request.form.get("loc")
    phone = request.form.get("phone")
    email = request.form.get("email")
    established = request.form.get("established")
    homepage = request.form.get("homepage")

    sql=text("""
                INSERT INTO departments(dname,loc,phone,email,established,homepage)
             VALUES(:dname,:loc,:phone,:email,:established,:homepage)
""")

    params = {
        "dname":dname, "loc":loc, "phone":phone,"email":email,"established":established,"homepage":homepage
    }

    conn.execute(sql,params)
    conn.commit()

    pk_result = conn.execute(text("SELECT LAST_INSERT_ID()"))
    pk = pk_result.scalar()

    sql = text("""
                SELECT id,dname,loc,phone,email,established,homepage
               FROM departments WHERE id=:id
""")
    
    result = conn.execute(sql,{"id":pk})
    resultset = result.mappings().all()
    MyDB.disconnect()

    return {
        "result":dict(resultset[0]),
        "timestamp":dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route("/departments/<id>", methods=['DELETE'])
def delete(id):
    conn = MyDB.connect()

    sql1 = text("""
        DELETE FROM enrollments
        WHERE subject_id IN (SELECT id FROM subjects WHERE department_id=:id)
        OR student_id IN (SELECT id FROM students WHERE department_id=:id)
    """)
    
    sql2 = text("DELETE FROM subjects WHERE department_id=:id")
    sql3 = text("DELETE FROM students WHERE department_id=:id")
    sql4 = text("DELETE FROM professors WHERE department_id=:id")
    sql5 = text("DELETE FROM departments WHERE id=:id")

    params = {"id": id}
    
    conn.execute(sql1, params)
    conn.execute(sql2, params)
    conn.execute(sql3, params)
    conn.execute(sql4, params)
    conn.execute(sql5, params)

    conn.commit()
    MyDB.disconnect()

    return {
        "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.errorhandler(Exception)
def error_handling(error):
    MyDB.disconnect()
    return{
        'message':"".join(error.args),
        'timestamp':dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },500

if __name__ == "__main__":
    app.run(port=9091,debug=True)