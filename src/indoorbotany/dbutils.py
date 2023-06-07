import mysql.connector as mysql
import random

if __name__ == '__main__':



   def create_plant_profile(name:str = 'NewPlant', plant:str = None):

      #Create a SQL query to insert a new plant profile into the 'profiles' table
      db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
      cursor = db.cursor(buffered=True)
      plant_id = grab_plant_id(plant)[0]
      cursor.execute("""
      INSERT into profiles (profile_name, plant_id)
      VALUES ('{}', {})
      """.format(name, plant_id))
      db.commit()
      db.close()
      create_empty_data_row(name)



   def create_empty_data_row(profile_name):

      #Create an SQL query to create a new row in 'plant_data' when a new plant profile is created
      db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
      cursor = db.cursor(buffered=True)
      profile_id = grab_profile_id(profile_name)[0]
      cursor.execute("""
      INSERT into plant_data (moisture, temp, humidity, light, profile_id)
      VALUES ({}, {}, {}, {}, {})
      """.format(50, 50, 50, 50, profile_id))
      db.commit()
      db.close()



   def grab_plants():

      #Create a SQL query to grab the plants in the 'plants' table
      db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
      cursor = db.cursor(buffered=True)
      cursor.execute("""
      SELECT plant_name
      FROM plants
      """)
      db.commit()
      db.close()
      return cursor.fetchall()
      


   def grab_plant_id(plant:str = None):

      #Create a SQL query to grab plant_id of a plant
      db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
      cursor = db.cursor(buffered=True)
      cursor.execute("""
      SELECT plant_id
      FROM plants 
      WHERE plant_name = '{}'
      """.format(plant))
      db.commit()
      db.close()
      return cursor.fetchone()


   def grab_plant_id_from_profile(profile_name:str = None):

      #Create SQL query to grab a plant_id given a profile name
      db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
      cursor = db.cursor(buffered=True)
      cursor.execute("""
      SELECT plant_id
      FROM profiles 
      WHERE profile_name = '{}'
      """.format(profile_name))
      db.commit()
      db.close()
      return cursor.fetchone()



   def grab_profile_id(profile_name:str = None):

      #Create a SQL query to grab profile_id of a profile
      db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
      cursor = db.cursor(buffered=True)
      cursor.execute("""
      SELECT profile_id
      FROM profiles 
      WHERE profile_name = '{}'
      """.format(profile_name))
      db.commit()
      db.close()
      return cursor.fetchone()
         


   def grab_plant_profiles():

      #Create a SQL query to grab the different plant profiles from 'profiles' table
      db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
      cursor = db.cursor(buffered=True)
      cursor.execute("""
      SELECT profile_name
      FROM profiles
      """)
      db.commit()
      db.close()
      return cursor.fetchall()
      


   def grab_plant_data(profile:str = None):
         
      #Create the SQL query to grab the plant data associated with a plant profile
      db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
      cursor = db.cursor(buffered=True)
      cursor.execute("""
      SELECT data_id, moisture, temp, humidity, light 
      FROM profiles 
      INNER JOIN plant_data 
      ON profiles.profile_id = plant_data.profile_id 
      WHERE profile_name = '{}'
      ORDER BY data_id DESC LIMIT 1
      """.format(profile))
      db.commit()
      db.close()
      return cursor.fetchall()



   def grab_plant_tutorial(plant:str = None):
         
      #Create the SQL query to grab the tutorial based on the plant
      db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
      cursor = db.cursor(buffered=True)
      plant_id = grab_plant_id(plant)[0]
      cursor.execute("""
      SELECT general_info, watering, sunlight, climate, summary 
      FROM tutorials
      WHERE plant_id = {}
      """.format(plant_id))
      db.commit()
      db.close()
      return cursor.fetchall()



   def grab_plant_from_profile_name(profile_name:str=None):

   #Create SQL query to grab a plant_id given a profile name
      db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
      cursor = db.cursor(buffered=True)
      cursor.execute("""
      SELECT plant_name
      FROM plants 
      INNER JOIN profiles
      ON plants.plant_id = profiles.plant_id
      WHERE profile_name = '{}'
      """.format(profile_name))
      db.commit()
      db.close()
      return cursor.fetchone()



   def get_question(profile_name:str = None):


      #Create an SQL query to grab quiz questions
      db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
      plant_id = grab_plant_id_from_profile(profile_name)[0]
      cursor = db.cursor()
      cursor.execute("""
      SELECT * 
      FROM quiz
      WHERE plant_id = {};
      """.format(plant_id))
      questions = cursor.fetchall()
      sample = random.sample(range(1, (len(questions))), 3)
      sampled_questions = []
      for i in sample:
         sampled_questions.append(questions[i])
      return sampled_questions