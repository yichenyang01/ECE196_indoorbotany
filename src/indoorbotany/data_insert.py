import mysql.connector as mysql

if __name__ == '__main__':
    

    #Connect to the database
    db = mysql.connect(host="sql9.freesqldatabase.com", user="sql9622826", password="hQNVN4TgY4", database="sql9622826")
    cursor = db.cursor()
    print('Connected')



    #Drop existing table
    cursor.execute('DROP TABLE if EXISTS plants;')

    #Create the table for the tutorial content
    try:
      cursor.execute("""
      CREATE TABLE plants (
        id          INT  AUTO_INCREMENT  PRIMARY KEY,
        plant       VARCHAR(255)  NOT NULL
      );
    """)
    except RuntimeError as err:
      print('runtime error: {0}'.format(err))

    #Insert values into the table
    plants = []
    query = ("INSERT INTO plants (plant) VALUES (%s)")
    cursor.executemany(query, plants)



    #We dont drop because we don't mind having the extra data
    #Create the table for the tutorial content
    try:
      cursor.execute("""
      CREATE TABLE plant_data (
        id        INT  AUTO_INCREMENT  PRIMARY KEY,
        data      INT  NOT NULL
      );
    """)
    except RuntimeError as err:
      print('runtime error: {0}'.format(err))

    #Insert values into the table
    data = []
    query = ("INSERT INTO plant_data (data) VALUES (%s)")
    cursor.executemany(query, data)



    #Drop existing table
    cursor.execute('DROP TABLE if EXISTS tutorials;')

    #Create the table for the tutorial content
    try:
      cursor.execute("""
      CREATE TABLE tutorials (
        id          INT  AUTO_INCREMENT  PRIMARY KEY,
        tutorial    VARHCAR()  NOT NULL
      );
    """)
    except RuntimeError as err:
      print('runtime error: {0}'.format(err))

    #Insert values into the table
    tutorials = []
    query = ("INSERT INTO tutorials (tutorial) VALUES (%s)")
    cursor.executemany(query, tutorials)



    #Drop existing table
    cursor.execute('DROP TABLE if EXISTS quiz;')

    #Create the table for the quiz content
    try:
      cursor.execute("""
      CREATE TABLE quiz (
        id              INT  AUTO_INCREMENT  PRIMARY KEY,
        question        VARCHAR(255)  NOT NULL,
        option1         VARCHAR(255)  NOT NULL,
        option2         VARCHAR(255)  NOT NULL,
        option3         VARCHAR(255)  NOT NULL,
        correct_answer  VARCHAR(255)  NOT NULL
      );
    """)
    except RuntimeError as err:
      print('runtime error: {0}'.format(err))

    #Insert values into the table
    questions = [
        ("What is the ideal temperature range for most indoor plants?",
         "40-50°F (4-10°C)", "60-70°F (15-21°C)", "80-90°F (27-32°C)", "B"),
        ("What type of soil is best for indoor plants?",
         "Sand", "Clay", "Loamy", "C"),
        ("What is the most important factor for successful indoor plant growth?",
         "Sunlight", "Watering", "Fertilizer", "A"),
        ("Which of the following is a common indoor plant pest?",
         "Grasshopper", "Spider mite", "Caterpillar", "B"),
        ("Which of the following is an effective way to increase humidity for indoor plants?",
         "Watering more frequently", "Using a humidifier", "Opening windows", "B"),
        ("Which of the following is NOT a common method of propagating plants at home?",
         "Stem cuttings", "Layering", "Shaking", "C"),
        ("What is the process of acclimating plants to new growing conditions called?",
         "Adaptation", "Transplanting", "Hardening off", "C"),
        ("What is the name of the process by which plants convert sunlight into energy?",
         "Photosynthesis", "Respiration", "Transpiration", "A"),
        ("What is the recommended pH range for most indoor plants?",
         "1-3", "4-6", "7-9", "B"),
        ("What is the best time of day to water indoor plants?",
         "Morning", "Afternoon", "Evening", "A"),
        ('What is the optimal humidity range for most indoor plants?',
         '20-30%', '40-60%', '70-80%', 'B'),
        ('Which of the following is NOT a common nutrient deficiency in plants?',
         'Nitrogen', 'Potassium', 'Chlorine', 'C'),
        ('Which of the following is not a common type of soil amendment?',
         'Compost', 'Perlite', 'Pesticide', 'C'),
        ('Which of the following plant species is not typically grown for food?',
         'Echeveria', 'Capsicum', 'Brassica', 'A'),
        ('Which of the following is not a common method of controlling indoor plant pests?',
         'Spraying the plant with water', 'Using insecticidal soap', 'Using beneficial insects like ladybugs', 'A')
    ]
    query = ("INSERT INTO quiz (question, option1, option2, option3, correct_answer) VALUES (%s, %s, %s, %s, %s)")
    cursor.executemany(query, questions)



    #Commit changes and disconnect from database
    db.commit()
    print('Done uploading')
    cursor.close()
    db.close()
