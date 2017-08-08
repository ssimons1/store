from bottle import route, run, template, static_file, get, post, delete, request
import json
import pymysql




connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='store',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
cursor = connection.cursor();

@get("/admin")
def admin_portal():
	return template("pages/admin.html")

# List Categories
@get("/categories")
def list_categories():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM categories;"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({'STATUS': 'SUCCESS', 'CATEGORIES': result, 'CODE': 200})
    except Exception:
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})

# List All Products
@get("/products")
def list_all_products():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products;"
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({'STATUS':'SUCCESS','PRODUCTS':result, 'CODE': 200})
    except Exception:
        return json.dumps({'STATUS':'ERROR','MSG':'Internal error','CODE': 500})

# List Products by Category
@get("/category/<id>/products")
def list_products_by_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE category={};".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return
    except Exception:
        return





# Creating a Category
@post("/category")
def create_category():
    try:
        with connection.cursor() as cursor:
            new_category = request.POST.get("name")
            sql_query = "INSERT INTO categories (id, name) VALUES (0, {})".format(new_category)
            cursor.execute(sql_query)
            result = cursor.lastrowid()
            return json.dumps({'STATUS': 'SUCCESS', 'CAT_ID': result, 'CODE': 201})
    except Exception:
        pass
        # return json.dumps({'STATUS':'ERROR','MSG':''})


@get("/")
def index():
    return template("index.html")


@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()