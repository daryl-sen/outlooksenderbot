import pyautogui as pag
import time
try:
    from data import names, emails, subject, message
except ImportError:
    print("data.py not found. Please open README.txt for instructions.")
    exit()




# settings
pag.PAUSE = 1 # interval between each action
pag.FAILSAFE = True # if set to true, script will stop when you move the cursor to the top left corner of the screen
run = True # if set to False, the script will do all the prep work but will not run the last send_cycle function
mode = 'discard' # if mode is set to 'discard' instead of 'send', the script will discard every email after constructing them




# DO NOT EDIT ANYTHING AFTER THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING
###########################################################################################################

def start(run, mode):
    print("Script has began running...")


    # calibrate button locations
    def find_coord(image, clvl):
        loc = pag.locateOnScreen(f"images/{image}.png", confidence = clvl)
        if loc == None:
            print(f"'{image}' not found.")
            return None
        else:
            print(f"'{image}' found.")
            return {'x': loc.left + 15, 'y': loc.top + 3}
    
    print("Calibrating button locations")
    inbox_loc = find_coord('inbox', 0.7)
    if inbox_loc == None:
        inbox_loc = find_coord('inboxd', 0.7)
        if inbox_loc is not None:
            inbox_loc = find_coord('inboxd', 0.7)
            print('Found dark-colored inbox instead')
        else:
            return print('Fatal error, could not find regular or dark-colored inbox button. Script terminated.')

    new_loc = find_coord('new', 0.85)
    if new_loc is not None:
        pag.click(new_loc['x'], new_loc['y'])
    else:
        pag.click(inbox_loc['x'], inbox_loc['y'])
        time.sleep(1) # wait for slower connections to open 
        new_loc = find_coord('new', 0.8)
        if new_loc == None:
            return print("Fatal error, could not find the 'new button' location.")
        else:
            pag.click(new_loc['x'], new_loc['y'])
            
    send_loc = find_coord('send', 0.8)
    discard_loc = find_coord('discard', 0.8)
    subject_loc = find_coord('subject', 0.8)
    if subject_loc is not None:
        subject_loc = {'x': subject_loc['x']+15, 'y':subject_loc['y']+35}
        print('Subject location tweaked.')
    body_loc = find_coord('body', 0.8)

    loc_list = (
        inbox_loc,
        new_loc,
        subject_loc,
        body_loc,
        send_loc,
        inbox_loc,
        discard_loc
        )
    if None in loc_list:
        return print("Script terminated due to missing coordinate(s).")
    
    print("Button coordinates calibration complete, please check the coordinates now.")
    print("This is the 'inbox' button location (see cursor)")
    pag.moveTo(inbox_loc['x'], inbox_loc['y'])
    time.sleep(1)
    pag.click()
    print("This is the 'new' button location (see cursor)")
    pag.moveTo(new_loc['x'], new_loc['y'])
    time.sleep(1)
    pag.click()
    print("This is the 'subject' field location (see cursor)")
    pag.moveTo(subject_loc['x'], subject_loc['y'])
    time.sleep(1)
    print("This is the 'body' field location (see cursor)")
    pag.moveTo(body_loc['x'], body_loc['y'])
    time.sleep(1)
    print("This is the 'send' button location (see cursor)")
    pag.moveTo(send_loc['x'], send_loc['y'])
    time.sleep(1)
    print("This is the 'discard' button location (see cursor)")
    pag.moveTo(discard_loc['x'], discard_loc['y'])
    time.sleep(1)
    print("Move cursor to the top right corner to terminate the script if you found any errors.")
    time.sleep(1)
    print("Proceeding in 3..")
    time.sleep(1)
    print("Proceeding in 2..")
    time.sleep(1)
    print("Proceeding in 1..")
    time.sleep(1)



    # create master list containing names and emails
    email_list = emails.split('\n')
    name_list = names.split('\n')
    contacts = [{'name': name_list[i].replace(" ",""), 'email': email_list[i]} for i in range(0, len(email_list))]
    
    print('Created contact list, printing contacts...')


    # check list integrity
    if len(email_list) != len(name_list):
        print("No. of emails: " + str(len(email_list)))
        print("No. of names: " + str(len(name_list)))
        return print("ERROR: The list of names and list of emails do not match up.")
    elif len(email_list) == len(name_list):
        print(f'({len(contacts)} contacts loaded.)')
        n = 1
        for contact in contacts:
            print(f"{n}. {contact['name']}, {contact['email']}")
            n += 1

    print("Preparation is complete.")
    if run == False:
        return print("Script is ready to proceed, please set the 'run' variable to True in 'run.py'.")




    def send_cycle(action, name, email):
        # click on the inbox link (new cycle)
        pag.moveTo(inbox_loc['x'], inbox_loc['y'])
        pag.click(inbox_loc['x'], inbox_loc['y'])

        # click on the "new email" button
        pag.moveTo(new_loc['x'], new_loc['y'])
        pag.click(new_loc['x'], new_loc['y'])

        # enter the email
        pag.typewrite(f"{email}")

        # click on the subject field
        pag.moveTo(x = subject_loc['x'], y = subject_loc['y'])
        pag.click(x = subject_loc['x'], y = subject_loc['y'])
        pag.click(x = subject_loc['x'], y = subject_loc['y'])

        # enter the subject
        pag.typewrite(subject)

        # click on the email body field
        pag.moveTo(body_loc['x'], body_loc['y'])
        pag.click(body_loc['x'], body_loc['y'])

        # enter salutation
        pag.typewrite(f"Dear {name},\n\n")
        pag.typewrite(message)
        time.sleep(1)

        # hit sent/discard
        if action == "send":
            pag.moveTo(send_loc['x'], send_loc['y'])
            pag.click(send_loc['x'], send_loc['y'])
        elif action == "discard":
            pag.moveTo(x = discard_loc['x'], y = discard_loc['y'])
            pag.click(x = discard_loc['x'], y = discard_loc['y'])
            pag.typewrite(['enter'])
            

        # wait 2 seconds
        print(f"Cycle completed using {name}, {email}")
        time.sleep(2)



    if run == True:
        for contact in contacts:
            send_cycle(mode, contact['name'], contact['email'])




if __name__ == "__main__":
    start(run, mode)
    print("Script has finished running.")