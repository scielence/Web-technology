from bottle import *
import sqlite3

@route('/show')
#this URI is to show contents of inventory.db
def show_db():
	conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("SELECT * FROM inventory")
        result = c.fetchall()
        c.close()
	return str(result)

@route('/new', method='GET')
#this URI is to add new content to the database
def new_item():
	if request.GET.get('save','').strip():
		new = request.GET.get('task', '').strip()
       	 	conn = sqlite3.connect('inventory.db')
        	c = conn.cursor()

        	c.execute("INSERT INTO inventory (task,status) VALUES (?,?)", (new,1))
        	new_id = c.lastrowid

        	conn.commit()
       		c.close()

        	return '<p>The new task was inserted into the database, the ID is %s</p>' % new_id

    	else:
        	return '<b>This is for use in the jQuery in the HTML file</b>'
	
@route('/get:json#[0-9]+#')
#this URI is for gettig specific data, used in a loop to populate HTML table (needs to be converted)
def show_json(json):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT task FROM inventory WHERE id LIKE ?", (json))
    result = c.fetchall()
    c.close()

    if not result:
        return {'task':'This item number does not exist!'}
    else:
        return {'Task': result[0]}

@route('/edit/:no', method='GET')
#this URI is for editing specific items
def edit_item(no):

    if request.GET.get('save','').strip():
        edit = request.GET.get('task','').strip()
        status = request.GET.get('status','').strip()

        if status == 'open':
            status = 1
        else:
            status = 0

        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("UPDATE inventory SET task = ?, status = ? WHERE id LIKE ?", (edit,status,no))
        conn.commit()

        return '<p>The item number %s was successfully updated</p>' %no

    else:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("SELECT task FROM todo WHERE id LIKE ?", (str(no)))
        cur_data = c.fetchone()

        return template('edit_task', old = cur_data, no = no)

@error(403)
def error403(code):
	return 'URL mismatch error.'

@error(404)
def error404(code):
	return 'This page does not exist.'

run(host='localhost', port=8080, debug=True, reloader=True)
