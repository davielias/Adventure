from bottle import route, run, template, static_file, request
import random
import json
import pymysql


connection = pymysql.connect(host = 'localhost',
                             user = 'root',
                             password = 'root',
                             db = 'adventure',
                             charset = 'utf8',
                             cursorclass=pymysql.cursors.DictCursor)


@route("/", method="GET")
def index():
    return template("adventure.html")


@route("/start", method="POST")
def start():
    username = request.POST.get("user")
    try:
        with connection.cursor() as cursor:
            sql = "SELECT username FROM userinfo WHERE username = '{}'".format(username)
            cursor.execute(sql)
            result = cursor.fetchone()
            if not result:
                resgister_sql = "INSERT INTO userinfo (username) VALUE ('{}')".format(username)
                cursor.execute(resgister_sql)
                get_user_sql = "SELECT * FROM userinfo WHERE username = '{}'".format(username)
                cursor.execute(get_user_sql)
                register_result = cursor.fetchone()
                print(register_result)
                print("Registering works")
                # return print("Registering works")
            pull_user_info_sql = "SELECT * from userinfo where username = '{}'".format(username)
            cursor.execute(pull_user_info_sql)
            user_info_sql = cursor.fetchone()
            print(user_info_sql)
            print(type(user_info_sql['story_id']))
#allows us to check what is current story id
            if user_info_sql['story_id'] == 1:
                story_info = "You're alone in the woods. There's no one around and your phone is dead. Out of the corner of your eye you spot him. Shia LaBeouf. What do you do?"
                next_steps_results = [
                {"id": 1, "option_text": "Fawn over him! You loved him in Transformers!", "next_story_id": 2},
                {"id": 2, "option_text": "Get into a powerful stance and shout \"JUST DO IT!\"", "next_story_id": 9},
                {"id": 3, "option_text": "You keep walking. Something tells you that something is wrong.", "next_story_id": 3},
                {"id": 4, "option_text": "Break into a run. You've seen enough horror movies and late night TV to know that you shouldn't be alone with anyone in the woods.", "next_story_id": 3},
                ]
                print(story_info, next_steps_results)
                

            # return (print("Already existing works?"))
    except Exception as e:
        print(repr(e))


    #todo add the next step based on db
    return json.dumps({"user": username,
                       "text": story_info,
                       "image": "shia lablood.gif",
                       "options": next_steps_results
                       })

@route("/story", method="POST")
def story():
    username = request.POST.get("user")
    current_adv_id = request.POST.get("adventure")
    next_story_id = request.POST.get("next") #this is what the user chose - use it!
    try:
        with connection.cursor() as cursor:
            sql = "SELECT goes_to_story_id from questions where story_id = '{}'".format(next_story_id)
            cursor.execute(sql)
            next_story_id = cursor.fetchone()
            if next_story_id['goes_to_story_id'] == 1:
                print(next_story_id['goes_to_story_id'])
                story_text = "You're alone in the woods. There's no one around and your phone is dead. Out of the corner of your eye you spot him. Shia LaBeouf. What do you do?"
                next_steps_result = [
                {"id": 1, "option_text": "Fawn over him! You loved him in Transformers!", "next_story_id": 2},
                {"id": 2, "option_text": "Get into a powerful stance and shout \"JUST DO IT!\"", "next_story_id": 9},
                {"id": 3, "option_text": "You keep walking. Something tells you that something is wrong.", "next_story_id": 3},
                {"id": 4, "option_text": "Break into a run. You've seen enough horror movies and late night TV to know that you shouldn't be alone with anyone in the woods.", "next_story_id": 3},
                ]
            elif next_story_id['goes_to_story_id'] == 2:
                print(next_story_id['goes_to_story_id'])
                story_text = "You're starstruck feelings blind you to your surroundings. As the two of you get closer, you suddenly find yourself on the ground. You've been suckerpunched by Shia LaBeouf! What's next?!"
                next_steps_result = [
                {"id": 1, "option_text": "Stand up and hug it out. He's a lovable guy, maybe it was a mistake?", "next_story_id": 9},
                {"id": 2, "option_text": "Get up and run! He's out of is mind!","next_story_id": 3},
                {"id": 3, "option_text": "Return the favor and punch him back! You ain't no sucka!", "next_story_id": 4},
                {"id": 4, "option_text": "Start insulting him. His modern art is trash and transformers was only good because of Megan Fox.", "next_story_id": 4},
                ]
            elif next_story_id['goes_to_story_id'] == 3:
                print(next_story_id['goes_to_story_id'])
                story_text = "He's following you about 30 feet back. He gets down on all fours and breaks into a sprint. He's gaining on you. Shia LaBeouf.You're looking for your car, but you're all turned around. He's almost upon you now and you can see there's blood on his face! My god, there's blood everywhere!"
                next_steps_result = [
                {"id": 1, "option_text": "Run for your life! He's crazed and must be escaped at all costs! Is that a knife in his hands? Is this REALLY Hollywood superstar Shia LaBeouf?!", "next_story_id": 5},
                {"id": 2, "option_text": "Turn back and take him head on. He's just a regular guy with a drinking problem!","next_story_id": 4},
                {"id": 3, "option_text": "Run as far as you can! You don't take any time to think about anything else. Your only goal is to NOT be where you are right then.", "next_story_id": 5},
                {"id": 4, "option_text": "You've been waiting your entire life for this moment. The day you can take Shia LaBeouf head on! You want your money back from all the Holes merchandise you bought. You got an old beat up Camaro because of him that didn't even make it to the summer. This is your revenge!", "next_story_id": 4},
                ]
            elif next_story_id['goes_to_story_id'] == 4:
                print(next_story_id['goes_to_story_id'])
                story_text = "The adrenaline flowing through you, you plan take your stand against Shia LaBeouf. He's coming at you, what's your plan?!"
                next_steps_result = [
                {"id": 1, "option_text": "Run up to him and fake him out. Have him collide face first with your fist. Show him who's the boss!", "next_story_id": 6},
                {"id": 2, "option_text": "You notice the knife in his pocket. You take the first hit just so you can get close enough to steal it. Turn the tables and attack!","next_story_id": 7},
                {"id": 3, "option_text": "Run! Run far away! You let the adrenaline in your body push you faster and farther than you can imagine!", "next_story_id": 5},
                {"id": 4, "option_text": "Grab him by his rat tail! Not gonna let some weirdo get the best of you!", "next_story_id": 6},
                ]
                print(next_story_id)
            elif next_story_id['goes_to_story_id'] == 9:
                print(next_story_id['goes_to_story_id'])
                story_text = "Game over. You've been defeated by Shia LaBeouf."
                next_steps_result = [
                {"id": 1, "option_text": "If you want to try again, press me.", "next_story_id": 1}
                ]
            elif next_story_id['goes_to_story_id'] == 5:
                print(next_story_id['goes_to_story_id'])
                story_text = "Running for your life, from Shia LaBeouf. He's brandishing a knife! Lurking in the shadows, Hollywood superstar Shia LaBeouf. Living in the woods, killing for sport, eating all the bodies... Actual, cannibal Shia LaBeouf!Now it's dark and you seem to have lost him, but you're hopelessly lost yourself. Stranded with a murderer. You creep silently through the underbrush. A-ha! In the distance, a small cottage with a light on. Whatever shall you do?"
                next_steps_result = [
                {"id": 1, "option_text": "Hope! You move stealthily toward it.", "next_story_id": 8},
                {"id": 2, "option_text": "Make a break for it! Someone in there might be able to help you!","next_story_id": 8},
                {"id": 3, "option_text": "Try and go around, make sure you aren't being followed before you make another move.", "next_story_id": 8},
                {"id": 4, "option_text": "Get far away from the house. Something tells you it isn't where you want to be.", "next_story_id": 8},
                ]
            else:
                print(next_story_id['goes_to_story_id'])
                story_text = "You've been killed"
                next_steps_result = [
                {"id": 1, "option_text": "Cry."},
                {"id": 2, "option_text": "Revenge."},
                {"id": 3, "option_text": "Again."},
                {"id": 4, "option_text": "Fuck it."},
                ]
    except Exception as e:
        print(repr(e))

    return json.dumps({"user": username,
                       "text": story_text,
                       "image": "shia lablood.gif",
                       "options": next_steps_result,
                       "next": next_story_id
                       })


@route('/js/<filename:re:.*\.js$>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')

def main():
    run(host='localhost', port=9000)

if __name__ == '__main__':
    main()
