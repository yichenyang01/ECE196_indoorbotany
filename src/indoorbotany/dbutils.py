import mysql.connector as mysql

if __name__ == '__main__':

   def grab_plant_data(profile = None):
    
   #Create the helper function to grab the plant data associated with a plant profile
      db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
      cursor = db.cursor()
      cursor.execute("SELECT moisture, temp, humidity, light FROM profiles INNER JOIN plant_data ON profiles.profile_id = plant_data.profile_id WHERE profiles.profile_name = " + "FLF_1")
      db.commit()
      db.close()
      return cursor.fetchall()

print(grab_plant_data())