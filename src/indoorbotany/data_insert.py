import mysql.connector as mysql

if __name__ == '__main__':
    db = mysql.connect(host="sql9.freemysqlhosting.net", user="sql9614741", password="gNXJLalcwM", database="sql9614741")

    cursor = db.cursor()
    print('Connected')

    # questions = [
    #     ("What is the ideal temperature range for most indoor plants?",
    #      "40-50°F (4-10°C)", "60-70°F (15-21°C)", "80-90°F (27-32°C)", "B"),
    #     ("What type of soil is best for indoor plants?",
    #      "Sand", "Clay", "Loamy", "C"),
    #     ("What is the most important factor for successful indoor plant growth?",
    #      "Sunlight", "Watering", "Fertilizer", "A"),
    #     ("Which of the following is a common indoor plant pest?",
    #      "Grasshopper", "Spider mite", "Caterpillar", "B"),
    #     ("Which of the following is an effective way to increase humidity for indoor plants?",
    #      "Watering more frequently", "Using a humidifier", "Opening windows", "B"),
    #     ("Which of the following is NOT a common method of propagating plants at home?",
    #      "Stem cuttings", "Layering", "Shaking", "C"),
    #     ("What is the process of acclimating plants to new growing conditions called?",
    #      "Adaptation", "Transplanting", "Hardening off", "C"),
    #     ("What is the name of the process by which plants convert sunlight into energy?",
    #      "Photosynthesis", "Respiration", "Transpiration", "A"),
    #     ("What is the recommended pH range for most indoor plants?",
    #      "1-3", "4-6", "7-9", "B"),
    #     ("What is the best time of day to water indoor plants?",
    #      "Morning", "Afternoon", "Evening", "A")
    #
    # ]
    #
    questions = [
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

    db.commit()
    print('Done uploading')
    cursor.close()
    db.close()
