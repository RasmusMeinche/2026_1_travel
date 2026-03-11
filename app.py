from flask import Flask, render_template, request, jsonify, session, redirect
import x
import uuid
import time
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from icecream import ic
ic.configureOutput(prefix=f'______ | ', includeContext=True)

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)



##############################
@app.get("/signup")
@x.no_cache
def show_signup():
    try:
        user = session.get("user", "")
        return render_template("page_signup.html", user=user, x=x)
    except Exception as ex:
        ic(ex)
        return "ups"

##############################
@app.post("/api-create-user")
def api_create_user():
    try:
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        user_hashed_password = generate_password_hash(user_password)
        # ic(user_hashed_password) # 'scrypt:32768:8:1$V0NLEqHQsgKyjyA7$3a9f6420e4e9fa7a4e4ce6c89927e7dcb532e5f557aee6309277243e5882cc4518c94bfd629b61672553362615cd5d668f62eedfe4905620a8c9bb7db573de31'

        user_pk = uuid.uuid4().hex
        user_created_at = int(time.time())

        db, cursor = x.db()
        q = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (user_pk, user_first_name, user_last_name, user_email, user_hashed_password, user_created_at))
        db.commit()

        form_signup = render_template("___form_signup.html", x=x)

        return f"""
            <browser mix-replace="form">{form_signup}</browser>
            <browser mix-redirect="/login"></browser>
        """

    except Exception as ex:
        ic(ex)

        if "company_exception user_first_name" in str(ex):
            error_message = f"user first name {x.USER_FIRST_NAME_MIN} to {x.USER_FIRST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_last_name" in str(ex):
            error_message = f"user last name {x.USER_LAST_NAME_MIN} to {x.USER_LAST_NAME_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_email" in str(ex):
            error_message = f"user email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "Duplicate entry" in str(ex) and "user_email" in str(ex):
            error_message = "Email already exists"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)        
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500


    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



##############################
@app.get("/login")
@x.no_cache
def show_login():
    try:
        user = session.get("user", "")
        if not user: 
            return render_template("page_login.html", user=user, x=x)
        return redirect("/profile")
    except Exception as ex:
        ic(ex)
        return "ups"


##############################
@app.post("/api-login")
def api_login():
    try:
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()

        db, cursor = x.db()
        q = "SELECT * FROM users WHERE user_email = %s"
        cursor.execute(q, (user_email,))
        user = cursor.fetchone()
        if not user:
            error_message = "Invalid credentials 1"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if not check_password_hash(user["user_password"], user_password):
            error_message = "Invalid credentials 2"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400            

        user.pop("user_password")
        session["user"] = user
        session["user_pk"] = user["user_pk"]

        return f"""<browser mix-redirect="/profile"></browser>"""

    except Exception as ex:
        ic(ex)


        if "company_exception user_email" in str(ex):
            error_message = f"user email invalid"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        if "company_exception user_password" in str(ex):
            error_message = f"user password {x.USER_PASSWORD_MIN} to {x.USER_PASSWORD_MAX} characters"
            ___tip = render_template("___tip.html", status="error", message=error_message)
            return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 400

        # Worst case
        error_message = "System under maintenance"
        ___tip = render_template("___tip.html", status="error", message=error_message)        
        return f"""<browser mix-after-begin="#tooltip">{___tip}</browser>""", 500


    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/profile")
@x.no_cache
def show_profile():
    try:
        user = session.get("user", "")
        if not user: return redirect("/login")
        return render_template("page_profile.html", user=user, x=x)
    except Exception as ex:
        ic(ex)
        return "ups"


##############################
@app.get("/logout")
def logout():
    try:
        session.clear()
        return redirect("/login")
    except Exception as ex:
        ic(ex)
        return "ups" 


##############################
@app.get("/travels")
def show_travels():
    try:
        user = session.get("user")
        user_pk = session.get("user_pk")

        if not user_pk:
            return redirect("/login")

        db, cursor = x.db()

        q = "SELECT * FROM travels WHERE user_fk = %s"
        cursor.execute(q, (user_pk,))
        travels = cursor.fetchall()
        

        return render_template("page_travels.html", x=x, travels=travels, user=user)

    except Exception as ex:
        ic(ex)
        return "ups"

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.post("/api-create-travel")
def api_create_travel():
    try:
        travel_pk = uuid.uuid4().hex
        user_fk = session.get("user_pk")
        if not user_fk:
            raise Exception("No user logged in")
        travel_title = x.validate_travel_title()
        travel_country = x.validate_travel_country()
        travel_location = x.validate_travel_location()
        travel_start_date = request.form.get("travel_start_date")
        travel_end_date = request.form.get("travel_end_date")
        travel_description = x.validate_travel_description()

        db, cursor = x.db()
        q = "INSERT INTO travels VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(q, (travel_pk, user_fk, travel_title, travel_country, travel_location, travel_start_date, travel_end_date, travel_description))
        db.commit()

        return f"""<browser mix-redirect="/travels"></browser>"""
    except Exception as ex:
        ic(ex)
        return "ups"
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/edit_travels")
def edit_travels():
    try:
        user = session.get("user")
        user_pk = session.get("user_pk")

        if not user_pk:
            return redirect("/login")

        db, cursor = x.db()

        q = "SELECT * FROM travels WHERE user_fk = %s"
        cursor.execute(q, (user_pk,))
        travels = cursor.fetchall()
        

        return render_template("page_update_travels.html", x=x, travels=travels, user=user)

    except Exception as ex:
        ic(ex)
        return "ups"

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.patch("/edit_travel/<travel_pk>")
def update_travel(travel_pk):
    try:

        parts = []
        values = []

        travel_title = request.form.get("travel_title", "").strip()
        if travel_title:
            parts.append("travel_title = %s")
            values.append(travel_title)

        travel_country = request.form.get("travel_country", "").strip()
        if travel_country:
            parts.append("travel_country = %s")
            values.append(travel_country)

        travel_location = request.form.get("travel_location", "").strip()
        if travel_location:
            parts.append("travel_location = %s")
            values.append(travel_location)

        travel_start_date = request.form.get("travel_start_date", "").strip()
        if travel_start_date:
            parts.append("travel_start_date = %s")
            values.append(travel_start_date)

        travel_end_date = request.form.get("travel_end_date", "").strip()
        if travel_end_date:
            parts.append("travel_end_date = %s")
            values.append(travel_end_date)

        travel_description = request.form.get("travel_description", "").strip()
        if travel_description:
            parts.append("travel_description = %s")
            values.append(travel_description)

        if not parts:
            return "nothing to update", 400

        partial_query = ", ".join(parts)

        values.append(travel_pk)

        q = f"""
            UPDATE travels
            SET {partial_query}
            WHERE travel_pk = %s
        """

        db, cursor = x.db()
        cursor.execute(q, values)
        db.commit()

        return f"""
            <browser mix-update="#travel-{travel_pk}" mix-fade-2000>
            </browser>
        """

    except Exception as ex:
        ic(ex)
        return str(ex), 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.delete("/edit_travels/<travel_pk>")
def delete_travel(travel_pk):
    try:
        db, cursor = x.db()
        q = "DELETE FROM travels WHERE travel_pk = %s"
        cursor.execute(q, (travel_pk,))
        db.commit()
        return f"""
            <browser mix-remove="#travel-{travel_pk}" mix-fade-2000>
            </browser>
        """
    except Exception as ex:
        pass
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()