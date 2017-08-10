from bottle import route, run, template, static_file, get, post, delete, request
import json
import pymysql

connection = pymysql.connect(host='sql11.freesqldatabase.com',
                             user='sql11189251',
                             password='bEzYRY6iRP',
                             db='sql11189251',
                             charset='utf8mb4',
                             autocommit=True,
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
            return json.dumps({'STATUS': 'SUCCESS', 'PRODUCTS': result, 'CODE': 200})
    except Exception:
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


# List Products by Category
@get("/category/<id>/products")
def list_products_by_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE category={};".format(id)
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({'STATUS': 'SUCCESS', 'PRODUCTS': result, 'CODE': 200})
    except Exception:
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


# Getting a Product
@get("/product/<id>")
def get_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM products WHERE id={};".format(id)
            cursor.execute(sql)
            result = cursor.fetchone()
            return json.dumps({'STATUS': 'SUCCESS', 'PRODUCT': result, 'CODE': 200})
    except Exception:
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


# Creating a Category (ignoring 'bad request' error as I accept any category name)
@post("/category")
def create_category():
    try:
        with connection.cursor() as cursor:
            new_category = request.POST.get("name")
            sql = "SELECT count(*) FROM categories WHERE name='{}'".format(new_category)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                return json.dumps({'STATUS': 'ERROR', 'MSG': 'Category already exists', 'CODE': 200})
            else:
                sql_query = "INSERT INTO categories (name) VALUES ('{0}')".format(new_category)
                cursor.execute(sql_query)
                result = cursor.lastrowid
                return json.dumps({'STATUS': 'SUCCESS', 'CAT_ID': result, 'CODE': 201})
    except Exception:
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


# Add/Edit a Product (ignoring 'category not found' because it is a drop-down so will always be correct)
@post("/product")
def add_edit_product():
    product_category = request.POST.get("category")
    product_description = request.POST.get("description")
    product_price = request.POST.get("price")
    product_title = request.POST.get("title")
    product_favorite = request.POST.get("favorite")
    if product_favorite is "on":
        product_favorite=1
    else:
        product_favorite=0
    product_img_url = request.POST.get("img_url")
    try:
        with connection.cursor() as cursor:
            sql = "SELECT count(*) FROM products WHERE title='{}'".format(product_title)
            cursor.execute(sql)
            result = cursor.fetchone()
            if result['count(*)'] > 0:
                sql_update = "UPDATE products SET category='{0}', description='{1}', price='{2}', favorite='{3}', img_url='{4}' WHERE title='{5}'".format(product_category, product_description, product_price, product_favorite, product_img_url, product_title)
                cursor.execute(sql_update)
                product_id = 0 #sorry, from Lauren
            else:
                sql_add = "INSERT INTO products (category, description, price, title, favorite, img_url) VALUES ({0},'{1}',{2},'{3}',{4},'{5}')".format(product_category, product_description, product_price, product_title, product_favorite, product_img_url)
                cursor.execute(sql_add)
                product_id = cursor.lastrowid
        return json.dumps({'STATUS': 'SUCCESS', 'PRODUCT_ID': product_id, 'CODE': 201})
    except Exception:
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


# Deleting a Category
@delete("/category/<id>")
def delete_category(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM categories WHERE id={0}".format(id)
            sql2 = "DELETE FROM products WHERE category={0}".format(id)
            cursor.execute(sql)
            cursor.execute(sql2)
            return json.dumps({'STATUS': 'SUCCESS', 'CODE': 201})
    except Exception:
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


# Deleting a Product
@delete("/product/<id>")
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM products WHERE id={0}".format(id)
            cursor.execute(sql)
            return json.dumps({'STATUS': 'SUCCESS', 'CODE': 201})
    except Exception:
        return json.dumps({'STATUS': 'ERROR', 'MSG': 'Internal error', 'CODE': 500})


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